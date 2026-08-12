import pytest

import terminal_bench_adapter as adapter


class RecordingEngine:
    def __init__(self):
        self.calls = []

    async def run_single_task(self, prompt, max_turns=40):
        self.calls.append({"prompt": prompt, "max_turns": max_turns})
        return {"success": True, "stop_reason": "completed", "output": "done"}


class FailingEngine:
    async def run_single_task(self, prompt, max_turns=40):
        return {"success": False, "stop_reason": "error", "error": "boom"}


class SyncEngine:
    def __init__(self):
        self.calls = []

    def run_single_task(self, prompt, max_turns=40):
        self.calls.append({"prompt": prompt, "max_turns": max_turns})
        return "sync done"


def test_adapter_exports_importable_base_agent_subclass():
    assert hasattr(adapter, "MiniClaudeCodeTerminalBenchAgent")
    assert adapter.MiniClaudeCodeAgent is adapter.MiniClaudeCodeTerminalBenchAgent
    assert issubclass(adapter.MiniClaudeCodeTerminalBenchAgent, adapter.BaseAgent)
    assert adapter.MiniClaudeCodeTerminalBenchAgent.name() == "mini-claude-code-cli"


def test_adapter_accepts_terminal_bench_style_kwargs_and_metadata():
    agent = adapter.MiniClaudeCodeTerminalBenchAgent(model="test-model", max_turns=5, task_ids=["demo"])

    assert agent.model == "test-model"
    assert agent.max_turns == 5
    assert agent.extra_kwargs == {"task_ids": ["demo"]}
    assert agent._identifying_params == {"model": "test-model", "max_turns": 5}


@pytest.mark.parametrize("max_turns", [0, -1, 1.5, "2"])
def test_adapter_rejects_invalid_max_turns(max_turns):
    with pytest.raises(ValueError, match="max_turns must be a positive integer"):
        adapter.MiniClaudeCodeTerminalBenchAgent(max_turns=max_turns)


@pytest.mark.parametrize("instruction", ["", "   ", None])
def test_adapter_rejects_empty_instruction(instruction):
    agent = adapter.MiniClaudeCodeTerminalBenchAgent(engine_factory=RecordingEngine)

    with pytest.raises(ValueError, match="instruction must be a non-empty string"):
        agent.perform_task(instruction, session=object())


def test_perform_task_calls_async_engine_and_stores_summary():
    engine = RecordingEngine()
    agent = adapter.MiniClaudeCodeTerminalBenchAgent(max_turns=7, engine_factory=lambda: engine)

    agent.perform_task("  solve this task  ", session=object())

    assert engine.calls == [{"prompt": "solve this task", "max_turns": 7}]
    assert agent.last_result == adapter.MiniClaudeRunSummary(
        success=True,
        stop_reason="completed",
        output="done",
        error=None,
    )


def test_perform_task_accepts_sync_engine_result():
    engine = SyncEngine()
    agent = adapter.MiniClaudeCodeTerminalBenchAgent(engine_factory=lambda: engine)

    agent.perform_task("solve", session=None)

    assert engine.calls == [{"prompt": "solve", "max_turns": 40}]
    assert agent.last_result == adapter.MiniClaudeRunSummary(
        success=True,
        stop_reason="completed",
        output="sync done",
        error=None,
    )


def test_perform_task_raises_when_engine_reports_failure():
    agent = adapter.MiniClaudeCodeTerminalBenchAgent(engine_factory=FailingEngine)

    with pytest.raises(RuntimeError, match="boom"):
        agent.perform_task("solve", session=None)

    assert agent.last_result == adapter.MiniClaudeRunSummary(
        success=False,
        stop_reason="error",
        output="",
        error="boom",
    )


def test_perform_task_accepts_terminal_bench_logging_dir_and_extra_kwargs():
    engine = RecordingEngine()
    agent = adapter.MiniClaudeCodeTerminalBenchAgent(max_turns=2, engine_factory=lambda: engine)

    agent.perform_task(
        "solve with harness context",
        session=object(),
        logging_dir="logs/demo",
        unexpected_harness_kwarg="ignored",
    )

    assert engine.calls == [{"prompt": "solve with harness context", "max_turns": 2}]
    assert agent.last_result.success is True


@pytest.mark.asyncio
async def test_perform_task_can_be_called_from_running_event_loop():
    engine = RecordingEngine()
    agent = adapter.MiniClaudeCodeTerminalBenchAgent(max_turns=3, engine_factory=lambda: engine)

    agent.perform_task("solve inside loop", session=None)

    assert engine.calls == [{"prompt": "solve inside loop", "max_turns": 3}]
    assert agent.last_result.success is True
