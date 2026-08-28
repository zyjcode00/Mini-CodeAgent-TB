"""Regression tests for Terminal-Bench Git automation isolation."""

import inspect

import core.engine as engine_module
import terminal_bench_adapter as adapter_module


def test_terminal_bench_agent_disables_git_automation(monkeypatch):
    captured = {}

    class FakeEngine:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    import core.engine as core_engine
    import core.memory_manager as memory_module
    import core.plan as plan_module
    import main as main_module
    import tools as tools_module
    import tools.execution_backend as backend_module

    monkeypatch.setattr(core_engine, "AgentEngine", FakeEngine)

    # Avoid constructing the external model/client and memory dependencies.
    monkeypatch.setattr(main_module, "get_agent_config", lambda: {"base_url": "", "api_key": "", "model": ""})
    monkeypatch.setattr(tools_module, "get_default_tools", lambda **_: [])
    monkeypatch.setattr(memory_module, "MemoryManager", lambda **_: object())
    monkeypatch.setattr(plan_module, "PlanManager", lambda: object())
    monkeypatch.setattr(backend_module, "TerminalBenchSessionBackend", lambda **_: object())

    adapter_module.MiniClaudeCodeTerminalBenchAgent()._create_default_engine()

    assert captured["enable_git_automation"] is False


def test_regular_agent_engine_keeps_git_automation_enabled_by_default():
    signature = inspect.signature(engine_module.AgentEngine.__init__)

    assert signature.parameters["enable_git_automation"].default is True
