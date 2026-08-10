"""Terminal-Bench import-path adapter for mini-claude-code-cli.

Terminal-Bench loads custom agents from Python import paths, for example::

    tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeTerminalBenchAgent

The real Terminal-Bench ``BaseAgent`` API is intentionally small: an agent class
is instantiated by the harness and then asked to ``perform_task(instruction,
session)``.  This module provides that importable class and bridges the call to
mini-claude-code-cli's non-interactive ``AgentEngine.run_single_task`` entry.

Notes
-----
The current mini agent tools run in the local Python process.  This adapter makes
mini-claude-code-cli loadable by Terminal-Bench and executes the task once, but a
full production-quality integration may still need Terminal-Bench-session-aware
shell/file tools so all actions happen inside the benchmark container.
"""

from __future__ import annotations

import asyncio
import os
import threading
from dataclasses import dataclass
from typing import Any, Callable, Optional

try:  # Prefer the real Terminal-Bench base class when available.
    from terminal_bench.agents.base_agent import BaseAgent  # type: ignore
except Exception:  # pragma: no cover - exercised when terminal-bench is absent.

    class BaseAgent:  # type: ignore[no-redef]
        """Small fallback that keeps this adapter importable in local tests."""

        def __init__(self, **_: Any) -> None:
            pass


EngineFactory = Callable[[], Any]


@dataclass
class MiniClaudeRunSummary:
    """JSON-friendly summary of one adapter execution."""

    success: bool
    stop_reason: str
    output: str = ""
    error: Optional[str] = None


class MiniClaudeCodeTerminalBenchAgent(BaseAgent):
    """Terminal-Bench ``BaseAgent`` implementation for mini-claude-code-cli.

    Parameters are intentionally permissive because Terminal-Bench forwards
    agent-specific kwargs from config/CLI.  Unknown kwargs are accepted and kept
    for diagnostics instead of failing construction.
    """

    def __init__(
        self,
        *args: Any,
        model: Optional[str] = None,
        max_turns: int = 40,
        engine_factory: Optional[EngineFactory] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        if not isinstance(max_turns, int) or max_turns <= 0:
            raise ValueError("max_turns must be a positive integer")

        self.model = model or os.getenv("MINI_CLAUDE_MODEL", "gpt-5.5")
        self.max_turns = max_turns
        self.engine_factory = engine_factory or self._create_default_engine
        self.extra_args = args
        self.extra_kwargs = kwargs
        self.last_result: Optional[MiniClaudeRunSummary] = None

    @staticmethod
    def name() -> str:
        """Return a stable agent name for harnesses that display it."""

        return "mini-claude-code-cli"

    @property
    def _identifying_params(self) -> dict[str, Any]:
        """Compatibility with Terminal-Bench agents that expose metadata."""

        return {"model": self.model, "max_turns": self.max_turns}

    def perform_task(self, instruction: str, session: Any = None) -> None:
        """Execute one Terminal-Bench task instruction.

        Terminal-Bench expects this method to be synchronous.  The mini engine is
        async, so this method safely runs the coroutine whether or not an event
        loop already exists in the current thread.
        """

        if not isinstance(instruction, str) or not instruction.strip():
            raise ValueError("instruction must be a non-empty string")

        # ``session`` is accepted to match the Terminal-Bench interface.  The
        # current engine does not consume it yet; keeping it here makes the next
        # evolution path explicit without breaking the importable API.
        del session

        result = self._run_coroutine_sync(self._run_engine(instruction.strip()))
        self.last_result = self._normalize_result(result)

        if not self.last_result.success:
            raise RuntimeError(self.last_result.error or self.last_result.output or "mini agent task failed")

    async def _run_engine(self, instruction: str) -> Any:
        engine = self.engine_factory()
        if not hasattr(engine, "run_single_task"):
            raise RuntimeError("engine_factory must return an object with run_single_task(prompt, max_turns=...)")
        result = engine.run_single_task(instruction, max_turns=self.max_turns)
        if asyncio.iscoroutine(result) or isinstance(result, asyncio.Future):
            return await result
        return result

    def _create_default_engine(self) -> Any:
        """Build the real mini-claude-code-cli AgentEngine lazily."""

        from core.engine import AgentEngine
        from core.memory_manager import MemoryManager
        from core.plan import PlanManager
        from main import get_agent_config
        from tools import get_default_tools

        plan_manager = PlanManager()
        memory_manager = MemoryManager(plan_manager=plan_manager)
        tools_list = get_default_tools(plan_manager=plan_manager, memory_manager=memory_manager)
        config = get_agent_config()

        return AgentEngine(
            tools=tools_list,
            model=self.model,
            plan_manager=plan_manager,
            session_id="terminal-bench",
            base_url=config["base_url"],
            api_key=config["api_key"],
            max_history=150,
            min_keep=8,
            memory_manager=memory_manager,
        )

    @staticmethod
    def _run_coroutine_sync(coro: Any) -> Any:
        """Run an awaitable from synchronous Terminal-Bench code."""

        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coro)

        result_box: dict[str, Any] = {}
        error_box: dict[str, BaseException] = {}

        def runner() -> None:
            try:
                result_box["result"] = asyncio.run(coro)
            except BaseException as exc:  # noqa: BLE001 - propagated below.
                error_box["error"] = exc

        thread = threading.Thread(target=runner, daemon=True)
        thread.start()
        thread.join()

        if "error" in error_box:
            raise error_box["error"]
        return result_box.get("result")

    @staticmethod
    def _normalize_result(result: Any) -> MiniClaudeRunSummary:
        if isinstance(result, MiniClaudeRunSummary):
            return result

        if isinstance(result, dict):
            success = bool(result.get("success", True))
            output = str(result.get("output") or result.get("response") or result.get("final_response") or "")
            error = result.get("error")
            return MiniClaudeRunSummary(
                success=success,
                stop_reason=str(result.get("stop_reason") or ("completed" if success else "error")),
                output=output,
                error=str(error) if error else None,
            )

        return MiniClaudeRunSummary(success=True, stop_reason="completed", output=str(result or ""))


# Short alias for convenient import paths:
#   terminal_bench_adapter:MiniClaudeCodeAgent
MiniClaudeCodeAgent = MiniClaudeCodeTerminalBenchAgent


__all__ = [
    "MiniClaudeCodeAgent",
    "MiniClaudeCodeTerminalBenchAgent",
    "MiniClaudeRunSummary",
]
