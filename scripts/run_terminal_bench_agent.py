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
import subprocess
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
    recovery_hint: Optional[str] = None
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
        "--require-path",
        action="append",
        default=[],
        help="Path relative to workspace that must exist before reporting success (repeatable).",
    )
    parser.add_argument(
        "--verify-command",
        action="append",
        default=[],
        help="Shell command run in workspace after the agent; must exit zero (repeatable).",
    )
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
        "请把任务当作一个可验收的工程任务，持续使用 shell、文件编辑和测试工具推进，直到工作区达到可验证完成态。\n"
        "执行流程必须分阶段：先检查任务与仓库状态，再实施修改；每次关键修改后运行针对性测试或构建；最后检查题目要求的文件、命令或可执行产物确实存在且可用。\n"
        "不要仅凭代码看起来正确、计划完成或口头说明完成就停止。若测试/构建失败，读取完整错误并修复后重试；若接近步数上限，优先完成最小可验证修复并运行验收命令。\n"
        "所有修改必须发生在当前 workspace 内。\n"
        "只有在完成验收后才返回；最终回复请简要列出实际执行的验收命令及其结果。\n\n"
        "任务说明：\n"
        f"{task_text}"
    )


_NON_TERMINAL_STOP_REASONS = frozenset(
    {
        "timeout",
        "agent_timeout",
        "max_turns",
        "max_steps",
        "cancelled",
        "aborted",
        "exception",
        "error",
    }
)


def apply_completion_guard(result: AgentRunResult) -> AgentRunResult:
    """Prevent runner success when the engine stopped without an accepted state.

    The task harness remains the source of truth for task correctness. This guard
    only prevents known incomplete engine states from being reported as success.
    """
    reason = result.stop_reason.strip().lower()
    if result.success and reason in _NON_TERMINAL_STOP_REASONS:
        result.success = False
        result.error = result.error or f"Agent stopped before completion ({result.stop_reason})."
    return result


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


async def close_engine(engine: Optional[SingleTaskEngine]) -> None:
    if engine is None:
        return

    close = getattr(engine, "close", None) or getattr(engine, "shutdown", None)
    if close is None:
        return

    await maybe_await(close())


def write_output_json(path: Optional[str], result: AgentRunResult) -> None:
    if not path:
        return
    output_path = Path(path).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(result), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def recovery_hint_for(reason: str) -> str:
    hints = {
        "timeout": "Split build, install, and verification into separate commands; inspect the last command output and resume from the unfinished phase.",
        "max_turns": "Prioritize the smallest build/install path and run the configured verification command before spending turns on cleanup.",
        "verification_failed": "Inspect the verification output, confirm the working directory and PATH, then repair or install the missing artifact before retrying.",
        "exception": "Read the exception traceback and rerun the failed phase with its inputs and working directory recorded.",
    }
    return hints.get(reason, "Inspect the recorded error and rerun the unfinished phase with an explicit postcondition.")


def verify_completion(args: argparse.Namespace, workspace: Path, result: AgentRunResult) -> AgentRunResult:
    """Validate task-specific postconditions after the engine reports completion."""
    if not result.success:
        return result

    errors: list[str] = []
    for required in args.require_path:
        candidate = (workspace / required).resolve()
        if not candidate.exists():
            errors.append(f"Required path does not exist: {required}")

    for command in args.verify_command:
        try:
            completed = subprocess.run(
                command,
                shell=True,
                cwd=workspace,
                text=True,
                capture_output=True,
                timeout=min(args.timeout, 120.0),
            )
        except subprocess.TimeoutExpired:
            errors.append(f"Verification command timed out: {command}")
            continue
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout or "no output").strip()[-1000:]
            errors.append(f"Verification command failed ({completed.returncode}): {command}: {detail}")

    if errors:
        result.success = False
        result.stop_reason = "verification_failed"
        result.error = "; ".join(errors)
    return result


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
    engine: Optional[SingleTaskEngine] = None
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
        result = apply_completion_guard(result)
        result = verify_completion(args, workspace, result)
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
        try:
            await close_engine(engine)
        except Exception as cleanup_exc:
            print(
                f"Warning: failed to close engine: {type(cleanup_exc).__name__}: {cleanup_exc}",
                file=sys.stderr,
            )
        os.chdir(old_cwd)

    if not result.success and not result.recovery_hint:
        result.recovery_hint = recovery_hint_for(result.stop_reason)
    result.workspace = str(workspace)
    result.duration_seconds = round(time.monotonic() - start, 3)
    write_output_json(args.output_json, result)
    return exit_code


def main(argv: Optional[Iterable[str]] = None) -> int:
    return asyncio.run(main_async(argv))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
