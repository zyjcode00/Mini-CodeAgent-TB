import json

from core.engine import AgentEngine


class DummyPlanManager:
    current_goal = ""

    def get_formatted_plan(self):
        return ""

    def is_plan_complete(self):
        return False

    def to_dict(self):
        return {}

    def load_from_dict(self, data):
        pass


def test_save_session_replaces_lone_surrogates(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    engine = AgentEngine(tools=[], model="gpt-test", plan_manager=DummyPlanManager())
    engine.session_path = str(tmp_path / "session.json")

    engine.context.messages = [
        {"role": "user", "content": "bad surrogate: \udce6"},
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": "nested surrogate: \udcff"},
            ],
        },
    ]
    engine.context.history_summary = "summary surrogate: \udce6"

    engine.save_session()

    raw = (tmp_path / "session.json").read_text(encoding="utf-8")
    assert "\udce6" not in raw
    assert "\udcff" not in raw
    assert "�" in raw

    data = json.loads(raw)
    assert data["messages"][0]["content"] == "bad surrogate: �"
    assert data["history_summary"] == "summary surrogate: �"
