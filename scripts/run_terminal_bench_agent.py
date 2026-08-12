"""Non-interactive runner for Terminal-Bench style tasks.

This module intentionally keeps the Terminal-Bench adapter thin:
- parse a one-shot task from --task or --task-file
- switch into the requested workspace
- call an injectable engine with a single-task interface
- map result / exception / timeout to process exit codes
- optionally write a structured JSON result

The default engine integration expects an object exposing::

    await engine.run_single_task(prompt, max_turns=...)

Tests can pass a custom ``engine_factory`` to ``main_async`` so the runner can be
validated without making real model calls.
"""

from __future__ import annotations

import argparse
import asyncio
import inspect
import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Awaitable, Callable, Iterable, Optional, Protocol


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_TIMEOUT = 124


class SingleTaskEngine(Protocol):
    """Protocol for engines usable by the Terminal-Bench runner."""

    def run_single_task(self, prompt: str, max_turns: int = 40) -> Any:
        """Run one task and return a result object or mapping."""


EngineFactory = Callable[[argparse.Namespace], SingleTaskEngine]


@dataclass
class AgentRunResult:
    """Structured result emitted by the runner."""

    success: bool
    stop_reason: str
    turns: int = 0
    message: str = ""
    error: Optional[str] = None
    workspace: Optional[str] = None
    duration_seconds: float = 0.0


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Mini Claude Code CLI as a non-interactive Terminal-Bench agent."
    )
    task_group = parser.add_mutually_exclusive_group(required=True)
    task_group.add_argument("--task", help="Task text passed directly on the command line.")
    task_group.add_argument("--task-file", help="Path to a file containing the task text.")
    parser.add_argument("--workspace", required=True, help="Task workspace directory.")
    parser.add_argument("--max-turns", type=int, default=40, help="Maximum agent turns.")
    parser.add_argument("--timeout", type=float, default=1800.0, help="Total timeout in seconds.")
    parser.add_argument("--output-json", help="Optional path for structured runner output.")
    parser.add_argument(
        "--disable-memory",
        action="store_true",
        default=True,
        help="Disable long-term memory side effects in benchmark mode when supported.",
    )
    parser.add_argument(
        "--disable-auto-commit",
        action="store_true",
        default=True,
        help="Disable automatic git commits in benchmark mode when supported.",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def load_task(args: argparse.Namespace) -> str:
    if args.task is not None:
        task_text = args.task
    else:
        task_path = Path(args.task_file).expanduser().resolve()
        task_text = task_path.read_text(encoding="utf-8")

    task_text = task_text.strip()
    if not task_text:
        raise ValueError("Task text is empty.")
    return task_text


def build_prompt(task_text: str) -> str:
    return (
        "你正在 Terminal-Bench 任务工作目录中运行。\n"
        "请阅读任务说明，使用 shell、文件编辑、测试运行等工具完成任务。\n"
        "所有修改必须发生在当前 workspace 内。\n"
        "完成后请停止，不要等待用户继续输入。\n\n"
        "任务说明：\n"
        f"{task_text}"
    )


def default_engine_factory(args: argparse.Namespace) -> SingleTaskEngine:
    """Build the real project engine for non-interactive benchmark runs.

    This mirrors the interactive entrypoint's construction path while keeping the
    runner independent from the REPL loop:
    - create a per-run ``PlanManager``
    - create one shared ``MemoryManager`` for tools and context
    - create default tools
    - instantiate ``AgentEngine`` with environment-provided model/API settings

    Required environment variables:
    - ``MINI_CLAUDE_API_KEY`` or ``OPENAI_API_KEY`` or ``ANTHROPIC_API_KEY``
    Optional environment variables:
    - ``MINI_CLAUDE_BASE_URL`` (defaults to OpenAI-compatible endpoint)
    - ``MINI_CLAUDE_MODEL`` (defaults to the interactive entrypoint default)
    """

    try:
        PlanManagerClass = globals().get("PlanManager")
        MemoryManagerClass = globals().get("MemoryManager")
        AgentEngineClass = globals().get("AgentEngine")
        get_default_tools_func = globals().get("get_default_tools")

        if PlanManagerClass is None:
            from core.plan import PlanManager as PlanManagerClass
        if MemoryManagerClass is None:
            from core.memory_manager import MemoryManager as MemoryManagerClass
        if AgentEngineClass is None:
            from core.engine import AgentEngine as AgentEngineClass  # type: ignore
        if get_default_tools_func is None:
            from tools import get_default_tools as get_default_tools_func
    except Exception as exc:  # pragma: no cover - depends on optional runtime config
        raise RuntimeError(f"Unable to import project AgentEngine dependencies: {exc}") from exc

    api_key = (
        os.getenv("MINI_CLAUDE_API_KEY")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("ANTHROPIC_API_KEY")
    )
    if not api_key:
        raise RuntimeError(
            "Missing API key for AgentEngine. Set MINI_CLAUDE_API_KEY, "
            "OPENAI_API_KEY, or ANTHROPIC_API_KEY."
        )

    plan_manager = PlanManagerClass()
    memory_manager = None if args.disable_memory else MemoryManagerClass(plan_manager=plan_manager)
    tools = get_default_tools_func(plan_manager=plan_manager, memory_manager=memory_manager)

    engine = AgentEngineClass(
        tools=tools,
        model=os.getenv("MINI_CLAUDE_MODEL", "gpt-5.5"),
        plan_manager=plan_manager,
        session_id=os.getenv("MINI_CLAUDE_SESSION", "terminal-bench"),
        base_url=os.getenv("MINI_CLAUDE_BASE_URL", "https://api.openai.com/v1"),
        api_key=api_key,
        max_history=150,
        min_keep=8,
        memory_manager=memory_manager,
    )

    if not hasattr(engine, "run_single_task"):
        raise RuntimeError(
            "AgentEngine does not expose run_single_task(prompt, max_turns=...). "
            "Add that method or provide a custom engine_factory."
        )
    return engine


def normalize_result(raw_result: Any) -> AgentRunResult:
    if isinstance(raw_result, AgentRunResult):
        return raw_result

    if isinstance(raw_result, dict):
        return AgentRunResult(
            success=bool(raw_result.get("success", False)),
            stop_reason=str(raw_result.get("stop_reason", "completed")),
            turns=int(raw_result.get("turns", 0) or 0),
            message=str(raw_result.get("message", "") or ""),
            error=raw_result.get("error"),
        )

    return AgentRunResult(
        success=bool(getattr(raw_result, "success", False)),
        stop_reason=str(getattr(raw_result, "stop_reason", "completed")),
        turns=int(getattr(raw_result, "turns", 0) or 0),
        message=str(getattr(raw_result, "message", "") or ""),
        error=getattr(raw_result, "error", None),
    )


async def maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


async def run_engine(engine: SingleTaskEngine, prompt: str, max_turns: int) -> AgentRunResult:
    raw_result = engine.run_single_task(prompt, max_turns=max_turns)
    return normalize_result(await maybe_await(raw_result))


def write_output_json(path: Optional[str], result: AgentRunResult) -> None:
    if not path:
        return
    output_path = Path(path).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(result), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


async def main_async(
    argv: Optional[Iterable[str]] = None,
    engine_factory: Optional[EngineFactory] = None,
) -> int:
    args = parse_args(argv)
    workspace = Path(args.workspace).expanduser().resolve()
    start = time.monotonic()

    if not workspace.exists() or not workspace.is_dir():
        print(f"Invalid workspace: {workspace}", file=sys.stderr)
        result = AgentRunResult(
            success=False,
            stop_reason="invalid_workspace",
            error=f"Invalid workspace: {workspace}",
            workspace=str(workspace),
        )
        write_output_json(args.output_json, result)
        return EXIT_ERROR

    old_cwd = Path.cwd()
    result: AgentRunResult
    exit_code = EXIT_ERROR

    try:
        task_text = load_task(args)
        prompt = build_prompt(task_text)
        os.chdir(workspace)

        factory = engine_factory or default_engine_factory
        engine = factory(args)
        result = await asyncio.wait_for(
            run_engine(engine, prompt, max_turns=args.max_turns),
            timeout=args.timeout,
        )
        exit_code = EXIT_SUCCESS if result.success else EXIT_ERROR
    except asyncio.TimeoutError:
        result = AgentRunResult(
            success=False,
            stop_reason="timeout",
            error=f"Timed out after {args.timeout} seconds.",
        )
        exit_code = EXIT_TIMEOUT
    except Exception as exc:
        result = AgentRunResult(
            success=False,
            stop_reason="exception",
            error=f"{type(exc).__name__}: {exc}",
        )
        print(result.error, file=sys.stderr)
        exit_code = EXIT_ERROR
    finally:
        os.chdir(old_cwd)

    result.workspace = str(workspace)
    result.duration_seconds = round(time.monotonic() - start, 3)
    write_output_json(args.output_json, result)
    return exit_code


def main(argv: Optional[Iterable[str]] = None) -> int:
    return asyncio.run(main_async(argv))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
