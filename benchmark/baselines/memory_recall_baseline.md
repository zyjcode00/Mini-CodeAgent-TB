# Memory Recall Benchmark Report

## Summary

- Cases: 44
- Hit@1: 88.64%
- Hit@3: 95.45%
- Hit@5: 95.45%
- MRR: 0.917
- Forbidden violation rate: 0.00%
- Expected file hit rate: 100.00%
- Expected kind hit rate: 100.00%

## Retrieval Signals

- bm25: 44
- error: 7
- file: 5
- metadata: 44
- vector: 44

## By Category

| Category | Cases | Hit@1 | Hit@3 | Hit@5 | MRR | Forbidden | File Hit | Kind Hit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| architecture | 3 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| architecture_decision | 5 | 60.00% | 100.00% | 100.00% | 0.767 | 0.00% | 100.00% | 100.00% |
| benchmark_coverage | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| chinese_query | 2 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| diagnostics | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| error_history | 6 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| file_history | 7 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| lifecycle | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| phase_task | 2 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| planning_protocol | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| preference | 5 | 60.00% | 60.00% | 60.00% | 0.600 | 0.00% | 100.00% | 100.00% |
| rerank_quality | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| semantic_rewrite | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| specialized_recall | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| tool_guard | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| workflow | 6 | 83.33% | 100.00% | 100.00% | 0.917 | 0.00% | 100.00% | 100.00% |

## Failures and Weak Rankings

### arch_evaluation_entrypoint

- Query: 项目评测系统为什么要统一到 scripts/run_evaluation.py，并支持 fast memory all 三种模式？
- Expected any: bench_arch_evaluation_entrypoint
- Expected files: scripts/run_evaluation.py
- Expected kinds: decision
- Hit rank: 2
- Diagnostic: weak_ranking
- Forbidden hits: none
- Expected file hits: scripts/run_evaluation.py
- Expected kind hits: decision
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_file_run_evaluation_entrypoint, bench_arch_evaluation_entrypoint, bench_file_evaluation_inventory, bench_phase2_index_persistence, bench_workflow_phase_roadmap_execution

#### Ranked Reasons

- #1 `bench_file_run_evaluation_entrypoint`: RRF 0.0194; BM25 rank2 (all, evaluation, fast, memory, py, run); BM25相关 31.09; Vector rank2; Vector相关 0.31; Metadata rank38: 重要性 0.28; 时间 0.20; BM25强度加权 0.0036; Vector强度加权 0.0013; 标题匹配加权 0.0004
- #2 `bench_arch_evaluation_entrypoint`: RRF 0.0191; BM25 rank1 (all, evaluation, fast, memory, py, run); BM25相关 34.92; Vector rank7; Vector相关 0.25; Metadata rank34: 重要性 0.29; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0010; 标题匹配加权 0.0001
- #3 `bench_file_evaluation_inventory`: RRF 0.0160; BM25 rank4 (evaluation, py, run, scripts, scripts/run_evaluation.py); BM25相关 15.29; Vector rank9; Vector相关 0.20; Metadata rank40: 重要性 0.27; 时间 0.20; BM25强度加权 0.0018; Vector强度加权 0.0008; 标题匹配加权 0.0001
- #4 `bench_phase2_index_persistence`: RRF 0.0158; BM25 rank16 (memory, py); BM25相关 2.89; Vector rank1; Vector相关 0.36; Metadata rank3: 重要性 0.34; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0015
- #5 `bench_workflow_phase_roadmap_execution`: RRF 0.0158; BM25 rank3 (evaluation, py, run, scripts, scripts/run_evaluation.py); BM25相关 15.37; Vector rank14; Vector相关 0.15; Metadata rank30: 重要性 0.29; 时间 0.20; BM25强度加权 0.0018; Vector强度加权 0.0006
### arch_write_quality_before_graph

- Query: 长期记忆系统下一步为什么先治理写入质量和去重，而不是马上加 graph retrieval？
- Expected any: bench_arch_write_quality_before_graph
- Expected files: core/memory_manager.py
- Expected kinds: decision
- Hit rank: 3
- Diagnostic: weak_ranking
- Forbidden hits: none
- Expected file hits: core/memory_manager.py
- Expected kind hits: decision
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_arch_retrieval_not_rewrite, bench_arch_graph_index_deferred, bench_arch_write_quality_before_graph, bench_workflow_plan_progress_marking, bench_context_compression_strategy_doc

#### Ranked Reasons

- #1 `bench_arch_retrieval_not_rewrite`: RRF 0.0203; BM25 rank1 (graph, retrieval, 一步, 下一, 下一步, 入质); BM25相关 55.75; Vector rank3; Vector相关 0.21; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0011; 标题匹配加权 0.0001
- #2 `bench_arch_graph_index_deferred`: RRF 0.0166; BM25 rank5 (graph); BM25相关 10.60; Vector rank1; Vector相关 0.28; Metadata rank19: 重要性 0.31; 时间 0.20; BM25强度加权 0.0008; Vector强度加权 0.0015
- #3 `bench_arch_write_quality_before_graph`: RRF 0.0162; BM25 rank3 (graph, retrieval); BM25相关 17.50; Vector rank6; Vector相关 0.18; Metadata rank33: 重要性 0.29; 时间 0.20; BM25强度加权 0.0013; Vector强度加权 0.0010; 标题匹配加权 0.0001
- #4 `bench_workflow_plan_progress_marking`: RRF 0.0162; BM25 rank4 (下一, 不是, 而不, 而不是); BM25相关 12.00; Vector rank4; Vector相关 0.20; Metadata rank20: 重要性 0.31; 时间 0.20; BM25强度加权 0.0009; Vector强度加权 0.0011
- #5 `bench_context_compression_strategy_doc`: RRF 0.0156; BM25 rank8 (系统); BM25相关 5.84; Vector rank2; Vector相关 0.24; Metadata rank24: 重要性 0.30; 时间 0.20; BM25强度加权 0.0004; Vector强度加权 0.0013; 标题匹配加权 0.0001
### preference_no_fake_results

- Query: 能不能没运行命令就说测试通过，或者没调用工具就说文件已经修改？
- Expected any: bench_preference_no_fake_results
- Expected files: CLAUDE.md
- Expected kinds: preference
- Hit rank: None
- Diagnostic: expected_missing
- Forbidden hits: none
- Expected file hits: CLAUDE.md
- Expected kind hits: preference
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_preference_tdd_pytest_required, bench_bug_git_conflict_engine_syntax, bench_bug_openai_tool_pairing, bench_workflow_git_push_main, bench_preference_file_edit_tool_choice

#### Ranked Reasons

- #1 `bench_preference_tdd_pytest_required`: RRF 0.0208; BM25 rank1 (测试, 测试通, 试通, 试通过, 运行, 通过); BM25相关 34.98; Vector rank1; Vector相关 0.30; Metadata rank14: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0003
- #2 `bench_bug_git_conflict_engine_syntax`: RRF 0.0159; BM25 rank7 (测试, 运行); BM25相关 4.38; Vector rank2; Vector相关 0.26; Metadata rank18: 重要性 0.32; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0013
- #3 `bench_bug_openai_tool_pairing`: RRF 0.0155; BM25 rank3 (不能, 工具, 调用); BM25相关 6.86; Vector rank9; Vector相关 0.08; Metadata rank10: 重要性 0.33; 时间 0.20; BM25强度加权 0.0008; Vector强度加权 0.0004
- #4 `bench_workflow_git_push_main`: RRF 0.0153; BM25 rank4 (修改, 运行); BM25相关 4.62; Vector rank11; Vector相关 0.04; Metadata rank1: 重要性 0.31; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0005; Vector强度加权 0.0002
- #5 `bench_preference_file_edit_tool_choice`: RRF 0.0152; BM25 rank2 (修改, 工具, 文件); BM25相关 9.95; Vector rank12; Vector相关 0.04; Metadata rank27: 重要性 0.30; 时间 0.20; BM25强度加权 0.0011; Vector强度加权 0.0002; 标题匹配加权 0.0001
### preference_stop_read_only_loop

- Query: 连续多轮只读工具后收到防空转提醒，下一步应该继续 read_file 还是先总结并开始修改？
- Expected any: bench_preference_stop_read_only_loop
- Expected files: tools/file_tool.py
- Expected kinds: preference
- Hit rank: None
- Diagnostic: expected_missing
- Forbidden hits: none
- Expected file hits: tools/file_tool.py
- Expected kind hits: preference
- Signal counts: bm25=5, error=0, file=4, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=1, metadata=1, vector=1
- Ranked ids: bench_bug_read_file_feedback_loop, bench_preference_file_edit_tool_choice, bench_arch_retrieval_not_rewrite, bench_workflow_plan_progress_marking, bench_workflow_git_push_main

#### Ranked Reasons

- #1 `bench_bug_read_file_feedback_loop`: RRF 0.0199; BM25 rank1 (file, read, read_file, 空转, 防空, 防空转); BM25相关 33.88; Vector rank6; Vector相关 0.12; Metadata rank13: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0009; 标题匹配加权 0.0003
- #2 `bench_preference_file_edit_tool_choice`: RRF 0.0159; BM25 rank2 (file, read, read_file, 修改, 工具); BM25相关 12.85; Vector rank13; Vector相关 0.07; Metadata rank23: 重要性 0.30; 时间 0.20; BM25强度加权 0.0015; Vector强度加权 0.0006; 标题匹配加权 0.0000
- #3 `bench_arch_retrieval_not_rewrite`: RRF 0.0153; BM25 rank3 (一步, 下一, 下一步); BM25相关 8.69; Vector rank19; Vector相关 0.04; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0010; Vector强度加权 0.0003
- #4 `bench_workflow_plan_progress_marking`: RRF 0.0152; BM25 rank5 (下一, 继续); BM25相关 5.76; Vector rank10; Vector相关 0.11; Metadata rank21: 重要性 0.31; 时间 0.20; BM25强度加权 0.0007; Vector强度加权 0.0008
- #5 `bench_workflow_git_push_main`: RRF 0.0149; BM25 rank9 (修改); BM25相关 2.44; Vector rank5; Vector相关 0.13; Metadata rank19: 重要性 0.31; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0010
### workflow_pytest_after_core_changes

- Query: 如果修改 core 或 tools 逻辑，按项目规范需要补测试并怎么验证？
- Expected any: bench_workflow_pytest_after_core_changes, bench_preference_tdd_pytest_required
- Expected files: CLAUDE.md
- Expected kinds: workflow
- Hit rank: 2
- Diagnostic: weak_ranking
- Forbidden hits: none
- Expected file hits: CLAUDE.md
- Expected kind hits: workflow
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_preference_file_edit_tool_choice, bench_preference_tdd_pytest_required, bench_workflow_git_push_main, bench_arch_retrieval_not_rewrite, bench_bug_read_file_feedback_loop

#### Ranked Reasons

- #1 `bench_preference_file_edit_tool_choice`: RRF 0.0201; BM25 rank1 (tools, 修改, 目规, 目规范, 规范, 项目); BM25相关 21.61; Vector rank1; Vector相关 0.17; Metadata rank27: 重要性 0.30; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015
- #2 `bench_preference_tdd_pytest_required`: RRF 0.0179; BM25 rank2 (测试, 目规, 目规范, 规范, 项目, 项目规); BM25相关 17.30; Vector rank9; Vector相关 0.03; Metadata rank14: 重要性 0.32; 时间 0.20; BM25强度加权 0.0032; Vector强度加权 0.0003; 标题匹配加权 0.0001
- #3 `bench_workflow_git_push_main`: RRF 0.0170; BM25 rank12 (修改, 规范); BM25相关 4.62; Vector rank10; Vector相关 0.03; Metadata rank1: 重要性 0.31; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0009; Vector强度加权 0.0003; 意图类型加权 0.0020
- #4 `bench_arch_retrieval_not_rewrite`: RRF 0.0154; BM25 rank9 (core, 需要); BM25相关 6.25; Vector rank7; Vector相关 0.05; Metadata rank13: 重要性 0.33; 时间 0.20; BM25强度加权 0.0012; Vector强度加权 0.0004; 标题匹配加权 0.0001
- #5 `bench_bug_read_file_feedback_loop`: RRF 0.0154; BM25 rank8 (tools); BM25相关 6.70; Vector rank6; Vector相关 0.06; Metadata rank20: 重要性 0.32; 时间 0.20; BM25强度加权 0.0012; Vector强度加权 0.0005

## Case Details

### phase5_rrf_done

- Category: phase_task
- Query: Phase 5 是不是已经做了 RRF，多路召回现在怎么融合排序？
- Expected any: bench_phase5_rrf_fusion
- Expected files: core/memory_retrieval.py
- Expected kinds: task
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_phase5_rrf_fusion, bench_arch_retrieval_not_rewrite, bench_decision_quality_over_recency, bench_task_phase_d_dataset_expansion, bench_phase4_vector_index

#### Ranked Reasons

- #1 `bench_phase5_rrf_fusion`: RRF 0.0218; BM25 rank1 (5, phase, rrf, 召回, 多路, 多路召); BM25相关 71.20; Vector rank1; Vector相关 0.53; Metadata rank1: 重要性 0.34; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0008
- #2 `bench_arch_retrieval_not_rewrite`: RRF 0.0171; BM25 rank2 (rrf, 已经); BM25相关 22.65; Vector rank25; Vector相关 0.02; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0013; Vector强度加权 0.0001; 意图类型加权 0.0020
- #3 `bench_decision_quality_over_recency`: RRF 0.0167; BM25 rank3 (召回, 排序); BM25相关 8.24; Vector rank17; Vector相关 0.06; Metadata rank9: 重要性 0.32; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0002; 标题匹配加权 0.0002; 意图类型加权 0.0020
- #4 `bench_task_phase_d_dataset_expansion`: RRF 0.0151; BM25 rank6 (phase); BM25相关 7.13; Vector rank8; Vector相关 0.15; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0004; Vector强度加权 0.0004; 标题匹配加权 0.0001
- #5 `bench_phase4_vector_index`: RRF 0.0147; BM25 rank7 (phase); BM25相关 7.11; Vector rank12; Vector相关 0.09; Metadata rank5: 重要性 0.33; 时间 0.20; BM25强度加权 0.0004; Vector强度加权 0.0003; 标题匹配加权 0.0001
### phase4_vector_index

- Category: phase_task
- Query: Phase 4 加的是不是向量检索和 HashEmbeddingProvider？
- Expected any: bench_phase4_vector_index
- Expected files: core/memory_embedding.py
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_phase4_vector_index, bench_arch_retrieval_not_rewrite, bench_task_phase_d_dataset_expansion, bench_decision_quality_over_recency, bench_phase3_lifecycle_governance

#### Ranked Reasons

- #1 `bench_phase4_vector_index`: RRF 0.0212; BM25 rank1 (4, embedding, hash, hashembeddingprovider, phase, provider); BM25相关 57.36; Vector rank1; Vector相关 0.42; Metadata rank5: 重要性 0.33; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0003
- #2 `bench_arch_retrieval_not_rewrite`: RRF 0.0168; BM25 rank2 (embedding, 检索); BM25相关 10.66; Vector rank25; Vector相关 0.03; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0007; Vector强度加权 0.0001; 标题匹配加权 0.0002; 意图类型加权 0.0020
- #3 `bench_task_phase_d_dataset_expansion`: RRF 0.0157; BM25 rank5 (phase); BM25相关 7.13; Vector rank4; Vector相关 0.13; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0005; 标题匹配加权 0.0002
- #4 `bench_decision_quality_over_recency`: RRF 0.0153; BM25 rank12 (检索); BM25相关 2.59; Vector rank19; Vector相关 0.06; Metadata rank9: 重要性 0.32; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0002; 意图类型加权 0.0020
- #5 `bench_phase3_lifecycle_governance`: RRF 0.0152; BM25 rank3 (phase); BM25相关 7.18; Vector rank13; Vector相关 0.08; Metadata rank6: 重要性 0.33; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0003; 标题匹配加权 0.0002
### index_persistence_incremental

- Category: file_history
- Query: core/memory_index.py 里 IndexPersistence 和增量 BM25 索引是什么时候做的？
- Expected any: bench_phase2_index_persistence
- Expected files: core/memory_index.py
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_phase2_index_persistence, bench_arch_memory_indexes_split, bench_phase4_vector_index, bench_phase5_rrf_fusion, bench_arch_write_quality_before_graph

#### Ranked Reasons

- #1 `bench_phase2_index_persistence`: RRF 0.0216; BM25 rank1 (25, bm25, core, core/memory_index.py, index, indexpersistence); BM25相关 87.84; Vector rank1; Vector相关 0.70; Metadata rank3: 重要性 0.34; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0006
- #2 `bench_arch_memory_indexes_split`: RRF 0.0164; BM25 rank2 (25, bm25, core, core/memory_index.py, index, memory); BM25相关 28.90; Vector rank2; Vector相关 0.32; Metadata rank30: 重要性 0.29; 时间 0.20; BM25强度加权 0.0013; Vector强度加权 0.0007; 标题匹配加权 0.0001
- #3 `bench_phase4_vector_index`: RRF 0.0164; BM25 rank3 (core, core/memory_index.py, index, memory, persistence, py); BM25相关 19.86; Vector rank3; Vector相关 0.25; Metadata rank6: 重要性 0.33; 时间 0.20; BM25强度加权 0.0009; Vector强度加权 0.0005
- #4 `bench_phase5_rrf_fusion`: RRF 0.0155; BM25 rank6 (25, bm25, core, memory, py); BM25相关 17.04; Vector rank9; Vector相关 0.15; Metadata rank1: 重要性 0.34; 时间 0.20; BM25强度加权 0.0008; Vector强度加权 0.0003
- #5 `bench_arch_write_quality_before_graph`: RRF 0.0152; BM25 rank4 (25, bm25, core, index, memory, py); BM25相关 19.17; Vector rank4; Vector相关 0.20; Metadata rank33: 重要性 0.29; 时间 0.20; BM25强度加权 0.0009; Vector强度加权 0.0004
### lifecycle_filters_old_memory

- Category: lifecycle
- Query: 长期记忆现在怎么过滤 archived superseded expired 旧记忆？
- Expected any: bench_phase3_lifecycle_governance
- Expected files: none
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=2, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_phase3_lifecycle_governance, bench_arch_retrieval_not_rewrite, bench_phase4_vector_index, bench_bug_openai_tool_pairing, bench_file_resume_templates_readme

#### Ranked Reasons

- #1 `bench_phase3_lifecycle_governance`: RRF 0.0208; BM25 rank1 (archived, expired, 期记, 期记忆, 记忆, 长期); BM25相关 45.70; Vector rank1; Vector相关 0.19; Metadata rank6: 重要性 0.33; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015
- #2 `bench_arch_retrieval_not_rewrite`: RRF 0.0183; BM25 rank2 (期记, 期记忆, 记忆, 长期, 长期记); BM25相关 20.12; Vector rank2; Vector相关 0.17; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0018; Vector强度加权 0.0014; 标题匹配加权 0.0001
- #3 `bench_phase4_vector_index`: RRF 0.0081; Vector rank4; Vector相关 0.04; Metadata rank5: 重要性 0.33; 时间 0.20; Vector强度加权 0.0003
- #4 `bench_bug_openai_tool_pairing`: RRF 0.0079; Vector rank6; Vector相关 0.03; Metadata rank4: 重要性 0.33; 时间 0.20; Vector强度加权 0.0003
- #5 `bench_file_resume_templates_readme`: RRF 0.0074; Vector rank3; Vector相关 0.06; Metadata rank31: 重要性 0.29; 时间 0.20; Vector强度加权 0.0005
### architecture_not_rewrite

- Category: architecture
- Query: 现在记忆检索还要推倒重写吗，下一步应该先做 Graph 还是质量测评？
- Expected any: bench_arch_retrieval_not_rewrite
- Expected files: none
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_arch_retrieval_not_rewrite, bench_decision_quality_over_recency, bench_workflow_plan_progress_marking, bench_arch_write_quality_before_graph, bench_phase3_lifecycle_governance

#### Ranked Reasons

- #1 `bench_arch_retrieval_not_rewrite`: RRF 0.0208; BM25 rank1 (graph, 一步, 下一, 下一步, 倒重, 倒重写); BM25相关 88.19; Vector rank5; Vector相关 0.12; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0010; 标题匹配加权 0.0008
- #2 `bench_decision_quality_over_recency`: RRF 0.0158; BM25 rank4 (检索, 质量); BM25相关 8.36; Vector rank6; Vector相关 0.10; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0004; Vector强度加权 0.0009; 标题匹配加权 0.0001
- #3 `bench_workflow_plan_progress_marking`: RRF 0.0157; BM25 rank6 (下一); BM25相关 2.64; Vector rank2; Vector相关 0.17; Metadata rank21: 重要性 0.31; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0015
- #4 `bench_arch_write_quality_before_graph`: RRF 0.0146; BM25 rank2 (graph); BM25相关 11.20; Vector rank13; Vector相关 0.06; Metadata rank32: 重要性 0.29; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0005; 标题匹配加权 0.0001
- #5 `bench_phase3_lifecycle_governance`: RRF 0.0141; BM25 rank5 (记忆); BM25相关 3.00; Vector rank19; Vector相关 0.03; Metadata rank6: 重要性 0.33; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0002
### winerror5_index_failure

- Category: error_history
- Query: PS D:\LLM\mini-claude-code-cli> python .\main.py 保存索引失败 WinError 5 拒绝访问 index.json
- Expected any: bench_bug_winerror5_index_json
- Expected files: none
- Expected kinds: bug
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=4, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=1, file=none, metadata=1, vector=1
- Ranked ids: bench_bug_winerror5_index_json, bench_bug_git_conflict_engine_syntax, bench_bug_module_not_found_pytest, bench_error_plan_branch_attribute, bench_phase5_rrf_fusion

#### Ranked Reasons

- #1 `bench_bug_winerror5_index_json`: RRF 0.0241; BM25 rank1 (5, error, index, index.json, json, main); BM25相关 116.14; Vector rank1; Vector相关 0.41; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0010; 意图类型加权 0.0020
- #2 `bench_bug_git_conflict_engine_syntax`: RRF 0.0172; BM25 rank3 (error, main, main.py, py); BM25相关 14.38; Vector rank15; Vector相关 0.08; Metadata rank3: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0005; Vector强度加权 0.0003; 标题匹配加权 0.0001; 意图类型加权 0.0020
- #3 `bench_bug_module_not_found_pytest`: RRF 0.0167; BM25 rank5 (error, py, python, 失败); BM25相关 13.91; Vector rank16; Vector相关 0.08; Metadata rank5: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0005; Vector强度加权 0.0003; 意图类型加权 0.0020
- #4 `bench_error_plan_branch_attribute`: RRF 0.0153; BM25 rank24 (error, py); BM25相关 3.55; Vector rank8; Vector相关 0.11; Metadata rank6: 重要性 0.31; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0001; Vector强度加权 0.0004; 意图类型加权 0.0020
- #5 `bench_phase5_rrf_fusion`: RRF 0.0152; BM25 rank9 (5, py); BM25相关 6.06; Vector rank5; Vector相关 0.21; Metadata rank7: 重要性 0.34; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0007; 标题匹配加权 0.0001
### openai_tool_pairing_bad_request

- Category: error_history
- Query: BadRequestError assistant tool_calls 后没有紧邻 tool response 是怎么修的？
- Expected any: bench_bug_openai_tool_pairing
- Expected files: tests/test_openai_tool_pairing.py
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=4, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=1, file=none, metadata=1, vector=1
- Ranked ids: bench_bug_openai_tool_pairing, bench_bug_read_file_feedback_loop, bench_bug_git_conflict_engine_syntax, bench_file_openai_pairing_regression_test_deleted, bench_bug_winerror5_index_json

#### Ranked Reasons

- #1 `bench_bug_openai_tool_pairing`: RRF 0.0236; BM25 rank1 (assistant, bad, badrequesterror, calls, error, request); BM25相关 79.45; Vector rank1; Vector相关 0.64; Metadata rank2: 重要性 0.33; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0005; 意图类型加权 0.0020
- #2 `bench_bug_read_file_feedback_loop`: RRF 0.0167; BM25 rank7 (tool); BM25相关 7.32; Vector rank9; Vector相关 0.09; Metadata rank5: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0004; Vector强度加权 0.0002; 意图类型加权 0.0020
- #3 `bench_bug_git_conflict_engine_syntax`: RRF 0.0166; BM25 rank12 (error); BM25相关 3.42; Vector rank5; Vector相关 0.15; Metadata rank3: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0002; Vector强度加权 0.0004; 意图类型加权 0.0020
- #4 `bench_file_openai_pairing_regression_test_deleted`: RRF 0.0165; BM25 rank2 (assistant, calls, response, tool, tool_calls); BM25相关 31.51; Vector rank2; Vector相关 0.27; Metadata rank39: 重要性 0.28; 时间 0.20; BM25强度加权 0.0016; Vector强度加权 0.0006; 标题匹配加权 0.0001
- #5 `bench_bug_winerror5_index_json`: RRF 0.0162; BM25 rank10 (error); BM25相关 3.56; Vector rank13; Vector相关 0.08; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0002; Vector强度加权 0.0002; 意图类型加权 0.0020
### module_not_found_core_pytest

- Category: error_history
- Query: Traceback ModuleNotFoundError No module named core pytest 应该怎么办？
- Expected any: bench_bug_module_not_found_pytest
- Expected files: none
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=4, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=1, file=none, metadata=1, vector=1
- Ranked ids: bench_bug_module_not_found_pytest, bench_error_plan_branch_attribute, bench_workflow_pytest_after_core_changes, bench_bug_winerror5_index_json, bench_preference_tdd_pytest_required

#### Ranked Reasons

- #1 `bench_bug_module_not_found_pytest`: RRF 0.0233; BM25 rank1 (core, error, found, module, modulenotfounderror, named); BM25相关 86.33; Vector rank1; Vector相关 0.42; Metadata rank5: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0004; 意图类型加权 0.0020
- #2 `bench_error_plan_branch_attribute`: RRF 0.0176; BM25 rank4 (core, error, no); BM25相关 11.63; Vector rank6; Vector相关 0.12; Metadata rank6: 重要性 0.31; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0005; Vector强度加权 0.0004; 意图类型加权 0.0020
- #3 `bench_workflow_pytest_after_core_changes`: RRF 0.0165; BM25 rank2 (core, pytest, traceback); BM25相关 19.10; Vector rank5; Vector相关 0.12; Metadata rank9: 重要性 0.30; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0009; Vector强度加权 0.0004; 标题匹配加权 0.0004
- #4 `bench_bug_winerror5_index_json`: RRF 0.0160; BM25 rank10 (core, error); BM25相关 5.44; Vector rank15; Vector相关 0.02; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0003; Vector强度加权 0.0001; 意图类型加权 0.0020
- #5 `bench_preference_tdd_pytest_required`: RRF 0.0155; BM25 rank3 (pytest, traceback); BM25相关 14.83; Vector rank4; Vector相关 0.14; Metadata rank20: 重要性 0.32; 时间 0.20; BM25强度加权 0.0007; Vector强度加权 0.0005
### user_tdd_preference

- Category: preference
- Query: 用户对实现功能和测试有什么要求，是不是必须 pytest 通过才能说完成？
- Expected any: bench_preference_tdd_pytest_required
- Expected files: none
- Expected kinds: preference
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_preference_tdd_pytest_required, bench_arch_evaluation_entrypoint, bench_workflow_plan_progress_marking, bench_workflow_pytest_after_core_changes, bench_decision_no_repeat_completed_task

#### Ranked Reasons

- #1 `bench_preference_tdd_pytest_required`: RRF 0.0209; BM25 rank1 (pytest, 功能, 完成, 实现, 实现功, 必须); BM25相关 55.25; Vector rank1; Vector相关 0.33; Metadata rank14: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0004
- #2 `bench_arch_evaluation_entrypoint`: RRF 0.0166; BM25 rank6 (pytest); BM25相关 7.27; Vector rank8; Vector相关 0.17; Metadata rank36: 重要性 0.29; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0008; 意图类型加权 0.0020
- #3 `bench_workflow_plan_progress_marking`: RRF 0.0164; BM25 rank2 (不是, 完成, 必须, 用户); BM25相关 12.77; Vector rank11; Vector相关 0.14; Metadata rank1: 重要性 0.31; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0009; Vector强度加权 0.0006; 标题匹配加权 0.0001
- #4 `bench_workflow_pytest_after_core_changes`: RRF 0.0157; BM25 rank4 (pytest); BM25相关 7.86; Vector rank10; Vector相关 0.14; Metadata rank3: 重要性 0.30; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0006; Vector强度加权 0.0006; 标题匹配加权 0.0001
- #5 `bench_decision_no_repeat_completed_task`: RRF 0.0155; BM25 rank3 (完成, 用户, 要求); BM25相关 8.33; Vector rank28; Vector相关 0.02; Metadata rank30: 重要性 0.30; 时间 0.20; BM25强度加权 0.0006; Vector强度加权 0.0001; 标题匹配加权 0.0001; 意图类型加权 0.0020
### context_compression_doc

- Category: architecture
- Query: 上下文压缩系统重构文档里说 token budget 和结构化摘要怎么做？
- Expected any: bench_context_compression_strategy_doc
- Expected files: docs/context_compression_strategy_architecture.md
- Expected kinds: architecture
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_context_compression_strategy_doc, bench_arch_compressed_session_state, bench_arch_context_assembler_budget, bench_workflow_plan_progress_marking, bench_decision_quality_over_recency

#### Ranked Reasons

- #1 `bench_context_compression_strategy_doc`: RRF 0.0212; BM25 rank1 (budget, token, 上下, 上下文, 下文, 下文压); BM25相关 120.47; Vector rank1; Vector相关 0.42; Metadata rank28: 重要性 0.30; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0011
- #2 `bench_arch_compressed_session_state`: RRF 0.0170; BM25 rank2 (上下, 上下文, 下文, 下文压, 压缩, 文压); BM25相关 37.93; Vector rank3; Vector相关 0.25; Metadata rank16: 重要性 0.32; 时间 0.20; BM25强度加权 0.0013; Vector强度加权 0.0009; 标题匹配加权 0.0002
- #3 `bench_arch_context_assembler_budget`: RRF 0.0152; BM25 rank3 (budget, token); BM25相关 24.48; Vector rank8; Vector相关 0.13; Metadata rank27: 重要性 0.30; 时间 0.20; BM25强度加权 0.0008; Vector强度加权 0.0005; 标题匹配加权 0.0001
- #4 `bench_workflow_plan_progress_marking`: RRF 0.0146; BM25 rank5 (构化, 结构, 结构化); BM25相关 6.73; Vector rank7; Vector相关 0.14; Metadata rank19: 重要性 0.31; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0005
- #5 `bench_decision_quality_over_recency`: RRF 0.0136; BM25 rank6 (摘要); BM25相关 4.46; Vector rank25; Vector相关 0.02; Metadata rank9: 重要性 0.32; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0001; 标题匹配加权 0.0001
### git_push_main_workflow

- Category: workflow
- Query: 把当前修改提交并推送到 GitHub main 分支前，需要按什么流程检查？
- Expected any: bench_workflow_git_push_main
- Expected files: README.md
- Expected kinds: workflow
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_workflow_git_push_main, bench_workflow_git_status_before_commit, bench_workflow_plan_progress_marking, bench_bug_git_conflict_engine_syntax, bench_bug_winerror5_index_json

#### Ranked Reasons

- #1 `bench_workflow_git_push_main`: RRF 0.0239; BM25 rank1 (git, github, hub, main, 交并, 交并推); BM25相关 101.82; Vector rank1; Vector相关 0.45; Metadata rank2: 重要性 0.31; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0009; 意图类型加权 0.0020
- #2 `bench_workflow_git_status_before_commit`: RRF 0.0171; BM25 rank3 (git, main); BM25相关 12.58; Vector rank13; Vector相关 0.11; Metadata rank6: 重要性 0.28; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0005; Vector强度加权 0.0004; 意图类型加权 0.0020
- #3 `bench_workflow_plan_progress_marking`: RRF 0.0167; BM25 rank11 (当前); BM25相关 2.32; Vector rank7; Vector相关 0.15; Metadata rank1: 重要性 0.31; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0001; Vector强度加权 0.0005; 意图类型加权 0.0020
- #4 `bench_bug_git_conflict_engine_syntax`: RRF 0.0159; BM25 rank2 (git, main, 检查); BM25相关 17.03; Vector rank3; Vector相关 0.19; Metadata rank17: 重要性 0.32; 时间 0.20; BM25强度加权 0.0007; Vector强度加权 0.0006
- #5 `bench_bug_winerror5_index_json`: RRF 0.0144; BM25 rank7 (main); BM25相关 3.95; Vector rank11; Vector相关 0.12; Metadata rank8: 重要性 0.34; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0004
### readme_resume_file_history

- Category: file_history
- Query: D:\LLM\mini-claude-code-cli\README.md 要在原规范基础上补充内容，相关简历模板文件是哪一个？
- Expected any: bench_file_resume_templates_readme
- Expected files: docs/resume_templates_for_mini_claude_code_cli.md
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_file_resume_templates_readme, bench_workflow_git_push_main, bench_workflow_git_status_before_commit, bench_preference_update_benchmark_readme, bench_file_benchmark_readme_metrics

#### Ranked Reasons

- #1 `bench_file_resume_templates_readme`: RRF 0.0204; BM25 rank1 (claude, cli, code, llm, llm/mini-claude-code-cli/readme.md, md); BM25相关 127.28; Vector rank1; Vector相关 0.49; Metadata rank29: 重要性 0.29; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0004
- #2 `bench_workflow_git_push_main`: RRF 0.0167; BM25 rank2 (md, readme, 规范); BM25相关 14.85; Vector rank13; Vector相关 0.14; Metadata rank20: 重要性 0.31; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0004; 意图类型加权 0.0020
- #3 `bench_workflow_git_status_before_commit`: RRF 0.0160; BM25 rank6 (md, readme); BM25相关 14.02; Vector rank12; Vector相关 0.16; Metadata rank36: 重要性 0.28; 时间 0.20; BM25强度加权 0.0004; Vector强度加权 0.0005; 意图类型加权 0.0020
- #4 `bench_preference_update_benchmark_readme`: RRF 0.0156; BM25 rank5 (md, readme); BM25相关 14.42; Vector rank2; Vector相关 0.35; Metadata rank28: 重要性 0.30; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0011; 标题匹配加权 0.0001
- #5 `bench_file_benchmark_readme_metrics`: RRF 0.0155; BM25 rank4 (md, readme); BM25相关 14.46; Vector rank3; Vector相关 0.35; Metadata rank37: 重要性 0.28; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0011; 标题匹配加权 0.0001
### agent_engine_plan_branch_attribute

- Category: error_history
- Query: 发生运行错误 AttributeError 'AgentEngine' object has no attribute 'current_plan_branch' 制定 plan 后报错怎么查？
- Expected any: bench_error_plan_branch_attribute
- Expected files: core/engine.py
- Expected kinds: bug
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=4, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=1, file=none, metadata=1, vector=1
- Ranked ids: bench_error_plan_branch_attribute, bench_bug_module_not_found_pytest, bench_bug_read_file_feedback_loop, bench_bug_openai_tool_pairing, bench_bug_winerror5_index_json

#### Ranked Reasons

- #1 `bench_error_plan_branch_attribute`: RRF 0.0237; BM25 rank1 (agent, agentengine, attribute, attributeerror, branch, current); BM25相关 154.78; Vector rank1; Vector相关 0.75; Metadata rank6: 重要性 0.31; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0009; 意图类型加权 0.0020
- #2 `bench_bug_module_not_found_pytest`: RRF 0.0178; BM25 rank5 (error, no, 运行); BM25相关 13.84; Vector rank2; Vector相关 0.24; Metadata rank4: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0004; Vector强度加权 0.0005; 标题匹配加权 0.0001; 意图类型加权 0.0020
- #3 `bench_bug_read_file_feedback_loop`: RRF 0.0167; BM25 rank10 (agent, plan); BM25相关 9.95; Vector rank5; Vector相关 0.18; Metadata rank5: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0003; Vector强度加权 0.0004; 意图类型加权 0.0020
- #4 `bench_bug_openai_tool_pairing`: RRF 0.0165; BM25 rank4 (agent, agentengine, engine, error); BM25相关 17.80; Vector rank20; Vector相关 0.04; Metadata rank2: 重要性 0.33; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0005; Vector强度加权 0.0001; 意图类型加权 0.0020
- #5 `bench_bug_winerror5_index_json`: RRF 0.0155; BM25 rank15 (error); BM25相关 3.56; Vector rank15; Vector相关 0.08; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0001; Vector强度加权 0.0002; 意图类型加权 0.0020
### semantic_rewrite_rrf

- Category: semantic_rewrite
- Query: BM25 和向量结果冲突时现在还是简单加权吗，还是倒数排名融合？
- Expected any: bench_phase5_rrf_fusion
- Expected files: none
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_phase5_rrf_fusion, bench_phase2_index_persistence, bench_arch_memory_indexes_split, bench_decision_quality_over_recency, bench_arch_retrieval_not_rewrite

#### Ranked Reasons

- #1 `bench_phase5_rrf_fusion`: RRF 0.0205; BM25 rank1 (25, bm25, 融合); BM25相关 20.76; Vector rank3; Vector相关 0.14; Metadata rank1: 重要性 0.34; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0010; 标题匹配加权 0.0001
- #2 `bench_phase2_index_persistence`: RRF 0.0195; BM25 rank3 (25, bm25); BM25相关 14.09; Vector rank1; Vector相关 0.21; Metadata rank3: 重要性 0.34; 时间 0.20; BM25强度加权 0.0027; Vector强度加权 0.0015
- #3 `bench_arch_memory_indexes_split`: RRF 0.0179; BM25 rank2 (25, bm25); BM25相关 14.39; Vector rank4; Vector相关 0.14; Metadata rank30: 重要性 0.29; 时间 0.20; BM25强度加权 0.0028; Vector强度加权 0.0010
- #4 `bench_decision_quality_over_recency`: RRF 0.0173; BM25 rank5 (25, bm25); BM25相关 9.59; Vector rank5; Vector相关 0.14; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0018; Vector强度加权 0.0010
- #5 `bench_arch_retrieval_not_rewrite`: RRF 0.0170; BM25 rank6 (25, bm25); BM25相关 9.57; Vector rank7; Vector相关 0.12; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0018; Vector强度加权 0.0009
### chinese_quality_question

- Category: chinese_query
- Query: 现在的长期记忆检索是不是已经不是以前那种简单关键词鸡肋检索了？
- Expected any: bench_arch_retrieval_not_rewrite, bench_phase5_rrf_fusion
- Expected files: none
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=3, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_arch_retrieval_not_rewrite, bench_decision_quality_over_recency, bench_phase3_lifecycle_governance, bench_arch_graph_index_deferred, bench_benchmark_diagnostics_plan

#### Ranked Reasons

- #1 `bench_arch_retrieval_not_rewrite`: RRF 0.0219; BM25 rank1 (已经, 忆检, 忆检索, 期记, 期记忆, 检索); BM25相关 45.46; Vector rank6; Vector相关 0.05; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0007; 标题匹配加权 0.0003; 意图类型加权 0.0020
- #2 `bench_decision_quality_over_recency`: RRF 0.0180; BM25 rank4 (检索); BM25相关 5.18; Vector rank3; Vector相关 0.07; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0008; 意图类型加权 0.0020
- #3 `bench_phase3_lifecycle_governance`: RRF 0.0178; BM25 rank2 (期记, 期记忆, 的长, 的长期, 记忆, 长期); BM25相关 22.08; Vector rank4; Vector相关 0.06; Metadata rank5: 重要性 0.33; 时间 0.20; BM25强度加权 0.0019; Vector强度加权 0.0008
- #4 `bench_arch_graph_index_deferred`: RRF 0.0109; Vector rank1; Vector相关 0.12; Metadata rank22: 重要性 0.31; 时间 0.20; Vector强度加权 0.0015; 意图类型加权 0.0020
- #5 `bench_benchmark_diagnostics_plan`: RRF 0.0104; Vector rank2; Vector相关 0.07; Metadata rank12: 重要性 0.32; 时间 0.20; Vector强度加权 0.0008; 意图类型加权 0.0020
### benchmark_failure_diagnostics

- Category: diagnostics
- Query: memory recall benchmark 失败时报告要怎么看 BM25 Vector metadata file error 各路贡献和 weak ranking？
- Expected any: bench_benchmark_diagnostics_plan
- Expected files: benchmark/memory_recall_benchmark.py
- Expected kinds: decision
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=3, file=1, metadata=5, vector=5
- Channel ranks: bm25=1, error=1, file=1, metadata=1, vector=1
- Ranked ids: bench_benchmark_diagnostics_plan, bench_phase5_rrf_fusion, bench_bug_winerror5_index_json, bench_bug_module_not_found_pytest, bench_decision_quality_over_recency

#### Ranked Reasons

- #1 `bench_benchmark_diagnostics_plan`: RRF 0.0209; BM25 rank1 (25, benchmark, bm25, error, file, memory); BM25相关 70.33; Vector rank1; Vector相关 0.48; Metadata rank15: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0005
- #2 `bench_phase5_rrf_fusion`: RRF 0.0182; BM25 rank2 (25, bm25, memory, metadata, recall, vector); BM25相关 36.83; Vector rank3; Vector相关 0.36; Metadata rank7: 重要性 0.34; 时间 0.20; BM25强度加权 0.0021; Vector强度加权 0.0011
- #3 `bench_bug_winerror5_index_json`: RRF 0.0175; BM25 rank7 (error, memory, 失败, 失败时, 败时); BM25相关 22.88; Vector rank25; Vector相关 0.12; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0013; Vector强度加权 0.0004; 标题匹配加权 0.0003; 意图类型加权 0.0020
- #4 `bench_bug_module_not_found_pytest`: RRF 0.0168; BM25 rank15 (error, memory, 失败); BM25相关 11.64; Vector rank9; Vector相关 0.24; Metadata rank5: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0007; Vector强度加权 0.0007; 意图类型加权 0.0020
- #5 `bench_decision_quality_over_recency`: RRF 0.0160; BM25 rank4 (25, benchmark, bm25, memory, metadata, recall); BM25相关 28.43; Vector rank15; Vector相关 0.19; Metadata rank12: 重要性 0.32; 时间 0.20; BM25强度加权 0.0016; Vector强度加权 0.0006
### quality_over_recent_summary

- Category: rerank_quality
- Query: 召回排序优化时如何避免近期低质量 session summary 淹没高质量旧决策？
- Expected any: bench_decision_quality_over_recency
- Expected files: core/memory_retrieval.py
- Expected kinds: decision
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_decision_quality_over_recency, bench_arch_compressed_session_state, bench_bug_read_file_feedback_loop, bench_context_compression_strategy_doc, bench_phase5_rrf_fusion

#### Ranked Reasons

- #1 `bench_decision_quality_over_recency`: RRF 0.0243; BM25 rank1 (session, summary, 优化, 优化时, 低质, 低质量); BM25相关 188.39; Vector rank1; Vector相关 0.58; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0016; 意图类型加权 0.0020
- #2 `bench_arch_compressed_session_state`: RRF 0.0147; BM25 rank2 (session, 决策); BM25相关 14.89; Vector rank9; Vector相关 0.04; Metadata rank15: 重要性 0.32; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0001
- #3 `bench_bug_read_file_feedback_loop`: RRF 0.0147; BM25 rank8 (避免); BM25相关 3.69; Vector rank3; Vector相关 0.17; Metadata rank14: 重要性 0.32; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0004; 标题匹配加权 0.0001
- #4 `bench_context_compression_strategy_doc`: RRF 0.0146; BM25 rank4 (summary); BM25相关 9.63; Vector rank4; Vector相关 0.15; Metadata rank26: 重要性 0.30; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0004
- #5 `bench_phase5_rrf_fusion`: RRF 0.0142; BM25 rank7 (召回); BM25相关 4.01; Vector rank15; Vector相关 0.02; Metadata rank1: 重要性 0.34; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0001; 标题匹配加权 0.0001
### file_error_specialized_recall

- Category: specialized_recall
- Query: 调整 hybrid recall 后 file history 和 error history 专用召回为什么仍要保持 exact match 强命中？
- Expected any: bench_file_history_specialized_recall
- Expected files: core/memory_manager.py
- Expected kinds: architecture
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=4, file=1, metadata=5, vector=5
- Channel ranks: bm25=1, error=1, file=1, metadata=1, vector=1
- Ranked ids: bench_file_history_specialized_recall, bench_bug_git_conflict_engine_syntax, bench_bug_winerror5_index_json, bench_bug_module_not_found_pytest, bench_phase5_rrf_fusion

#### Ranked Reasons

- #1 `bench_file_history_specialized_recall`: RRF 0.0215; BM25 rank1 (error, exact, file, history, hybrid, match); BM25相关 126.94; Vector rank1; Vector相关 0.57; Metadata rank18: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0011
- #2 `bench_bug_git_conflict_engine_syntax`: RRF 0.0165; BM25 rank14 (error); BM25相关 6.83; Vector rank5; Vector相关 0.15; Metadata rank3: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0002; Vector强度加权 0.0004; 意图类型加权 0.0020
- #3 `bench_bug_winerror5_index_json`: RRF 0.0164; BM25 rank13 (error); BM25相关 7.12; Vector rank8; Vector相关 0.13; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0002; Vector强度加权 0.0004; 意图类型加权 0.0020
- #4 `bench_bug_module_not_found_pytest`: RRF 0.0162; BM25 rank15 (error); BM25相关 6.80; Vector rank6; Vector相关 0.14; Metadata rank5: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0002; Vector强度加权 0.0004; 意图类型加权 0.0020
- #5 `bench_phase5_rrf_fusion`: RRF 0.0158; BM25 rank6 (hybrid, recall, 召回); BM25相关 17.99; Vector rank2; Vector相关 0.19; Metadata rank7: 重要性 0.34; 时间 0.20; BM25强度加权 0.0006; Vector强度加权 0.0005; 标题匹配加权 0.0001
### read_file_feedback_loop_guard

- Category: tool_guard
- Query: read_file 一直重复读同一个范围或者 EOF 空范围导致 agent 空转，防护逻辑在哪个文件？
- Expected any: bench_bug_read_file_feedback_loop
- Expected files: tools/file_tool.py
- Expected kinds: bug
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=4, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=1, metadata=1, vector=1
- Ranked ids: bench_bug_read_file_feedback_loop, bench_preference_file_edit_tool_choice, bench_workflow_git_push_main, bench_bug_git_conflict_engine_syntax, bench_bug_winerror5_index_json

#### Ranked Reasons

- #1 `bench_bug_read_file_feedback_loop`: RRF 0.0204; BM25 rank1 (agent, eof, file, read, read_file, 同一); BM25相关 79.84; Vector rank2; Vector相关 0.19; Metadata rank15: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0012; 标题匹配加权 0.0003
- #2 `bench_preference_file_edit_tool_choice`: RRF 0.0161; BM25 rank3 (file, read, read_file, 文件); BM25相关 10.79; Vector rank3; Vector相关 0.18; Metadata rank23: 重要性 0.30; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0012; 标题匹配加权 0.0001
- #3 `bench_workflow_git_push_main`: RRF 0.0157; BM25 rank9 (范围); BM25相关 5.54; Vector rank1; Vector相关 0.23; Metadata rank20: 重要性 0.31; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0015
- #4 `bench_bug_git_conflict_engine_syntax`: RRF 0.0150; BM25 rank5 (agent, 导致); BM25相关 7.95; Vector rank10; Vector相关 0.08; Metadata rank11: 重要性 0.32; 时间 0.20; BM25强度加权 0.0004; Vector强度加权 0.0005; 标题匹配加权 0.0001
- #5 `bench_bug_winerror5_index_json`: RRF 0.0149; BM25 rank15 (文件); BM25相关 2.43; Vector rank5; Vector相关 0.15; Metadata rank2: 重要性 0.34; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0009
### file_edit_tool_choice_rule

- Category: preference
- Query: 修改小文件和大文件时应该用 write_full_file 还是 edit_file，raw_mode 什么时候用？
- Expected any: bench_preference_file_edit_tool_choice
- Expected files: CLAUDE.md
- Expected kinds: preference
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=3, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=1, metadata=1, vector=1
- Ranked ids: bench_preference_file_edit_tool_choice, bench_bug_winerror5_index_json, bench_decision_quality_over_recency, bench_arch_write_quality_before_graph, bench_preference_no_fake_results

#### Ranked Reasons

- #1 `bench_preference_file_edit_tool_choice`: RRF 0.0203; BM25 rank1 (edit, edit_file, file, full, mode, raw); BM25相关 67.84; Vector rank1; Vector相关 0.32; Metadata rank23: 重要性 0.30; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0001
- #2 `bench_bug_winerror5_index_json`: RRF 0.0160; BM25 rank2 (write, 文件); BM25相关 9.54; Vector rank6; Vector相关 0.08; Metadata rank2: 重要性 0.34; 时间 0.20; BM25强度加权 0.0006; Vector强度加权 0.0004
- #3 `bench_decision_quality_over_recency`: RRF 0.0146; BM25 rank8 (文件); BM25相关 4.98; Vector rank8; Vector相关 0.08; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0004
- #4 `bench_arch_write_quality_before_graph`: RRF 0.0145; BM25 rank7 (write); BM25相关 5.06; Vector rank3; Vector相关 0.10; Metadata rank32: 重要性 0.29; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0005; 标题匹配加权 0.0001
- #5 `bench_preference_no_fake_results`: RRF 0.0143; BM25 rank9 (file); BM25相关 4.84; Vector rank7; Vector相关 0.08; Metadata rank17: 重要性 0.32; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0004; 标题匹配加权 0.0001
### plan_progress_resume_workflow

- Category: workflow
- Query: 用户说继续时如果已有未完成 Plan，应该重新 manage_plan 还是执行下一个 mark_task_done 步骤？
- Expected any: bench_workflow_plan_progress_marking
- Expected files: none
- Expected kinds: workflow
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_workflow_plan_progress_marking, bench_workflow_phase_roadmap_execution, bench_error_plan_branch_attribute, bench_decision_no_repeat_completed_task, bench_task_phase_d_dataset_expansion

#### Ranked Reasons

- #1 `bench_workflow_plan_progress_marking`: RRF 0.0224; BM25 rank1 (done, manage, manage_plan, mark, mark_task_done, plan); BM25相关 106.90; Vector rank1; Vector相关 0.29; Metadata rank21: 重要性 0.31; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0001; 意图类型加权 0.0020
- #2 `bench_workflow_phase_roadmap_execution`: RRF 0.0171; BM25 rank3 (done, mark, mark_task_done, plan, task); BM25相关 26.31; Vector rank7; Vector相关 0.05; Metadata rank31: 重要性 0.29; 时间 0.20; BM25强度加权 0.0010; Vector强度加权 0.0003; 意图类型加权 0.0020
- #3 `bench_error_plan_branch_attribute`: RRF 0.0163; BM25 rank4 (plan, 如果); BM25相关 14.29; Vector rank2; Vector相关 0.25; Metadata rank18: 重要性 0.31; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0013; 标题匹配加权 0.0001
- #4 `bench_decision_no_repeat_completed_task`: RRF 0.0162; BM25 rank2 (manage, manage_plan, plan, task, 如果, 完成); BM25相关 36.77; Vector rank5; Vector相关 0.10; Metadata rank27: 重要性 0.30; 时间 0.20; BM25强度加权 0.0014; Vector强度加权 0.0005; 标题匹配加权 0.0001
- #5 `bench_task_phase_d_dataset_expansion`: RRF 0.0146; BM25 rank5 (plan, task); BM25相关 10.38; Vector rank10; Vector相关 0.03; Metadata rank10: 重要性 0.32; 时间 0.20; BM25强度加权 0.0004; Vector强度加权 0.0002
### compressed_session_state_phase3

- Category: architecture
- Query: Phase 3 上下文压缩为什么要用结构化 CompressedSessionState 保存任务、文件、测试和错误？
- Expected any: bench_arch_compressed_session_state
- Expected files: tests/test_compressed_session_state.py
- Expected kinds: architecture
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_arch_compressed_session_state, bench_context_compression_strategy_doc, bench_bug_winerror5_index_json, bench_phase3_lifecycle_governance, bench_bug_read_file_feedback_loop

#### Ranked Reasons

- #1 `bench_arch_compressed_session_state`: RRF 0.0206; BM25 rank1 (3, compressed, compressedsessionstate, phase, session, state); BM25相关 101.36; Vector rank1; Vector相关 0.58; Metadata rank24: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0004
- #2 `bench_context_compression_strategy_doc`: RRF 0.0170; BM25 rank2 (上下, 上下文, 下文, 下文压, 保存, 压缩); BM25相关 45.52; Vector rank4; Vector相关 0.15; Metadata rank29: 重要性 0.30; 时间 0.20; BM25强度加权 0.0018; Vector强度加权 0.0004; 标题匹配加权 0.0006
- #3 `bench_bug_winerror5_index_json`: RRF 0.0160; BM25 rank8 (保存, 文件); BM25相关 9.10; Vector rank22; Vector相关 0.02; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0004; Vector强度加权 0.0000; 标题匹配加权 0.0001; 意图类型加权 0.0020
- #4 `bench_phase3_lifecycle_governance`: RRF 0.0158; BM25 rank3 (3, phase); BM25相关 13.06; Vector rank2; Vector相关 0.19; Metadata rank15: 重要性 0.33; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0005; 标题匹配加权 0.0001
- #5 `bench_bug_read_file_feedback_loop`: RRF 0.0153; BM25 rank18 (文件); BM25相关 3.07; Vector rank13; Vector相关 0.09; Metadata rank4: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0001; Vector强度加权 0.0002; 意图类型加权 0.0020
### git_conflict_marker_syntax_error

- Category: error_history
- Query: main.py 启动 SyntaxError，core/engine.py 里有 <<<<<<< ======= >>>>>>> 冲突标记怎么办？
- Expected any: bench_bug_git_conflict_engine_syntax
- Expected files: core/engine.py
- Expected kinds: bug
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=4, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=1, file=none, metadata=1, vector=1
- Ranked ids: bench_bug_git_conflict_engine_syntax, bench_bug_openai_tool_pairing, bench_bug_winerror5_index_json, bench_bug_read_file_feedback_loop, bench_file_history_specialized_recall

#### Ranked Reasons

- #1 `bench_bug_git_conflict_engine_syntax`: RRF 0.0244; BM25 rank1 (core, core/engine.py, engine, error, main, main.py); BM25相关 90.34; Vector rank1; Vector相关 0.63; Metadata rank3: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0014; 意图类型加权 0.0020
- #2 `bench_bug_openai_tool_pairing`: RRF 0.0173; BM25 rank4 (core, core/engine.py, engine, error, py); BM25相关 10.57; Vector rank8; Vector相关 0.08; Metadata rank2: 重要性 0.33; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0005; Vector强度加权 0.0002; 意图类型加权 0.0020
- #3 `bench_bug_winerror5_index_json`: RRF 0.0170; BM25 rank2 (core, error, main, main.py, py, 启动); BM25相关 14.07; Vector rank19; Vector相关 0.01; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0006; Vector强度加权 0.0000; 意图类型加权 0.0020
- #4 `bench_bug_read_file_feedback_loop`: RRF 0.0149; BM25 rank28 (py); BM25相关 0.69; Vector rank7; Vector相关 0.08; Metadata rank4: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0000; Vector强度加权 0.0002; 意图类型加权 0.0020
- #5 `bench_file_history_specialized_recall`: RRF 0.0142; BM25 rank10 (core, error, py); BM25相关 5.33; Vector rank4; Vector相关 0.12; Metadata rank18: 重要性 0.32; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0003
### phase_d_dataset_expansion_goal

- Category: benchmark_coverage
- Query: Phase D 的 memory recall benchmark 数据集扩展要求是不是至少 25 条 case 和 8 个分类？
- Expected any: bench_task_phase_d_dataset_expansion
- Expected files: benchmark/memory_recall_benchmark.py
- Expected kinds: task
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_task_phase_d_dataset_expansion, bench_benchmark_diagnostics_plan, bench_arch_graph_index_deferred, bench_phase3_lifecycle_governance, bench_phase5_rrf_fusion

#### Ranked Reasons

- #1 `bench_task_phase_d_dataset_expansion`: RRF 0.0215; BM25 rank1 (25, 8, benchmark, case, memory, phase); BM25相关 59.65; Vector rank1; Vector相关 0.60; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0008
- #2 `bench_benchmark_diagnostics_plan`: RRF 0.0194; BM25 rank2 (25, benchmark, case, memory, recall); BM25相关 19.55; Vector rank3; Vector相关 0.41; Metadata rank12: 重要性 0.32; 时间 0.20; BM25强度加权 0.0013; Vector强度加权 0.0010; 标题匹配加权 0.0003; 意图类型加权 0.0020
- #3 `bench_arch_graph_index_deferred`: RRF 0.0164; BM25 rank14 (benchmark, memory, recall); BM25相关 9.91; Vector rank8; Vector相关 0.25; Metadata rank21: 重要性 0.31; 时间 0.20; BM25强度加权 0.0007; Vector强度加权 0.0006; 标题匹配加权 0.0001; 意图类型加权 0.0020
- #4 `bench_phase3_lifecycle_governance`: RRF 0.0161; BM25 rank5 (memory, phase, recall); BM25相关 12.63; Vector rank7; Vector相关 0.26; Metadata rank5: 重要性 0.33; 时间 0.20; BM25强度加权 0.0008; Vector强度加权 0.0007; 标题匹配加权 0.0001
- #5 `bench_phase5_rrf_fusion`: RRF 0.0160; BM25 rank3 (25, memory, phase, recall); BM25相关 16.40; Vector rank16; Vector相关 0.17; Metadata rank1: 重要性 0.34; 时间 0.20; BM25强度加权 0.0011; Vector强度加权 0.0004; 标题匹配加权 0.0001
### completed_task_no_repeat_plan

- Category: planning_protocol
- Query: 如果用户提出一个已经完成的相似任务，agent 应该直接重复创建计划吗？
- Expected any: bench_decision_no_repeat_completed_task
- Expected files: none
- Expected kinds: decision
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_decision_no_repeat_completed_task, bench_bug_read_file_feedback_loop, bench_workflow_plan_progress_marking, bench_phase2_index_persistence, bench_error_plan_branch_attribute

#### Ranked Reasons

- #1 `bench_decision_no_repeat_completed_task`: RRF 0.0226; BM25 rank1 (任务, 创建, 复创, 复创建, 如果, 如果用); BM25相关 77.74; Vector rank1; Vector相关 0.30; Metadata rank25: 重要性 0.30; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0004; 意图类型加权 0.0020
- #2 `bench_bug_read_file_feedback_loop`: RRF 0.0160; BM25 rank4 (agent, 重复); BM25相关 8.81; Vector rank2; Vector相关 0.18; Metadata rank14: 重要性 0.32; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0009; 标题匹配加权 0.0001
- #3 `bench_workflow_plan_progress_marking`: RRF 0.0156; BM25 rank2 (一个, 任务, 创建, 如果, 完成, 用户); BM25相关 21.97; Vector rank10; Vector相关 0.07; Metadata rank20: 重要性 0.31; 时间 0.20; BM25强度加权 0.0011; Vector强度加权 0.0004; 标题匹配加权 0.0001
- #4 `bench_phase2_index_persistence`: RRF 0.0151; BM25 rank13 (完成); BM25相关 2.71; Vector rank3; Vector相关 0.17; Metadata rank3: 重要性 0.34; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0009
- #5 `bench_error_plan_branch_attribute`: RRF 0.0147; BM25 rank3 (agent, 创建, 如果, 计划); BM25相关 14.55; Vector rank15; Vector相关 0.05; Metadata rank18: 重要性 0.31; 时间 0.20; BM25强度加权 0.0007; Vector强度加权 0.0003
### arch_context_assembler_budget

- Category: architecture_decision
- Query: 为什么上下文预算装配要由 ContextAssembler 统一处理，而不是 AgentEngine 直接拼接记忆？
- Expected any: bench_arch_context_assembler_budget
- Expected files: core/context_assembler.py
- Expected kinds: decision
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_arch_context_assembler_budget, bench_error_plan_branch_attribute, bench_context_compression_strategy_doc, bench_bug_git_conflict_engine_syntax, bench_phase3_lifecycle_governance

#### Ranked Reasons

- #1 `bench_arch_context_assembler_budget`: RRF 0.0202; BM25 rank1 (agent, agentengine, assembler, context, contextassembler, engine); BM25相关 47.84; Vector rank1; Vector相关 0.33; Metadata rank27: 重要性 0.30; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0001
- #2 `bench_error_plan_branch_attribute`: RRF 0.0179; BM25 rank4 (agent, agentengine, engine); BM25相关 23.02; Vector rank2; Vector相关 0.32; Metadata rank18: 重要性 0.31; 时间 0.20; BM25强度加权 0.0019; Vector强度加权 0.0015; 标题匹配加权 0.0001
- #3 `bench_context_compression_strategy_doc`: RRF 0.0177; BM25 rank2 (assembler, context, contextassembler, engine, 上下, 上下文); BM25相关 41.79; Vector rank12; Vector相关 0.05; Metadata rank25: 重要性 0.30; 时间 0.20; BM25强度加权 0.0035; Vector强度加权 0.0002; 标题匹配加权 0.0002
- #4 `bench_bug_git_conflict_engine_syntax`: RRF 0.0149; BM25 rank5 (agent, agentengine, engine); BM25相关 15.87; Vector rank18; Vector相关 0.01; Metadata rank12: 重要性 0.32; 时间 0.20; BM25强度加权 0.0013; Vector强度加权 0.0001
- #5 `bench_phase3_lifecycle_governance`: RRF 0.0141; BM25 rank11 (记忆); BM25相关 3.00; Vector rank11; Vector相关 0.05; Metadata rank5: 重要性 0.33; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0002
### arch_memory_indexes_split

- Category: architecture_decision
- Query: 为什么要删除或隔离旧 index.json 路径，改成 memory/long_term/indexes 下的 BM25 和 vector 索引？
- Expected any: bench_arch_memory_indexes_split
- Expected files: core/memory_index.py
- Expected kinds: decision
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_arch_memory_indexes_split, bench_phase2_index_persistence, bench_phase5_rrf_fusion, bench_bug_winerror5_index_json, bench_phase4_vector_index

#### Ranked Reasons

- #1 `bench_arch_memory_indexes_split`: RRF 0.0204; BM25 rank1 (25, bm25, index, index.json, indexes, json); BM25相关 54.42; Vector rank1; Vector相关 0.43; Metadata rank30: 重要性 0.29; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0004
- #2 `bench_phase2_index_persistence`: RRF 0.0188; BM25 rank2 (25, bm25, index, indexes, json, long); BM25相关 36.72; Vector rank3; Vector相关 0.23; Metadata rank2: 重要性 0.34; 时间 0.20; BM25强度加权 0.0027; Vector强度加权 0.0008; 标题匹配加权 0.0001
- #3 `bench_phase5_rrf_fusion`: RRF 0.0177; BM25 rank5 (25, bm25, memory, vector); BM25相关 23.01; Vector rank2; Vector相关 0.29; Metadata rank1: 重要性 0.34; 时间 0.20; BM25强度加权 0.0017; Vector强度加权 0.0010
- #4 `bench_bug_winerror5_index_json`: RRF 0.0172; BM25 rank3 (index, index.json, json, long, memory, term); BM25相关 26.29; Vector rank7; Vector相关 0.11; Metadata rank3: 重要性 0.34; 时间 0.20; BM25强度加权 0.0019; Vector强度加权 0.0004; 标题匹配加权 0.0001
- #5 `bench_phase4_vector_index`: RRF 0.0162; BM25 rank7 (index, memory, vector, 索引); BM25相关 17.49; Vector rank4; Vector相关 0.14; Metadata rank6: 重要性 0.33; 时间 0.20; BM25强度加权 0.0013; Vector强度加权 0.0005
### arch_graph_index_deferred

- Category: architecture_decision
- Query: GraphIndex 为什么必须等 benchmark 40 条以上并且 compare 稳定后再做？
- Expected any: bench_arch_graph_index_deferred
- Expected files: docs/evaluation_system_improvement_roadmap.md
- Expected kinds: decision
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_arch_graph_index_deferred, bench_arch_retrieval_not_rewrite, bench_arch_write_quality_before_graph, bench_workflow_memory_benchmark_command, bench_preference_tdd_pytest_required

#### Ranked Reasons

- #1 `bench_arch_graph_index_deferred`: RRF 0.0205; BM25 rank1 (40, benchmark, compare, graph, graphindex, index); BM25相关 40.85; Vector rank1; Vector相关 0.47; Metadata rank20: 重要性 0.31; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0002
- #2 `bench_arch_retrieval_not_rewrite`: RRF 0.0181; BM25 rank3 (benchmark, graph, graphindex, index); BM25相关 27.19; Vector rank6; Vector相关 0.23; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0027; Vector强度加权 0.0007
- #3 `bench_arch_write_quality_before_graph`: RRF 0.0169; BM25 rank2 (benchmark, graph, graphindex, index); BM25相关 27.92; Vector rank11; Vector相关 0.16; Metadata rank32: 重要性 0.29; 时间 0.20; BM25强度加权 0.0027; Vector强度加权 0.0005
- #4 `bench_workflow_memory_benchmark_command`: RRF 0.0163; BM25 rank4 (benchmark, compare); BM25相关 15.80; Vector rank5; Vector相关 0.23; Metadata rank33: 重要性 0.29; 时间 0.20; BM25强度加权 0.0015; Vector强度加权 0.0007; 标题匹配加权 0.0002
- #5 `bench_preference_tdd_pytest_required`: RRF 0.0153; BM25 rank6 (benchmark, 必须); BM25相关 6.97; Vector rank9; Vector相关 0.17; Metadata rank10: 重要性 0.32; 时间 0.20; BM25强度加权 0.0007; Vector强度加权 0.0005; 标题匹配加权 0.0001
### arch_evaluation_entrypoint

- Category: architecture_decision
- Query: 项目评测系统为什么要统一到 scripts/run_evaluation.py，并支持 fast memory all 三种模式？
- Expected any: bench_arch_evaluation_entrypoint
- Expected files: scripts/run_evaluation.py
- Expected kinds: decision
- Hit rank: 2
- Diagnostic: weak_ranking
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_file_run_evaluation_entrypoint, bench_arch_evaluation_entrypoint, bench_file_evaluation_inventory, bench_phase2_index_persistence, bench_workflow_phase_roadmap_execution

#### Ranked Reasons

- #1 `bench_file_run_evaluation_entrypoint`: RRF 0.0194; BM25 rank2 (all, evaluation, fast, memory, py, run); BM25相关 31.09; Vector rank2; Vector相关 0.31; Metadata rank38: 重要性 0.28; 时间 0.20; BM25强度加权 0.0036; Vector强度加权 0.0013; 标题匹配加权 0.0004
- #2 `bench_arch_evaluation_entrypoint`: RRF 0.0191; BM25 rank1 (all, evaluation, fast, memory, py, run); BM25相关 34.92; Vector rank7; Vector相关 0.25; Metadata rank34: 重要性 0.29; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0010; 标题匹配加权 0.0001
- #3 `bench_file_evaluation_inventory`: RRF 0.0160; BM25 rank4 (evaluation, py, run, scripts, scripts/run_evaluation.py); BM25相关 15.29; Vector rank9; Vector相关 0.20; Metadata rank40: 重要性 0.27; 时间 0.20; BM25强度加权 0.0018; Vector强度加权 0.0008; 标题匹配加权 0.0001
- #4 `bench_phase2_index_persistence`: RRF 0.0158; BM25 rank16 (memory, py); BM25相关 2.89; Vector rank1; Vector相关 0.36; Metadata rank3: 重要性 0.34; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0015
- #5 `bench_workflow_phase_roadmap_execution`: RRF 0.0158; BM25 rank3 (evaluation, py, run, scripts, scripts/run_evaluation.py); BM25相关 15.37; Vector rank14; Vector相关 0.15; Metadata rank30: 重要性 0.29; 时间 0.20; BM25强度加权 0.0018; Vector强度加权 0.0006
### arch_write_quality_before_graph

- Category: architecture_decision
- Query: 长期记忆系统下一步为什么先治理写入质量和去重，而不是马上加 graph retrieval？
- Expected any: bench_arch_write_quality_before_graph
- Expected files: core/memory_manager.py
- Expected kinds: decision
- Hit rank: 3
- Diagnostic: weak_ranking
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_arch_retrieval_not_rewrite, bench_arch_graph_index_deferred, bench_arch_write_quality_before_graph, bench_workflow_plan_progress_marking, bench_context_compression_strategy_doc

#### Ranked Reasons

- #1 `bench_arch_retrieval_not_rewrite`: RRF 0.0203; BM25 rank1 (graph, retrieval, 一步, 下一, 下一步, 入质); BM25相关 55.75; Vector rank3; Vector相关 0.21; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0011; 标题匹配加权 0.0001
- #2 `bench_arch_graph_index_deferred`: RRF 0.0166; BM25 rank5 (graph); BM25相关 10.60; Vector rank1; Vector相关 0.28; Metadata rank19: 重要性 0.31; 时间 0.20; BM25强度加权 0.0008; Vector强度加权 0.0015
- #3 `bench_arch_write_quality_before_graph`: RRF 0.0162; BM25 rank3 (graph, retrieval); BM25相关 17.50; Vector rank6; Vector相关 0.18; Metadata rank33: 重要性 0.29; 时间 0.20; BM25强度加权 0.0013; Vector强度加权 0.0010; 标题匹配加权 0.0001
- #4 `bench_workflow_plan_progress_marking`: RRF 0.0162; BM25 rank4 (下一, 不是, 而不, 而不是); BM25相关 12.00; Vector rank4; Vector相关 0.20; Metadata rank20: 重要性 0.31; 时间 0.20; BM25强度加权 0.0009; Vector强度加权 0.0011
- #5 `bench_context_compression_strategy_doc`: RRF 0.0156; BM25 rank8 (系统); BM25相关 5.84; Vector rank2; Vector相关 0.24; Metadata rank24: 重要性 0.30; 时间 0.20; BM25强度加权 0.0004; Vector强度加权 0.0013; 标题匹配加权 0.0001
### file_run_evaluation_entrypoint

- Category: file_history
- Query: scripts/run_evaluation.py 是什么时候加的，它负责哪些本地评测模式？
- Expected any: bench_file_run_evaluation_entrypoint
- Expected files: scripts/run_evaluation.py
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_file_run_evaluation_entrypoint, bench_arch_evaluation_entrypoint, bench_workflow_phase_roadmap_execution, bench_preference_update_benchmark_readme, bench_workflow_pytest_after_core_changes

#### Ranked Reasons

- #1 `bench_file_run_evaluation_entrypoint`: RRF 0.0203; BM25 rank1 (evaluation, py, run, scripts, scripts/run_evaluation.py); BM25相关 17.33; Vector rank1; Vector相关 0.23; Metadata rank36: 重要性 0.28; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0004
- #2 `bench_arch_evaluation_entrypoint`: RRF 0.0193; BM25 rank2 (evaluation, py, run, scripts, scripts/run_evaluation.py); BM25相关 16.13; Vector rank3; Vector相关 0.21; Metadata rank34: 重要性 0.29; 时间 0.20; BM25强度加权 0.0037; Vector强度加权 0.0014; 标题匹配加权 0.0001
- #3 `bench_workflow_phase_roadmap_execution`: RRF 0.0173; BM25 rank3 (evaluation, py, run, scripts, scripts/run_evaluation.py); BM25相关 15.37; Vector rank16; Vector相关 0.06; Metadata rank29: 重要性 0.29; 时间 0.20; BM25强度加权 0.0035; Vector强度加权 0.0004
- #4 `bench_preference_update_benchmark_readme`: RRF 0.0162; BM25 rank5 (evaluation, run); BM25相关 5.35; Vector rank6; Vector相关 0.17; Metadata rank27: 重要性 0.30; 时间 0.20; BM25强度加权 0.0012; Vector强度加权 0.0012
- #5 `bench_workflow_pytest_after_core_changes`: RRF 0.0152; BM25 rank9 (py, run); BM25相关 3.31; Vector rank8; Vector相关 0.17; Metadata rank28: 重要性 0.30; 时间 0.20; BM25强度加权 0.0008; Vector强度加权 0.0011; 标题匹配加权 0.0001
### file_benchmark_readme_metrics

- Category: file_history
- Query: benchmark/README.md 记录了哪些 memory recall benchmark 指标和 baseline 规则？
- Expected any: bench_file_benchmark_readme_metrics
- Expected files: benchmark/README.md
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_file_benchmark_readme_metrics, bench_preference_update_benchmark_readme, bench_arch_evaluation_entrypoint, bench_workflow_memory_benchmark_command, bench_benchmark_diagnostics_plan

#### Ranked Reasons

- #1 `bench_file_benchmark_readme_metrics`: RRF 0.0205; BM25 rank1 (baseline, benchmark, benchmark/readme.md, md, memory, readme); BM25相关 38.60; Vector rank1; Vector相关 0.77; Metadata rank37: 重要性 0.28; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0006
- #2 `bench_preference_update_benchmark_readme`: RRF 0.0191; BM25 rank3 (baseline, benchmark, benchmark/readme.md, md, readme); BM25相关 30.29; Vector rank2; Vector相关 0.67; Metadata rank25: 重要性 0.30; 时间 0.20; BM25强度加权 0.0031; Vector强度加权 0.0013; 标题匹配加权 0.0003
- #3 `bench_arch_evaluation_entrypoint`: RRF 0.0181; BM25 rank2 (baseline, benchmark, benchmark/readme.md, md, memory, readme); BM25相关 32.65; Vector rank8; Vector相关 0.46; Metadata rank34: 重要性 0.29; 时间 0.20; BM25强度加权 0.0034; Vector强度加权 0.0009
- #4 `bench_workflow_memory_benchmark_command`: RRF 0.0179; BM25 rank5 (baseline, benchmark, md, memory, recall); BM25相关 21.83; Vector rank3; Vector相关 0.66; Metadata rank33: 重要性 0.29; 时间 0.20; BM25强度加权 0.0023; Vector强度加权 0.0013; 标题匹配加权 0.0005
- #5 `bench_benchmark_diagnostics_plan`: RRF 0.0172; BM25 rank9 (benchmark, md, memory, recall); BM25相关 14.24; Vector rank4; Vector相关 0.62; Metadata rank12: 重要性 0.32; 时间 0.20; BM25强度加权 0.0015; Vector强度加权 0.0012; 标题匹配加权 0.0005
### file_evaluation_inventory

- Category: file_history
- Query: docs/evaluation_system_inventory.md 这个评测资产盘点文档包含哪些测试和 benchmark 信息？
- Expected any: bench_file_evaluation_inventory
- Expected files: docs/evaluation_system_inventory.md
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_file_evaluation_inventory, bench_arch_evaluation_entrypoint, bench_arch_graph_index_deferred, bench_preference_update_benchmark_readme, bench_file_resume_templates_readme

#### Ranked Reasons

- #1 `bench_file_evaluation_inventory`: RRF 0.0193; BM25 rank1 (benchmark, docs, docs/evaluation_system_inventory.md, evaluation, inventory, md); BM25相关 28.43; Vector rank7; Vector相关 0.21; Metadata rank40: 重要性 0.27; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0010; 标题匹配加权 0.0005
- #2 `bench_arch_evaluation_entrypoint`: RRF 0.0185; BM25 rank2 (benchmark, docs, docs/evaluation_system_inventory.md, evaluation, inventory, md); BM25相关 25.16; Vector rank8; Vector相关 0.21; Metadata rank35: 重要性 0.29; 时间 0.20; BM25强度加权 0.0035; Vector强度加权 0.0010; 标题匹配加权 0.0002
- #3 `bench_arch_graph_index_deferred`: RRF 0.0171; BM25 rank3 (benchmark, docs, evaluation, md, system); BM25相关 13.40; Vector rank6; Vector相关 0.22; Metadata rank25: 重要性 0.31; 时间 0.20; BM25强度加权 0.0019; Vector强度加权 0.0010; 标题匹配加权 0.0001
- #4 `bench_preference_update_benchmark_readme`: RRF 0.0165; BM25 rank9 (benchmark, evaluation, md); BM25相关 8.28; Vector rank1; Vector相关 0.31; Metadata rank28: 重要性 0.30; 时间 0.20; BM25强度加权 0.0012; Vector强度加权 0.0015; 标题匹配加权 0.0001
- #5 `bench_file_resume_templates_readme`: RRF 0.0162; BM25 rank8 (docs, md, 文档); BM25相关 8.65; Vector rank2; Vector相关 0.29; Metadata rank33: 重要性 0.29; 时间 0.20; BM25强度加权 0.0012; Vector强度加权 0.0014
### file_memory_recall_baseline_json

- Category: file_history
- Query: benchmark/baselines/memory_recall_baseline.json 为什么是已提交的质量下限，什么时候才能更新？
- Expected any: bench_file_memory_recall_baseline_json
- Expected files: benchmark/baselines/memory_recall_baseline.json
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_file_memory_recall_baseline_json, bench_task_phase_d_dataset_expansion, bench_workflow_memory_benchmark_command, bench_preference_tdd_pytest_required, bench_benchmark_diagnostics_plan

#### Ranked Reasons

- #1 `bench_file_memory_recall_baseline_json`: RRF 0.0189; BM25 rank1 (baseline, baselines, benchmark, benchmark/baselines/memory_recall_baseline.json, json, memory); BM25相关 23.79; Vector rank7; Vector相关 0.07; Metadata rank35: 重要性 0.29; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0006; 标题匹配加权 0.0003
- #2 `bench_task_phase_d_dataset_expansion`: RRF 0.0166; BM25 rank13 (benchmark, memory, recall); BM25相关 5.61; Vector rank1; Vector相关 0.17; Metadata rank9: 重要性 0.32; 时间 0.20; BM25强度加权 0.0009; Vector强度加权 0.0015; 标题匹配加权 0.0002
- #3 `bench_workflow_memory_benchmark_command`: RRF 0.0165; BM25 rank2 (baseline, baselines, benchmark, benchmark/baselines/memory_recall_baseline.json, json, memory); BM25相关 18.96; Vector rank23; Vector相关 0.00; Metadata rank32: 重要性 0.29; 时间 0.20; BM25强度加权 0.0032; Vector强度加权 0.0000; 标题匹配加权 0.0002
- #4 `bench_preference_tdd_pytest_required`: RRF 0.0165; BM25 rank8 (benchmark, memory, recall, 才能); BM25相关 7.15; Vector rank3; Vector相关 0.10; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0012; Vector强度加权 0.0009
- #5 `bench_benchmark_diagnostics_plan`: RRF 0.0156; BM25 rank12 (benchmark, memory, recall); BM25相关 5.63; Vector rank5; Vector相关 0.08; Metadata rank11: 重要性 0.32; 时间 0.20; BM25强度加权 0.0009; Vector强度加权 0.0008; 标题匹配加权 0.0002
### file_openai_pairing_regression_test_deleted

- Category: file_history
- Query: tests/test_openai_tool_pairing.py 如果被删除或移动，还要保留什么 OpenAI tool pairing 回归覆盖？
- Expected any: bench_file_openai_pairing_regression_test_deleted, bench_bug_openai_tool_pairing
- Expected files: tests/test_openai_tool_pairing.py
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_bug_openai_tool_pairing, bench_file_openai_pairing_regression_test_deleted, bench_workflow_git_push_main, bench_arch_context_assembler_budget, bench_bug_read_file_feedback_loop

#### Ranked Reasons

- #1 `bench_bug_openai_tool_pairing`: RRF 0.0202; BM25 rank2 (ai, open, openai, pairing, py, test); BM25相关 59.36; Vector rank2; Vector相关 0.53; Metadata rank4: 重要性 0.33; 时间 0.20; BM25强度加权 0.0036; Vector强度加权 0.0012; 标题匹配加权 0.0002
- #2 `bench_file_openai_pairing_regression_test_deleted`: RRF 0.0201; BM25 rank1 (ai, open, openai, pairing, py, test); BM25相关 66.21; Vector rank1; Vector相关 0.67; Metadata rank39: 重要性 0.28; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0003
- #3 `bench_workflow_git_push_main`: RRF 0.0168; BM25 rank3 (openai, pairing, py, test, tests, tests/test_openai_tool_pairing.py); BM25相关 40.90; Vector rank9; Vector相关 0.15; Metadata rank21: 重要性 0.31; 时间 0.20; BM25强度加权 0.0025; Vector强度加权 0.0003
- #4 `bench_arch_context_assembler_budget`: RRF 0.0165; BM25 rank4 (ai, open, openai, py, test, tests); BM25相关 31.52; Vector rank3; Vector相关 0.21; Metadata rank27: 重要性 0.30; 时间 0.20; BM25强度加权 0.0019; Vector强度加权 0.0005
- #5 `bench_bug_read_file_feedback_loop`: RRF 0.0155; BM25 rank5 (py, test, tests, tool, 覆盖); BM25相关 12.58; Vector rank4; Vector相关 0.17; Metadata rank13: 重要性 0.32; 时间 0.20; BM25强度加权 0.0008; Vector强度加权 0.0004
### preference_no_fake_results

- Category: preference
- Query: 能不能没运行命令就说测试通过，或者没调用工具就说文件已经修改？
- Expected any: bench_preference_no_fake_results
- Expected files: CLAUDE.md
- Expected kinds: preference
- Hit rank: None
- Diagnostic: expected_missing
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_preference_tdd_pytest_required, bench_bug_git_conflict_engine_syntax, bench_bug_openai_tool_pairing, bench_workflow_git_push_main, bench_preference_file_edit_tool_choice

#### Ranked Reasons

- #1 `bench_preference_tdd_pytest_required`: RRF 0.0208; BM25 rank1 (测试, 测试通, 试通, 试通过, 运行, 通过); BM25相关 34.98; Vector rank1; Vector相关 0.30; Metadata rank14: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0003
- #2 `bench_bug_git_conflict_engine_syntax`: RRF 0.0159; BM25 rank7 (测试, 运行); BM25相关 4.38; Vector rank2; Vector相关 0.26; Metadata rank18: 重要性 0.32; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0013
- #3 `bench_bug_openai_tool_pairing`: RRF 0.0155; BM25 rank3 (不能, 工具, 调用); BM25相关 6.86; Vector rank9; Vector相关 0.08; Metadata rank10: 重要性 0.33; 时间 0.20; BM25强度加权 0.0008; Vector强度加权 0.0004
- #4 `bench_workflow_git_push_main`: RRF 0.0153; BM25 rank4 (修改, 运行); BM25相关 4.62; Vector rank11; Vector相关 0.04; Metadata rank1: 重要性 0.31; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0005; Vector强度加权 0.0002
- #5 `bench_preference_file_edit_tool_choice`: RRF 0.0152; BM25 rank2 (修改, 工具, 文件); BM25相关 9.95; Vector rank12; Vector相关 0.04; Metadata rank27: 重要性 0.30; 时间 0.20; BM25强度加权 0.0011; Vector强度加权 0.0002; 标题匹配加权 0.0001
### preference_stop_read_only_loop

- Category: preference
- Query: 连续多轮只读工具后收到防空转提醒，下一步应该继续 read_file 还是先总结并开始修改？
- Expected any: bench_preference_stop_read_only_loop
- Expected files: tools/file_tool.py
- Expected kinds: preference
- Hit rank: None
- Diagnostic: expected_missing
- Signal counts: bm25=5, error=0, file=4, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=1, metadata=1, vector=1
- Ranked ids: bench_bug_read_file_feedback_loop, bench_preference_file_edit_tool_choice, bench_arch_retrieval_not_rewrite, bench_workflow_plan_progress_marking, bench_workflow_git_push_main

#### Ranked Reasons

- #1 `bench_bug_read_file_feedback_loop`: RRF 0.0199; BM25 rank1 (file, read, read_file, 空转, 防空, 防空转); BM25相关 33.88; Vector rank6; Vector相关 0.12; Metadata rank13: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0009; 标题匹配加权 0.0003
- #2 `bench_preference_file_edit_tool_choice`: RRF 0.0159; BM25 rank2 (file, read, read_file, 修改, 工具); BM25相关 12.85; Vector rank13; Vector相关 0.07; Metadata rank23: 重要性 0.30; 时间 0.20; BM25强度加权 0.0015; Vector强度加权 0.0006; 标题匹配加权 0.0000
- #3 `bench_arch_retrieval_not_rewrite`: RRF 0.0153; BM25 rank3 (一步, 下一, 下一步); BM25相关 8.69; Vector rank19; Vector相关 0.04; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0010; Vector强度加权 0.0003
- #4 `bench_workflow_plan_progress_marking`: RRF 0.0152; BM25 rank5 (下一, 继续); BM25相关 5.76; Vector rank10; Vector相关 0.11; Metadata rank21: 重要性 0.31; 时间 0.20; BM25强度加权 0.0007; Vector强度加权 0.0008
- #5 `bench_workflow_git_push_main`: RRF 0.0149; BM25 rank9 (修改); BM25相关 2.44; Vector rank5; Vector相关 0.13; Metadata rank19: 重要性 0.31; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0010
### preference_update_benchmark_readme

- Category: preference
- Query: 修改 benchmark case 数量、指标或运行方式后，benchmark/README.md 要不要同步更新？
- Expected any: bench_preference_update_benchmark_readme
- Expected files: benchmark/README.md
- Expected kinds: preference
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_preference_update_benchmark_readme, bench_file_resume_templates_readme, bench_arch_evaluation_entrypoint, bench_file_benchmark_readme_metrics, bench_benchmark_diagnostics_plan

#### Ranked Reasons

- #1 `bench_preference_update_benchmark_readme`: RRF 0.0203; BM25 rank1 (benchmark, benchmark/readme.md, case, md, readme); BM25相关 33.16; Vector rank1; Vector相关 0.72; Metadata rank25: 重要性 0.30; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0002
- #2 `bench_file_resume_templates_readme`: RRF 0.0192; BM25 rank2 (md, readme, 不要, 修改, 更新); BM25相关 28.86; Vector rank3; Vector相关 0.62; Metadata rank29: 重要性 0.29; 时间 0.20; BM25强度加权 0.0035; Vector强度加权 0.0013; 标题匹配加权 0.0002
- #3 `bench_arch_evaluation_entrypoint`: RRF 0.0189; BM25 rank5 (benchmark, benchmark/readme.md, md, readme); BM25相关 22.96; Vector rank8; Vector相关 0.34; Metadata rank35: 重要性 0.29; 时间 0.20; BM25强度加权 0.0028; Vector强度加权 0.0007; 意图类型加权 0.0020
- #4 `bench_file_benchmark_readme_metrics`: RRF 0.0189; BM25 rank3 (benchmark, benchmark/readme.md, md, readme); BM25相关 25.65; Vector rank2; Vector相关 0.66; Metadata rank36: 重要性 0.28; 时间 0.20; BM25强度加权 0.0031; Vector强度加权 0.0014; 标题匹配加权 0.0004
- #5 `bench_benchmark_diagnostics_plan`: RRF 0.0182; BM25 rank8 (benchmark, case, md); BM25相关 14.05; Vector rank9; Vector相关 0.33; Metadata rank12: 重要性 0.32; 时间 0.20; BM25强度加权 0.0017; Vector强度加权 0.0007; 标题匹配加权 0.0001; 意图类型加权 0.0020
### workflow_phase_roadmap_execution

- Category: workflow
- Query: 按照 evaluation_system_improvement_roadmap 执行 Phase 2 时，应该怎么分步实现、测测试并标记计划？
- Expected any: bench_workflow_phase_roadmap_execution
- Expected files: docs/evaluation_system_improvement_roadmap.md
- Expected kinds: workflow
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_workflow_phase_roadmap_execution, bench_phase2_index_persistence, bench_arch_graph_index_deferred, bench_phase5_rrf_fusion, bench_arch_compressed_session_state

#### Ranked Reasons

- #1 `bench_workflow_phase_roadmap_execution`: RRF 0.0200; BM25 rank1 (evaluation, improvement, phase, roadmap, system); BM25相关 25.63; Vector rank5; Vector相关 0.13; Metadata rank4: 重要性 0.29; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0040; Vector强度加权 0.0008; 标题匹配加权 0.0001
- #2 `bench_phase2_index_persistence`: RRF 0.0181; BM25 rank2 (2, phase, 实现); BM25相关 18.11; Vector rank9; Vector相关 0.07; Metadata rank8: 重要性 0.34; 时间 0.20; BM25强度加权 0.0028; Vector强度加权 0.0005; 标题匹配加权 0.0002
- #3 `bench_arch_graph_index_deferred`: RRF 0.0176; BM25 rank4 (evaluation, improvement, roadmap, system); BM25相关 14.82; Vector rank20; Vector相关 0.02; Metadata rank25: 重要性 0.31; 时间 0.20; BM25强度加权 0.0023; Vector强度加权 0.0001; 意图类型加权 0.0020
- #4 `bench_phase5_rrf_fusion`: RRF 0.0175; BM25 rank6 (phase, 实现); BM25相关 11.03; Vector rank4; Vector相关 0.17; Metadata rank7: 重要性 0.34; 时间 0.20; BM25强度加权 0.0017; Vector强度加权 0.0011; 标题匹配加权 0.0002
- #5 `bench_arch_compressed_session_state`: RRF 0.0173; BM25 rank5 (phase, 实现, 测试); BM25相关 11.51; Vector rank3; Vector相关 0.20; Metadata rank21: 重要性 0.32; 时间 0.20; BM25强度加权 0.0018; Vector强度加权 0.0013; 标题匹配加权 0.0001
### workflow_memory_benchmark_command

- Category: workflow
- Query: 刷新 memory recall latest json、latest markdown 和 baseline compare report 的完整命令是什么？
- Expected any: bench_workflow_memory_benchmark_command
- Expected files: benchmark/memory_recall_benchmark.py
- Expected kinds: workflow
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_workflow_memory_benchmark_command, bench_file_memory_recall_baseline_json, bench_benchmark_diagnostics_plan, bench_file_run_evaluation_entrypoint, bench_phase3_lifecycle_governance

#### Ranked Reasons

- #1 `bench_workflow_memory_benchmark_command`: RRF 0.0204; BM25 rank1 (baseline, compare, json, latest, memory, recall); BM25相关 57.92; Vector rank1; Vector相关 0.60; Metadata rank32: 重要性 0.29; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0004
- #2 `bench_file_memory_recall_baseline_json`: RRF 0.0178; BM25 rank3 (baseline, compare, json, memory, recall); BM25相关 31.13; Vector rank3; Vector相关 0.46; Metadata rank35: 重要性 0.29; 时间 0.20; BM25强度加权 0.0022; Vector强度加权 0.0012; 标题匹配加权 0.0005
- #3 `bench_benchmark_diagnostics_plan`: RRF 0.0171; BM25 rank6 (latest, memory, recall); BM25相关 18.00; Vector rank2; Vector相关 0.47; Metadata rank11: 重要性 0.32; 时间 0.20; BM25强度加权 0.0012; Vector强度加权 0.0012; 标题匹配加权 0.0003
- #4 `bench_file_run_evaluation_entrypoint`: RRF 0.0170; BM25 rank2 (baseline, json, latest, markdown, memory, recall); BM25相关 40.53; Vector rank10; Vector相关 0.24; Metadata rank37: 重要性 0.28; 时间 0.20; BM25强度加权 0.0028; Vector强度加权 0.0006
- #5 `bench_phase3_lifecycle_governance`: RRF 0.0162; BM25 rank9 (latest, memory, recall); BM25相关 15.64; Vector rank4; Vector相关 0.37; Metadata rank6: 重要性 0.33; 时间 0.20; BM25强度加权 0.0011; Vector强度加权 0.0009
### workflow_pytest_after_core_changes

- Category: workflow
- Query: 如果修改 core 或 tools 逻辑，按项目规范需要补测试并怎么验证？
- Expected any: bench_workflow_pytest_after_core_changes, bench_preference_tdd_pytest_required
- Expected files: CLAUDE.md
- Expected kinds: workflow
- Hit rank: 2
- Diagnostic: weak_ranking
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_preference_file_edit_tool_choice, bench_preference_tdd_pytest_required, bench_workflow_git_push_main, bench_arch_retrieval_not_rewrite, bench_bug_read_file_feedback_loop

#### Ranked Reasons

- #1 `bench_preference_file_edit_tool_choice`: RRF 0.0201; BM25 rank1 (tools, 修改, 目规, 目规范, 规范, 项目); BM25相关 21.61; Vector rank1; Vector相关 0.17; Metadata rank27: 重要性 0.30; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015
- #2 `bench_preference_tdd_pytest_required`: RRF 0.0179; BM25 rank2 (测试, 目规, 目规范, 规范, 项目, 项目规); BM25相关 17.30; Vector rank9; Vector相关 0.03; Metadata rank14: 重要性 0.32; 时间 0.20; BM25强度加权 0.0032; Vector强度加权 0.0003; 标题匹配加权 0.0001
- #3 `bench_workflow_git_push_main`: RRF 0.0170; BM25 rank12 (修改, 规范); BM25相关 4.62; Vector rank10; Vector相关 0.03; Metadata rank1: 重要性 0.31; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0009; Vector强度加权 0.0003; 意图类型加权 0.0020
- #4 `bench_arch_retrieval_not_rewrite`: RRF 0.0154; BM25 rank9 (core, 需要); BM25相关 6.25; Vector rank7; Vector相关 0.05; Metadata rank13: 重要性 0.33; 时间 0.20; BM25强度加权 0.0012; Vector强度加权 0.0004; 标题匹配加权 0.0001
- #5 `bench_bug_read_file_feedback_loop`: RRF 0.0154; BM25 rank8 (tools); BM25相关 6.70; Vector rank6; Vector相关 0.06; Metadata rank20: 重要性 0.32; 时间 0.20; BM25强度加权 0.0012; Vector强度加权 0.0005
### workflow_git_status_before_commit

- Category: workflow
- Query: 提交或推送 main 前为什么要先看 git status、区分 benchmark 生成物和无关文件？
- Expected any: bench_workflow_git_status_before_commit, bench_workflow_git_push_main
- Expected files: README.md
- Expected kinds: workflow
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_workflow_git_push_main, bench_workflow_git_status_before_commit, bench_bug_git_conflict_engine_syntax, bench_preference_update_benchmark_readme, bench_file_benchmark_readme_metrics

#### Ranked Reasons

- #1 `bench_workflow_git_push_main`: RRF 0.0206; BM25 rank1 (git, main, status, 推送, 提交); BM25相关 39.55; Vector rank1; Vector相关 0.39; Metadata rank19: 重要性 0.31; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0002
- #2 `bench_workflow_git_status_before_commit`: RRF 0.0186; BM25 rank2 (benchmark, git, main, status); BM25相关 33.08; Vector rank2; Vector相关 0.26; Metadata rank38: 重要性 0.28; 时间 0.20; BM25强度加权 0.0033; Vector强度加权 0.0010; 标题匹配加权 0.0002
- #3 `bench_bug_git_conflict_engine_syntax`: RRF 0.0176; BM25 rank3 (git, main); BM25相关 20.59; Vector rank3; Vector相关 0.21; Metadata rank12: 重要性 0.32; 时间 0.20; BM25强度加权 0.0021; Vector强度加权 0.0008; 标题匹配加权 0.0001
- #4 `bench_preference_update_benchmark_readme`: RRF 0.0147; BM25 rank9 (benchmark); BM25相关 4.29; Vector rank5; Vector相关 0.17; Metadata rank24: 重要性 0.30; 时间 0.20; BM25强度加权 0.0004; Vector强度加权 0.0006; 标题匹配加权 0.0001
- #5 `bench_file_benchmark_readme_metrics`: RRF 0.0140; BM25 rank8 (benchmark); BM25相关 4.33; Vector rank8; Vector相关 0.11; Metadata rank37: 重要性 0.28; 时间 0.20; BM25强度加权 0.0004; Vector强度加权 0.0004; 标题匹配加权 0.0001
### error_compression_empty_summary_fallback

- Category: error_history
- Query: LLM 摘要返回空导致压缩失败时，应该怎么安全降级并保持 OpenAI tool pair 约束？
- Expected any: bench_bug_openai_tool_pairing
- Expected files: tests/test_openai_tool_pairing.py
- Expected kinds: bug
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_bug_openai_tool_pairing, bench_file_openai_pairing_regression_test_deleted, bench_arch_context_assembler_budget, bench_bug_module_not_found_pytest, bench_bug_read_file_feedback_loop

#### Ranked Reasons

- #1 `bench_bug_openai_tool_pairing`: RRF 0.0223; BM25 rank2 (ai, open, openai, tool); BM25相关 32.76; Vector rank4; Vector相关 0.17; Metadata rank2: 重要性 0.33; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0037; Vector强度加权 0.0013; 标题匹配加权 0.0001; 意图类型加权 0.0020
- #2 `bench_file_openai_pairing_regression_test_deleted`: RRF 0.0193; BM25 rank3 (ai, open, openai, tool); BM25相关 32.57; Vector rank1; Vector相关 0.19; Metadata rank39: 重要性 0.28; 时间 0.20; BM25强度加权 0.0036; Vector强度加权 0.0015; 标题匹配加权 0.0001
- #3 `bench_arch_context_assembler_budget`: RRF 0.0188; BM25 rank1 (ai, open, openai, pair, tool); BM25相关 35.87; Vector rank8; Vector相关 0.08; Metadata rank25: 重要性 0.30; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0006
- #4 `bench_bug_module_not_found_pytest`: RRF 0.0164; BM25 rank20 (失败); BM25相关 2.69; Vector rank7; Vector相关 0.12; Metadata rank5: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0003; Vector强度加权 0.0010; 意图类型加权 0.0020
- #5 `bench_bug_read_file_feedback_loop`: RRF 0.0162; BM25 rank13 (tool); BM25相关 4.88; Vector rank13; Vector相关 0.04; Metadata rank4: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0005; Vector强度加权 0.0003; 意图类型加权 0.0020
### chinese_fuzzy_tool_guard

- Category: chinese_query
- Query: 读文件老是读不到内容还一直读同一段，这种空转守卫之前修过哪里？
- Expected any: bench_bug_read_file_feedback_loop
- Expected files: tests/test_read_guard.py
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=2
- Channel ranks: bm25=1, error=none, file=none, metadata=1, vector=1
- Ranked ids: bench_bug_read_file_feedback_loop, bench_file_resume_templates_readme, bench_preference_file_edit_tool_choice, bench_bug_winerror5_index_json, bench_decision_quality_over_recency

#### Ranked Reasons

- #1 `bench_bug_read_file_feedback_loop`: RRF 0.0206; BM25 rank1 (同一, 守卫, 文件, 空转, 空转守, 转守); BM25相关 33.13; Vector rank2; Vector相关 0.13; Metadata rank13: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0014; 标题匹配加权 0.0003
- #2 `bench_file_resume_templates_readme`: RRF 0.0147; BM25 rank3 (内容); BM25相关 4.87; Vector rank9; Vector相关 0.04; Metadata rank30: 重要性 0.29; 时间 0.20; BM25强度加权 0.0006; Vector强度加权 0.0004; 标题匹配加权 0.0001
- #3 `bench_preference_file_edit_tool_choice`: RRF 0.0105; BM25 rank2 (内容, 文件); BM25相关 6.43; Metadata rank23: 重要性 0.30; 时间 0.20; BM25强度加权 0.0008; 标题匹配加权 0.0001
- #4 `bench_bug_winerror5_index_json`: RRF 0.0104; BM25 rank5 (文件); BM25相关 2.43; Metadata rank3: 重要性 0.34; 时间 0.20; BM25强度加权 0.0003
- #5 `bench_decision_quality_over_recency`: RRF 0.0102; BM25 rank4 (文件); BM25相关 2.49; Metadata rank10: 重要性 0.32; 时间 0.20; BM25强度加权 0.0003