import importlib
import sys


def test_main_imports_from_repo_root_without_missing_tool_modules():
    sys.modules.pop("main", None)

    module = importlib.import_module("main")
    remote_workspace = importlib.import_module("tools.remote_workspace")

    assert hasattr(module, "AgentEngine")
    assert callable(remote_workspace.python_command)
