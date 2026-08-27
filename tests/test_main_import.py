import importlib


def test_main_imports_agent_engine():
    main = importlib.import_module("main")
    engine = importlib.import_module("core.engine")

    assert main.AgentEngine is engine.AgentEngine


def test_remote_workspace_module_available():
    remote_workspace = importlib.import_module("tools.remote_workspace")

    assert callable(remote_workspace.python_command)
