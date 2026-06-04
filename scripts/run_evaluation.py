"""Unified evaluation runner for the project.

This script is the unified entrypoint for running project evaluations with a
small set of stable modes:

- fast: quick unit/regression checks for normal development.
- memory: memory-recall benchmark related checks.
- baseline: benchmark baseline comparison / regression gate checks.
- all: the full pytest suite plus memory benchmark and baseline checks.

Use ``--dry-run`` to print the commands without executing them.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class EvaluationCommand:
    """A single command in an evaluation plan."""

    name: str
    argv: tuple[str, ...]
    description: str


FAST_COMMANDS: tuple[EvaluationCommand, ...] = (
    EvaluationCommand(
        name="pytest-fast",
        argv=(sys.executable, "-m", "pytest", "tests", "-q"),
        description="Run the project pytest suite in quiet mode.",
    ),
)

MEMORY_COMMANDS: tuple[EvaluationCommand, ...] = (
    EvaluationCommand(
        name="memory-benchmark-tests",
        argv=(sys.executable, "-m", "pytest", "tests/test_memory_recall_benchmark.py", "-q"),
        description="Run tests for the memory recall benchmark harness.",
    ),
    EvaluationCommand(
        name="memory-recall-benchmark",
        argv=(sys.executable, "benchmark/memory_recall_benchmark.py"),
        description="Run the memory recall benchmark and refresh latest report artifacts.",
    ),
)

BASELINE_COMMANDS: tuple[EvaluationCommand, ...] = (
    EvaluationCommand(
        name="memory-baseline-compare",
        argv=(
            sys.executable,
            "benchmark/memory_recall_benchmark.py",
            "--compare-baseline",
            "benchmark/baselines/memory_recall_baseline.json",
        ),
        description="Compare current memory recall quality against the checked-in baseline.",
    ),
)


COMMAND_GROUPS: dict[str, tuple[EvaluationCommand, ...]] = {
    "fast": FAST_COMMANDS,
    "memory": MEMORY_COMMANDS,
    "baseline": BASELINE_COMMANDS,
    "all": FAST_COMMANDS + MEMORY_COMMANDS + BASELINE_COMMANDS,
}


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""

    parser = argparse.ArgumentParser(
        description="Run unified project evaluation suites.",
    )
    parser.add_argument(
        "mode",
        choices=sorted(COMMAND_GROUPS),
        help="Evaluation suite to run: fast, memory, baseline, or all.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned commands without executing them.",
    )
    parser.add_argument(
        "--continue-on-failure",
        action="store_true",
        help="Continue running later commands after a command fails.",
    )
    return parser


def get_commands(mode: str) -> tuple[EvaluationCommand, ...]:
    """Return the command plan for a supported evaluation mode."""

    try:
        return COMMAND_GROUPS[mode]
    except KeyError as exc:
        supported = ", ".join(sorted(COMMAND_GROUPS))
        raise ValueError(f"Unsupported evaluation mode {mode!r}. Supported: {supported}") from exc


def format_command(argv: Sequence[str]) -> str:
    """Format a command for readable console output."""

    return " ".join(argv)


def print_plan(commands: Iterable[EvaluationCommand]) -> None:
    """Print the command plan."""

    for index, command in enumerate(commands, start=1):
        print(f"[{index}] {command.name}: {command.description}")
        print(f"    $ {format_command(command.argv)}")


def run_commands(
    commands: Sequence[EvaluationCommand],
    *,
    dry_run: bool = False,
    continue_on_failure: bool = False,
) -> int:
    """Run a sequence of evaluation commands and return a process exit code."""

    print_plan(commands)
    if dry_run:
        print("Dry run complete; no commands were executed.")
        return 0

    exit_code = 0
    for command in commands:
        print(f"\n>>> Running {command.name}")
        result = subprocess.run(command.argv, cwd=PROJECT_ROOT, check=False)
        if result.returncode != 0:
            exit_code = result.returncode
            print(f"Command failed with exit code {result.returncode}: {format_command(command.argv)}")
            if not continue_on_failure:
                return exit_code

    return exit_code


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint."""

    args = build_parser().parse_args(argv)
    commands = get_commands(args.mode)
    return run_commands(
        commands,
        dry_run=args.dry_run,
        continue_on_failure=args.continue_on_failure,
    )


if __name__ == "__main__":
    raise SystemExit(main())
