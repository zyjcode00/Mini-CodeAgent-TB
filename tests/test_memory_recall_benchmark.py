"""Pytest regression tests for the project-local memory recall benchmark."""

from __future__ import annotations

import json
from pathlib import Path

from benchmark.memory_recall_benchmark import (
    BenchmarkReport,
    default_cases,
    evaluate_cases,
    format_markdown_report,
    load_report_json,
    main as benchmark_main,
    run_default_benchmark,
    seed_manager,
)
from core.memory_manager import MemoryManager


def test_memory_recall_benchmark_metrics_pass_quality_gate(tmp_path):
    report = run_default_benchmark(storage_dir=tmp_path / "long_term")

    assert isinstance(report, BenchmarkReport)
    assert report.total_cases >= 13
    assert report.hit_at_5 >= 0.75, report.to_dict()
    assert report.hit_at_3 >= 0.65, report.to_dict()
    assert report.mrr >= 0.50, report.to_dict()
    assert report.forbidden_violation_rate == 0.0, report.to_dict()


def test_memory_recall_benchmark_reports_category_breakdown(tmp_path):
    report = run_default_benchmark(storage_dir=tmp_path / "long_term")

    expected_categories = {case.category for case in default_cases()}
    assert expected_categories.issubset(report.by_category.keys())
    for category in expected_categories:
        assert report.by_category[category]["cases"] >= 1
        assert "hit@5" in report.by_category[category]
        assert "mrr" in report.by_category[category]
        assert "expected_file_hit_rate" in report.by_category[category]
        assert "expected_kind_hit_rate" in report.by_category[category]


def test_memory_recall_benchmark_reports_signal_and_expectation_metrics(tmp_path):
    report = run_default_benchmark(storage_dir=tmp_path / "long_term")

    assert 0.0 <= report.expected_file_hit_rate <= 1.0
    assert 0.0 <= report.expected_kind_hit_rate <= 1.0
    assert report.expected_file_hit_rate >= 0.75, report.to_dict()
    assert report.expected_kind_hit_rate >= 0.75, report.to_dict()
    assert {"bm25", "vector", "metadata", "file", "error"}.issubset(report.retrieval_signal_counts)
    assert report.retrieval_signal_counts["bm25"] >= 1
    assert report.retrieval_signal_counts["vector"] >= 1


def test_memory_recall_benchmark_forbidden_archived_memory_not_returned(tmp_path):
    manager = MemoryManager(long_term_storage_dir=str(tmp_path / "long_term"))
    seed_manager(manager)

    report = evaluate_cases(manager)

    archived_id = "bench_old_keyword_retrieval_archived"
    assert report.forbidden_violation_rate == 0.0, report.to_dict()
    for result in report.case_results:
        assert archived_id not in result.ranked_ids


def test_memory_recall_benchmark_markdown_and_json_are_serializable(tmp_path):
    report = run_default_benchmark(storage_dir=tmp_path / "long_term")

    markdown = format_markdown_report(report)
    encoded = json.dumps(report.to_dict(), ensure_ascii=False)

    assert "# Memory Recall Benchmark Report" in markdown
    assert "Hit@5" in markdown
    assert "Expected file hit rate" in markdown
    assert "## Retrieval Signals" in markdown
    assert "File Hit" in markdown
    assert "phase5_rrf_done" in markdown
    assert "## Failures and Weak Rankings" in markdown
    assert "#### Ranked Reasons" in markdown
    assert "Signal counts:" in markdown
    assert "Diagnostic:" in markdown
    assert "benchmark_failure_diagnostics" in encoded
    assert "ranked_signal_counts" in encoded
    assert "diagnostic_flags" in encoded
    assert "case_results" in encoded


def test_memory_recall_benchmark_baseline_is_loadable_and_records_current_quality_floor():
    baseline_path = Path("benchmark/baselines/memory_recall_baseline.json")

    assert baseline_path.exists(), "Phase A requires a checked-in benchmark baseline JSON file"
    baseline = load_report_json(baseline_path)
    current_case_ids = {case.id for case in default_cases()}
    baseline_case_ids = {result.case_id for result in baseline.case_results}

    assert baseline.total_cases == len(baseline.case_results)
    assert baseline.total_cases >= 13
    assert baseline_case_ids == current_case_ids
    assert baseline.hit_at_5 >= 0.75
    assert baseline.hit_at_3 >= 0.65
    assert baseline.mrr >= 0.50
    assert baseline.forbidden_violation_rate == 0.0
    assert baseline.expected_file_hit_rate >= 0.75
    assert baseline.expected_kind_hit_rate >= 0.75


def test_memory_recall_benchmark_cli_generates_json_and_markdown_reports(tmp_path):
    json_path = tmp_path / "memory_recall_latest.json"
    markdown_path = tmp_path / "memory_recall_latest.md"

    exit_code = benchmark_main(["--output-json", str(json_path), "--output-md", str(markdown_path)])

    assert exit_code == 0
    assert json_path.exists()
    assert markdown_path.exists()

    report = load_report_json(json_path)
    markdown = markdown_path.read_text(encoding="utf-8")
    assert report.total_cases == len(default_cases())
    assert report.case_results
    assert "# Memory Recall Benchmark Report" in markdown
    assert "## Summary" in markdown
    assert "## Case Details" in markdown
