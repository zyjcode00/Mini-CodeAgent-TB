# Memory Recall Benchmark Report

## Summary

- Cases: 18
- Hit@1: 100.00%
- Hit@3: 100.00%
- Hit@5: 100.00%
- MRR: 1.000
- Forbidden violation rate: 0.00%
- Expected file hit rate: 100.00%
- Expected kind hit rate: 100.00%

## Retrieval Signals

- bm25: 18
- error: 6
- file: 2
- metadata: 18
- vector: 18

## By Category

| Category | Cases | Hit@1 | Hit@3 | Hit@5 | MRR | Forbidden | File Hit | Kind Hit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| architecture | 2 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| chinese_query | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| diagnostics | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| error_history | 4 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| file_history | 2 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| lifecycle | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| phase_task | 2 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| preference | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| rerank_quality | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| semantic_rewrite | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| specialized_recall | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |
| workflow | 1 | 100.00% | 100.00% | 100.00% | 1.000 | 0.00% | 100.00% | 100.00% |

## Failures and Weak Rankings

No failed, forbidden, or weak-ranking cases.

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
- Ranked ids: bench_phase5_rrf_fusion, bench_arch_retrieval_not_rewrite, bench_decision_quality_over_recency, bench_phase4_vector_index, bench_phase3_lifecycle_governance

#### Ranked Reasons

- #1 `bench_phase5_rrf_fusion`: RRF 0.0218; BM25 rank1 (5, phase, rrf, 召回, 多路, 多路召); BM25相关 51.92; Vector rank1; Vector相关 0.53; Metadata rank1: 重要性 0.34; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0008
- #2 `bench_arch_retrieval_not_rewrite`: RRF 0.0178; BM25 rank2 (rrf, 已经); BM25相关 16.14; Vector rank11; Vector相关 0.02; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0012; Vector强度加权 0.0001; 意图类型加权 0.0020
- #3 `bench_decision_quality_over_recency`: RRF 0.0169; BM25 rank6 (召回, 排序); BM25相关 5.44; Vector rank8; Vector相关 0.06; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0004; Vector强度加权 0.0002; 标题匹配加权 0.0002; 意图类型加权 0.0020
- #4 `bench_phase4_vector_index`: RRF 0.0153; BM25 rank5 (phase); BM25相关 6.05; Vector rank7; Vector相关 0.09; Metadata rank5: 重要性 0.33; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0003; 标题匹配加权 0.0001
- #5 `bench_phase3_lifecycle_governance`: RRF 0.0151; BM25 rank3 (phase); BM25相关 6.11; Vector rank10; Vector相关 0.03; Metadata rank6: 重要性 0.33; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0001; 标题匹配加权 0.0001
### phase4_vector_index

- Category: phase_task
- Query: Phase 4 加的是不是向量检索和 HashEmbeddingProvider？
- Expected any: bench_phase4_vector_index
- Expected files: core/memory_embedding.py
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Ranked ids: bench_phase4_vector_index, bench_arch_retrieval_not_rewrite, bench_decision_quality_over_recency, bench_phase5_rrf_fusion, bench_phase3_lifecycle_governance

#### Ranked Reasons

- #1 `bench_phase4_vector_index`: RRF 0.0211; BM25 rank1 (4, embedding, hash, hashembeddingprovider, phase, provider); BM25相关 42.91; Vector rank1; Vector相关 0.42; Metadata rank6: 重要性 0.33; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0003
- #2 `bench_arch_retrieval_not_rewrite`: RRF 0.0174; BM25 rank2 (embedding, 检索); BM25相关 7.45; Vector rank11; Vector相关 0.03; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0007; Vector强度加权 0.0001; 标题匹配加权 0.0002; 意图类型加权 0.0020
- #3 `bench_decision_quality_over_recency`: RRF 0.0164; BM25 rank7 (检索); BM25相关 1.87; Vector rank9; Vector相关 0.06; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0002; 意图类型加权 0.0020
- #4 `bench_phase5_rrf_fusion`: RRF 0.0158; BM25 rank5 (phase); BM25相关 6.01; Vector rank5; Vector相关 0.09; Metadata rank1: 重要性 0.34; 时间 0.20; BM25强度加权 0.0006; Vector强度加权 0.0003; 标题匹配加权 0.0002
- #5 `bench_phase3_lifecycle_governance`: RRF 0.0157; BM25 rank3 (phase); BM25相关 6.11; Vector rank7; Vector相关 0.08; Metadata rank5: 重要性 0.33; 时间 0.20; BM25强度加权 0.0006; Vector强度加权 0.0003; 标题匹配加权 0.0002
### index_persistence_incremental

- Category: file_history
- Query: core/memory_index.py 里 IndexPersistence 和增量 BM25 索引是什么时候做的？
- Expected any: bench_phase2_index_persistence
- Expected files: core/memory_index.py
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Ranked ids: bench_phase2_index_persistence, bench_phase4_vector_index, bench_phase5_rrf_fusion, bench_bug_winerror5_index_json, bench_arch_retrieval_not_rewrite

#### Ranked Reasons

- #1 `bench_phase2_index_persistence`: RRF 0.0216; BM25 rank1 (25, bm25, core, core/memory_index.py, index, indexpersistence); BM25相关 63.75; Vector rank1; Vector相关 0.70; Metadata rank3: 重要性 0.34; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0006
- #2 `bench_phase4_vector_index`: RRF 0.0166; BM25 rank2 (core, core/memory_index.py, index, memory, persistence, py); BM25相关 14.54; Vector rank2; Vector相关 0.25; Metadata rank6: 重要性 0.33; 时间 0.20; BM25强度加权 0.0009; Vector强度加权 0.0005
- #3 `bench_phase5_rrf_fusion`: RRF 0.0159; BM25 rank4 (25, bm25, core, memory, py); BM25相关 11.27; Vector rank6; Vector相关 0.15; Metadata rank1: 重要性 0.34; 时间 0.20; BM25强度加权 0.0007; Vector强度加权 0.0003
- #4 `bench_bug_winerror5_index_json`: RRF 0.0156; BM25 rank5 (core, index, memory, py, 索引); BM25相关 9.39; Vector rank7; Vector相关 0.12; Metadata rank2: 重要性 0.34; 时间 0.20; BM25强度加权 0.0006; Vector强度加权 0.0003; 标题匹配加权 0.0001
- #5 `bench_arch_retrieval_not_rewrite`: RRF 0.0153; BM25 rank3 (25, bm25, core, index, memory, py); BM25相关 12.89; Vector rank11; Vector相关 0.06; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0008; Vector强度加权 0.0001
### lifecycle_filters_old_memory

- Category: lifecycle
- Query: 长期记忆现在怎么过滤 archived superseded expired 旧记忆？
- Expected any: bench_phase3_lifecycle_governance
- Expected files: none
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=2, error=0, file=0, metadata=5, vector=5
- Ranked ids: bench_phase3_lifecycle_governance, bench_arch_retrieval_not_rewrite, bench_phase4_vector_index, bench_bug_openai_tool_pairing, bench_file_resume_templates_readme

#### Ranked Reasons

- #1 `bench_phase3_lifecycle_governance`: RRF 0.0208; BM25 rank1 (archived, expired, 期记, 期记忆, 记忆, 长期); BM25相关 33.49; Vector rank1; Vector相关 0.19; Metadata rank6: 重要性 0.33; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015
- #2 `bench_arch_retrieval_not_rewrite`: RRF 0.0183; BM25 rank2 (期记, 期记忆, 记忆, 长期, 长期记); BM25相关 14.36; Vector rank2; Vector相关 0.17; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0017; Vector强度加权 0.0014; 标题匹配加权 0.0001
- #3 `bench_phase4_vector_index`: RRF 0.0081; Vector rank4; Vector相关 0.04; Metadata rank5: 重要性 0.33; 时间 0.20; Vector强度加权 0.0003
- #4 `bench_bug_openai_tool_pairing`: RRF 0.0080; Vector rank5; Vector相关 0.03; Metadata rank4: 重要性 0.33; 时间 0.20; Vector强度加权 0.0003
- #5 `bench_file_resume_templates_readme`: RRF 0.0079; Vector rank3; Vector相关 0.06; Metadata rank16: 重要性 0.29; 时间 0.20; Vector强度加权 0.0005
### architecture_not_rewrite

- Category: architecture
- Query: 现在记忆检索还要推倒重写吗，下一步应该先做 Graph 还是质量测评？
- Expected any: bench_arch_retrieval_not_rewrite
- Expected files: none
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=3, error=0, file=0, metadata=5, vector=5
- Ranked ids: bench_arch_retrieval_not_rewrite, bench_decision_quality_over_recency, bench_phase3_lifecycle_governance, bench_context_compression_strategy_doc, bench_phase2_index_persistence

#### Ranked Reasons

- #1 `bench_arch_retrieval_not_rewrite`: RRF 0.0210; BM25 rank1 (graph, 一步, 下一, 下一步, 倒重, 倒重写); BM25相关 68.75; Vector rank2; Vector相关 0.12; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0010; 标题匹配加权 0.0008
- #2 `bench_decision_quality_over_recency`: RRF 0.0163; BM25 rank2 (检索, 质量); BM25相关 5.89; Vector rank3; Vector相关 0.10; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0009; 标题匹配加权 0.0001
- #3 `bench_phase3_lifecycle_governance`: RRF 0.0150; BM25 rank3 (记忆); BM25相关 2.15; Vector rank7; Vector相关 0.03; Metadata rank6: 重要性 0.33; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0002
- #4 `bench_context_compression_strategy_doc`: RRF 0.0091; Vector rank1; Vector相关 0.17; Metadata rank15: 重要性 0.30; 时间 0.20; Vector强度加权 0.0015
- #5 `bench_phase2_index_persistence`: RRF 0.0084; Vector rank5; Vector相关 0.07; Metadata rank3: 重要性 0.34; 时间 0.20; Vector强度加权 0.0006
### winerror5_index_failure

- Category: error_history
- Query: PS D:\LLM\mini-claude-code-cli> python .\main.py 保存索引失败 WinError 5 拒绝访问 index.json
- Expected any: bench_bug_winerror5_index_json
- Expected files: none
- Expected kinds: bug
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=3, file=0, metadata=5, vector=5
- Ranked ids: bench_bug_winerror5_index_json, bench_bug_module_not_found_pytest, bench_error_plan_branch_attribute, bench_phase5_rrf_fusion, bench_file_resume_templates_readme

#### Ranked Reasons

- #1 `bench_bug_winerror5_index_json`: RRF 0.0241; BM25 rank1 (5, error, index, index.json, json, main); BM25相关 88.27; Vector rank1; Vector相关 0.41; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0010; 意图类型加权 0.0020
- #2 `bench_bug_module_not_found_pytest`: RRF 0.0176; BM25 rank3 (error, py, python, 失败); BM25相关 10.90; Vector rank6; Vector相关 0.08; Metadata rank3: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0005; Vector强度加权 0.0003; 意图类型加权 0.0020
- #3 `bench_error_plan_branch_attribute`: RRF 0.0164; BM25 rank14 (error, py); BM25相关 2.18; Vector rank4; Vector相关 0.11; Metadata rank4: 重要性 0.31; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0001; Vector强度加权 0.0004; 意图类型加权 0.0020
- #4 `bench_phase5_rrf_fusion`: RRF 0.0156; BM25 rank8 (5, py); BM25相关 4.16; Vector rank2; Vector相关 0.21; Metadata rank5: 重要性 0.34; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0007; 标题匹配加权 0.0001
- #5 `bench_file_resume_templates_readme`: RRF 0.0155; BM25 rank2 (claude, cli, code, llm, mini); BM25相关 29.29; Vector rank12; Vector相关 0.03; Metadata rank16: 重要性 0.29; 时间 0.20; BM25强度加权 0.0013; Vector强度加权 0.0001
### openai_tool_pairing_bad_request

- Category: error_history
- Query: BadRequestError assistant tool_calls 后没有紧邻 tool response 是怎么修的？
- Expected any: bench_bug_openai_tool_pairing
- Expected files: tests/test_openai_tool_pairing.py
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=5, file=0, metadata=5, vector=5
- Ranked ids: bench_bug_openai_tool_pairing, bench_bug_winerror5_index_json, bench_error_plan_branch_attribute, bench_bug_module_not_found_pytest, bench_workflow_git_push_main

#### Ranked Reasons

- #1 `bench_bug_openai_tool_pairing`: RRF 0.0236; BM25 rank1 (assistant, bad, badrequesterror, calls, error, request); BM25相关 70.30; Vector rank1; Vector相关 0.64; Metadata rank2: 重要性 0.33; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0005; 意图类型加权 0.0020
- #2 `bench_bug_winerror5_index_json`: RRF 0.0174; BM25 rank3 (error); BM25相关 2.19; Vector rank5; Vector相关 0.08; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0001; Vector强度加权 0.0002; 意图类型加权 0.0020
- #3 `bench_error_plan_branch_attribute`: RRF 0.0170; BM25 rank6 (error); BM25相关 2.00; Vector rank3; Vector相关 0.09; Metadata rank4: 重要性 0.31; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0001; Vector强度加权 0.0002; 意图类型加权 0.0020
- #4 `bench_bug_module_not_found_pytest`: RRF 0.0168; BM25 rank5 (error); BM25相关 2.10; Vector rank7; Vector相关 0.03; Metadata rank3: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0001; Vector强度加权 0.0001; 意图类型加权 0.0020
- #5 `bench_workflow_git_push_main`: RRF 0.0158; BM25 rank2 (tool); BM25相关 9.80; Vector rank2; Vector相关 0.20; Metadata rank14: 重要性 0.31; 时间 0.20; BM25强度加权 0.0006; Vector强度加权 0.0005
### module_not_found_core_pytest

- Category: error_history
- Query: Traceback ModuleNotFoundError No module named core pytest 应该怎么办？
- Expected any: bench_bug_module_not_found_pytest
- Expected files: none
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=4, file=0, metadata=5, vector=5
- Ranked ids: bench_bug_module_not_found_pytest, bench_error_plan_branch_attribute, bench_bug_winerror5_index_json, bench_preference_tdd_pytest_required, bench_phase5_rrf_fusion

#### Ranked Reasons

- #1 `bench_bug_module_not_found_pytest`: RRF 0.0234; BM25 rank1 (core, error, found, module, modulenotfounderror, named); BM25相关 66.02; Vector rank1; Vector相关 0.42; Metadata rank3: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0004; 意图类型加权 0.0020
- #2 `bench_error_plan_branch_attribute`: RRF 0.0179; BM25 rank3 (core, error, no); BM25相关 8.28; Vector rank4; Vector相关 0.12; Metadata rank4: 重要性 0.31; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0005; Vector强度加权 0.0004; 意图类型加权 0.0020
- #3 `bench_bug_winerror5_index_json`: RRF 0.0168; BM25 rank7 (core, error); BM25相关 3.19; Vector rank6; Vector相关 0.02; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0002; Vector强度加权 0.0001; 意图类型加权 0.0020
- #4 `bench_preference_tdd_pytest_required`: RRF 0.0161; BM25 rank2 (pytest, traceback); BM25相关 13.66; Vector rank3; Vector相关 0.14; Metadata rank12: 重要性 0.32; 时间 0.20; BM25强度加权 0.0008; Vector强度加权 0.0005
- #5 `bench_phase5_rrf_fusion`: RRF 0.0153; BM25 rank13 (core); BM25相关 1.03; Vector rank2; Vector相关 0.34; Metadata rank6: 重要性 0.34; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0012
### user_tdd_preference

- Category: preference
- Query: 用户对实现功能和测试有什么要求，是不是必须 pytest 通过才能说完成？
- Expected any: bench_preference_tdd_pytest_required
- Expected files: none
- Expected kinds: preference
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Ranked ids: bench_preference_tdd_pytest_required, bench_phase5_rrf_fusion, bench_workflow_git_push_main, bench_phase3_lifecycle_governance, bench_bug_module_not_found_pytest

#### Ranked Reasons

- #1 `bench_preference_tdd_pytest_required`: RRF 0.0211; BM25 rank1 (pytest, 功能, 完成, 实现, 实现功, 必须); BM25相关 46.71; Vector rank1; Vector相关 0.33; Metadata rank9: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0004
- #2 `bench_phase5_rrf_fusion`: RRF 0.0161; BM25 rank7 (实现); BM25相关 2.67; Vector rank2; Vector相关 0.23; Metadata rank2: 重要性 0.34; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0010; 标题匹配加权 0.0001
- #3 `bench_workflow_git_push_main`: RRF 0.0160; BM25 rank3 (pytest); BM25相关 6.72; Vector rank6; Vector相关 0.10; Metadata rank1: 重要性 0.31; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0006; Vector强度加权 0.0004
- #4 `bench_phase3_lifecycle_governance`: RRF 0.0158; BM25 rank6 (完成); BM25相关 3.28; Vector rank3; Vector相关 0.18; Metadata rank6: 重要性 0.33; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0008; 标题匹配加权 0.0001
- #5 `bench_bug_module_not_found_pytest`: RRF 0.0156; BM25 rank2 (pytest); BM25相关 7.32; Vector rank7; Vector相关 0.08; Metadata rank12: 重要性 0.32; 时间 0.20; BM25强度加权 0.0006; Vector强度加权 0.0003; 标题匹配加权 0.0001
### context_compression_doc

- Category: architecture
- Query: 上下文压缩系统重构文档里说 token budget 和结构化摘要怎么做？
- Expected any: bench_context_compression_strategy_doc
- Expected files: docs/context_compression_strategy_architecture.md
- Expected kinds: architecture
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=3, error=0, file=0, metadata=5, vector=5
- Ranked ids: bench_context_compression_strategy_doc, bench_file_resume_templates_readme, bench_decision_quality_over_recency, bench_arch_retrieval_not_rewrite, bench_phase5_rrf_fusion

#### Ranked Reasons

- #1 `bench_context_compression_strategy_doc`: RRF 0.0216; BM25 rank1 (budget, token, 上下, 上下文, 下文, 下文压); BM25相关 100.86; Vector rank1; Vector相关 0.42; Metadata rank15: 重要性 0.30; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0011
- #2 `bench_file_resume_templates_readme`: RRF 0.0148; BM25 rank2 (文档, 结构); BM25相关 5.80; Vector rank7; Vector相关 0.05; Metadata rank16: 重要性 0.29; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0002
- #3 `bench_decision_quality_over_recency`: RRF 0.0146; BM25 rank3 (摘要); BM25相关 3.15; Vector rank10; Vector相关 0.02; Metadata rank9: 重要性 0.32; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0001; 标题匹配加权 0.0001
- #4 `bench_arch_retrieval_not_rewrite`: RRF 0.0085; Vector rank2; Vector相关 0.19; Metadata rank7: 重要性 0.33; 时间 0.20; Vector强度加权 0.0007
- #5 `bench_phase5_rrf_fusion`: RRF 0.0083; Vector rank4; Vector相关 0.10; Metadata rank1: 重要性 0.34; 时间 0.20; Vector强度加权 0.0004
### git_push_main_workflow

- Category: workflow
- Query: 把当前修改提交并推送到 GitHub main 分支前，需要按什么流程检查？
- Expected any: bench_workflow_git_push_main
- Expected files: README.md
- Expected kinds: workflow
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Ranked ids: bench_workflow_git_push_main, bench_bug_winerror5_index_json, bench_arch_retrieval_not_rewrite, bench_file_resume_templates_readme, bench_error_plan_branch_attribute

#### Ranked Reasons

- #1 `bench_workflow_git_push_main`: RRF 0.0240; BM25 rank1 (git, github, hub, main, 交并, 交并推); BM25相关 79.30; Vector rank1; Vector相关 0.45; Metadata rank1: 重要性 0.31; 时间 0.20; 类型匹配 0.25; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0009; 意图类型加权 0.0020
- #2 `bench_bug_winerror5_index_json`: RRF 0.0156; BM25 rank4 (main); BM25相关 3.63; Vector rank3; Vector相关 0.12; Metadata rank3: 重要性 0.34; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0004
- #3 `bench_arch_retrieval_not_rewrite`: RRF 0.0152; BM25 rank2 (当前, 需要); BM25相关 4.96; Vector rank6; Vector相关 0.05; Metadata rank8: 重要性 0.33; 时间 0.20; BM25强度加权 0.0003; Vector强度加权 0.0002; 标题匹配加权 0.0001
- #4 `bench_file_resume_templates_readme`: RRF 0.0148; BM25 rank5 (修改); BM25相关 3.12; Vector rank4; Vector相关 0.11; Metadata rank16: 重要性 0.29; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0004; 标题匹配加权 0.0001
- #5 `bench_error_plan_branch_attribute`: RRF 0.0144; BM25 rank3 (分支, 检查); BM25相关 3.65; Vector rank10; Vector相关 0.03; Metadata rank14: 重要性 0.31; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0001
### readme_resume_file_history

- Category: file_history
- Query: D:\LLM\mini-claude-code-cli\README.md 要在原规范基础上补充内容，相关简历模板文件是哪一个？
- Expected any: bench_file_resume_templates_readme
- Expected files: docs/resume_templates_for_mini_claude_code_cli.md
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Ranked ids: bench_file_resume_templates_readme, bench_workflow_git_push_main, bench_decision_quality_over_recency, bench_bug_winerror5_index_json, bench_benchmark_diagnostics_plan

#### Ranked Reasons

- #1 `bench_file_resume_templates_readme`: RRF 0.0208; BM25 rank1 (claude, cli, code, llm, llm/mini-claude-code-cli/readme.md, md); BM25相关 103.98; Vector rank1; Vector相关 0.49; Metadata rank16: 重要性 0.29; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0004
- #2 `bench_workflow_git_push_main`: RRF 0.0176; BM25 rank2 (md, readme, 规范); BM25相关 15.72; Vector rank5; Vector相关 0.14; Metadata rank14: 重要性 0.31; 时间 0.20; BM25强度加权 0.0006; Vector强度加权 0.0004; 意图类型加权 0.0020
- #3 `bench_decision_quality_over_recency`: RRF 0.0152; BM25 rank4 (文件); BM25相关 2.22; Vector rank4; Vector相关 0.16; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0005
- #4 `bench_bug_winerror5_index_json`: RRF 0.0151; BM25 rank5 (文件); BM25相关 2.17; Vector rank6; Vector相关 0.10; Metadata rank2: 重要性 0.34; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0003
- #5 `bench_benchmark_diagnostics_plan`: RRF 0.0149; BM25 rank8 (md); BM25相关 1.61; Vector rank3; Vector相关 0.20; Metadata rank10: 重要性 0.32; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0006
### agent_engine_plan_branch_attribute

- Category: error_history
- Query: 发生运行错误 AttributeError 'AgentEngine' object has no attribute 'current_plan_branch' 制定 plan 后报错怎么查？
- Expected any: bench_error_plan_branch_attribute
- Expected files: core/engine.py
- Expected kinds: bug
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=5, file=0, metadata=5, vector=5
- Ranked ids: bench_error_plan_branch_attribute, bench_bug_module_not_found_pytest, bench_bug_openai_tool_pairing, bench_bug_winerror5_index_json, bench_file_history_specialized_recall

#### Ranked Reasons

- #1 `bench_error_plan_branch_attribute`: RRF 0.0238; BM25 rank1 (agent, agentengine, attribute, attributeerror, branch, current); BM25相关 129.45; Vector rank1; Vector相关 0.75; Metadata rank4: 重要性 0.31; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0009; 意图类型加权 0.0020
- #2 `bench_bug_module_not_found_pytest`: RRF 0.0181; BM25 rank3 (error, no, 运行); BM25相关 10.27; Vector rank2; Vector相关 0.24; Metadata rank3: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0003; Vector强度加权 0.0005; 标题匹配加权 0.0001; 意图类型加权 0.0020
- #3 `bench_bug_openai_tool_pairing`: RRF 0.0173; BM25 rank2 (agent, agentengine, engine, error); BM25相关 15.79; Vector rank10; Vector相关 0.04; Metadata rank2: 重要性 0.33; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0005; Vector强度加权 0.0001; 意图类型加权 0.0020
- #4 `bench_bug_winerror5_index_json`: RRF 0.0166; BM25 rank7 (error); BM25相关 2.19; Vector rank8; Vector相关 0.08; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0001; Vector强度加权 0.0002; 意图类型加权 0.0020
- #5 `bench_file_history_specialized_recall`: RRF 0.0149; BM25 rank4 (error, 错误); BM25相关 4.03; Vector rank4; Vector相关 0.14; Metadata rank13: 重要性 0.32; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0003
### semantic_rewrite_rrf

- Category: semantic_rewrite
- Query: BM25 和向量结果冲突时现在还是简单加权吗，还是倒数排名融合？
- Expected any: bench_phase5_rrf_fusion
- Expected files: none
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=5
- Ranked ids: bench_phase5_rrf_fusion, bench_phase2_index_persistence, bench_decision_quality_over_recency, bench_arch_retrieval_not_rewrite, bench_benchmark_diagnostics_plan

#### Ranked Reasons

- #1 `bench_phase5_rrf_fusion`: RRF 0.0206; BM25 rank1 (25, bm25, 融合); BM25相关 14.58; Vector rank2; Vector相关 0.14; Metadata rank1: 重要性 0.34; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0010; 标题匹配加权 0.0001
- #2 `bench_phase2_index_persistence`: RRF 0.0195; BM25 rank2 (25, bm25); BM25相关 9.63; Vector rank1; Vector相关 0.21; Metadata rank3: 重要性 0.34; 时间 0.20; BM25强度加权 0.0026; Vector强度加权 0.0015
- #3 `bench_decision_quality_over_recency`: RRF 0.0177; BM25 rank3 (25, bm25); BM25相关 6.67; Vector rank3; Vector相关 0.14; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0018; Vector强度加权 0.0010
- #4 `bench_arch_retrieval_not_rewrite`: RRF 0.0174; BM25 rank4 (25, bm25); BM25相关 6.66; Vector rank4; Vector相关 0.12; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0018; Vector强度加权 0.0009
- #5 `bench_benchmark_diagnostics_plan`: RRF 0.0166; BM25 rank5 (25, bm25); BM25相关 5.98; Vector rank6; Vector相关 0.09; Metadata rank10: 重要性 0.32; 时间 0.20; BM25强度加权 0.0016; Vector强度加权 0.0006
### chinese_quality_question

- Category: chinese_query
- Query: 现在的长期记忆检索是不是已经不是以前那种简单关键词鸡肋检索了？
- Expected any: bench_arch_retrieval_not_rewrite, bench_phase5_rrf_fusion
- Expected files: none
- Expected kinds: none
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=4, error=0, file=0, metadata=5, vector=4
- Ranked ids: bench_arch_retrieval_not_rewrite, bench_decision_quality_over_recency, bench_phase3_lifecycle_governance, bench_benchmark_diagnostics_plan, bench_context_compression_strategy_doc

#### Ranked Reasons

- #1 `bench_arch_retrieval_not_rewrite`: RRF 0.0225; BM25 rank1 (已经, 忆检, 忆检索, 期记, 期记忆, 检索); BM25相关 33.25; Vector rank5; Vector相关 0.05; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0012; 标题匹配加权 0.0003; 意图类型加权 0.0020
- #2 `bench_decision_quality_over_recency`: RRF 0.0188; BM25 rank3 (检索); BM25相关 3.75; Vector rank2; Vector相关 0.07; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0015; 意图类型加权 0.0020
- #3 `bench_phase3_lifecycle_governance`: RRF 0.0185; BM25 rank2 (期记, 期记忆, 的长, 的长期, 记忆, 长期); BM25相关 16.19; Vector rank3; Vector相关 0.06; Metadata rank5: 重要性 0.33; 时间 0.20; BM25强度加权 0.0019; Vector强度加权 0.0015
- #4 `bench_benchmark_diagnostics_plan`: RRF 0.0113; Vector rank1; Vector相关 0.07; Metadata rank10: 重要性 0.32; 时间 0.20; Vector强度加权 0.0015; 意图类型加权 0.0020
- #5 `bench_context_compression_strategy_doc`: RRF 0.0100; BM25 rank4 (关键); BM25相关 2.40; Metadata rank15: 重要性 0.30; 时间 0.20; BM25强度加权 0.0003
### benchmark_failure_diagnostics

- Category: diagnostics
- Query: memory recall benchmark 失败时报告要怎么看 BM25 Vector metadata file error 各路贡献和 weak ranking？
- Expected any: bench_benchmark_diagnostics_plan
- Expected files: benchmark/memory_recall_benchmark.py
- Expected kinds: decision
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=3, file=1, metadata=5, vector=5
- Ranked ids: bench_benchmark_diagnostics_plan, bench_phase5_rrf_fusion, bench_bug_winerror5_index_json, bench_bug_module_not_found_pytest, bench_decision_quality_over_recency

#### Ranked Reasons

- #1 `bench_benchmark_diagnostics_plan`: RRF 0.0210; BM25 rank1 (25, benchmark, bm25, error, file, memory); BM25相关 58.04; Vector rank1; Vector相关 0.48; Metadata rank12: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0005
- #2 `bench_phase5_rrf_fusion`: RRF 0.0181; BM25 rank2 (25, bm25, memory, metadata, recall, vector); BM25相关 25.92; Vector rank2; Vector相关 0.36; Metadata rank5: 重要性 0.34; 时间 0.20; BM25强度加权 0.0018; Vector强度加权 0.0011
- #3 `bench_bug_winerror5_index_json`: RRF 0.0180; BM25 rank6 (error, memory, 失败, 失败时, 败时); BM25相关 15.65; Vector rank11; Vector相关 0.12; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0011; Vector强度加权 0.0004; 标题匹配加权 0.0003; 意图类型加权 0.0020
- #4 `bench_bug_module_not_found_pytest`: RRF 0.0176; BM25 rank9 (error, memory, 失败); BM25相关 7.27; Vector rank4; Vector相关 0.24; Metadata rank3: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0005; Vector强度加权 0.0007; 意图类型加权 0.0020
- #5 `bench_decision_quality_over_recency`: RRF 0.0168; BM25 rank3 (25, benchmark, bm25, memory, metadata, recall); BM25相关 23.24; Vector rank5; Vector相关 0.19; Metadata rank10: 重要性 0.32; 时间 0.20; BM25强度加权 0.0016; Vector强度加权 0.0006
### quality_over_recent_summary

- Category: rerank_quality
- Query: 召回排序优化时如何避免近期低质量 session summary 淹没高质量旧决策？
- Expected any: bench_decision_quality_over_recency
- Expected files: core/memory_retrieval.py
- Expected kinds: decision
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=0, file=0, metadata=5, vector=4
- Ranked ids: bench_decision_quality_over_recency, bench_context_compression_strategy_doc, bench_phase5_rrf_fusion, bench_file_history_specialized_recall, bench_arch_retrieval_not_rewrite

#### Ranked Reasons

- #1 `bench_decision_quality_over_recency`: RRF 0.0243; BM25 rank1 (session, summary, 优化, 优化时, 低质, 低质量); BM25相关 144.88; Vector rank1; Vector相关 0.58; Metadata rank8: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0016; 意图类型加权 0.0020
- #2 `bench_context_compression_strategy_doc`: RRF 0.0153; BM25 rank2 (summary); BM25相关 7.64; Vector rank3; Vector相关 0.15; Metadata rank15: 重要性 0.30; 时间 0.20; BM25强度加权 0.0002; Vector强度加权 0.0004
- #3 `bench_phase5_rrf_fusion`: RRF 0.0150; BM25 rank5 (召回); BM25相关 2.65; Vector rank5; Vector相关 0.02; Metadata rank1: 重要性 0.34; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0001; 标题匹配加权 0.0001
- #4 `bench_file_history_specialized_recall`: RRF 0.0146; BM25 rank4 (召回, 排序); BM25相关 4.45; Vector rank6; Vector相关 0.02; Metadata rank12: 重要性 0.32; 时间 0.20; BM25强度加权 0.0001; Vector强度加权 0.0001; 标题匹配加权 0.0001
- #5 `bench_arch_retrieval_not_rewrite`: RRF 0.0123; BM25 rank3 (质量); BM25相关 5.37; Metadata rank7: 重要性 0.33; 时间 0.20; BM25强度加权 0.0001; 意图类型加权 0.0020
### file_error_specialized_recall

- Category: specialized_recall
- Query: 调整 hybrid recall 后 file history 和 error history 专用召回为什么仍要保持 exact match 强命中？
- Expected any: bench_file_history_specialized_recall
- Expected files: core/memory_manager.py
- Expected kinds: architecture
- Hit rank: 1
- Diagnostic: ok
- Signal counts: bm25=5, error=4, file=2, metadata=5, vector=5
- Ranked ids: bench_file_history_specialized_recall, bench_bug_winerror5_index_json, bench_bug_module_not_found_pytest, bench_phase5_rrf_fusion, bench_benchmark_diagnostics_plan

#### Ranked Reasons

- #1 `bench_file_history_specialized_recall`: RRF 0.0216; BM25 rank1 (error, exact, file, history, hybrid, match); BM25相关 109.33; Vector rank1; Vector相关 0.57; Metadata rank13: 重要性 0.32; 时间 0.20; BM25强度加权 0.0040; Vector强度加权 0.0015; 标题匹配加权 0.0011
- #2 `bench_bug_winerror5_index_json`: RRF 0.0172; BM25 rank6 (error); BM25相关 4.38; Vector rank5; Vector相关 0.13; Metadata rank1: 重要性 0.34; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0002; Vector强度加权 0.0004; 意图类型加权 0.0020
- #3 `bench_bug_module_not_found_pytest`: RRF 0.0172; BM25 rank7 (error); BM25相关 4.20; Vector rank3; Vector相关 0.14; Metadata rank3: 重要性 0.32; 时间 0.20; 类型匹配 0.35; BM25强度加权 0.0002; Vector强度加权 0.0004; 意图类型加权 0.0020
- #4 `bench_phase5_rrf_fusion`: RRF 0.0163; BM25 rank2 (hybrid, recall, 召回); BM25相关 13.16; Vector rank2; Vector相关 0.19; Metadata rank5: 重要性 0.34; 时间 0.20; BM25强度加权 0.0005; Vector强度加权 0.0005; 标题匹配加权 0.0001
- #5 `bench_benchmark_diagnostics_plan`: RRF 0.0155; BM25 rank3 (error, file, recall); BM25相关 11.84; Vector rank4; Vector相关 0.14; Metadata rank12: 重要性 0.32; 时间 0.20; BM25强度加权 0.0004; Vector强度加权 0.0004; 标题匹配加权 0.0001