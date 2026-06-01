"""Memory recall quality benchmark.

This module provides a small, deterministic project-local benchmark for the
long-term memory retrieval stack.  It intentionally uses synthetic-but-realistic
MemoryItem fixtures based on this repository's actual development history, then
measures whether MemoryManager.hybrid_recall can retrieve the expected memories.

The benchmark is designed for two uses:
- imported by pytest as a stable regression gate;
- executed manually with ``python -m benchmark.memory_recall_benchmark`` to
  inspect Hit@K / MRR / forbidden-hit failures and top-k reasons.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

from core.memory_items import MemoryItem, MemoryKind, MemoryStatus
from core.memory_manager import MemoryManager


@dataclass(frozen=True)
class BenchmarkMemorySpec:
    """Serializable fixture spec used to seed benchmark MemoryItems."""

    id: str
    kind: str
    title: str
    content: str
    concepts: List[str] = field(default_factory=list)
    files: List[str] = field(default_factory=list)
    importance: float = 0.8
    confidence: float = 0.9
    status: str = MemoryStatus.ACTIVE.value
    is_latest: bool = True
    metadata: Dict[str, object] = field(default_factory=dict)

    def to_memory_item(self) -> MemoryItem:
        return MemoryItem(
            id=self.id,
            kind=self.kind,
            title=self.title,
            content=self.content,
            concepts=list(self.concepts),
            files=list(self.files),
            importance=self.importance,
            confidence=self.confidence,
            status=self.status,
            is_latest=self.is_latest,
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class BenchmarkCase:
    """A single recall-quality evaluation case."""

    id: str
    category: str
    query: str
    expected_any: List[str]
    top_k: int = 5
    expected_files: List[str] = field(default_factory=list)
    expected_kinds: List[str] = field(default_factory=list)
    forbidden: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class BenchmarkCaseResult:
    case_id: str
    category: str
    query: str
    expected_any: List[str]
    expected_files: List[str]
    expected_kinds: List[str]
    forbidden: List[str]
    top_k: int
    ranked_ids: List[str]
    ranked_titles: List[str]
    ranked_reasons: List[str]
    ranked_files: List[List[str]]
    ranked_kinds: List[str]
    hit_rank: Optional[int]
    matched_expected_id: Optional[str]
    reciprocal_rank: float
    forbidden_hits: List[str]
    expected_file_hits: List[str]
    expected_kind_hits: List[str]

    @property
    def hit(self) -> bool:
        return self.hit_rank is not None

    @property
    def expected_files_satisfied(self) -> bool:
        return not self.expected_files or bool(self.expected_file_hits)

    @property
    def expected_kinds_satisfied(self) -> bool:
        return not self.expected_kinds or bool(self.expected_kind_hits)


@dataclass
class BenchmarkReport:
    total_cases: int
    hit_at_1: float
    hit_at_3: float
    hit_at_5: float
    mrr: float
    forbidden_violation_rate: float
    expected_file_hit_rate: float
    expected_kind_hit_rate: float
    retrieval_signal_counts: Dict[str, int]
    by_category: Dict[str, Dict[str, float]]
    case_results: List[BenchmarkCaseResult]

    def to_dict(self) -> Dict[str, object]:
        data = asdict(self)
        return data


def default_memory_specs() -> List[BenchmarkMemorySpec]:
    """Return deterministic benchmark memories.

    The items cover the most important code-agent memory scenarios: phase/task
    recall, file history, traceback/error history, architectural decisions,
    Chinese natural-language queries, user preferences, and negative filtering.
    """

    return [
        BenchmarkMemorySpec(
            id="bench_phase2_index_persistence",
            kind=MemoryKind.TASK.value,
            title="Phase 2 实现 IndexPersistence 和增量索引",
            content=(
                "Phase 2 完成 BM25MemoryIndex 的 IndexPersistence、MemoryIndexManager "
                "和增量 add/remove/rebuild。保存 MemoryItem 后会更新 memory/long_term/indexes/bm25.json。"
            ),
            concepts=["Phase 2", "IndexPersistence", "BM25", "incremental index"],
            files=["core/memory_index.py", "core/memory_layers.py", "tests/test_memory_index_persistence.py"],
            importance=0.96,
        ),
        BenchmarkMemorySpec(
            id="bench_phase3_lifecycle_governance",
            kind=MemoryKind.TASK.value,
            title="Phase 3 完成 MemoryItem 生命周期治理",
            content=(
                "Phase 3 增加 MemoryStatus、is_latest、forget_after、archive、dedup、supersede 和 access tracking，"
                "hybrid recall 只返回 active/latest/not expired 的长期记忆。"
            ),
            concepts=["Phase 3", "lifecycle", "supersede", "archived", "expired"],
            files=["core/memory_items.py", "core/memory_maintenance.py", "tests/test_memory_lifecycle.py"],
            importance=0.94,
        ),
        BenchmarkMemorySpec(
            id="bench_phase4_vector_index",
            kind=MemoryKind.TASK.value,
            title="Phase 4 实现轻量 VectorIndex",
            content=(
                "Phase 4 接入 VectorMemoryIndex、HashEmbeddingProvider 和 VectorIndexPersistence。"
                "无外部 API key 时使用本地 hash embedding，并在维度或模型不匹配时禁用旧向量索引。"
            ),
            concepts=["Phase 4", "VectorMemoryIndex", "HashEmbeddingProvider", "embedding"],
            files=["core/memory_index.py", "core/memory_embedding.py", "tests/test_memory_vector_index.py"],
            importance=0.94,
        ),
        BenchmarkMemorySpec(
            id="bench_phase5_rrf_fusion",
            kind=MemoryKind.TASK.value,
            title="Phase 5 实现 RRF 多路召回融合",
            content=(
                "Phase 5 在 MemoryRetriever.hybrid_recall 中用 RRF 融合 BM25、Vector 和 Metadata hit。"
                "原因说明包含 BM25 rank、Vector rank、Metadata rank，不再直接把不同尺度分数硬加。"
            ),
            concepts=["Phase 5", "RRF", "hybrid recall", "BM25", "Vector", "Metadata"],
            files=["core/memory_retrieval.py", "tests/test_memory_rrf_fusion.py", "tests/test_memory_phase5.py"],
            importance=0.97,
        ),
        BenchmarkMemorySpec(
            id="bench_arch_retrieval_not_rewrite",
            kind=MemoryKind.DECISION.value,
            title="记忆检索主干不需要推倒重写",
            content=(
                "当前长期记忆检索已经形成 MemoryManager 统一入口、BM25、Vector、Metadata 和 RRF 的主线。"
                "下一步优先做质量 benchmark、写入质量治理、可观测性，再考虑 GraphIndex、rerank 和真实 embedding。"
            ),
            concepts=["architecture decision", "benchmark", "GraphIndex", "rerank", "embedding"],
            files=["core/memory_manager.py", "core/memory_retrieval.py", "docs/new_long_term_memory_system.md"],
            importance=0.93,
        ),
        BenchmarkMemorySpec(
            id="bench_bug_winerror5_index_json",
            kind=MemoryKind.BUG.value,
            title="WinError 5 保存索引失败时保留 pending snapshot",
            content=(
                "Windows 下启动 main.py 时保存 memory/long_term/index.json 可能出现 PermissionError: [WinError 5] 拒绝访问。"
                "LongTermMemory._save_index 应清理临时 tmp 文件，保留 _pending_index_snapshot，后续再 flush。"
            ),
            concepts=["WinError 5", "PermissionError", "index.json", "atomic write"],
            files=["core/memory_layers.py", "tests/test_memory_layers.py"],
            importance=0.96,
            metadata={"error_type": "PermissionError"},
        ),
        BenchmarkMemorySpec(
            id="bench_bug_openai_tool_pairing",
            kind=MemoryKind.BUG.value,
            title="OpenAI strict tool_calls 必须和 tool response 成对",
            content=(
                "OpenAI-compatible provider 会拒绝半截 tool call：assistant tool_calls 后必须紧跟对应 tool response。"
                "ContextAssembler 和 AgentEngine 不能在工具调用对中间插入 memory hint。"
            ),
            concepts=["OpenAI", "tool_calls", "tool response", "BadRequestError"],
            files=["core/engine.py", "core/turn_builder.py", "tests/test_openai_tool_pairing.py"],
            importance=0.95,
            metadata={"error_type": "BadRequestError"},
        ),
        BenchmarkMemorySpec(
            id="bench_bug_module_not_found_pytest",
            kind=MemoryKind.BUG.value,
            title="pytest ModuleNotFoundError 需要从项目根目录运行",
            content=(
                "pytest 失败 ModuleNotFoundError: No module named core 时，通常是启动目录或 PYTHONPATH 不正确。"
                "应在项目根目录运行 python -m pytest，确保 core 包可导入。"
            ),
            concepts=["ModuleNotFoundError", "pytest", "PYTHONPATH", "core"],
            files=["tests/test_memory_phase4.py", "core/memory_retrieval.py"],
            importance=0.9,
            metadata={"error_type": "ModuleNotFoundError"},
        ),
        BenchmarkMemorySpec(
            id="bench_preference_tdd_pytest_required",
            kind=MemoryKind.PREFERENCE.value,
            title="用户要求功能实现必须测试通过",
            content=(
                "用户偏好和项目规范要求：实现功能时主动写 tests/test_*.py，运行 pytest，"
                "失败则读取 traceback 并修复，只有测试通过后才能报告完成。"
            ),
            concepts=["用户偏好", "TDD", "pytest", "测试通过"],
            files=["CLAUDE.md", "tests/test_memory_recall_benchmark.py"],
            importance=0.92,
        ),
        BenchmarkMemorySpec(
            id="bench_context_compression_strategy_doc",
            kind=MemoryKind.ARCHITECTURE.value,
            title="上下文压缩系统重构路线保存在 docs",
            content=(
                "context_compression_strategy_architecture.md 规划稳定可控的上下文压缩系统："
                "结构化摘要、关键帧、工具调用成对校验、token budget 和压缩状态注入。"
            ),
            concepts=["context compression", "ContextAssembler", "token budget", "structured summary"],
            files=["docs/context_compression_strategy_architecture.md", "core/compression_engine.py", "core/context_assembler.py"],
            importance=0.86,
        ),
        BenchmarkMemorySpec(
            id="bench_workflow_git_push_main",
            kind=MemoryKind.WORKFLOW.value,
            title="提交并推送到 GitHub main 分支的工作流",
            content=(
                "提交前先检查 git status、运行必要 pytest，确认工作区修改范围；"
                "然后创建规范 commit，最后 git push origin main 并确认远端 main 分支更新。"
            ),
            concepts=["git", "commit", "push", "main", "pytest", "workflow"],
            files=["README.md", "tests/test_openai_tool_pairing.py"],
            importance=0.88,
        ),
        BenchmarkMemorySpec(
            id="bench_file_resume_templates_readme",
            kind=MemoryKind.TASK.value,
            title="README 保持原规范并补充项目修改内容",
            content=(
                "更新 D:\\LLM\\mini-claude-code-cli\\README.md 时，应在原 README 结构基础上补充新增功能，"
                "不要大幅删除原内容；相关简历模板记录在 docs/resume_templates_for_mini_claude_code_cli.md。"
            ),
            concepts=["README", "resume templates", "文档更新", "保持规范"],
            files=["README.md", "docs/resume_templates_for_mini_claude_code_cli.md"],
            importance=0.84,
        ),
        BenchmarkMemorySpec(
            id="bench_error_plan_branch_attribute",
            kind=MemoryKind.BUG.value,
            title="AgentEngine 缺少 current_plan_branch 会导致制定 plan 后报错",
            content=(
                "制定 plan 后如果出现 AttributeError: 'AgentEngine' object has no attribute 'current_plan_branch'，"
                "应检查 AgentEngine 初始化计划分支状态，并保证 plan 相关属性在使用前已创建。"
            ),
            concepts=["AgentEngine", "current_plan_branch", "AttributeError", "plan"],
            files=["core/engine.py", "tests/test_plan_branch.py"],
            importance=0.89,
            metadata={"error_type": "AttributeError"},
        ),
        BenchmarkMemorySpec(
            id="bench_old_keyword_retrieval_archived",
            kind=MemoryKind.DECISION.value,
            title="旧版简单关键词检索已经废弃",
            content=(
                "旧方案只做简单关键词重叠，没有标准 BM25、没有 VectorIndex、没有 RRF。"
                "这条旧记忆应该被 archived，不应该作为当前检索架构结论召回。"
            ),
            concepts=["old retrieval", "keyword only", "deprecated"],
            files=["core/keyword_indexer.py", "core/bm25_retriever.py"],
            importance=0.7,
            status=MemoryStatus.ARCHIVED.value,
            is_latest=False,
        ),
    ]


def default_cases() -> List[BenchmarkCase]:
    """Return default project-local recall benchmark cases."""

    return [
        BenchmarkCase(
            id="phase5_rrf_done",
            category="phase_task",
            query="Phase 5 是不是已经做了 RRF，多路召回现在怎么融合排序？",
            expected_any=["bench_phase5_rrf_fusion"],
            expected_files=["core/memory_retrieval.py"],
            expected_kinds=[MemoryKind.TASK.value],
        ),
        BenchmarkCase(
            id="phase4_vector_index",
            category="phase_task",
            query="Phase 4 加的是不是向量检索和 HashEmbeddingProvider？",
            expected_any=["bench_phase4_vector_index"],
            expected_files=["core/memory_embedding.py"],
        ),
        BenchmarkCase(
            id="index_persistence_incremental",
            category="file_history",
            query="core/memory_index.py 里 IndexPersistence 和增量 BM25 索引是什么时候做的？",
            expected_any=["bench_phase2_index_persistence"],
            expected_files=["core/memory_index.py"],
        ),
        BenchmarkCase(
            id="lifecycle_filters_old_memory",
            category="lifecycle",
            query="长期记忆现在怎么过滤 archived superseded expired 旧记忆？",
            expected_any=["bench_phase3_lifecycle_governance"],
            forbidden=["bench_old_keyword_retrieval_archived"],
        ),
        BenchmarkCase(
            id="architecture_not_rewrite",
            category="architecture",
            query="现在记忆检索还要推倒重写吗，下一步应该先做 Graph 还是质量测评？",
            expected_any=["bench_arch_retrieval_not_rewrite"],
            forbidden=["bench_old_keyword_retrieval_archived"],
        ),
        BenchmarkCase(
            id="winerror5_index_failure",
            category="error_history",
            query="PS D:\\LLM\\mini-claude-code-cli> python .\\main.py 保存索引失败 WinError 5 拒绝访问 index.json",
            expected_any=["bench_bug_winerror5_index_json"],
            expected_kinds=[MemoryKind.BUG.value],
        ),
        BenchmarkCase(
            id="openai_tool_pairing_bad_request",
            category="error_history",
            query="BadRequestError assistant tool_calls 后没有紧邻 tool response 是怎么修的？",
            expected_any=["bench_bug_openai_tool_pairing"],
            expected_files=["tests/test_openai_tool_pairing.py"],
        ),
        BenchmarkCase(
            id="module_not_found_core_pytest",
            category="error_history",
            query="Traceback ModuleNotFoundError No module named core pytest 应该怎么办？",
            expected_any=["bench_bug_module_not_found_pytest"],
        ),
        BenchmarkCase(
            id="user_tdd_preference",
            category="preference",
            query="用户对实现功能和测试有什么要求，是不是必须 pytest 通过才能说完成？",
            expected_any=["bench_preference_tdd_pytest_required"],
            expected_kinds=[MemoryKind.PREFERENCE.value],
        ),
        BenchmarkCase(
            id="context_compression_doc",
            category="architecture",
            query="上下文压缩系统重构文档里说 token budget 和结构化摘要怎么做？",
            expected_any=["bench_context_compression_strategy_doc"],
            expected_files=["docs/context_compression_strategy_architecture.md"],
            expected_kinds=[MemoryKind.ARCHITECTURE.value],
        ),
        BenchmarkCase(
            id="git_push_main_workflow",
            category="workflow",
            query="把当前修改提交并推送到 GitHub main 分支前，需要按什么流程检查？",
            expected_any=["bench_workflow_git_push_main"],
            expected_files=["README.md"],
            expected_kinds=[MemoryKind.WORKFLOW.value],
        ),
        BenchmarkCase(
            id="readme_resume_file_history",
            category="file_history",
            query="D:\\LLM\\mini-claude-code-cli\\README.md 要在原规范基础上补充内容，相关简历模板文件是哪一个？",
            expected_any=["bench_file_resume_templates_readme"],
            expected_files=["docs/resume_templates_for_mini_claude_code_cli.md"],
        ),
        BenchmarkCase(
            id="agent_engine_plan_branch_attribute",
            category="error_history",
            query="发生运行错误 AttributeError 'AgentEngine' object has no attribute 'current_plan_branch' 制定 plan 后报错怎么查？",
            expected_any=["bench_error_plan_branch_attribute"],
            expected_files=["core/engine.py"],
            expected_kinds=[MemoryKind.BUG.value],
        ),
        BenchmarkCase(
            id="semantic_rewrite_rrf",
            category="semantic_rewrite",
            query="BM25 和向量结果冲突时现在还是简单加权吗，还是倒数排名融合？",
            expected_any=["bench_phase5_rrf_fusion"],
        ),
        BenchmarkCase(
            id="chinese_quality_question",
            category="chinese_query",
            query="现在的长期记忆检索是不是已经不是以前那种简单关键词鸡肋检索了？",
            expected_any=["bench_arch_retrieval_not_rewrite", "bench_phase5_rrf_fusion"],
            forbidden=["bench_old_keyword_retrieval_archived"],
        ),
    ]


def seed_manager(manager: MemoryManager, specs: Sequence[BenchmarkMemorySpec] | None = None) -> None:
    """Seed a MemoryManager with benchmark fixture items."""

    for spec in specs or default_memory_specs():
        manager.save_memory_item(spec.to_memory_item())


def _ranked_ids(results: Iterable) -> List[str]:
    return [result.item.id for result in results]


def evaluate_cases(manager: MemoryManager, cases: Sequence[BenchmarkCase] | None = None) -> BenchmarkReport:
    """Evaluate benchmark cases against a seeded MemoryManager."""

    selected_cases = list(cases or default_cases())
    case_results: List[BenchmarkCaseResult] = []

    for case in selected_cases:
        results = manager.hybrid_recall(case.query, top_k=case.top_k)
        ranked_ids = _ranked_ids(results)
        ranked_titles = [result.item.title for result in results]
        ranked_reasons = [result.reason for result in results]
        ranked_files = [list(result.item.files) for result in results]
        ranked_kinds = [result.item.kind for result in results]

        hit_rank: Optional[int] = None
        matched_expected_id: Optional[str] = None
        for expected_id in case.expected_any:
            if expected_id in ranked_ids:
                candidate_rank = ranked_ids.index(expected_id) + 1
                if hit_rank is None or candidate_rank < hit_rank:
                    hit_rank = candidate_rank
                    matched_expected_id = expected_id

        expected_file_set = set(case.expected_files)
        expected_kind_set = set(case.expected_kinds)
        expected_file_hits = sorted(
            {
                file_path
                for item_files in ranked_files
                for file_path in item_files
                if file_path in expected_file_set
            }
        )
        expected_kind_hits = sorted({kind for kind in ranked_kinds if kind in expected_kind_set})

        forbidden_hits = [item_id for item_id in ranked_ids if item_id in set(case.forbidden)]
        case_results.append(
            BenchmarkCaseResult(
                case_id=case.id,
                category=case.category,
                query=case.query,
                expected_any=list(case.expected_any),
                expected_files=list(case.expected_files),
                expected_kinds=list(case.expected_kinds),
                forbidden=list(case.forbidden),
                top_k=case.top_k,
                ranked_ids=ranked_ids,
                ranked_titles=ranked_titles,
                ranked_reasons=ranked_reasons,
                ranked_files=ranked_files,
                ranked_kinds=ranked_kinds,
                hit_rank=hit_rank,
                matched_expected_id=matched_expected_id,
                reciprocal_rank=(1.0 / hit_rank) if hit_rank else 0.0,
                forbidden_hits=forbidden_hits,
                expected_file_hits=expected_file_hits,
                expected_kind_hits=expected_kind_hits,
            )
        )

    return _build_report(case_results)


def _build_report(case_results: Sequence[BenchmarkCaseResult]) -> BenchmarkReport:
    total = len(case_results) or 1

    def hit_at(k: int) -> float:
        return sum(1 for result in case_results if result.hit_rank is not None and result.hit_rank <= k) / total

    forbidden_violations = sum(1 for result in case_results if result.forbidden_hits)
    expected_file_satisfied = sum(1 for result in case_results if result.expected_files_satisfied)
    expected_kind_satisfied = sum(1 for result in case_results if result.expected_kinds_satisfied)
    retrieval_signal_counts = _count_retrieval_signals(case_results)
    categories = sorted({result.category for result in case_results})
    by_category: Dict[str, Dict[str, float]] = {}
    for category in categories:
        category_results = [result for result in case_results if result.category == category]
        category_total = len(category_results) or 1
        by_category[category] = {
            "cases": float(len(category_results)),
            "hit@1": sum(1 for result in category_results if result.hit_rank == 1) / category_total,
            "hit@3": sum(1 for result in category_results if result.hit_rank is not None and result.hit_rank <= 3) / category_total,
            "hit@5": sum(1 for result in category_results if result.hit_rank is not None and result.hit_rank <= 5) / category_total,
            "mrr": sum(result.reciprocal_rank for result in category_results) / category_total,
            "forbidden_violation_rate": sum(1 for result in category_results if result.forbidden_hits) / category_total,
            "expected_file_hit_rate": sum(1 for result in category_results if result.expected_files_satisfied) / category_total,
            "expected_kind_hit_rate": sum(1 for result in category_results if result.expected_kinds_satisfied) / category_total,
        }

    return BenchmarkReport(
        total_cases=len(case_results),
        hit_at_1=hit_at(1),
        hit_at_3=hit_at(3),
        hit_at_5=hit_at(5),
        mrr=sum(result.reciprocal_rank for result in case_results) / total,
        forbidden_violation_rate=forbidden_violations / total,
        expected_file_hit_rate=expected_file_satisfied / total,
        expected_kind_hit_rate=expected_kind_satisfied / total,
        retrieval_signal_counts=retrieval_signal_counts,
        by_category=by_category,
        case_results=list(case_results),
    )


def _count_retrieval_signals(case_results: Sequence[BenchmarkCaseResult]) -> Dict[str, int]:
    """Count retrieval signal mentions from result reason strings.

    The retriever exposes human-readable reasons such as ``BM25 rank`` or
    ``Vector rank``.  Counting these markers in benchmark output gives a small
    observability signal for whether a regression is isolated to lexical,
    semantic, metadata, or specialized history recall paths.
    """

    signal_markers = {
        "bm25": "BM25 rank",
        "vector": "Vector rank",
        "metadata": "Metadata rank",
        "file": "file",
        "error": "error",
    }
    counts = {signal: 0 for signal in signal_markers}
    for result in case_results:
        reason_blob = "\n".join(result.ranked_reasons).lower()
        for signal, marker in signal_markers.items():
            if marker.lower() in reason_blob:
                counts[signal] += 1
    return counts


def run_default_benchmark(storage_dir: str | Path | None = None) -> BenchmarkReport:
    """Create an isolated MemoryManager, seed fixtures, and evaluate cases."""

    if storage_dir is None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            manager = MemoryManager(long_term_storage_dir=str(Path(tmp_dir) / "long_term"))
            seed_manager(manager)
            return evaluate_cases(manager)

    manager = MemoryManager(long_term_storage_dir=str(storage_dir))
    seed_manager(manager)
    return evaluate_cases(manager)


def format_markdown_report(report: BenchmarkReport) -> str:
    """Render a human-readable markdown benchmark report."""

    lines = [
        "# Memory Recall Benchmark Report",
        "",
        "## Summary",
        "",
        f"- Cases: {report.total_cases}",
        f"- Hit@1: {report.hit_at_1:.2%}",
        f"- Hit@3: {report.hit_at_3:.2%}",
        f"- Hit@5: {report.hit_at_5:.2%}",
        f"- MRR: {report.mrr:.3f}",
        f"- Forbidden violation rate: {report.forbidden_violation_rate:.2%}",
        f"- Expected file hit rate: {report.expected_file_hit_rate:.2%}",
        f"- Expected kind hit rate: {report.expected_kind_hit_rate:.2%}",
        "",
        "## Retrieval Signals",
        "",
    ]
    for signal, count in sorted(report.retrieval_signal_counts.items()):
        lines.append(f"- {signal}: {count}")

    lines.extend([
        "",
        "## By Category",
        "",
        "| Category | Cases | Hit@1 | Hit@3 | Hit@5 | MRR | Forbidden | File Hit | Kind Hit |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for category, metrics in sorted(report.by_category.items()):
        lines.append(
            "| {category} | {cases:.0f} | {h1:.2%} | {h3:.2%} | {h5:.2%} | {mrr:.3f} | {forbidden:.2%} | {file_hit:.2%} | {kind_hit:.2%} |".format(
                category=category,
                cases=metrics["cases"],
                h1=metrics["hit@1"],
                h3=metrics["hit@3"],
                h5=metrics["hit@5"],
                mrr=metrics["mrr"],
                forbidden=metrics["forbidden_violation_rate"],
                file_hit=metrics["expected_file_hit_rate"],
                kind_hit=metrics["expected_kind_hit_rate"],
            )
        )

    failures = [result for result in report.case_results if not result.hit or result.forbidden_hits]
    lines.extend(["", "## Failures", ""])
    if not failures:
        lines.append("No failed cases or forbidden hits.")
    else:
        for result in failures:
            lines.extend(
                [
                    f"### {result.case_id}",
                    "",
                    f"- Query: {result.query}",
                    f"- Expected any: {', '.join(result.expected_any)}",
                    f"- Hit rank: {result.hit_rank}",
                    f"- Forbidden hits: {', '.join(result.forbidden_hits) if result.forbidden_hits else 'none'}",
                    f"- Ranked ids: {', '.join(result.ranked_ids)}",
                    "",
                ]
            )

    lines.extend(["", "## Case Details", ""])
    for result in report.case_results:
        lines.extend(
            [
                f"### {result.case_id}",
                "",
                f"- Category: {result.category}",
                f"- Query: {result.query}",
                f"- Expected any: {', '.join(result.expected_any)}",
                f"- Hit rank: {result.hit_rank}",
                f"- Ranked ids: {', '.join(result.ranked_ids)}",
                "",
            ]
        )
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the project-local memory recall benchmark.")
    parser.add_argument("--output-json", type=Path, default=None, help="Optional path for a JSON report.")
    parser.add_argument("--output-md", type=Path, default=None, help="Optional path for a markdown report.")
    args = parser.parse_args(argv)

    report = run_default_benchmark()
    print(format_markdown_report(report))

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(format_markdown_report(report), encoding="utf-8")

    return 0 if report.hit_at_5 >= 0.75 and report.forbidden_violation_rate == 0.0 else 1


if __name__ == "__main__":  # pragma: no cover - exercised manually via CLI
    raise SystemExit(main())
