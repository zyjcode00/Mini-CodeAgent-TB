from pathlib import Path

path = Path('benchmark/memory_recall_benchmark.py')
text = path.read_text(encoding='utf-8')

case_insert = '''        BenchmarkCase(
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

if 'id="arch_context_assembler_budget"' not in text:
    marker = '        BenchmarkCase(\n            id="chinese_fuzzy_tool_guard",'
    if marker not in text:
        raise SystemExit('marker not found')
    text = text.replace(marker, case_insert + marker)

path.write_text(text, encoding='utf-8')
print('inserted additional benchmark cases')
