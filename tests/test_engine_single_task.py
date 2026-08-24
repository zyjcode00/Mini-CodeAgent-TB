import pytest

from core.engine import AgentEngine
from core.plan import PlanManager
from tools.execution_backend import ExecutorShutdownError


def make_engine():
    return AgentEngine(
        tools=[],
        model="fake-model",
        plan_manager=PlanManager(),
        base_url="http://example.invalid",
        api_key="test-key",
    )


@pytest.mark.asyncio
async def test_run_single_task_wraps_execute_query_success(monkeypatch):
    engine = make_engine()
    seen = {}

    async def fake_execute_query(prompt):
        seen["prompt"] = prompt
        return "task complete"

    monkeypatch.setattr(engine, "execute_query", fake_execute_query)

    result = await engine.run_single_task("  solve task  ", max_turns=7)

    assert seen == {"prompt": "solve task"}
    assert result == {
        "success": True,
        "stop_reason": "completed",
        "final_answer": "task complete",
        "turns": 1,
        "max_turns": 7,
        "error": None,
    }


@pytest.mark.asyncio
async def test_run_single_task_detects_internal_turn_limit(monkeypatch):
    engine = make_engine()

    async def fake_execute_query(prompt):
        return "任务达到最大思考步数限制。"

    monkeypatch.setattr(engine, "execute_query", fake_execute_query)

    result = await engine.run_single_task("solve task", max_turns=3)

    assert result["success"] is False
    assert result["stop_reason"] == "max_turns"
    assert result["final_answer"] == "任务达到最大思考步数限制。"
    assert result["error"] == "Agent reached its internal reasoning limit before completion."


@pytest.mark.asyncio
async def test_run_single_task_reports_execute_query_error(monkeypatch):
    engine = make_engine()

    async def fake_execute_query(prompt):
        raise RuntimeError("boom")

    monkeypatch.setattr(engine, "execute_query", fake_execute_query)

    result = await engine.run_single_task("solve task", max_turns=3)

    assert result["success"] is False
    assert result["final_answer"] == ""
    assert result["turns"] == 1
    assert result["max_turns"] == 3
    assert result["error"] == "RuntimeError: boom"


@pytest.mark.asyncio
async def test_run_single_task_reports_executor_shutdown(monkeypatch):
    engine = make_engine()

    async def fake_execute_query(prompt):
        raise ExecutorShutdownError("cannot schedule new futures after shutdown")

    monkeypatch.setattr(engine, "execute_query", fake_execute_query)

    result = await engine.run_single_task("solve task", max_turns=3)

    assert result["success"] is False
    assert result["stop_reason"] == "executor_shutdown"
    assert result["error"] == (
        "ExecutorShutdownError: cannot schedule new futures after shutdown"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("prompt", ["", "   ", None])
async def test_run_single_task_rejects_empty_prompt(prompt):
    engine = make_engine()

    with pytest.raises(ValueError, match="prompt must be a non-empty string"):
        await engine.run_single_task(prompt)


@pytest.mark.asyncio
@pytest.mark.parametrize("max_turns", [0, -1, 1.5, "2"])
async def test_run_single_task_rejects_invalid_max_turns(max_turns):
    engine = make_engine()

    with pytest.raises(ValueError, match="max_turns must be a positive integer"):
        await engine.run_single_task("solve task", max_turns=max_turns)
