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
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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
    ranked_signal_counts: Dict[str, int]
    channel_ranks: Dict[str, Optional[int]]
    diagnostic_flags: List[str]
    diagnostic_summary: str

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
        return asdict(self)


def _case_result_from_dict(data: Dict[str, Any]) -> BenchmarkCaseResult:
    """Deserialize a BenchmarkCaseResult from a JSON-compatible dict."""

    return BenchmarkCaseResult(
        case_id=str(data["case_id"]),
        category=str(data["category"]),
        query=str(data.get("query", "")),
        expected_any=list(data.get("expected_any", [])),
        expected_files=list(data.get("expected_files", [])),
        expected_kinds=list(data.get("expected_kinds", [])),
        forbidden=list(data.get("forbidden", [])),
        top_k=int(data.get("top_k", 5)),
        ranked_ids=list(data.get("ranked_ids", [])),
        ranked_titles=list(data.get("ranked_titles", [])),
        ranked_reasons=list(data.get("ranked_reasons", [])),
        ranked_files=[list(files) for files in data.get("ranked_files", [])],
        ranked_kinds=list(data.get("ranked_kinds", [])),
        hit_rank=data.get("hit_rank"),
        matched_expected_id=data.get("matched_expected_id"),
        reciprocal_rank=float(data.get("reciprocal_rank", 0.0)),
        forbidden_hits=list(data.get("forbidden_hits", [])),
        expected_file_hits=list(data.get("expected_file_hits", [])),
        expected_kind_hits=list(data.get("expected_kind_hits", [])),
        ranked_signal_counts={str(key): int(value) for key, value in data.get("ranked_signal_counts", {}).items()},
        channel_ranks={
            str(key): (None if value is None else int(value))
            for key, value in data.get("channel_ranks", {}).items()
        },
        diagnostic_flags=list(data.get("diagnostic_flags", [])),
        diagnostic_summary=str(data.get("diagnostic_summary", "")),
    )


def report_from_dict(data: Dict[str, Any]) -> BenchmarkReport:
    """Deserialize a BenchmarkReport from JSON-compatible data."""

    return BenchmarkReport(
        total_cases=int(data["total_cases"]),
        hit_at_1=float(data["hit_at_1"]),
        hit_at_3=float(data["hit_at_3"]),
        hit_at_5=float(data["hit_at_5"]),
        mrr=float(data["mrr"]),
        forbidden_violation_rate=float(data["forbidden_violation_rate"]),
        expected_file_hit_rate=float(data["expected_file_hit_rate"]),
        expected_kind_hit_rate=float(data["expected_kind_hit_rate"]),
        retrieval_signal_counts={str(key): int(value) for key, value in data.get("retrieval_signal_counts", {}).items()},
        by_category={
            str(category): {str(metric): float(value) for metric, value in metrics.items()}
            for category, metrics in data.get("by_category", {}).items()
        },
        case_results=[_case_result_from_dict(result) for result in data.get("case_results", [])],
    )


def load_report_json(path: str | Path) -> BenchmarkReport:
    """Load a BenchmarkReport from a JSON report file."""

    return report_from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


@dataclass(frozen=True)
class BenchmarkMetricDelta:
    """A numeric benchmark metric before/after comparison."""

    name: str
    baseline: float
    current: float
    delta: float


@dataclass(frozen=True)
class BenchmarkCaseChange:
    """Case-level change between baseline and current benchmark reports."""

    case_id: str
    category: str
    baseline_hit_rank: Optional[int]
    current_hit_rank: Optional[int]
    baseline_forbidden_hits: List[str]
    current_forbidden_hits: List[str]
    summary: str


@dataclass(frozen=True)
class BenchmarkComparisonReport:
    """Structured comparison of a baseline report and current report."""

    baseline_total_cases: int
    current_total_cases: int
    metric_deltas: List[BenchmarkMetricDelta]
    improved_cases: List[BenchmarkCaseChange]
    regressed_cases: List[BenchmarkCaseChange]
    changed_cases: List[BenchmarkCaseChange]
    added_cases: List[BenchmarkCaseResult]
    removed_cases: List[BenchmarkCaseResult]

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


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
            id="bench_benchmark_diagnostics_plan",
            kind=MemoryKind.DECISION.value,
            title="Memory recall benchmark 应增强失败诊断报告",
            content=(
                "memory recall benchmark 后续应扩充 cases，并在报告中展示每个 case 的 query、expected、top-k ids、"
                "ranked reasons、BM25/Vector/Metadata/file/error 信号贡献、缺失 expected file/kind、forbidden hits 和弱排序诊断。"
            ),
            concepts=["benchmark", "diagnostics", "failure analysis", "retrieval signals", "weak ranking"],
            files=["benchmark/memory_recall_benchmark.py", "tests/test_memory_recall_benchmark.py", "benchmark/memory_recall_latest.md"],
            importance=0.91,
        ),
        BenchmarkMemorySpec(
            id="bench_decision_quality_over_recency",
            kind=MemoryKind.DECISION.value,
            title="召回排序应避免近期低质量摘要淹没高质量决策",
            content=(
                "检索排序优化时不要让近期低质量 session summary 淹没高质量旧决策。"
                "应综合 importance、confidence、kind、文件/错误精确命中、BM25、Vector 和 Metadata 信号。"
            ),
            concepts=["rerank", "recency", "quality", "decision", "session summary"],
            files=["core/memory_retrieval.py", "benchmark/memory_recall_benchmark.py"],
            importance=0.92,
        ),
        BenchmarkMemorySpec(
            id="bench_file_history_specialized_recall",
            kind=MemoryKind.ARCHITECTURE.value,
            title="File/Error 专用召回应保持强命中能力",
            content=(
                "memory_file_history 与 memory_error_history 这类专用召回入口需要强命中文件路径和错误类型。"
                "即使 general hybrid recall 调整排序，也不能削弱 file exact match 与 error_type match。"
            ),
            concepts=["file history", "error history", "specialized recall", "exact match"],
            files=["core/memory_manager.py", "core/memory_retrieval.py", "tests/test_memory_manager.py"],
            importance=0.9,
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
            id="bench_bug_read_file_feedback_loop",
            kind=MemoryKind.BUG.value,
            title="read_file 防空转守卫避免重复空读",
            content=(
                "当 agent 反复 read_file 同一文件范围或读取超出 EOF 的空范围时，容易形成无效反馈循环。"
                "tools/file_tool.py 应提供防空转守卫，在 tests/test_read_guard.py 覆盖 repeated range 与 empty range 场景。"
            ),
            concepts=["read_file", "feedback loop", "empty range", "repeated range", "防空转"],
            files=["tools/file_tool.py", "tests/test_read_guard.py", "docs/read_file_feedback_loop_fix_plan.md"],
            importance=0.9,
            metadata={"error_type": "FeedbackLoop"},
        ),
        BenchmarkMemorySpec(
            id="bench_preference_file_edit_tool_choice",
            kind=MemoryKind.PREFERENCE.value,
            title="文件编辑工具按文件长度和匹配风险选择",
            content=(
                "项目规范要求：小文件优先 write_full_file，全量覆盖避免匹配失败；"
                "大文件明确位置用 edit_file，复杂修改前用 read_file(raw_mode=True) 获取原始内容。"
            ),
            concepts=["write_full_file", "edit_file", "raw_mode", "文件编辑规范", "CLAUDE.md"],
            files=["CLAUDE.md", "tools/file_tool.py"],
            importance=0.87,
        ),
        BenchmarkMemorySpec(
            id="bench_workflow_plan_progress_marking",
            kind=MemoryKind.WORKFLOW.value,
            title="多步骤任务必须维护 plan 进度",
            content=(
                "复杂任务先调用 manage_plan 创建结构化任务清单；每完成一个步骤必须立即调用 mark_task_done。"
                "如果当前 plan 有未完成项，用户说继续时应从下一个未完成步骤恢复，而不是覆盖计划。"
            ),
            concepts=["manage_plan", "mark_task_done", "continue", "任务清单", "workflow"],
            files=["CLAUDE.md", "core/engine.py"],
            importance=0.88,
        ),
        BenchmarkMemorySpec(
            id="bench_arch_compressed_session_state",
            kind=MemoryKind.ARCHITECTURE.value,
            title="Phase 3 引入结构化 CompressedSessionState",
            content=(
                "上下文压缩重构 Phase 3 实现结构化 CompressedSessionState，"
                "压缩结果保留目标、已完成/未完成任务、文件变更、测试结果、错误和关键决策。"
            ),
            concepts=["Phase 3", "CompressedSessionState", "context compression", "结构化状态"],
            files=["core/compression_engine.py", "tests/test_compressed_session_state.py"],
            importance=0.9,
        ),
        BenchmarkMemorySpec(
            id="bench_bug_git_conflict_engine_syntax",
            kind=MemoryKind.BUG.value,
            title="core/engine.py 残留 Git 冲突标记会导致 SyntaxError",
            content=(
                "main.py 启动时报 SyntaxError 时，应检查 core/engine.py 是否残留 <<<<<<<、=======、>>>>>>> Git 冲突标记，"
                "修复后运行语法或启动测试确认 AgentEngine 可导入。"
            ),
            concepts=["SyntaxError", "Git conflict", "core/engine.py", "main.py", "<<<<<<<"],
            files=["core/engine.py", "main.py"],
            importance=0.91,
            metadata={"error_type": "SyntaxError"},
        ),
        BenchmarkMemorySpec(
            id="bench_task_phase_d_dataset_expansion",
            kind=MemoryKind.TASK.value,
            title="Phase D 扩展 memory recall benchmark 数据集覆盖",
            content=(
                "memory recall benchmark Phase D 要把默认 case 扩展到至少 25 条、至少 8 个 category，"
                "并覆盖 error/file/preference/workflow、语义改写和中文模糊 query。"
            ),
            concepts=["Phase D", "benchmark cases", "dataset expansion", "中文模糊 query", "coverage"],
            files=["docs/memory_recall_benchmark_optimization_plan.md", "benchmark/memory_recall_benchmark.py"],
            importance=0.92,
        ),
        BenchmarkMemorySpec(
            id="bench_decision_no_repeat_completed_task",
            kind=MemoryKind.DECISION.value,
            title="已完成任务不要重复创建 plan",
            content=(
                "规划协议要求检查已完成任务记录；如果用户提出相似已完成任务，应告知已完成并询问是否重新执行，"
                "不要直接重复创建 plan 或覆盖当前进度。"
            ),
            concepts=["completed task", "planning protocol", "不要重复", "manage_plan"],
            files=["CLAUDE.md", "core/engine.py"],
            importance=0.86,
        ),
        BenchmarkMemorySpec(
            id="bench_arch_context_assembler_budget",
            kind=MemoryKind.DECISION.value,
            title="ContextAssembler owns prompt budget allocation",
            content=(
                "Architecture decision: ContextAssembler is responsible for assembling system prompt, "
                "memory snippets, current request and tool-call-safe history within a deterministic token budget. "
                "AgentEngine should not directly concatenate long-term memories because budget priority and OpenAI "
                "tool pair atomicity must be enforced in one place."
            ),
            concepts=["ContextAssembler", "token budget", "AgentEngine", "tool pair"],
            files=["core/context_assembler.py", "core/engine.py", "tests/test_context_assembler.py"],
            importance=0.86,
        ),
        BenchmarkMemorySpec(
            id="bench_arch_memory_indexes_split",
            kind=MemoryKind.DECISION.value,
            title="Long-term memory indexes are split by retrieval signal",
            content=(
                "Architecture decision: the old monolithic index.json compatibility path should be removed or isolated. "
                "The primary memory retrieval chain persists BM25 and vector indexes under memory/long_term/indexes so "
                "each retrieval signal can be rebuilt, tested and diagnosed independently."
            ),
            concepts=["memory index", "BM25", "vector index", "index.json"],
            files=["core/memory_index.py", "memory/long_term/indexes/bm25.json", "memory/long_term/indexes/vector.json"],
            importance=0.84,
        ),
        BenchmarkMemorySpec(
            id="bench_arch_graph_index_deferred",
            kind=MemoryKind.DECISION.value,
            title="GraphIndex is deferred until benchmark quality stabilizes",
            content=(
                "Architecture decision: do not implement GraphIndex before recall benchmark cases reach at least 40, "
                "baseline compare is stable, failure diagnostics are explainable and write-quality governance exists. "
                "Graph must be feature-gated and must not regress existing benchmark categories."
            ),
            concepts=["GraphIndex", "benchmark", "quality gate", "feature gate"],
            files=["docs/evaluation_system_improvement_roadmap.md", "benchmark/memory_recall_benchmark.py"],
            importance=0.88,
        ),
        BenchmarkMemorySpec(
            id="bench_arch_evaluation_entrypoint",
            kind=MemoryKind.DECISION.value,
            title="Evaluation system uses one local entrypoint",
            content=(
                "Architecture decision: scripts/run_evaluation.py is the unified local evaluation entrypoint. "
                "It supports fast, memory and all modes so agents can run core pytest, memory recall benchmark, "
                "latest report generation and baseline comparison without relying on external APIs."
            ),
            concepts=["evaluation", "run_evaluation", "benchmark", "pytest"],
            files=["scripts/run_evaluation.py", "docs/evaluation_system_inventory.md", "benchmark/README.md"],
            importance=0.82,
        ),
        BenchmarkMemorySpec(
            id="bench_arch_write_quality_before_graph",
            kind=MemoryKind.DECISION.value,
            title="Write quality governance comes before graph retrieval",
            content=(
                "Architecture decision: improve memory write quality, deduplication, lifecycle metadata and diagnostics "
                "before adding Graph retrieval. Better written MemoryItems make BM25, vector and future graph recall more reliable."
            ),
            concepts=["write quality", "deduplication", "lifecycle", "GraphIndex"],
            files=["docs/memory_recall_benchmark_optimization_plan.md", "core/memory_manager.py"],
            importance=0.83,
        ),
        BenchmarkMemorySpec(
            id="bench_file_run_evaluation_entrypoint",
            kind=MemoryKind.TASK.value,
            title="scripts/run_evaluation.py created as unified evaluation runner",
            content=(
                "File history: scripts/run_evaluation.py was added during Phase 1 of the evaluation system roadmap. "
                "It runs pytest in fast/all modes and invokes benchmark.memory_recall_benchmark in memory mode with "
                "baseline, latest JSON, latest Markdown and comparison Markdown outputs."
            ),
            concepts=["file history", "run_evaluation.py", "Phase 1", "evaluation"],
            files=["scripts/run_evaluation.py", "tests/test_run_evaluation.py"],
            importance=0.80,
        ),
        BenchmarkMemorySpec(
            id="bench_file_benchmark_readme_metrics",
            kind=MemoryKind.TASK.value,
            title="benchmark/README.md documents benchmark metrics",
            content=(
                "File history: benchmark/README.md was added to describe memory recall benchmark coverage, Hit@K, MRR, "
                "expected file/kind hit rates, forbidden violation rate, retrieval signal counts and baseline update rules."
            ),
            concepts=["benchmark README", "metrics", "baseline", "documentation"],
            files=["benchmark/README.md", "benchmark/memory_recall_latest.md"],
            importance=0.80,
        ),
        BenchmarkMemorySpec(
            id="bench_file_evaluation_inventory",
            kind=MemoryKind.TASK.value,
            title="docs/evaluation_system_inventory.md inventories tests and benchmarks",
            content=(
                "File history: docs/evaluation_system_inventory.md records the project's pytest suites, benchmark assets, "
                "baseline files, latest reports and recommended evaluation commands for future agents."
            ),
            concepts=["evaluation inventory", "tests", "benchmark assets"],
            files=["docs/evaluation_system_inventory.md", "scripts/run_evaluation.py"],
            importance=0.78,
        ),
        BenchmarkMemorySpec(
            id="bench_file_memory_recall_baseline_json",
            kind=MemoryKind.TASK.value,
            title="memory_recall_baseline.json is checked-in quality floor",
            content=(
                "File history: benchmark/baselines/memory_recall_baseline.json is the checked-in recall quality floor. "
                "It must only be updated when new or improved cases pass quality gates and comparison shows no unacceptable regressions."
            ),
            concepts=["baseline", "quality floor", "memory_recall_baseline.json"],
            files=["benchmark/baselines/memory_recall_baseline.json", "benchmark/memory_recall_compare.md"],
            importance=0.82,
        ),
        BenchmarkMemorySpec(
            id="bench_file_openai_pairing_regression_test_deleted",
            kind=MemoryKind.TASK.value,
            title="OpenAI tool pairing regression test location changed",
            content=(
                "File history: tests/test_openai_tool_pairing.py previously covered OpenAI assistant tool_calls and tool response pairing. "
                "If the file is deleted or moved, preserve equivalent coverage around compression fallback and message pairing constraints."
            ),
            concepts=["file history", "OpenAI", "tool pairing", "regression test"],
            files=["tests/test_openai_tool_pairing.py", "core/turn_builder.py", "core/context_assembler.py"],
            importance=0.79,
        ),
        BenchmarkMemorySpec(
            id="bench_preference_no_fake_results",
            kind=MemoryKind.PREFERENCE.value,
            title="Do not claim file or command results without tools",
            content=(
                "User preference: follow the truthfulness principle. When claiming a file was created, modified or a command was run, "
                "the agent must actually call the corresponding tool and inspect stdout/stderr before reporting success."
            ),
            concepts=["truthfulness", "tool use", "stdout", "stderr"],
            files=["CLAUDE.md"],
            importance=0.90,
        ),
        BenchmarkMemorySpec(
            id="bench_preference_stop_read_only_loop",
            kind=MemoryKind.PREFERENCE.value,
            title="Stop read-only loops after guard warning",
            content=(
                "User preference: after repeated read/search-only tool calls and a guard warning, summarize what is known, "
                "state the next concrete action, and start editing or answering instead of repeatedly reading the same ranges."
            ),
            concepts=["read-only loop", "feedback guard", "summary", "next action"],
            files=["tools/file_tool.py", "CLAUDE.md"],
            importance=0.88,
        ),
        BenchmarkMemorySpec(
            id="bench_preference_update_benchmark_readme",
            kind=MemoryKind.PREFERENCE.value,
            title="Keep benchmark README synchronized",
            content=(
                "User preference: whenever benchmark behavior, metrics, case counts, baseline policy or run commands change, "
                "benchmark/README.md must be updated in the same task so future agents have accurate evaluation guidance."
            ),
            concepts=["benchmark README", "documentation", "synchronization"],
            files=["benchmark/README.md"],
            importance=0.86,
        ),
        BenchmarkMemorySpec(
            id="bench_workflow_phase_roadmap_execution",
            kind=MemoryKind.WORKFLOW.value,
            title="Execute roadmap phases incrementally",
            content=(
                "Workflow: when following docs/evaluation_system_improvement_roadmap.md, read the current phase goals, "
                "implement only the active phase, update tests and docs, run the relevant evaluation mode, then mark plan steps done."
            ),
            concepts=["roadmap", "phase", "tests", "mark_task_done"],
            files=["docs/evaluation_system_improvement_roadmap.md", "scripts/run_evaluation.py"],
            importance=0.84,
        ),
        BenchmarkMemorySpec(
            id="bench_workflow_memory_benchmark_command",
            kind=MemoryKind.WORKFLOW.value,
            title="Run memory benchmark with baseline compare outputs",
            content=(
                "Workflow: run python -m benchmark.memory_recall_benchmark --baseline-json benchmark/baselines/memory_recall_baseline.json "
                "--output-json benchmark/memory_recall_latest.json --output-md benchmark/memory_recall_latest.md "
                "--compare-output-md benchmark/memory_recall_compare.md to refresh latest and comparison reports."
            ),
            concepts=["memory benchmark", "baseline compare", "latest report"],
            files=["benchmark/memory_recall_benchmark.py", "benchmark/memory_recall_compare.md"],
            importance=0.83,
        ),
        BenchmarkMemorySpec(
            id="bench_workflow_pytest_after_core_changes",
            kind=MemoryKind.WORKFLOW.value,
            title="Run pytest after core or tool logic changes",
            content=(
                "Workflow: any logic change under core/ or tools/ must include or update tests and must be verified with pytest. "
                "If tests fail, inspect the traceback lines, edit the affected file and rerun until pytest passes."
            ),
            concepts=["pytest", "core", "tools", "self-healing"],
            files=["CLAUDE.md", "tests/test_memory_recall_benchmark.py"],
            importance=0.86,
        ),
        BenchmarkMemorySpec(
            id="bench_workflow_git_status_before_commit",
            kind=MemoryKind.WORKFLOW.value,
            title="Check git status before committing or pushing",
            content=(
                "Workflow: before creating a commit or pushing to main, inspect git status, identify generated benchmark/report files, "
                "run necessary tests and avoid accidentally committing unrelated local artifacts."
            ),
            concepts=["git status", "commit", "push", "generated files"],
            files=["README.md", "benchmark/README.md"],
            importance=0.80,
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
        BenchmarkCase(
            id="benchmark_failure_diagnostics",
            category="diagnostics",
            query="memory recall benchmark 失败时报告要怎么看 BM25 Vector metadata file error 各路贡献和 weak ranking？",
            expected_any=["bench_benchmark_diagnostics_plan"],
            expected_files=["benchmark/memory_recall_benchmark.py"],
            expected_kinds=[MemoryKind.DECISION.value],
        ),
        BenchmarkCase(
            id="quality_over_recent_summary",
            category="rerank_quality",
            query="召回排序优化时如何避免近期低质量 session summary 淹没高质量旧决策？",
            expected_any=["bench_decision_quality_over_recency"],
            expected_files=["core/memory_retrieval.py"],
            expected_kinds=[MemoryKind.DECISION.value],
        ),
        BenchmarkCase(
            id="file_error_specialized_recall",
            category="specialized_recall",
            query="调整 hybrid recall 后 file history 和 error history 专用召回为什么仍要保持 exact match 强命中？",
            expected_any=["bench_file_history_specialized_recall"],
            expected_files=["core/memory_manager.py"],
            expected_kinds=[MemoryKind.ARCHITECTURE.value],
        ),
        BenchmarkCase(
            id="read_file_feedback_loop_guard",
            category="tool_guard",
            query="read_file 一直重复读同一个范围或者 EOF 空范围导致 agent 空转，防护逻辑在哪个文件？",
            expected_any=["bench_bug_read_file_feedback_loop"],
            expected_files=["tools/file_tool.py"],
            expected_kinds=[MemoryKind.BUG.value],
        ),
        BenchmarkCase(
            id="file_edit_tool_choice_rule",
            category="preference",
            query="修改小文件和大文件时应该用 write_full_file 还是 edit_file，raw_mode 什么时候用？",
            expected_any=["bench_preference_file_edit_tool_choice"],
            expected_files=["CLAUDE.md"],
            expected_kinds=[MemoryKind.PREFERENCE.value],
        ),
        BenchmarkCase(
            id="plan_progress_resume_workflow",
            category="workflow",
            query="用户说继续时如果已有未完成 Plan，应该重新 manage_plan 还是执行下一个 mark_task_done 步骤？",
            expected_any=["bench_workflow_plan_progress_marking"],
            expected_kinds=[MemoryKind.WORKFLOW.value],
        ),
        BenchmarkCase(
            id="compressed_session_state_phase3",
            category="architecture",
            query="Phase 3 上下文压缩为什么要用结构化 CompressedSessionState 保存任务、文件、测试和错误？",
            expected_any=["bench_arch_compressed_session_state"],
            expected_files=["tests/test_compressed_session_state.py"],
            expected_kinds=[MemoryKind.ARCHITECTURE.value],
        ),
        BenchmarkCase(
            id="git_conflict_marker_syntax_error",
            category="error_history",
            query="main.py 启动 SyntaxError，core/engine.py 里有 <<<<<<< ======= >>>>>>> 冲突标记怎么办？",
            expected_any=["bench_bug_git_conflict_engine_syntax"],
            expected_files=["core/engine.py"],
            expected_kinds=[MemoryKind.BUG.value],
        ),
        BenchmarkCase(
            id="phase_d_dataset_expansion_goal",
            category="benchmark_coverage",
            query="Phase D 的 memory recall benchmark 数据集扩展要求是不是至少 25 条 case 和 8 个分类？",
            expected_any=["bench_task_phase_d_dataset_expansion"],
            expected_files=["benchmark/memory_recall_benchmark.py"],
            expected_kinds=[MemoryKind.TASK.value],
        ),
        BenchmarkCase(
            id="completed_task_no_repeat_plan",
            category="planning_protocol",
            query="如果用户提出一个已经完成的相似任务，agent 应该直接重复创建计划吗？",
            expected_any=["bench_decision_no_repeat_completed_task"],
            expected_kinds=[MemoryKind.DECISION.value],
        ),
        BenchmarkCase(
            id="arch_context_assembler_budget",
            category="architecture_decision",
            query="为什么上下文预算装配要由 ContextAssembler 统一处理，而不是 AgentEngine 直接拼接记忆？",
            expected_any=["bench_arch_context_assembler_budget"],
            expected_files=["core/context_assembler.py"],
            expected_kinds=[MemoryKind.DECISION.value],
        ),
        BenchmarkCase(
            id="arch_memory_indexes_split",
            category="architecture_decision",
            query="为什么要删除或隔离旧 index.json 路径，改成 memory/long_term/indexes 下的 BM25 和 vector 索引？",
            expected_any=["bench_arch_memory_indexes_split"],
            expected_files=["core/memory_index.py"],
            expected_kinds=[MemoryKind.DECISION.value],
        ),
        BenchmarkCase(
            id="arch_graph_index_deferred",
            category="architecture_decision",
            query="GraphIndex 为什么必须等 benchmark 40 条以上并且 compare 稳定后再做？",
            expected_any=["bench_arch_graph_index_deferred"],
            expected_files=["docs/evaluation_system_improvement_roadmap.md"],
            expected_kinds=[MemoryKind.DECISION.value],
        ),
        BenchmarkCase(
            id="arch_evaluation_entrypoint",
            category="architecture_decision",
            query="项目评测系统为什么要统一到 scripts/run_evaluation.py，并支持 fast memory all 三种模式？",
            expected_any=["bench_arch_evaluation_entrypoint"],
            expected_files=["scripts/run_evaluation.py"],
            expected_kinds=[MemoryKind.DECISION.value],
        ),
        BenchmarkCase(
            id="arch_write_quality_before_graph",
            category="architecture_decision",
            query="长期记忆系统下一步为什么先治理写入质量和去重，而不是马上加 graph retrieval？",
            expected_any=["bench_arch_write_quality_before_graph"],
            expected_files=["core/memory_manager.py"],
            expected_kinds=[MemoryKind.DECISION.value],
        ),
        BenchmarkCase(
            id="file_run_evaluation_entrypoint",
            category="file_history",
            query="scripts/run_evaluation.py 是什么时候加的，它负责哪些本地评测模式？",
            expected_any=["bench_file_run_evaluation_entrypoint"],
            expected_files=["scripts/run_evaluation.py"],
        ),
        BenchmarkCase(
            id="file_benchmark_readme_metrics",
            category="file_history",
            query="benchmark/README.md 记录了哪些 memory recall benchmark 指标和 baseline 规则？",
            expected_any=["bench_file_benchmark_readme_metrics"],
            expected_files=["benchmark/README.md"],
        ),
        BenchmarkCase(
            id="file_evaluation_inventory",
            category="file_history",
            query="docs/evaluation_system_inventory.md 这个评测资产盘点文档包含哪些测试和 benchmark 信息？",
            expected_any=["bench_file_evaluation_inventory"],
            expected_files=["docs/evaluation_system_inventory.md"],
        ),
        BenchmarkCase(
            id="file_memory_recall_baseline_json",
            category="file_history",
            query="benchmark/baselines/memory_recall_baseline.json 为什么是已提交的质量下限，什么时候才能更新？",
            expected_any=["bench_file_memory_recall_baseline_json"],
            expected_files=["benchmark/baselines/memory_recall_baseline.json"],
        ),
        BenchmarkCase(
            id="file_openai_pairing_regression_test_deleted",
            category="file_history",
            query="tests/test_openai_tool_pairing.py 如果被删除或移动，还要保留什么 OpenAI tool pairing 回归覆盖？",
            expected_any=["bench_file_openai_pairing_regression_test_deleted", "bench_bug_openai_tool_pairing"],
            expected_files=["tests/test_openai_tool_pairing.py"],
        ),
        BenchmarkCase(
            id="preference_no_fake_results",
            category="preference",
            query="能不能没运行命令就说测试通过，或者没调用工具就说文件已经修改？",
            expected_any=["bench_preference_no_fake_results"],
            expected_files=["CLAUDE.md"],
            expected_kinds=[MemoryKind.PREFERENCE.value],
        ),
        BenchmarkCase(
            id="preference_stop_read_only_loop",
            category="preference",
            query="连续多轮只读工具后收到防空转提醒，下一步应该继续 read_file 还是先总结并开始修改？",
            expected_any=["bench_preference_stop_read_only_loop"],
            expected_files=["tools/file_tool.py"],
            expected_kinds=[MemoryKind.PREFERENCE.value],
        ),
        BenchmarkCase(
            id="preference_update_benchmark_readme",
            category="preference",
            query="修改 benchmark case 数量、指标或运行方式后，benchmark/README.md 要不要同步更新？",
            expected_any=["bench_preference_update_benchmark_readme"],
            expected_files=["benchmark/README.md"],
            expected_kinds=[MemoryKind.PREFERENCE.value],
        ),
        BenchmarkCase(
            id="workflow_phase_roadmap_execution",
            category="workflow",
            query="按照 evaluation_system_improvement_roadmap 执行 Phase 2 时，应该怎么分步实现、测测试并标记计划？",
            expected_any=["bench_workflow_phase_roadmap_execution"],
            expected_files=["docs/evaluation_system_improvement_roadmap.md"],
            expected_kinds=[MemoryKind.WORKFLOW.value],
        ),
        BenchmarkCase(
            id="workflow_memory_benchmark_command",
            category="workflow",
            query="刷新 memory recall latest json、latest markdown 和 baseline compare report 的完整命令是什么？",
            expected_any=["bench_workflow_memory_benchmark_command"],
            expected_files=["benchmark/memory_recall_benchmark.py"],
            expected_kinds=[MemoryKind.WORKFLOW.value],
        ),
        BenchmarkCase(
            id="workflow_pytest_after_core_changes",
            category="workflow",
            query="如果修改 core 或 tools 逻辑，按项目规范需要补测试并怎么验证？",
            expected_any=["bench_workflow_pytest_after_core_changes", "bench_preference_tdd_pytest_required"],
            expected_files=["CLAUDE.md"],
            expected_kinds=[MemoryKind.WORKFLOW.value],
        ),
        BenchmarkCase(
            id="workflow_git_status_before_commit",
            category="workflow",
            query="提交或推送 main 前为什么要先看 git status、区分 benchmark 生成物和无关文件？",
            expected_any=["bench_workflow_git_status_before_commit", "bench_workflow_git_push_main"],
            expected_files=["README.md"],
            expected_kinds=[MemoryKind.WORKFLOW.value],
        ),
        BenchmarkCase(
            id="error_compression_empty_summary_fallback",
            category="error_history",
            query="LLM 摘要返回空导致压缩失败时，应该怎么安全降级并保持 OpenAI tool pair 约束？",
            expected_any=["bench_bug_openai_tool_pairing"],
            expected_files=["tests/test_openai_tool_pairing.py"],
            expected_kinds=[MemoryKind.BUG.value],
        ),
        BenchmarkCase(
            id="chinese_fuzzy_tool_guard",
            category="chinese_query",
            query="读文件老是读不到内容还一直读同一段，这种空转守卫之前修过哪里？",
            expected_any=["bench_bug_read_file_feedback_loop"],
            expected_files=["tests/test_read_guard.py"],
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
        ranked_signal_counts = _count_reason_signals(ranked_reasons)
        channel_ranks = _extract_channel_ranks(ranked_reasons)
        diagnostic_flags = _diagnose_case(
            case=case,
            hit_rank=hit_rank,
            forbidden_hits=forbidden_hits,
            expected_file_hits=expected_file_hits,
            expected_kind_hits=expected_kind_hits,
            ranked_signal_counts=ranked_signal_counts,
        )
        diagnostic_summary = "; ".join(diagnostic_flags) if diagnostic_flags else "ok"
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
                ranked_signal_counts=ranked_signal_counts,
                channel_ranks=channel_ranks,
                diagnostic_flags=diagnostic_flags,
                diagnostic_summary=diagnostic_summary,
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

    counts = {signal: 0 for signal in _signal_markers()}
    for result in case_results:
        for signal, count in result.ranked_signal_counts.items():
            if count > 0:
                counts[signal] += 1
    return counts


def _signal_markers() -> Dict[str, str]:
    return {
        "bm25": "BM25 rank",
        "vector": "Vector rank",
        "metadata": "Metadata rank",
        "file": "file",
        "error": "error",
    }


def _count_reason_signals(reasons: Sequence[str]) -> Dict[str, int]:
    counts = {signal: 0 for signal in _signal_markers()}
    reason_blob = "\n".join(reasons).lower()
    for signal, marker in _signal_markers().items():
        counts[signal] = reason_blob.count(marker.lower())
    return counts


def _extract_channel_ranks(reasons: Sequence[str]) -> Dict[str, Optional[int]]:
    """Return the first top-k result position where each retrieval signal appears."""

    channel_ranks: Dict[str, Optional[int]] = {signal: None for signal in _signal_markers()}
    for rank, reason in enumerate(reasons, start=1):
        lowered_reason = reason.lower()
        for signal, marker in _signal_markers().items():
            if channel_ranks[signal] is None and marker.lower() in lowered_reason:
                channel_ranks[signal] = rank
    return channel_ranks


def _diagnose_case(
    *,
    case: BenchmarkCase,
    hit_rank: Optional[int],
    forbidden_hits: Sequence[str],
    expected_file_hits: Sequence[str],
    expected_kind_hits: Sequence[str],
    ranked_signal_counts: Dict[str, int],
) -> List[str]:
    flags: List[str] = []
    if hit_rank is None:
        flags.append("expected_missing")
    elif hit_rank > 1:
        flags.append("weak_ranking")
    if forbidden_hits:
        flags.append("forbidden_hit")
    if case.expected_files and not expected_file_hits:
        flags.append("expected_file_missing")
    if case.expected_kinds and not expected_kind_hits:
        flags.append("expected_kind_missing")
    if not any(ranked_signal_counts.values()):
        flags.append("no_rank_reason_signals")
    if ranked_signal_counts.get("bm25", 0) == 0:
        flags.append("bm25_signal_absent")
    if ranked_signal_counts.get("vector", 0) == 0:
        flags.append("vector_signal_absent")
    return flags


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

    failures = [
        result
        for result in report.case_results
        if not result.hit or result.forbidden_hits or result.diagnostic_flags
    ]
    lines.extend(["", "## Failures and Weak Rankings", ""])
    if not failures:
        lines.append("No failed, forbidden, or weak-ranking cases.")
    else:
        for result in failures:
            lines.extend(
                [
                    f"### {result.case_id}",
                    "",
                    f"- Query: {result.query}",
                    f"- Expected any: {', '.join(result.expected_any)}",
                    f"- Expected files: {', '.join(result.expected_files) if result.expected_files else 'none'}",
                    f"- Expected kinds: {', '.join(result.expected_kinds) if result.expected_kinds else 'none'}",
                    f"- Hit rank: {result.hit_rank}",
                    f"- Diagnostic: {result.diagnostic_summary}",
                    f"- Forbidden hits: {', '.join(result.forbidden_hits) if result.forbidden_hits else 'none'}",
                    f"- Expected file hits: {', '.join(result.expected_file_hits) if result.expected_file_hits else 'none'}",
                    f"- Expected kind hits: {', '.join(result.expected_kind_hits) if result.expected_kind_hits else 'none'}",
                    f"- Signal counts: {_format_signal_counts(result.ranked_signal_counts)}",
                    f"- Channel ranks: {_format_channel_ranks(result.channel_ranks)}",
                    f"- Ranked ids: {', '.join(result.ranked_ids)}",
                    "",
                    "#### Ranked Reasons",
                    "",
                ]
            )
            lines.extend(_format_ranked_reasons(result))

    lines.extend(["", "## Case Details", ""])
    for result in report.case_results:
        lines.extend(
            [
                f"### {result.case_id}",
                "",
                f"- Category: {result.category}",
                f"- Query: {result.query}",
                f"- Expected any: {', '.join(result.expected_any)}",
                f"- Expected files: {', '.join(result.expected_files) if result.expected_files else 'none'}",
                f"- Expected kinds: {', '.join(result.expected_kinds) if result.expected_kinds else 'none'}",
                f"- Hit rank: {result.hit_rank}",
                f"- Diagnostic: {result.diagnostic_summary}",
                f"- Signal counts: {_format_signal_counts(result.ranked_signal_counts)}",
                f"- Channel ranks: {_format_channel_ranks(result.channel_ranks)}",
                f"- Ranked ids: {', '.join(result.ranked_ids)}",
                "",
                "#### Ranked Reasons",
                "",
            ]
        )
        lines.extend(_format_ranked_reasons(result))
    return "\n".join(lines)


def _format_signal_counts(signal_counts: Dict[str, int]) -> str:
    """Render per-case retrieval signal counts in a stable order."""

    return ", ".join(f"{signal}={count}" for signal, count in sorted(signal_counts.items()))


def _format_channel_ranks(channel_ranks: Dict[str, Optional[int]]) -> str:
    """Render first-hit rank per retrieval signal in a stable order."""

    return ", ".join(
        f"{signal}={rank if rank is not None else 'none'}"
        for signal, rank in sorted(channel_ranks.items())
    )


def _format_ranked_reasons(result: BenchmarkCaseResult) -> List[str]:
    """Render aligned top-k ids and reasons for diagnosis."""

    if not result.ranked_ids:
        return ["- none"]
    return [
        f"- #{rank} `{item_id}`: {reason}"
        for rank, (item_id, reason) in enumerate(zip(result.ranked_ids, result.ranked_reasons), start=1)
    ]


def compare_reports(baseline: BenchmarkReport, current: BenchmarkReport) -> BenchmarkComparisonReport:
    """Compare aggregate metrics and identify improved or regressed cases."""

    metrics = [
        ("hit@1", baseline.hit_at_1, current.hit_at_1),
        ("hit@3", baseline.hit_at_3, current.hit_at_3),
        ("hit@5", baseline.hit_at_5, current.hit_at_5),
        ("mrr", baseline.mrr, current.mrr),
        ("forbidden_violation_rate", baseline.forbidden_violation_rate, current.forbidden_violation_rate),
        ("expected_file_hit_rate", baseline.expected_file_hit_rate, current.expected_file_hit_rate),
        ("expected_kind_hit_rate", baseline.expected_kind_hit_rate, current.expected_kind_hit_rate),
    ]
    metric_deltas = [BenchmarkMetricDelta(name, old, new, new - old) for name, old, new in metrics]
    baseline_cases = {result.case_id: result for result in baseline.case_results}
    current_cases = {result.case_id: result for result in current.case_results}
    improved: List[BenchmarkCaseChange] = []
    regressed: List[BenchmarkCaseChange] = []
    changed: List[BenchmarkCaseChange] = []

    for case_id in sorted(baseline_cases.keys() & current_cases.keys()):
        old = baseline_cases[case_id]
        new = current_cases[case_id]
        old_rank = old.hit_rank or float("inf")
        new_rank = new.hit_rank or float("inf")
        old_forbidden = bool(old.forbidden_hits)
        new_forbidden = bool(new.forbidden_hits)
        if old_rank == new_rank and old_forbidden == new_forbidden:
            continue
        if new_rank < old_rank or (old_forbidden and not new_forbidden):
            summary = "improved"
        elif new_rank > old_rank or (not old_forbidden and new_forbidden):
            summary = "regressed"
        else:
            summary = "changed"
        change = BenchmarkCaseChange(
            case_id=case_id,
            category=new.category,
            baseline_hit_rank=old.hit_rank,
            current_hit_rank=new.hit_rank,
            baseline_forbidden_hits=list(old.forbidden_hits),
            current_forbidden_hits=list(new.forbidden_hits),
            summary=summary,
        )
        changed.append(change)
        if summary == "improved":
            improved.append(change)
        elif summary == "regressed":
            regressed.append(change)

    return BenchmarkComparisonReport(
        baseline_total_cases=baseline.total_cases,
        current_total_cases=current.total_cases,
        metric_deltas=metric_deltas,
        improved_cases=improved,
        regressed_cases=regressed,
        changed_cases=changed,
        added_cases=[current_cases[key] for key in sorted(current_cases.keys() - baseline_cases.keys())],
        removed_cases=[baseline_cases[key] for key in sorted(baseline_cases.keys() - current_cases.keys())],
    )


def format_markdown_comparison(report: BenchmarkComparisonReport) -> str:
    """Render a compact baseline/current comparison report."""

    lines = ["# Memory Recall Benchmark Comparison", "", "## Summary", "",
             f"- Baseline cases: {report.baseline_total_cases}", f"- Current cases: {report.current_total_cases}",
             f"- Improved cases: {len(report.improved_cases)}", f"- Regressed cases: {len(report.regressed_cases)}",
             f"- Added cases: {len(report.added_cases)}", f"- Removed cases: {len(report.removed_cases)}", "",
             "## Metric Deltas", "", "| Metric | Baseline | Current | Delta |", "|---|---:|---:|---:|"]
    for metric in report.metric_deltas:
        lines.append(f"| {metric.name} | {metric.baseline:.3f} | {metric.current:.3f} | {metric.delta:+.3f} |")
    lines.extend(["", "## Case Changes", ""])
    if not report.changed_cases:
        lines.append("No case-level rank or forbidden-hit changes.")
    for change in report.changed_cases:
        lines.append(f"- **{change.case_id}** ({change.category}): {change.summary}; rank {change.baseline_hit_rank} -> {change.current_hit_rank}")

    if report.added_cases:
        lines.extend(["", "## Added Cases", ""])
        for case in report.added_cases:
            status = "fail-or-weak" if case.hit_rank is None or case.hit_rank > 5 or case.forbidden_hits else "pass"
            diagnostic = f"; diagnostic: {case.diagnostic_summary}" if case.diagnostic_summary else ""
            lines.append(f"- **{case.case_id}** ({case.category}, {status}): rank={case.hit_rank}{diagnostic}")

    if report.removed_cases:
        lines.extend(["", "## Removed Cases", ""])
        for case in report.removed_cases:
            lines.append(f"- **{case.case_id}** ({case.category}): previous rank={case.hit_rank}")

    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the project-local memory recall benchmark.")
    parser.add_argument("--output-json", type=Path, default=None, help="Optional path for a JSON report.")
    parser.add_argument("--output-md", type=Path, default=None, help="Optional path for a markdown report.")
    parser.add_argument(
        "--compare-baseline",
        "--baseline-json",
        dest="compare_baseline",
        type=Path,
        default=None,
        help="Optional baseline JSON report to compare against.",
    )
    parser.add_argument("--output-compare-json", type=Path, default=None, help="Optional path for a JSON comparison report.")
    parser.add_argument(
        "--output-compare-md",
        "--compare-output-md",
        dest="output_compare_md",
        type=Path,
        default=None,
        help="Optional path for a markdown comparison report.",
    )
    args = parser.parse_args(argv)

    report = run_default_benchmark()
    markdown_report = format_markdown_report(report)
    print(markdown_report)

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(markdown_report, encoding="utf-8")

    if args.compare_baseline:
        comparison = compare_reports(load_report_json(args.compare_baseline), report)
        comparison_markdown = format_markdown_comparison(comparison)
        print("\n" + comparison_markdown)
        if args.output_compare_json:
            args.output_compare_json.parent.mkdir(parents=True, exist_ok=True)
            args.output_compare_json.write_text(json.dumps(comparison.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        if args.output_compare_md:
            args.output_compare_md.parent.mkdir(parents=True, exist_ok=True)
            args.output_compare_md.write_text(comparison_markdown, encoding="utf-8")

    return 0 if report.hit_at_5 >= 0.75 and report.forbidden_violation_rate == 0.0 else 1


if __name__ == "__main__":  # pragma: no cover - exercised manually via CLI
    raise SystemExit(main())
