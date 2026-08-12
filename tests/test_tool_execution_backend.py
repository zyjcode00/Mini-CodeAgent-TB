from __future__ import annotations

import types

from tools import get_default_tools
from tools.bash_tool import BashTool
from tools.execution_backend import LocalExecutionBackend, TerminalBenchSessionBackend
from terminal_bench_adapter import MiniClaudeCodeTerminalBenchAgent


class FakeSession:
    def __init__(self):
        self.commands: list[str] = []

    def run(self, command: str):
        self.commands.append(command)
        return {"stdout": f"session saw: {command}", "stderr": "", "exit_code": 0}


def _find_bash_tool(tools):
    return next(tool for tool in tools if getattr(tool, "name", None) == "execute_bash")


def test_get_default_tools_injects_terminal_bench_backend_into_bash():
    session = FakeSession()
    backend = TerminalBenchSessionBackend(session)

    tools = get_default_tools(execution_backend=backend)
    bash_tool = _find_bash_tool(tools)

    result = bash_tool.run("echo from-container")

    assert session.commands == ["echo from-container"]
    assert "STDOUT:" in result
    assert "session saw: echo from-container" in result


def test_get_default_tools_keeps_local_bash_backend_by_default():
    tools = get_default_tools()
    bash_tool = _find_bash_tool(tools)

    assert isinstance(bash_tool, BashTool)
    assert isinstance(bash_tool.backend, LocalExecutionBackend)


def test_terminal_bench_adapter_default_engine_uses_session_backend(monkeypatch):
    captured = {}

    class FakePlanManager:
        pass

    class FakeMemoryManager:
        def __init__(self, plan_manager=None):
            self.plan_manager = plan_manager

    class FakeAgentEngine:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    def fake_get_agent_config():
        return {"base_url": "https://example.invalid", "api_key": "test-key"}

    import core.engine as core_engine
    import core.memory_manager as core_memory_manager
    import core.plan as core_plan
    import main as main_module

    monkeypatch.setattr(core_engine, "AgentEngine", FakeAgentEngine)
    monkeypatch.setattr(core_memory_manager, "MemoryManager", FakeMemoryManager)
    monkeypatch.setattr(core_plan, "PlanManager", FakePlanManager)
    monkeypatch.setattr(main_module, "get_agent_config", fake_get_agent_config)

    session = FakeSession()
    agent = MiniClaudeCodeTerminalBenchAgent(model="test-model")
    agent._current_session = session

    engine = agent._create_default_engine()
    bash_tool = _find_bash_tool(captured["tools"])

    assert isinstance(engine, FakeAgentEngine)
    assert isinstance(bash_tool.backend, TerminalBenchSessionBackend)
    result = bash_tool.run("pwd")
    assert session.commands == ["pwd"]
    assert "session saw: pwd" in result
