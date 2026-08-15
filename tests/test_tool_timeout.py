import asyncio
import time

import pytest
from pydantic import BaseModel

from core.engine import AgentEngine
from core.plan import PlanManager
from tools.base import BaseTool


class BlockingArgs(BaseModel):
    delay: float = 2.0


class BlockingTool(BaseTool):
    name = "blocking"
    description = "blocks longer than the agent tool timeout"
    args_schema = BlockingArgs

    def run(self, **kwargs) -> str:
        time.sleep(kwargs.get("delay", 2.0))
        return "finished"


class DummyPlanManager(PlanManager):
    pass


def make_engine() -> AgentEngine:
    return AgentEngine(
        tools=[BlockingTool()],
        model="gpt-test",
        plan_manager=DummyPlanManager(),
        base_url="http://example.invalid/v1",
        api_key="test",
        session_id="test_tool_timeout_unit",
    )


@pytest.mark.asyncio
async def test_blocking_sync_tool_times_out_without_waiting_for_thread_completion():
    engine = make_engine()
    tool = engine.tools[0]
    engine.tool_timeout_seconds = 0.05

    start = time.monotonic()
    with pytest.raises(TimeoutError, match="Tool 'blocking' exceeded timeout"):
        await engine._run_tool_with_timeout(tool, {"delay": 2.0})
    elapsed = time.monotonic() - start

    assert elapsed < 0.5


@pytest.mark.asyncio
async def test_sync_tool_success_still_returns_result():
    engine = make_engine()
    tool = engine.tools[0]
    engine.tool_timeout_seconds = 1.0

    result = await engine._run_tool_with_timeout(tool, {"delay": 0.01})

    assert result == "finished"
