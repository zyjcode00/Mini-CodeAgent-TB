from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUN_EVALUATION_PATH = PROJECT_ROOT / "scripts" / "run_evaluation.py"

spec = importlib.util.spec_from_file_location("project_run_evaluation", RUN_EVALUATION_PATH)
assert spec is not None
assert spec.loader is not None
run_evaluation = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = run_evaluation
spec.loader.exec_module(run_evaluation)


def test_get_commands_supports_expected_modes() -> None:
    fast = run_evaluation.get_commands("fast")
    memory = run_evaluation.get_commands("memory")
    baseline = run_evaluation.get_commands("baseline")
    all_commands = run_evaluation.get_commands("all")

    assert [command.name for command in fast] == ["pytest-fast"]
    assert [command.name for command in memory] == [
        "memory-benchmark-tests",
        "memory-recall-benchmark",
    ]
    assert [command.name for command in baseline] == ["memory-baseline-compare"]
    assert all_commands == fast + memory + baseline


def test_baseline_command_compares_against_checked_in_baseline() -> None:
    (command,) = run_evaluation.get_commands("baseline")

    assert command.argv == (
        sys.executable,
        "benchmark/memory_recall_benchmark.py",
        "--compare-baseline",
        "benchmark/baselines/memory_recall_baseline.json",
    )
    assert "baseline" in command.description.lower()


def test_get_commands_rejects_unknown_mode() -> None:
    with pytest.raises(ValueError, match="Unsupported evaluation mode"):
        run_evaluation.get_commands("unknown")


def test_dry_run_prints_plan_without_executing(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    calls: list[tuple[str, ...]] = []

    def fake_run(*args, **kwargs):  # pragma: no cover - should never be called
        calls.append(args[0])
        return subprocess.CompletedProcess(args[0], 0)

    monkeypatch.setattr(run_evaluation.subprocess, "run", fake_run)

    exit_code = run_evaluation.main(["baseline", "--dry-run"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert calls == []
    assert "memory-baseline-compare" in output
    assert "--compare-baseline" in output
    assert "Dry run complete" in output


def test_run_commands_stops_on_first_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[str, ...]] = []
    commands = (
        run_evaluation.EvaluationCommand("first", ("cmd-first",), "first command"),
        run_evaluation.EvaluationCommand("second", ("cmd-second",), "second command"),
    )

    def fake_run(argv, cwd, check):
        calls.append(tuple(argv))
        return subprocess.CompletedProcess(argv, 7)

    monkeypatch.setattr(run_evaluation.subprocess, "run", fake_run)

    exit_code = run_evaluation.run_commands(commands)

    assert exit_code == 7
    assert calls == [("cmd-first",)]


def test_run_commands_can_continue_after_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[str, ...]] = []
    commands = (
        run_evaluation.EvaluationCommand("first", ("cmd-first",), "first command"),
        run_evaluation.EvaluationCommand("second", ("cmd-second",), "second command"),
    )

    def fake_run(argv, cwd, check):
        calls.append(tuple(argv))
        return subprocess.CompletedProcess(argv, 5 if argv[0] == "cmd-first" else 0)

    monkeypatch.setattr(run_evaluation.subprocess, "run", fake_run)

    exit_code = run_evaluation.run_commands(commands, continue_on_failure=True)

    assert exit_code == 5
    assert calls == [("cmd-first",), ("cmd-second",)]
