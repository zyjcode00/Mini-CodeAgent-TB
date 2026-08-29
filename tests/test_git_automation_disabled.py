"""Regression tests for disabling AgentEngine git automation."""

import asyncio

from core.engine import AgentEngine
from core.plan import PlanManager
from tools.base import BaseTool


class DummyTool(BaseTool):
    name = "dummy"
    description = "dummy"
    args_schema = None

    def run(self, **kwargs):
        return "ok"


def make_engine(tmp_path):
    return AgentEngine(
        tools=[DummyTool()],
        model="fake-model",
        plan_manager=PlanManager(),
        base_url="http://example.invalid",
        api_key="test-key",
        session_id="git-disabled-regression",
        enable_git_automation=False,
    )


def test_disabled_git_automation_skips_plan_branch_creation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    engine = make_engine(tmp_path)
    calls = []

    monkeypatch.setattr("core.engine.start_plan_branch", lambda plan_id: calls.append(plan_id))

    async def fake_compress_messages():
        return None

    async def fake_call_llm(relevant_history="", user_input=""):
        return [{"type": "text", "text": "done"}], "end_turn"

    monkeypatch.setattr(engine, "compress_messages", fake_compress_messages)
    monkeypatch.setattr(engine, "_call_llm", fake_call_llm)

    assert asyncio.run(engine.execute_query("make progress")) == "done"
    assert calls == []
    assert engine.current_plan_branch is None


def test_disabled_git_automation_skips_snapshot_and_rollback(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    engine = make_engine(tmp_path)
    calls = []

    for name in ("create_snapshot", "rollback_to", "start_plan_branch"):
        monkeypatch.setattr(
            f"core.engine.{name}",
            lambda *args, _name=name, **kwargs: calls.append((_name, args, kwargs)),
        )

    # Exercise the tool loop with a successful task completion.  The patched
    # Git functions must remain untouched when automation is disabled.
    async def fake_compress_messages():
        return None

    responses = iter([
        ([{"type": "tool_use", "id": "tool-1", "name": "dummy", "input": {}}], "tool_use"),
        ([{"type": "text", "text": "done"}], "end_turn"),
    ])

    async def fake_call_llm(relevant_history="", user_input=""):
        return next(responses)

    monkeypatch.setattr(engine, "compress_messages", fake_compress_messages)
    monkeypatch.setattr(engine, "_call_llm", fake_call_llm)

    assert asyncio.run(engine.execute_query("run tool")) == "done"
    assert calls == []
