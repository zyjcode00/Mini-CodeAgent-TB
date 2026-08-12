"""Optional real end-to-end smoke test for the Terminal-Bench runner.

This test is skipped by default because it may call the real agent backend and
therefore can require network access, credentials, and more time than unit tests.
Enable it explicitly with:

    set TERMINAL_BENCH_REAL_SMOKE=1
    pytest tests/test_terminal_bench_real_smoke.py

On POSIX shells:

    TERMINAL_BENCH_REAL_SMOKE=1 pytest tests/test_terminal_bench_real_smoke.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNNER = PROJECT_ROOT / "scripts" / "run_terminal_bench_agent.py"
ENABLE_ENV = "TERMINAL_BENCH_REAL_SMOKE"


@pytest.mark.skipif(
    os.environ.get(ENABLE_ENV) != "1",
    reason=f"set {ENABLE_ENV}=1 to run the real Terminal-Bench smoke test",
)
def test_real_terminal_bench_runner_creates_file_and_writes_json(tmp_path: Path) -> None:
    """Run the real runner on a tiny file task in an isolated workspace."""

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    output_json = tmp_path / "agent_result.json"

    task = (
        "In the current workspace, create a file named hello.txt containing "
        "exactly the text: hello from terminal bench smoke"
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--task",
            task,
            "--workspace",
            str(workspace),
            "--max-turns",
            "6",
            "--timeout",
            "120",
            "--output-json",
            str(output_json),
            "--disable-memory",
            "--disable-auto-commit",
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        timeout=150,
    )

    assert completed.returncode == 0, (
        "runner failed\n"
        f"STDOUT:\n{completed.stdout}\n\n"
        f"STDERR:\n{completed.stderr}"
    )
    assert output_json.exists(), "runner did not write the requested JSON output"

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    assert payload.get("success") is True
    assert str(payload.get("workspace")) == str(workspace)
    assert "error" in payload

    created_file = workspace / "hello.txt"
    assert created_file.exists(), "agent did not create hello.txt in the workspace"
    assert created_file.read_text(encoding="utf-8").strip() == (
        "hello from terminal bench smoke"
    )
