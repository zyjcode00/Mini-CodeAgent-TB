from pathlib import Path

path = Path('benchmark/memory_recall_benchmark.py')
text = path.read_text(encoding='utf-8')

spec_insert = r'''        BenchmarkMemorySpec(
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
'''

case_insert = r'''        BenchmarkCase(
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
'''

if 'bench_arch_context_assembler_budget' not in text:
    marker = '        BenchmarkMemorySpec(\n            id="bench_old_keyword_retrieval_archived",'
    text = text.replace(marker, spec_insert + marker)
if 'arch_context_assembler_budget' not in text:
    marker = '        BenchmarkCase(\n            id="chinese_fuzzy_tool_guard",'
    text = text.replace(marker, case_insert + marker)

path.write_text(text, encoding='utf-8')
print('updated memory benchmark dataset')
