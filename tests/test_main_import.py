import importlib


def test_main_imports_agent_engine():
    main = importlib.import_module("main")

    assert main.AgentEngine.__name__ == "AgentEngine"
