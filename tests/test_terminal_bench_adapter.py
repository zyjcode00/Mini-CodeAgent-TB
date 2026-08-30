import pytest

import terminal_bench_adapter as adapter


class RecordingEngine:
    def __init__(self):
        self.calls = []

    async def run_single_task(self, prompt, max_turns=40):
        self.calls.append((prompt, max_turns))
        return {"success": True, "stop_reason": "completed", "output": "done"}


class FailingEngine:
    async def run_single_task(self, prompt, max_turns=40):
        return {"success": False, "stop_reason": "error", "error": "boom"}


def test_adapter_exports_terminal_bench_agent():
    assert hasattr(adapter, "MiniClaudeCodeTerminalBenchAgent")
    assert adapter.MiniClaudeCodeAgent is adapter.MiniClaudeCodeTerminalBenchAgent
    assert issubclass(adapter.MiniClaudeCodeTerminalBenchAgent, adapter.BaseAgent)
    assert adapter.MiniClaudeCodeTerminalBenchAgent.name() == "mini-claude-code-cli"


def test_adapter_accepts_terminal_bench_kwargs():
    agent = adapter.MiniClaudeCodeTerminalBenchAgent(
        model="test-model", max_turns=5, task_ids=["demo"]
    )
    assert agent.model == "test-model"
    assert agent.max_turns == 5
    assert agent.extra_kwargs == {"task_ids": ["demo"]}


@pytest.mark.parametrize("max_turns", [0, -1, 1.5, "2"])
def test_adapter_rejects_invalid_max_turns(max_turns):
    with pytest.raises(ValueError, match="max_turns must be a positive integer"):
        adapter.MiniClaudeCodeTerminalBenchAgent(max_turns=max_turns)


def test_perform_task_runs_engine_and_stores_summary():
    engine = RecordingEngine()
    agent = adapter.MiniClaudeCodeTerminalBenchAgent(
        max_turns=7, engine_factory=lambda: engine
    )

    agent.perform_task("  solve this task  ", session=None)

    assert engine.calls == [("solve this task", 7)]
    assert agent.last_result == adapter.MiniClaudeRunSummary(
        success=True, stop_reason="completed", output="done", error=None
    )


def test_perform_task_raises_when_engine_reports_failure():
    agent = adapter.MiniClaudeCodeTerminalBenchAgent(engine_factory=FailingEngine)

    with pytest.raises(RuntimeError, match="boom"):
        agent.perform_task("solve", session=None)

    assert agent.last_result.success is False
    assert agent.last_result.error == "boom"


def test_task_session_id_prefers_explicit_configuration():
    assert adapter.task_session_id(
        "manual/session", task_name="fix-git", logging_dir="other"
    ) == "manual-session"


def test_task_session_id_uses_task_id_and_sanitizes_filename():
    assert adapter.task_session_id(
        None, task_id="fix-git", task_name=None
    ) == "fix-git"
    assert adapter.safe_session_id("fix/git: v1") == "fix-git-v1"


def test_task_session_id_falls_back_to_session_metadata_and_logging_dir(tmp_path):
    session = type("Session", (), {"task_id": "metadata-task"})()
    assert adapter.task_session_id(None, session=session) == "metadata-task"
    assert adapter.task_session_id(
        None, logging_dir=tmp_path / "fix-git"
    ) == "fix-git"


def test_default_engine_passes_task_id_as_session_id(monkeypatch):
    captured = {}

    class FakeAgentEngine:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    class FakeMemoryManager:
        def __init__(self, *args, **kwargs):
            pass

    class FakePlanManager:
        def __init__(self, *args, **kwargs):
            pass

    monkeypatch.setattr("core.engine.AgentEngine", FakeAgentEngine, raising=False)
    monkeypatch.setattr("core.memory_manager.MemoryManager", FakeMemoryManager)
    monkeypatch.setattr("core.plan.PlanManager", FakePlanManager)
    monkeypatch.setattr(
        "main.get_agent_config",
        lambda: {"base_url": "https://example.invalid", "api_key": "test-key"},
    )
    monkeypatch.setattr("tools.get_default_tools", lambda **kwargs: [])

    agent = adapter.MiniClaudeCodeTerminalBenchAgent(
        model="test-model", task_id="fix-git"
    )
    agent._current_task_name = "fix-git"
    agent._create_default_engine()

    assert captured["session_id"] == "fix-git"
