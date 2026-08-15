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
