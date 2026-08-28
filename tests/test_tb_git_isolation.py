"""Regression tests for Terminal-Bench Git automation isolation."""

import inspect

import core.engine as engine_module
import terminal_bench_adapter as adapter_module


def test_terminal_bench_agent_disables_git_automation(monkeypatch):
    captured = {}

    class FakeEngine:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(adapter_module, "AgentEngine", FakeEngine)

    # Avoid constructing the external model/client and memory dependencies.
    monkeypatch.setattr(adapter_module, "get_agent_config", lambda: {})
    monkeypatch.setattr(adapter_module, "get_default_tools", lambda: [])
    monkeypatch.setattr(adapter_module, "MemoryManager", lambda **_: object())
    monkeypatch.setattr(adapter_module, "PlanManager", lambda: object())

    adapter_module.TerminalBenchAgent()

    assert captured["enable_git_automation"] is False


def test_regular_agent_engine_keeps_git_automation_enabled_by_default():
    signature = inspect.signature(engine_module.AgentEngine.__init__)

    assert signature.parameters["enable_git_automation"].default is True
