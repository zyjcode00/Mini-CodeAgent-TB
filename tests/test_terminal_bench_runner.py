import asyncio
import json
import os
from pathlib import Path

import pytest

from scripts import run_terminal_bench_agent as runner
from scripts.run_terminal_bench_agent import (
    EXIT_ERROR,
    EXIT_SUCCESS,
    EXIT_TIMEOUT,
    main_async,
)


class RecordingEngine:
    def __init__(self, calls, result=None):
        self.calls = calls
        self.result = result or {
            "success": True,
            "stop_reason": "completed",
            "turns": 3,
            "message": "done",
        }

    async def run_single_task(self, prompt, max_turns=40):
        self.calls.append(
            {
                "prompt": prompt,
                "max_turns": max_turns,
                "cwd": Path.cwd(),
            }
        )
        return self.result


class FailingEngine:
    async def run_single_task(self, prompt, max_turns=40):
        raise RuntimeError("boom")


class SlowEngine:
    async def run_single_task(self, prompt, max_turns=40):
        await asyncio.sleep(10)
        return {"success": True, "stop_reason": "completed"}


class ClosableSlowEngine(SlowEngine):
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


def test_runner_accepts_inline_task_switches_cwd_and_writes_json(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    output_json = tmp_path / "result" / "agent_result.json"
    calls = []

    exit_code = asyncio.run(
        main_async(
            [
                "--task",
                "Fix the bug and run tests.",
                "--workspace",
                str(workspace),
                "--max-turns",
                "7",
                "--output-json",
                str(output_json),
            ],
            engine_factory=lambda args: RecordingEngine(calls),
        )
    )

    assert exit_code == EXIT_SUCCESS
    assert len(calls) == 1
    assert calls[0]["cwd"] == workspace.resolve()
    assert calls[0]["max_turns"] == 7
    assert "Terminal-Bench" in calls[0]["prompt"]
    assert "Fix the bug and run tests." in calls[0]["prompt"]
    assert Path.cwd() != workspace.resolve()

    data = json.loads(output_json.read_text(encoding="utf-8"))
    assert data["success"] is True
    assert data["stop_reason"] == "completed"
    assert data["turns"] == 3
    assert data["workspace"] == str(workspace.resolve())
    assert isinstance(data["duration_seconds"], float)


def test_runner_accepts_task_file(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    task_file = tmp_path / "task.txt"
    task_file.write_text("Use pytest to verify the fix.", encoding="utf-8")
    calls = []

    exit_code = asyncio.run(
        main_async(
            [
                "--task-file",
                str(task_file),
                "--workspace",
                str(workspace),
            ],
            engine_factory=lambda args: RecordingEngine(calls),
        )
    )

    assert exit_code == EXIT_SUCCESS
    assert len(calls) == 1
    assert "Use pytest to verify the fix." in calls[0]["prompt"]


def test_invalid_workspace_returns_error_and_writes_json(tmp_path):
    missing_workspace = tmp_path / "missing"
    output_json = tmp_path / "result.json"

    exit_code = asyncio.run(
        main_async(
            [
                "--task",
                "hello",
                "--workspace",
                str(missing_workspace),
                "--output-json",
                str(output_json),
            ],
            engine_factory=lambda args: RecordingEngine([]),
        )
    )

    assert exit_code == EXIT_ERROR
    data = json.loads(output_json.read_text(encoding="utf-8"))
    assert data["success"] is False
    assert data["stop_reason"] == "invalid_workspace"
    assert "Invalid workspace" in data["error"]


def test_required_path_postcondition_prevents_false_success(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    output_json = tmp_path / "result.json"

    exit_code = asyncio.run(main_async([
        "--task", "build", "--workspace", str(workspace),
        "--require-path", "bin/stp", "--output-json", str(output_json),
    ], engine_factory=lambda args: RecordingEngine([])))

    assert exit_code == EXIT_ERROR
    data = json.loads(output_json.read_text(encoding="utf-8"))
    assert data["success"] is False
    assert data["stop_reason"] == "verification_failed"
    assert "bin/stp" in data["error"]
    assert "PATH" in data["recovery_hint"]


def test_verify_command_postcondition(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    failed = asyncio.run(main_async([
        "--task", "build", "--workspace", str(workspace),
        "--verify-command", "test -x bin/stp",
    ], engine_factory=lambda args: RecordingEngine([])))
    assert failed == EXIT_ERROR

    (workspace / "bin").mkdir()
    (workspace / "bin" / "stp").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    (workspace / "bin" / "stp").chmod(0o755)
    passed = asyncio.run(main_async([
        "--task", "build", "--workspace", str(workspace),
        "--verify-command", "test -x bin/stp",
    ], engine_factory=lambda args: RecordingEngine([])))
    assert passed == EXIT_SUCCESS


def test_engine_exception_returns_error_and_restores_cwd(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    original_cwd = Path.cwd()
    output_json = tmp_path / "result.json"

    exit_code = asyncio.run(
        main_async(
            [
                "--task",
                "trigger failure",
                "--workspace",
                str(workspace),
                "--output-json",
                str(output_json),
            ],
            engine_factory=lambda args: FailingEngine(),
        )
    )

    assert exit_code == EXIT_ERROR
    assert Path.cwd() == original_cwd
    data = json.loads(output_json.read_text(encoding="utf-8"))
    assert data["success"] is False
    assert data["stop_reason"] == "exception"
    assert "RuntimeError: boom" == data["error"]


def test_timeout_returns_124_and_writes_json(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    output_json = tmp_path / "timeout.json"

    exit_code = asyncio.run(
        main_async(
            [
                "--task",
                "slow task",
                "--workspace",
                str(workspace),
                "--timeout",
                "0.01",
                "--output-json",
                str(output_json),
            ],
            engine_factory=lambda args: SlowEngine(),
        )
    )

    assert exit_code == EXIT_TIMEOUT
    data = json.loads(output_json.read_text(encoding="utf-8"))
    assert data["success"] is False
    assert data["stop_reason"] == "timeout"
    assert "Timed out" in data["error"]


def test_timeout_closes_engine(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    engine = ClosableSlowEngine()

    exit_code = asyncio.run(
        main_async(
            [
                "--task",
                "slow task",
                "--workspace",
                str(workspace),
                "--timeout",
                "0.01",
            ],
            engine_factory=lambda args: engine,
        )
    )

    assert exit_code == EXIT_TIMEOUT
    assert engine.closed is True


def test_non_terminal_stop_reason_cannot_report_success(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    output_json = tmp_path / "guarded.json"

    class GuardedEngine:
        async def run_single_task(self, prompt, max_turns=40):
            return {
                "success": True,
                "stop_reason": "agent_timeout",
                "turns": 6,
                "message": "stopped early",
            }

    exit_code = asyncio.run(
        main_async(
            [
                "--task",
                "complete the work",
                "--workspace",
                str(workspace),
                "--output-json",
                str(output_json),
            ],
            engine_factory=lambda args: GuardedEngine(),
        )
    )

    assert exit_code == EXIT_ERROR
    data = json.loads(output_json.read_text(encoding="utf-8"))
    assert data["success"] is False
    assert data["stop_reason"] == "agent_timeout"
    assert "Agent stopped before completion" in data["error"]


def test_session_id_for_args_prefers_explicit_task_id_then_task_file(monkeypatch, tmp_path):
    monkeypatch.setenv("MINI_CLAUDE_SESSION", "agent-logs")

    explicit = runner.parse_args([
        "--task", "solve", "--workspace", str(tmp_path),
        "--task-id", "fix-git", "--session-id", "manual session",
    ])
    assert runner.session_id_for_args(explicit) == "manual-session"

    task_id_args = runner.parse_args([
        "--task", "solve", "--workspace", str(tmp_path), "--task-id", "fix-git",
    ])
    assert runner.session_id_for_args(task_id_args) == "fix-git"

    task_file = tmp_path / "mailman task.txt"
    task_file.write_text("solve", encoding="utf-8")
    task_file_args = runner.parse_args([
        "--task-file", str(task_file), "--workspace", str(tmp_path),
    ])
    assert runner.session_id_for_args(task_file_args) == "mailman-task"


def test_default_engine_factory_uses_task_id_session_instead_of_agent_logs(monkeypatch, tmp_path):
    captured = {}

    class FakeAgentEngine:
        def __init__(self, **kwargs):
            captured.update(kwargs)

        async def run_single_task(self, prompt, max_turns=40):
            return {"success": True, "stop_reason": "completed"}

    class FakePlanManager:
        pass

    monkeypatch.setenv("MINI_CLAUDE_API_KEY", "test-key")
    monkeypatch.setenv("MINI_CLAUDE_SESSION", "agent-logs")
    monkeypatch.setattr(runner, "AgentEngine", FakeAgentEngine, raising=False)
    monkeypatch.setattr(runner, "PlanManager", FakePlanManager, raising=False)
    monkeypatch.setattr(runner, "MemoryManager", None, raising=False)
    monkeypatch.setattr(runner, "get_default_tools", lambda **kwargs: [], raising=False)

    args = runner.parse_args([
        "--task", "solve", "--workspace", str(tmp_path), "--task-id", "fix-git",
    ])
    engine = runner.default_engine_factory(args)

    assert isinstance(engine, FakeAgentEngine)
    assert captured["session_id"] == "fix-git"
