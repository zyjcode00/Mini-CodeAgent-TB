import pytest
from pydantic import BaseModel

from core.engine import AgentEngine
from core.plan import PlanManager
from core.read_guard import ReadOnlyStreakGuard, RuntimeReadLedger
from tools.base import BaseTool


class ReadFileArgs(BaseModel):
    path: str
    start_line: int | None = None
    end_line: int | None = None


class DummyReadFileTool(BaseTool):
    name = "read_file"
    description = "dummy read file tool"
    args_schema = ReadFileArgs

    def run(self, **kwargs) -> str:
        return f"content:{kwargs.get('path')}:{kwargs.get('start_line')}-{kwargs.get('end_line')}"


class DummyPlanManager(PlanManager):
    pass


def make_engine():
    return AgentEngine(
        tools=[DummyReadFileTool()],
        model="gpt-test",
        plan_manager=DummyPlanManager(),
        base_url="http://example.invalid/v1",
        api_key="test",
        session_id="test_read_guard_unit",
    )


def assert_valid_openai_tool_pairs(messages):
    for i, msg in enumerate(messages):
        if msg.get("role") == "assistant" and msg.get("tool_calls"):
            expected_ids = {tc["id"] for tc in msg["tool_calls"]}
            contiguous_ids = set()
            j = i + 1
            while j < len(messages) and messages[j].get("role") == "tool":
                contiguous_ids.add(messages[j].get("tool_call_id"))
                j += 1
            assert expected_ids.issubset(contiguous_ids)

        if msg.get("role") == "tool":
            block_start = i
            while block_start > 0 and messages[block_start - 1].get("role") == "tool":
                block_start -= 1
            assert block_start > 0
            prev_msg = messages[block_start - 1]
            assert prev_msg.get("role") == "assistant" and prev_msg.get("tool_calls")
            assert msg.get("tool_call_id") in {tc["id"] for tc in prev_msg["tool_calls"]}


def test_runtime_read_ledger_warns_on_duplicate_but_not_forward_pagination():
    ledger = RuntimeReadLedger(duplicate_threshold=2)

    assert ledger.record({"path": "core/engine.py", "start_line": 1, "end_line": 100}) == []
    duplicate_reminders = ledger.record({"path": "core/engine.py", "start_line": 1, "end_line": 100})

    assert any("相同范围" in reminder for reminder in duplicate_reminders)

    # Normal forward pagination is allowed and should not produce reminders.
    assert ledger.record({"path": "core/engine.py", "start_line": 100, "end_line": 200}) == []
    assert ledger.record({"path": "core/engine.py", "start_line": 200, "end_line": 300}) == []


def test_runtime_read_ledger_warns_on_contained_range_without_blocking():
    ledger = RuntimeReadLedger(duplicate_threshold=2)

    assert ledger.record({"path": "core/engine.py", "start_line": 1, "end_line": 300}) == []
    reminders = ledger.record({"path": "core/engine.py", "start_line": 50, "end_line": 80})

    assert any("已被先前读取" in reminder for reminder in reminders)


def test_read_only_streak_guard_checkpoint_resets_after_write_tool():
    guard = ReadOnlyStreakGuard(checkpoint_threshold=3)

    assert guard.record_round(["read_file"]) is None
    assert guard.record_round(["search_code"]) is None
    assert "只读工具防空转检查点" in guard.record_round(["read_file"])

    assert guard.record_round(["edit_file"]) is None
    assert guard.streak == 0
    assert guard.record_round(["read_file"]) is None


@pytest.mark.asyncio
async def test_engine_injects_read_guard_messages_after_tool_pairs(monkeypatch):
    engine = make_engine()

    async def fake_compress_messages():
        return None

    monkeypatch.setattr(engine, "compress_messages", fake_compress_messages)
    monkeypatch.setattr(engine, "_build_relevant_memory_context", lambda user_input: "")
    monkeypatch.setattr(engine, "_observe_prompt_submit", lambda user_input: None)
    monkeypatch.setattr(engine, "_observe_tool_result", lambda name, inp, res: None)
    monkeypatch.setattr(engine, "_build_post_tool_failure_memory_context", lambda name, res: "")
    monkeypatch.setattr(engine, "_build_pre_tool_memory_context", lambda name, inp: "")
    monkeypatch.setattr(engine, "save_session", lambda: None)
    monkeypatch.setattr(engine, "_remember_task_completion", lambda user_input, final_ans: None)

    read_inputs = [
        {"path": "core/engine.py", "start_line": 1, "end_line": 100},
        {"path": "core/engine.py", "start_line": 1, "end_line": 100},
        {"path": "core/engine.py", "start_line": 100, "end_line": 200},
    ]
    calls = {"count": 0}

    async def fake_call_llm(relevant_history="", user_input=""):
        calls["count"] += 1
        if calls["count"] <= len(read_inputs):
            call_id = f"call_{calls['count']}"
            tool_input = read_inputs[calls["count"] - 1]
            engine.last_oa_msg = {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": call_id,
                        "type": "function",
                        "function": {"name": "read_file", "arguments": "{}"},
                    }
                ],
            }
            return [
                {"type": "tool_use", "id": call_id, "name": "read_file", "input": tool_input}
            ], "tool_use"

        engine.last_oa_msg = {"role": "assistant", "content": "done"}
        return [{"type": "text", "text": "done"}], "end_turn"

    monkeypatch.setattr(engine, "_call_llm", fake_call_llm)

    result = await engine.execute_query("inspect")

    assert result == "done"
    assert_valid_openai_tool_pairs(engine.context.messages)

    duplicate_messages = [
        m for m in engine.context.messages
        if m.get("role") == "user" and "相同范围" in str(m.get("content"))
    ]
    checkpoint_messages = [
        m for m in engine.context.messages
        if m.get("role") == "user" and "只读工具防空转检查点" in str(m.get("content"))
    ]

    assert duplicate_messages
    assert checkpoint_messages

    for msg in duplicate_messages + checkpoint_messages:
        idx = engine.context.messages.index(msg)
        assert idx > 0
        assert engine.context.messages[idx - 1].get("role") == "tool"
