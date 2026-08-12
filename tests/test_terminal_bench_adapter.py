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

    class NoopSession:
        def run(self, command):
            return ""

    agent.perform_task("  solve this task  ", session=NoopSession())

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


def test_perform_task_runs_terminal_bench_setup_before_engine():
    session = type("Session", (), {"commands": []})()

    class OrderingEngine:
        def __init__(self):
            self.calls = []

        async def run_single_task(self, prompt, max_turns=40):
            self.calls.append({"prompt": prompt, "max_turns": max_turns, "commands_before_run": list(session.commands)})
            return {"success": True, "stop_reason": "completed", "output": "done"}

    class FakeTerminalBenchSessionBackend:
        def __init__(self, session_obj):
            self.session_obj = session_obj

        def run_command(self, command):
            self.session_obj.commands.append(command)
            return "setup ok"

    engine = OrderingEngine()
    agent = adapter.MiniClaudeCodeTerminalBenchAgent(max_turns=4, engine_factory=lambda: engine)

    original_backend = adapter.__dict__.get("TerminalBenchSessionBackend")
    try:
        import tools.execution_backend as execution_backend

        original_execution_backend = execution_backend.TerminalBenchSessionBackend
        execution_backend.TerminalBenchSessionBackend = FakeTerminalBenchSessionBackend
        try:
            agent.perform_task(" solve ", session=session)
        finally:
            execution_backend.TerminalBenchSessionBackend = original_execution_backend
    finally:
        if original_backend is not None:
            adapter.TerminalBenchSessionBackend = original_backend

    assert session.commands == [adapter.APT_MIRROR_SETUP_COMMAND]
    assert engine.calls == [
        {"prompt": "solve", "max_turns": 4, "commands_before_run": [adapter.APT_MIRROR_SETUP_COMMAND]}
    ]

    engine = RecordingEngine()
    agent = adapter.MiniClaudeCodeTerminalBenchAgent(max_turns=3, engine_factory=lambda: engine)

    agent.perform_task("solve inside loop", session=None)

    assert engine.calls == [{"prompt": "solve inside loop", "max_turns": 3}]
    assert agent.last_result.success is True
