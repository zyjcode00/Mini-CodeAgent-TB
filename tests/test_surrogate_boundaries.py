"""Regression tests for lone-surrogate data crossing session persistence boundaries."""

import json
from pathlib import Path

from core.engine import AgentEngine


class _DummyPlanManager:
    current_goal = None

    def is_plan_complete(self):
        return False

    def to_dict(self):
        return {"current_goal": None, "tasks": []}


class _DummyContext:
    def __init__(self, messages, memories, history_summary=""):
        self.history_summary = history_summary
        self.messages = messages
        self._enable_memory_layers = False
        self.session_summaries = []
        self._memories = memories

    def get_serializable_messages(self):
        return self.messages

    def export_memories(self):
        return self._memories


def test_save_session_sanitizes_lone_surrogates_in_nested_runtime_data(tmp_path: Path):
    """Session persistence must not crash when runtime data contains lone surrogates.

    Python can create lone surrogate characters from subprocess/file-system edge
    cases via surrogateescape.  json.dump(..., ensure_ascii=False) followed by a
    UTF-8 TextIO write raises UnicodeEncodeError unless these values are cleaned
    before reaching the persistence boundary.
    """

    bad = chr(0xDCE5)
    engine = AgentEngine.__new__(AgentEngine)
    engine.session_path = str(tmp_path / "session.json")
    engine.plan_manager = _DummyPlanManager()
    engine.context = _DummyContext(
        messages=[
            {"role": "user", "content": f"run output: {bad}"},
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": f"nested text {bad}"},
                    {"type": "tool_result", "content": {"stderr": f"err {bad}"}},
                ],
            },
        ],
        memories={
            "observations": [f"memory {bad}", {"tool": f"bash {bad}"}],
            "metadata": {"cwd": f"/tmp/{bad}"},
        },
        history_summary=f"summary {bad}",
    )
    engine.todo_manager = None

    engine.save_session()

    raw = Path(engine.session_path).read_text(encoding="utf-8")
    assert bad not in raw
    data = json.loads(raw)
    assert data["history_summary"] == "summary �"
    assert data["messages"][0]["content"] == "run output: �"
    assert data["messages"][1]["content"][0]["text"] == "nested text �"
    assert data["messages"][1]["content"][1]["content"]["stderr"] == "err �"
    assert data["memories"]["observations"][0] == "memory �"
    assert data["memories"]["metadata"]["cwd"] == "/tmp/�"
