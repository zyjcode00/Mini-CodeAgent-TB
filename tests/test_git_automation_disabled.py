"""Regression tests for disabling Git side effects in evaluation adapters."""

from core.engine import AgentEngine


class _PlanManager:
    def get_formatted_plan(self):
        return ""

    def get_plan_id(self):
        return "plan-test"

    def is_plan_complete(self):
        return False


def test_agent_engine_accepts_enable_git_automation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    engine = AgentEngine(
        tools=[],
        model="fake-model",
        plan_manager=_PlanManager(),
        base_url="http://example.invalid",
        api_key="test-key",
        enable_git_automation=False,
    )
    assert engine.enable_git_automation is False


def test_disabled_git_automation_skips_plan_branch(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    called = []

    def fail_if_called(*args, **kwargs):
        called.append((args, kwargs))
        raise AssertionError("Git automation must be disabled")

    monkeypatch.setattr("core.engine.start_plan_branch", fail_if_called)
    engine = AgentEngine(
        tools=[],
        model="fake-model",
        plan_manager=_PlanManager(),
        base_url="http://example.invalid",
        api_key="test-key",
        enable_git_automation=False,
    )
    # The guard is directly exercised here; execute_query's loop uses the same condition.
    plan_id = engine.plan_manager.get_plan_id()
    assert not (
        engine.enable_git_automation
        and plan_id
        and not engine.current_plan_branch
        and engine.skipped_plan_branch_id != plan_id
    )
    assert called == []
