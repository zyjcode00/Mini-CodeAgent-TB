from __future__ import annotations

import types

from tools import get_default_tools
from tools.bash_tool import BashTool
from tools.execution_backend import LocalExecutionBackend, TerminalBenchSessionBackend
from tools.file_tool import FileEditTool, ReadTool, WriteFullFileTool
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


def test_get_default_tools_keeps_local_backends_by_default():
    tools = get_default_tools()
    for name in ("execute_bash", "search_code", "list_all_symbols", "find_symbol_definition", "run_pytest"):
        tool = _find_tool(tools, name)
        assert isinstance(tool.backend, LocalExecutionBackend)


def test_get_default_tools_injects_session_backend_into_workspace_tools():
    session = FakeSession()
    backend = TerminalBenchSessionBackend(session)
    tools = get_default_tools(execution_backend=backend)

    for name in ("execute_bash", "search_code", "list_all_symbols", "find_symbol_definition", "run_pytest"):
        tool = _find_tool(tools, name)
        assert tool.backend is backend

    _find_tool(tools, "search_code").run("needle", path="/container/project")
    _find_tool(tools, "list_all_symbols").run(path="/container/project")
    _find_tool(tools, "find_symbol_definition").run("Needle", path="/container/project")
    _find_tool(tools, "run_pytest").run("tests/test_needle.py")

    assert len(session.commands) == 4
    assert all("workspace-tool" in command or command.startswith("pytest -v") for command in session.commands)


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


def _find_tool(tools, name):
    return next(tool for tool in tools if getattr(tool, "name", None) == name)


def test_terminal_bench_backend_routes_file_tools_to_session(tmp_path, monkeypatch):
    class FileSession(FakeSession):
        def run(self, command: str):
            self.commands.append(command)
            if "cat --" in command:
                return {"stdout": "container README\nsecond line\n", "stderr": "", "exit_code": 0}
            if "find" in command:
                return {"stdout": "./\n./README.md\n", "stderr": "", "exit_code": 0}
            return {"stdout": "", "stderr": "", "exit_code": 0}

    local_file = tmp_path / "README.md"
    local_file.write_text("host README\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    session = FileSession()
    backend = TerminalBenchSessionBackend(session)
    tools = get_default_tools(execution_backend=backend)

    read_result = _find_tool(tools, "read_file").run("README.md", raw_mode=True)
    tree_result = _find_tool(tools, "list_files_recursive").run()

    assert read_result == "container README\nsecond line\n"
    assert "container README" in read_result
    assert "host README" not in read_result
    assert "README.md" in tree_result
    assert any("cat --" in command for command in session.commands)
    assert any("find" in command for command in session.commands)


def test_backend_file_tools_pass_arguments_before_heredoc(tmp_path):
    backend = LocalExecutionBackend()
    path = tmp_path / "file with spaces.txt"

    write_result = WriteFullFileTool(backend).run(str(path), "first\nsecond\n")
    read_result = ReadTool(backend).run(str(path), start_line=2, end_line=2, raw_mode=True)
    edit_result = FileEditTool(backend).run(str(path), "second", "updated")

    assert "成功: 已写入" in write_result
    assert read_result == "second\n"
    assert "成功: 已更新" in edit_result
    assert path.read_text(encoding="utf-8") == "first\nupdated\n"
