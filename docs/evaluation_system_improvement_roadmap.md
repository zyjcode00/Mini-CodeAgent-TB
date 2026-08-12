# mini-claude-code-cli 评测系统完善路线图

> 适用项目：`D:\LLM\mini-claude-code-cli`  
> 保存位置：`docs/evaluation_system_improvement_roadmap.md`  
> 目标读者：后续接手本项目的 code agent  
> 核心目标：在不推倒重写现有系统的前提下，把项目评测体系从“已有单点 benchmark/pytest”完善为“可重复、可对比、可诊断、可门禁、可扩展”的工程质量闭环。

---

## 1. 当前结论

当前项目已经具备继续完善评测系统的基础，不需要从零开始搭建，也不建议先做大规模架构重写。

优先方向应为：

1. **先固化和扩展现有 memory recall benchmark**：这是目前最成形、最关键的评测链路。
2. **再补齐对比报告、失败诊断、质量门禁**：让后续检索、长期记忆、上下文压缩改动都能被量化验证。
3. **再逐步扩展到上下文压缩、tool call 合规、CLI 行为、性能、端到端 agent 场景**。
4. **最后再考虑 GraphIndex、真实 embedding、多跳召回等高级能力**，并且必须通过 benchmark 证明收益。

一句话：**接下来应继续完善评测体系，而不是凭感觉调检索权重，也不是马上重写架构。**

---

## 2. 已有评测系统现状

### 2.1 已有 benchmark 能力

项目已有长期记忆召回评测骨架：

- `benchmark/memory_recall_benchmark.py`
- `tests/test_memory_recall_benchmark.py`
- `benchmark/baselines/memory_recall_baseline.json`
- `benchmark/baselines/memory_recall_baseline.md`

当前 memory recall benchmark 已具备：

- 默认 case 集合 `default_cases()`。
- 可重复 seed 的测试 memory 数据。
- `run_default_benchmark()` 一键运行。
- JSON/Markdown 报告输出。
- baseline 加载能力。
- compare report 能力。
- category breakdown。
- retrieval signal counts。
- expected file/kind 命中率。
- forbidden archived memory 检查。
- 初步失败诊断字段：`diagnostic_flags`、`diagnostic_summary`、`channel_ranks`、`ranked_signal_counts`。

### 2.2 已有 pytest 覆盖

`tests/test_memory_recall_benchmark.py` 已覆盖：

- benchmark 指标质量门禁。
- category breakdown 输出。
- Phase D case 类型覆盖。
- signal 与 expectation metrics。
- archived memory 不应召回。
- Markdown/JSON 序列化。
- baseline 文件可加载且与当前 case id 对齐。
- CLI 生成 JSON/Markdown。
- compare report 检测指标退化、case 退化、新增失败、删除 case。

此外项目还有多类测试：

- 记忆系统与检索：`tests/test_memory_*.py`
- RRF 融合：`tests/test_memory_rrf_fusion.py`
- OpenAI tool pair 合规：`tests/test_openai_tool_pairing.py`
- read_file 防重复读取：`tests/test_read_guard.py`
- symbol tool：`tests/test_symbol_tool.py`
- turn builder / context / compression 相关测试

### 2.3 已有规划文档

与评测体系直接相关的已有文档包括：

- `docs/memory_recall_benchmark_optimization_plan.md`
- `docs/memory_system_phase5_followup_plan.md`
- `docs/memory_system_next_architecture.md`
- `docs/project_architecture_overview.md`

这些文档已明确一个重要方向：

> 先建立质量 benchmark 与回归基线，再做写入质量治理、Explain/Debug、Hybrid/Rerank、Embedding，最后再考虑 GraphIndex。

---

## 3. 当前主要缺口

虽然已有 memory recall benchmark，但完整评测系统仍有以下缺口：

### 3.1 评测范围仍偏 memory recall

当前最成熟的是长期记忆召回评测。后续还需要覆盖：

- 上下文压缩质量。
- OpenAI / tool call 消息合规。
- AgentEngine 端到端任务执行。
- CLI 交互与命令参数。
- 工具错误自愈能力。
- 文件编辑安全性。
- 性能与稳定性。
- 跨会话 plan / memory 恢复。

### 3.2 benchmark case 数量仍需继续扩大

当前 memory recall case 已达到短期可用水平，但长期目标应为：

- 总 case 数量 >= 40。
- 每个核心 category 至少 5 个 case。
- 覆盖中文、英文、traceback、文件路径、架构决策、用户偏好、工作流、多轮任务恢复等真实场景。

### 3.3 失败诊断还应更细

当前已有诊断字段，但后续需要让每个失败 case 能明确区分：

- 测试数据未入库。
- metadata 不完整。
- BM25 未召回。
- vector 未召回。
- file/error 专用通道未命中。
- 候选进入但排序过低。
- 被 archived/superseded/filter 过滤。
- query rewrite 或语义理解问题。
- 过度依赖近期 session summary。

### 3.4 缺少统一评测入口

当前 benchmark 与 pytest 可运行，但还缺一个统一入口来组织：

- fast unit tests。
- memory benchmark。
- compare report。
- smoke / integration tests。
- 可选 performance tests。
- CI 或本地质量门禁脚本。

### 3.5 缺少评测结果归档策略

应明确：

- 哪些报告要提交到仓库。
- 哪些 latest 报告只作为本地运行产物。
- baseline 什么时候更新。
- compare report 如何命名和归档。
- 退化时如何处理。

---

## 4. 总体原则

后续所有 code agent 必须遵循以下原则：

### 4.1 先测试，后改代码

凡是修改 `core/`、`tools/`、`benchmark/` 中的逻辑，必须：

1. 先新增或更新测试。
2. 再修改代码。
3. 运行相关 pytest。
4. 运行对应 benchmark。
5. 对照 baseline 判断是否接受改动。

### 4.2 不凭感觉调检索

任何检索权重、过滤规则、metadata boost、vector/BM25/RRF 逻辑变化，都必须通过 benchmark compare report 验证。

至少检查：

- Hit@1
- Hit@3
- Hit@5
- MRR
- forbidden violation rate
- expected file hit rate
- expected kind hit rate
- error/file/preference/workflow category 是否退化

### 4.3 baseline 不可随意更新

baseline 只在以下情况更新：

- 新增 case 后，当前实现通过质量门槛。
- 明确接受了某次整体质量提升。
- 文档记录更新原因。
- compare report 显示关键 category 没有不可接受退化。

禁止为了让测试通过而无理由降低 baseline 或删除失败 case。

### 4.4 评测系统优先稳定可重复

测试环境应尽量不依赖外部 API。真实 embedding、真实 LLM、网络服务应作为可选 integration/e2e 测试，不应影响默认 pytest。

### 4.5 GraphIndex 必须后置

GraphIndex 只有在以下条件满足后才进入实现：

- benchmark cases >= 40。
- baseline compare 稳定。
- 失败诊断可解释。
- 写入质量治理初步完成。
- Graph 开关打开后不导致原有 benchmark 退化。

---

## 5. 分阶段执行路线

## Phase 1：评测资产盘点与统一入口

### 目标

让后续 agent 清楚知道项目有哪些测试、benchmark、报告和质量门禁，并能用统一命令运行。

### 任务

1. 新增或完善 `docs/evaluation_system_inventory.md`，列出：
   - `tests/` 下测试分类。
   - `benchmark/` 下 benchmark 分类。
   - baseline 文件。
   - latest/compare 报告文件。
2. 新增本地评测入口脚本，例如：
   - `scripts/run_evaluation.py`
   - 或 `scripts/run_evaluation.ps1`
3. 支持至少三个模式：
   - `fast`：运行核心单元测试。
   - `memory`：运行 memory recall benchmark 与 compare。
   - `all`：运行默认全量 pytest + benchmark。
4. 在 README 或 docs 中记录命令。

### 建议命令

```bash
python -m pytest -q
python -m pytest tests/test_memory_recall_benchmark.py -q
python -m benchmark.memory_recall_benchmark --baseline-json benchmark/baselines/memory_recall_baseline.json --output-json benchmark/memory_recall_latest.json --output-md benchmark/memory_recall_latest.md --compare-output-md benchmark/memory_recall_compare.md
```

### 验收标准

- 文档能说明每类测试负责什么。
- 一条命令能跑 memory benchmark 并生成 compare report。
- 默认命令不依赖外部服务。
- pytest 通过。

---

## Phase 2：Memory Recall Benchmark 扩展到 40+ case

### 目标

把当前最重要的长期记忆评测扩展到更接近真实 agent 使用场景。

### 必须覆盖的 category

每个核心 category 至少 5 个 case：

1. `architecture_decision`
2. `file_history`
3. `error_history`
4. `preference`
5. `workflow`
6. `tool_usage`
7. `context_compression`
8. `semantic_rewrite`
9. `chinese_query`
10. `regression_guard`

### 建议新增 case 类型

- “之前为什么不建议先做 GraphIndex？”
- “哪个文件负责 memory recall benchmark？”
- “read_file 重复读取的问题以前怎么处理？”
- “OpenAI tool call pair 约束失败时怎么修？”
- “用户偏好：不要重复读取已读文档。”
- “中文问法：是不是应该先做评测而不是重写？”
- “Traceback 问法：SyntaxError conflict marker 应召回哪个修复经验？”
- “某个 Phase 的完成状态与下一步是什么？”

### 测试要求

更新 `tests/test_memory_recall_benchmark.py`：

- case 数量断言提高到 >= 40。
- 每个核心 category 至少 5 个 case。
- 新增中文、traceback、文件路径、偏好、工作流断言。
- baseline case id 与当前 case id 对齐。

### 验收标准

- `tests/test_memory_recall_benchmark.py` 通过。
- total cases >= 40。
- forbidden violation rate == 0。
- Hit@5 不低于 baseline 可接受阈值。
- 不因新增 case 删除已有关键 case。

---

## Phase 3：失败诊断与 Explain Debug 深化

### 目标

让每个失败或弱排序 case 都能说明“为什么失败”。

### 任务

1. 在 benchmark result 中记录每个 expected memory 的候选状态：
   - 是否存在于 seed 数据。
   - 是否进入 BM25 候选。
   - 是否进入 vector 候选。
   - 是否进入 metadata 候选。
   - 是否进入 file/error 专用候选。
   - 最终 rank。
   - 是否被 filter。
2. 标准化诊断枚举，例如：
   - `expected_not_seeded`
   - `metadata_missing`
   - `bm25_miss`
   - `vector_miss`
   - `channel_candidate_but_ranked_low`
   - `filtered_archived`
   - `query_rewrite_gap`
   - `recent_summary_noise`
3. Markdown 报告中增加 `Why failed / Why weak` 小节。
4. compare report 中对退化 case 展示诊断变化。

### 测试要求

新增或扩展测试：

- 构造一个 expected id 不存在的 case，应输出 `expected_not_seeded`。
- 构造一个候选进入但 rank 低的 case，应输出 `channel_candidate_but_ranked_low`。
- archived memory 被过滤时，应输出 filter reason 但不得进入最终 top-k。
- Markdown 中必须包含诊断摘要。

### 验收标准

- 失败 case 不再只是 failed，而是能定位失败阶段。
- Markdown/JSON 均包含诊断字段。
- benchmark 调参时不需要靠猜。

---

## Phase 4：质量门禁与回归策略

### 目标

把 benchmark 从“报告工具”升级为“可阻止退化的质量门禁”。

### 任务

1. 为 benchmark 增加可配置阈值：
   - `--min-hit-at-5`
   - `--min-hit-at-3`
   - `--min-mrr`
   - `--max-forbidden-violation-rate`
2. compare report 增加 pass/fail summary。
3. CLI exit code 根据门禁结果返回：
   - 0：通过。
   - 1：质量退化或低于阈值。
4. 文档记录什么时候允许更新 baseline。
5. 可选：增加 `benchmark/quality_gates/memory_recall_gate.json`。

### 初始建议阈值

```text
Hit@5 >= baseline Hit@5
Hit@3 >= baseline Hit@3 - 0.03
MRR >= baseline MRR - 0.03
forbidden violation rate == 0.0
expected file hit rate >= 0.75
expected kind hit rate >= 0.75
error_history category 不得退化超过 0.05
file_history category 不得退化超过 0.05
```

### 测试要求

- 构造低于阈值的 report，CLI 应返回非 0。
- 构造通过阈值的 report，CLI 应返回 0。
- compare markdown 包含 pass/fail summary。

### 验收标准

- 本地能一键判断 memory recall 是否退化。
- CI 或后续自动化可直接使用 exit code。
- baseline 更新有明确规则。

---

## Phase 5：上下文压缩与 Tool Pair 合规评测

### 目标

保证上下文压缩不会破坏 OpenAI tool call pair 约束，也不会丢失关键用户请求、计划和记忆。

### 背景

项目历史中已有重要约束：

> 压缩结果不得包含半截 assistant tool call 与 tool 响应。

已有 `tests/test_openai_tool_pairing.py` 相关测试，应继续扩展为系统性评测。

### 任务

1. 建立 context compression benchmark 或 fixtures：
   - 长对话。
   - tool call + tool response 成对消息。
   - tool call 被压缩边界切开。
   - LLM 摘要为空时 fallback。
   - 包含当前 plan 的对话。
2. 评测指标：
   - tool pair violation count。
   - current user request preserved。
   - current plan preserved。
   - safety instruction preserved。
   - compression ratio。
3. 报告输出：
   - JSON。
   - Markdown。
   - violation details。
4. 将关键用例纳入 pytest。

### 验收标准

- 任何压缩策略都不得产生 OpenAI tool pair 非法消息。
- LLM 摘要失败时必须安全 fallback。
- 当前用户请求和未完成 plan 不得被压缩丢失。
- 默认测试不依赖真实 LLM API。

---

## Phase 6：AgentEngine 端到端评测

### 目标

用最小可控任务验证 agent 从规划、工具调用、文件修改、测试、自愈到完成汇报的完整闭环。

### 建议场景

1. 文档创建任务：
   - 用户要求创建 docs 文件。
   - agent 应写文件、读取校验、报告完成。
2. 小型代码修改任务：
   - 修改一个纯函数。
   - 先写测试。
   - 运行 pytest。
   - 修复失败。
3. 工具错误自愈任务：
   - read_file 文件不存在。
   - grep 无结果。
   - pytest 失败。
4. plan 恢复任务：
   - 已有未完成 plan。
   - 用户说“继续”。
   - agent 从下一个未完成步骤执行。

### 测试方式

优先使用 fake model / fake tool runtime，避免真实 API。必要时把真实模型测试标记为 integration。

### 验收标准

- agent 不会在未调用工具时谎称已修改/运行。
- 多步骤任务必须创建 plan。
- 每完成一步必须 mark_task_done。
- pytest 失败时能读取 traceback 并修复。

---

## Phase 7：CLI 与工具层评测

### 目标

确保命令行入口、工具参数、文件编辑、安全保护在真实开发中稳定。

### 任务

1. CLI 参数 smoke test：
   - help 输出。
   - benchmark 命令。
   - memory recall debug 命令。
2. 文件工具测试：
   - read_file 行范围。
   - edit_file 精确替换。
   - write_full_file 创建文件。
   - search_code 正则搜索。
3. 安全测试：
   - 禁止危险命令或要求确认。
   - 防止越权路径写入。
   - 防止误删关键文件。
4. Windows 路径兼容：
   - `D:\...` 路径。
   - 反斜杠与正斜杠混用。
   - UTF-8 中文文件名。

### 验收标准

- CLI smoke tests 通过。
- Windows 本地路径测试通过。
- 工具错误返回结构稳定，可被 agent 自愈逻辑识别。

---

## Phase 8：性能与稳定性评测

### 目标

防止记忆数量、测试数量、上下文长度增加后系统明显变慢或不稳定。

### 指标

建议记录：

- memory recall P50/P95 latency。
- benchmark 总耗时。
- index rebuild 耗时。
- context assembly 耗时。
- compression 耗时。
- 单次 AgentEngine loop 平均耗时。

### 任务

1. 新增 `benchmark/performance_benchmark.py`。
2. 构造不同规模的 memory 数据：
   - 100
   - 1,000
   - 10,000（可选）
3. 输出 JSON/Markdown 性能报告。
4. 不把性能 benchmark 纳入默认 fast pytest，但可提供手动命令。

### 验收标准

- 性能报告可重复生成。
- 关键路径耗时有 baseline。
- 性能退化可被 compare report 发现。

---

## Phase 9：真实 Embedding / LLM 可选集成评测

### 目标

在默认 hash/fake provider 稳定后，再评估真实外部服务带来的收益。

### 原则

- 默认测试不能依赖外部 API。
- 真实 provider 测试必须显式启用。
- API key 缺失时应 skip，而不是 fail。

### 任务

1. 为真实 embedding provider 增加 integration benchmark。
2. 对比 hash embedding 与真实 embedding：
   - semantic query。
   - 中文 query。
   - paraphrase query。
3. 记录成本、耗时、质量收益。
4. 只有收益稳定时才考虑作为推荐配置。

### 验收标准

- 无 API key 时 pytest 仍通过。
- 有 API key 时可生成 integration report。
- 真实 provider 的收益可通过 compare report 证明。

---

## Phase 10：GraphIndex 前置评测与验收

### 目标

在数据质量和评测体系成熟后，再决定是否实现 GraphIndex。

### 启动条件

必须同时满足：

- memory recall case >= 40。
- 每个核心 category 至少 5 个 case。
- baseline compare report 稳定。
- failure diagnosis 可解释主要失败。
- 写入质量治理已减少低质量 memory。
- forbidden violation rate 长期为 0。

### Graph 相关 benchmark case

新增 `graph_related` category：

- “某个错误以前在哪些文件修过？”
- “某个架构决策影响了哪些模块？”
- “某个用户偏好在哪些任务中被执行过？”
- “某个 Phase 从规划到实现经历了哪些步骤？”

### 验收标准

- GraphIndex 第一版只能作为辅助召回，不替代 hybrid recall。
- Graph 开启后，原有 memory recall benchmark 不得退化。
- graph_related category 有明确收益。

---

## 6. 推荐执行顺序

后续 code agent 应按以下顺序推进，不要跳步：

1. **Phase 1：评测资产盘点与统一入口**
2. **Phase 2：Memory Recall Benchmark 扩展到 40+ case**
3. **Phase 3：失败诊断与 Explain Debug 深化**
4. **Phase 4：质量门禁与回归策略**
5. **Phase 5：上下文压缩与 Tool Pair 合规评测**
6. **Phase 6：AgentEngine 端到端评测**
7. **Phase 7：CLI 与工具层评测**
8. **Phase 8：性能与稳定性评测**
9. **Phase 9：真实 Embedding / LLM 可选集成评测**
10. **Phase 10：GraphIndex 前置评测与验收**

如果只能做下一步，优先做：

> 新增统一评测入口，并把 memory recall benchmark 的 40+ case、compare report、quality gate 串起来。

---

## 7. 每次开发的标准流程

每一轮完善评测系统都必须按以下流程：

1. 读取本路线图和相关已有文档。
2. 选择一个小 Phase 或 Phase 内子任务。
3. 先写或更新测试。
4. 运行当前相关 pytest，确认失败符合预期。
5. 修改代码或 benchmark。
6. 重新运行 pytest。
7. 运行 benchmark。
8. 生成 compare report。
9. 判断是否接受改动。
10. 更新文档、baseline 或 latest 报告。
11. 记录下一步。

推荐命令：

```bash
python -m pytest tests/test_memory_recall_benchmark.py -q
python -m benchmark.memory_recall_benchmark --baseline-json benchmark/baselines/memory_recall_baseline.json --output-json benchmark/memory_recall_latest.json --output-md benchmark/memory_recall_latest.md --compare-output-md benchmark/memory_recall_compare.md
python -m pytest -q
```

---

## 8. 报告与 baseline 管理规范

### 8.1 建议提交到仓库的文件

应提交：

- `benchmark/baselines/*.json`
- `benchmark/baselines/*.md`
- benchmark 源码。
- benchmark 测试。
- 评测系统文档。
- 稳定质量门禁配置。

### 8.2 通常不必提交的文件

除非用户明确要求，否则 latest 运行产物可不提交：

- `benchmark/memory_recall_latest.json`
- `benchmark/memory_recall_latest.md`
- `benchmark/memory_recall_compare.md`
- 临时性能报告。

如果决定提交 latest/compare，应在 commit message 中说明原因。

### 8.3 baseline 更新条件

更新 baseline 前必须确认：

1. 当前 pytest 通过。
2. benchmark 命令通过。
3. compare report 显示没有不可接受退化。
4. 新 baseline 的 case id 与 `default_cases()` 对齐。
5. 文档或 commit message 说明更新原因。

---

## 9. 质量门禁总表

| 阶段 | 门禁 |
|---|---|
| 所有代码修改 | `python -m pytest -q` 通过 |
| memory recall 修改 | `tests/test_memory_recall_benchmark.py` 通过，benchmark compare 不退化 |
| 压缩修改 | OpenAI tool pair 合规测试通过 |
| AgentEngine 修改 | 端到端 fake model 测试通过 |
| CLI 修改 | CLI smoke test 通过 |
| 性能敏感修改 | 性能 benchmark 不明显退化 |
| baseline 更新 | 有 compare report 和更新理由 |
| GraphIndex 修改 | 原有 hybrid recall benchmark 不退化 |

---

## 10. 不建议做的事

短期不建议：

1. 不建议重写整个 memory system。
2. 不建议马上做 GraphIndex。
3. 不建议为了提升少数 case 指标而过拟合。
4. 不建议直接接入真实 embedding 并让默认测试依赖外部 API。
5. 不建议无理由降低 benchmark 阈值。
6. 不建议删除失败 case 来让报告变好看。
7. 不建议让 session summary 无门槛进入长期记忆。
8. 不建议只看总体 Hit@5，而忽略 error/file/preference/workflow 分类退化。

---

## 11. 后续 code agent 的第一批具体任务

### 任务 A：创建评测资产清单

产物：

- `docs/evaluation_system_inventory.md`

内容：

- 测试文件分类。
- benchmark 文件分类。
- baseline/report 文件说明。
- 推荐运行命令。

验收：

- 文档存在。
- 列表与当前仓库实际文件一致。

### 任务 B：新增统一评测入口

产物：

- `scripts/run_evaluation.py` 或等价脚本。
- 对应测试，例如 `tests/test_run_evaluation.py`。

验收：

- 支持 `fast`、`memory`、`all`。
- memory 模式能调用 benchmark compare。
- dry-run 或 command construction 可被 pytest 覆盖。

### 任务 C：扩展 memory recall cases 到 40+

产物：

- 更新 `benchmark/memory_recall_benchmark.py`。
- 更新 `tests/test_memory_recall_benchmark.py`。
- 更新 baseline。

验收：

- total cases >= 40。
- 每个核心 category 至少 5 个 case。
- benchmark 与 pytest 通过。

### 任务 D：实现 benchmark quality gate exit code

产物：

- benchmark CLI 新增阈值参数。
- compare report pass/fail summary。
- pytest 覆盖。

验收：

- 低于阈值返回非 0。
- 达到阈值返回 0。

---

## 12. 最终目标形态

最终项目应具备如下评测能力：

- 一条命令运行核心单元测试。
- 一条命令运行 memory recall benchmark 与 compare。
- 一条命令生成完整本地评测报告。
- 每次检索改动都能判断是否退化。
- 每个失败 recall case 都有可解释诊断。
- 上下文压缩永远不破坏 tool pair 合规。
- AgentEngine 的关键工作流有端到端测试。
- CLI 和工具层有 smoke / regression test。
- 性能变化可被记录和比较。
- 真实 embedding / LLM 只作为可选 integration 测试。
- GraphIndex 是否值得做由 benchmark 证明，而不是主观判断。

最终，`mini-claude-code-cli` 的评测系统应成为后续 agent 迭代项目时的安全护栏：**先评测、再修改、再对比、再接受**。
