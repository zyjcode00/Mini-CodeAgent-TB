# 长期记忆 Benchmark 与检索优化执行计划

> 适用项目：`mini-claude-code-cli`  
> 保存位置：`docs/memory_recall_benchmark_optimization_plan.md`  
> 关联文件：
> - `benchmark/memory_recall_benchmark.py`
> - `tests/test_memory_recall_benchmark.py`
> - `benchmark/memory_recall_latest.json`
> - `benchmark/memory_recall_latest.md`
> - `core/memory_manager.py`
> - `core/memory_retrieval.py`
> - `core/memory_index.py`
>
> 总目标：先把长期记忆系统的检索质量变成可测量、可解释、可回归对比的工程体系，再基于真实失败样本逐步优化召回、排序、写入质量和后续 Graph 能力。

---

## 1. 总体结论

当前长期记忆系统已经具备继续演进的基础，不建议推倒重写。

后续优化顺序应当是：

1. **先完善 benchmark 质量评估体系**：让每次检索改动都能被量化验证。
2. **再补失败诊断与对比报告**：知道每个 case 为什么成功、为什么失败、比上次变好还是变差。
3. **再基于 benchmark 结果优化检索链路**：调整 BM25、vector、metadata、file/error 专用召回、RRF/rerank 权重。
4. **同步治理长期记忆写入质量**：减少重复、临时、低价值和 metadata 不完整的长期记忆。
5. **最后再考虑 GraphIndex**：Graph 应建立在稳定数据质量和稳定召回评价体系之上。

一句话：**下一步优先做 benchmark 对比与失败诊断，不要先做 Graph，也不要重写记忆系统。**

---

## 2. 当前基础状态

当前已经具备以下基础能力：

- 已有 `benchmark/memory_recall_benchmark.py`。
- 已有 `tests/test_memory_recall_benchmark.py` 回归测试。
- benchmark 已覆盖多类任务：
  - phase/task 查询
  - file history 查询
  - error history 查询
  - preference 查询
  - workflow 查询
  - architecture 查询
  - semantic rewrite 查询
  - chinese query 查询
- 当前报告已包含：
  - Hit@1
  - Hit@3
  - Hit@5
  - MRR
  - Forbidden violation rate
  - Expected file hit rate
  - Expected kind hit rate
  - Retrieval signal counts
  - By category breakdown
- 当前 benchmark 可以生成：
  - `benchmark/memory_recall_latest.json`
  - `benchmark/memory_recall_latest.md`

这说明项目已经有了可继续完善的 benchmark 骨架，后续重点不是从零开始，而是把它升级成检索优化的核心工程护栏。

---

## 3. 优化总原则

### 3.1 不凭感觉改检索

任何检索权重、排序、过滤、embedding、metadata boost 的改动，都必须经过 benchmark 对比。

每次改动至少回答：

- Hit@1 是否提升？
- Hit@3 / Hit@5 是否退化？
- MRR 是否变化？
- error/file/preference/workflow 等分类是否有局部退化？
- 是否产生 forbidden memory 命中？
- 是否导致旧的高价值决策被新 session summary 淹没？

### 3.2 先诊断，再调参

不要直接盲目调 BM25/vector/metadata 权重。

每个失败 case 先归因：

- query 没理解？
- expected memory 没进入候选集？
- BM25 没召回？
- vector 没召回？
- metadata 没提权？
- RRF/rerank 排错？
- 数据本身 metadata 缺失？
- 旧记忆 lifecycle 状态过滤错误？

### 3.3 写入质量和检索质量一起治理

检索不准不一定只是算法问题，也可能是长期记忆库里噪声太多。

因此后续要同时关注：

- 检索算法优化。
- 长期记忆 item 的 title/content/kind/project/files/concepts 质量。
- session summary 晋升为 long-term memory 的门槛。
- archived/superseded/expired 记忆过滤。

### 3.4 GraphIndex 延后

GraphIndex 有价值，但不应早于 benchmark 和写入质量治理。

原因：

- 如果基础记忆质量差，Graph 只会把噪声结构化。
- 如果没有 benchmark，Graph 的收益无法客观判断。
- 如果没有失败诊断，很难知道 Graph 是否真的解决了召回问题。

---

## 4. 分阶段执行路线

## Phase A：Benchmark 基线固化

### A.1 目标

把当前 benchmark 固化为后续优化的质量基线。

### A.2 具体任务

1. 确认当前 benchmark case 数量和分类。
2. 确认 `run_default_benchmark()` 可以稳定运行。
3. 确认 JSON/Markdown 报告字段完整。
4. 将当前 `memory_recall_latest.json` 复制或另存为 baseline 文件，例如：
   - `benchmark/baselines/memory_recall_baseline.json`
   - `benchmark/baselines/memory_recall_baseline.md`
5. 在 README 或 docs 中记录运行命令。

建议命令：

```bash
python -m pytest tests/test_memory_recall_benchmark.py -q
python -m benchmark.memory_recall_benchmark --output-json benchmark/memory_recall_latest.json --output-md benchmark/memory_recall_latest.md
```

### A.3 验收标准

- `tests/test_memory_recall_benchmark.py` 全部通过。
- benchmark 命令可以生成 JSON 和 Markdown。
- baseline 文件存在。
- 当前质量指标被记录。
- 后续所有检索优化都以该 baseline 为对比起点。

### A.4 建议优先级

最高。建议作为下一步第一件事执行。

---

## Phase B：Benchmark 对比报告

### B.1 目标

让 benchmark 不只输出当前结果，还能和历史 baseline 对比，明确告诉开发者这次改动是变好还是变差。

### B.2 具体任务

在 `benchmark/memory_recall_benchmark.py` 中增加对比能力：

1. 新增 CLI 参数：
   - `--baseline-json benchmark/baselines/memory_recall_baseline.json`
   - `--compare-output-md benchmark/memory_recall_compare.md`
2. 新增对比指标：
   - total cases delta
   - Hit@1 delta
   - Hit@3 delta
   - Hit@5 delta
   - MRR delta
   - forbidden violation delta
   - expected file hit rate delta
   - expected kind hit rate delta
3. 新增 case 级别对比：
   - 新增失败 case。
   - 修复的失败 case。
   - hit rank 上升的 case。
   - hit rank 下降的 case。
   - ranked ids 发生明显变化的 case。
4. 新增 category 级别对比：
   - 哪些 category 退化。
   - 哪些 category 提升。
5. Markdown 报告中增加 `Regression Summary`。

### B.3 推荐数据结构

可以新增：

```python
@dataclass
class BenchmarkComparison:
    baseline_path: str
    current_path: str
    metric_deltas: dict[str, float]
    improved_cases: list[str]
    regressed_cases: list[str]
    fixed_cases: list[str]
    new_failures: list[str]
    category_deltas: dict[str, dict[str, float]]
```

### B.4 回归测试

新增或扩展 `tests/test_memory_recall_benchmark.py`：

- 构造一个 baseline report。
- 构造一个 current report。
- 验证 delta 计算正确。
- 验证新增失败 case 能被识别。
- 验证修复 case 能被识别。
- 验证 Markdown 对比报告包含关键字段。

### B.5 验收标准

- 可以通过命令生成对比报告。
- 对比报告能明确列出退化 case。
- pytest 通过。
- 不依赖外部 API。

### B.6 建议优先级

最高。建议紧跟 Phase A 执行。

---

## Phase C：失败诊断能力

### C.1 目标

让每个失败 case 不只是显示“没命中”，还要尽可能说明失败原因。

### C.2 失败原因分类

建议定义以下诊断类型：

| 类型 | 含义 |
|---|---|
| `not_recalled_by_any_channel` | expected memory 没被任何通道召回 |
| `bm25_miss` | BM25 没召回 expected memory |
| `vector_miss` | vector 没召回 expected memory |
| `metadata_miss` | metadata 没给 expected memory 提权 |
| `rerank_regression` | 召回了但排序太低 |
| `file_filter_miss` | 文件路径相关 query 没命中文件历史 |
| `error_filter_miss` | 错误相关 query 没命中错误历史 |
| `lifecycle_filter_issue` | archived/superseded/expired 过滤异常 |
| `memory_quality_issue` | expected memory 自身元数据或内容质量差 |
| `query_ambiguity` | query 太短或歧义太强 |

### C.3 具体任务

1. 在 benchmark result 中记录每个通道的候选：
   - BM25 candidates
   - vector candidates
   - metadata candidates
   - file candidates
   - error candidates
2. 对每个 case 计算：
   - expected id 是否进入任一候选。
   - expected id 是否进入最终 top-k。
   - expected id 在各通道 rank。
   - expected id 最终 rank。
3. 根据规则生成 diagnosis。
4. Markdown 中增加每个失败 case 的诊断说明。

### C.4 推荐数据结构

可以扩展 case result：

```python
@dataclass
class CaseResult:
    id: str
    category: str
    query: str
    expected_any: list[str]
    ranked_ids: list[str]
    hit_rank: int | None
    channel_ranks: dict[str, int | None]
    diagnosis: list[str]
```

### C.5 回归测试

新增测试覆盖：

- expected memory 完全没召回时，诊断为 `not_recalled_by_any_channel`。
- expected memory 被召回但 rank > 5 时，诊断为 `rerank_regression`。
- file case 没命中文件 metadata 时，诊断为 `file_filter_miss`。
- error case 没命中错误 metadata 时，诊断为 `error_filter_miss`。

### C.6 验收标准

- 每个失败 case 都有至少一个 diagnosis。
- Markdown 报告可以直接看出失败原因。
- pytest 通过。

### C.7 建议优先级

最高。建议在对比报告之后执行。

---

## Phase D：扩展 Benchmark Case 覆盖

### D.1 目标

让 benchmark 更接近真实使用场景，防止只对少量手工 query 过拟合。

### D.2 需要补充的 case 类型

#### 1. 中文模糊查询

例如：

- “之前那个索引报权限问题是咋回事？”
- “记忆系统现在是不是不用重写？”
- “我之前说实现功能要怎么测试？”

#### 2. 文件路径查询

例如：

- `core/memory_index.py` 之前改过什么？
- `benchmark/memory_recall_benchmark.py` 现在负责什么？
- README 相关的历史修改有哪些？

#### 3. 错误 traceback 查询

例如：

- `ModuleNotFoundError: No module named core`
- `BadRequestError tool_calls missing tool response`
- `WinError 5 Access is denied index.json`

#### 4. 用户偏好查询

例如：

- 用户是否要求 pytest 通过才能报告完成？
- 用户是否偏好保存详细计划到 docs？
- 用户是否要求不删除 README 原有内容？

#### 5. 长期架构决策查询

例如：

- 为什么不先做 Graph？
- 为什么下一步先完善 benchmark？
- 为什么不推倒重写长期记忆系统？

#### 6. 噪声与反例查询

例如：

- archived memory 不应返回。
- superseded memory 不应优先返回。
- 临时 session summary 不应压过长期 decision。

### D.3 case 增长节奏

建议不要一次性加入太多 case。

推荐节奏：

- 第一轮：15 -> 25 cases。
- 第二轮：25 -> 40 cases。
- 第三轮：40 -> 60 cases。

每轮新增后都要观察：

- 总体指标是否稳定。
- 哪些 category 最差。
- 是否暴露新的系统性问题。

### D.4 验收标准

- 至少覆盖 8 个以上 category。
- 至少包含 5 个 error history case。
- 至少包含 5 个 file history case。
- 至少包含 5 个 preference/workflow case。
- 至少包含 5 个中文模糊 query。
- forbidden violation rate 仍为 0。

### D.5 建议优先级

高。建议在失败诊断框架完成后持续补充。

---

## Phase E：基于 Benchmark 的检索调优

### E.1 目标

在有基线、对比、诊断之后，再开始优化检索算法和权重。

### E.2 可优化方向

#### 1. BM25 调优

适合：

- 文件路径。
- 错误消息。
- 代码符号。
- 精确关键词。

可尝试：

- 文件路径 token 特殊加权。
- traceback token 特殊加权。
- title 字段加权。
- concepts 字段加权。

#### 2. Vector 调优

适合：

- 中文自然语言模糊 query。
- 语义改写。
- “之前那个问题”类描述。

可尝试：

- 更稳定的 embedding provider。
- query expansion。
- title + content + concepts 组合 embedding。
- 对过短 query 做降权或补充上下文。

#### 3. Metadata 调优

适合：

- project 匹配。
- files 匹配。
- kind 匹配。
- concepts 匹配。
- error pattern 匹配。

可尝试：

- exact file match 强提权。
- kind=bug 对错误查询提权。
- kind=decision 对架构问题提权。
- user preference query 对 kind=preference 提权。

#### 4. RRF / Rerank 调优

适合解决：

- 多通道都召回但排序不对。
- 高价值旧 decision 被近期低质量 summary 淹没。
- error/file 专用召回被 general recall 稀释。

可尝试：

- category-aware rerank。
- kind-aware rerank。
- recency 不再无条件强提权。
- importance 和 confidence 合理参与排序。

### E.3 调优执行规则

每次只改一个变量。

推荐流程：

1. 运行 baseline benchmark。
2. 修改一个权重或规则。
3. 运行 benchmark。
4. 生成 compare report。
5. 如果总体变好且关键 category 不退化，保留。
6. 如果局部变好但关键 category 退化，回滚或进一步分析。

### E.4 验收标准

- Hit@1 不低于 baseline。
- Hit@3 / Hit@5 不退化。
- MRR 不低于 baseline。
- forbidden violation rate 必须为 0。
- error/file category 不得明显退化。

### E.5 建议优先级

中高。必须排在 Phase B/C 之后。

---

## Phase F：长期记忆写入质量治理

### F.1 目标

减少低质量内容进入长期记忆，从源头降低检索噪声。

### F.2 具体任务

1. 增加 memory save 前质量评分。
2. 评分维度包括：
   - 是否有长期复用价值。
   - 是否包含明确项目。
   - 是否包含 concepts。
   - 是否包含 files。
   - 是否包含 kind。
   - 是否过短。
   - 是否过长。
   - 是否重复。
   - 是否是半截工具输出。
   - 是否是临时闲聊。
3. 对低质量记忆执行：
   - 拒绝写入。
   - 降级为 session summary。
   - 合并到已有 memory item。
   - 要求补充 metadata。
4. 增加 memory quality report。
5. 增加去重机制。

### F.3 建议质量规则

| 问题 | 处理 |
|---|---|
| content 太短 | 拒绝或降级 |
| 没有 concepts | 降低 importance |
| 没有 project | 降低可召回优先级 |
| 重复内容 | 合并或标记 superseded |
| 半截 traceback | 降级或补全 |
| 半截 tool output | 不进入长期记忆 |
| 明确用户偏好 | 提高 kind=preference 权重 |
| 架构决策 | 提高 kind=decision 权重 |

### F.4 回归测试

新增测试：

- 低质量临时文本不会保存为长期记忆。
- 明确用户偏好会保存为 preference。
- 重复 memory 会被识别。
- archived/superseded memory 不会在 recall 中优先返回。

### F.5 验收标准

- 新增记忆质量更稳定。
- benchmark 不因新增 session summary 明显退化。
- 可以输出低质量 memory 清单。
- index 与 memory item 状态一致。

### F.6 建议优先级

中高。可以与检索调优并行，但不应早于 benchmark 对比能力。

---

## Phase G：可观测性与调试工具

### G.1 目标

让开发者能够解释每次召回结果的来源、分数和过滤原因。

### G.2 具体任务

1. 增加 debug recall 输出。
2. 输出每个通道候选：
   - bm25 rank/score
   - vector rank/score
   - metadata boost
   - file boost
   - error boost
   - final score/rank
3. 输出过滤原因：
   - archived
   - superseded
   - expired
   - project mismatch
   - confidence too low
4. 在 benchmark markdown 中为失败 case 添加 debug 摘要。
5. 增加 CLI 或工具入口：
   - `memory recall --debug`
   - 或 benchmark 内部 debug 模式。

### G.3 验收标准

- 任意 query 都能看到候选来源。
- 失败 case 能看到 expected memory 是否进过候选集。
- 调参时不需要靠猜。

### G.4 建议优先级

中。建议与 Phase C 失败诊断配合做。

---

## Phase H：GraphIndex 预研与落地条件

### H.1 目标

在 benchmark、写入质量、诊断体系稳定后，再引入 GraphIndex。

### H.2 GraphIndex 适合解决的问题

- 项目、文件、错误、决策、任务之间的关系追踪。
- “这个 bug 以前在哪些文件修过？”
- “某个架构决策后来影响了哪些模块？”
- “某个用户偏好在哪些任务中被执行过？”
- “某个错误从出现到修复经历了哪些步骤？”

### H.3 暂缓原因

现在不建议立即做 GraphIndex，原因：

- 当前最重要的问题是质量评估和失败诊断。
- Graph 会放大低质量 memory 的影响。
- 没有 benchmark 无法证明 Graph 带来的收益。

### H.4 启动条件

只有满足以下条件后才建议进入 Graph：

- benchmark cases >= 40。
- 有 baseline compare report。
- 有失败诊断。
- forbidden violation rate 长期为 0。
- error/file/preference/workflow 分类稳定。
- 低质量 memory 写入已被明显抑制。

### H.5 验收标准

GraphIndex 第一版只做辅助召回，不替代现有 hybrid recall。

第一版目标：

- 能建立 project -> file -> memory 的边。
- 能建立 error -> fix -> file 的边。
- 能建立 decision -> implementation 的边。
- benchmark 中新增 graph_related category。
- Graph 开关打开时，不得导致原有 benchmark 退化。

### H.6 建议优先级

低。排在 Phase A-G 之后。

---

## 5. 推荐执行顺序

推荐严格按以下顺序推进：

1. **Phase A：Benchmark 基线固化**
2. **Phase B：Benchmark 对比报告**
3. **Phase C：失败诊断能力**
4. **Phase D：扩展 Benchmark Case 覆盖到 25+**
5. **Phase E：基于 Benchmark 的检索调优第一轮**
6. **Phase F：长期记忆写入质量治理第一轮**
7. **Phase G：可观测性与 Debug 工具**
8. **Phase D：继续扩展 Benchmark Case 到 40+**
9. **Phase E：检索调优第二轮**
10. **Phase H：GraphIndex 预研**

---

## 6. 每轮开发的标准工作流

每次优化都按这个流程执行：

1. 选定一个小目标。
2. 先写或更新测试。
3. 运行现有 benchmark，记录 baseline。
4. 修改代码。
5. 运行 pytest。
6. 运行 benchmark。
7. 生成 compare report。
8. 判断是否接受改动。
9. 更新文档或报告。
10. 再进入下一轮。

推荐命令：

```bash
python -m pytest tests/test_memory_recall_benchmark.py -q
python -m benchmark.memory_recall_benchmark --output-json benchmark/memory_recall_latest.json --output-md benchmark/memory_recall_latest.md
```

后续实现 compare 后，推荐命令变为：

```bash
python -m benchmark.memory_recall_benchmark \
  --baseline-json benchmark/baselines/memory_recall_baseline.json \
  --output-json benchmark/memory_recall_latest.json \
  --output-md benchmark/memory_recall_latest.md \
  --compare-output-md benchmark/memory_recall_compare.md
```

---

## 7. 质量门禁建议

短期门禁：

- pytest 必须通过。
- benchmark 命令必须运行成功。
- forbidden violation rate 必须为 0。
- Hit@5 不得低于当前 baseline。
- error_history 和 file_history 分类不得明显退化。

中期门禁：

- Hit@1 稳定提升。
- MRR 稳定提升。
- 每个失败 case 都有 diagnosis。
- 对比报告能识别退化 case。
- benchmark case 数量达到 25+。

长期门禁：

- benchmark case 数量达到 40+。
- 每个核心 category 至少 5 个 case。
- 新增 memory 不会明显污染 recall。
- 检索 debug 输出可以解释主要排序结果。
- GraphIndex 引入后不破坏原有 benchmark。

---

## 8. 下一步最小可执行任务

建议下一步就做以下任务：

### 任务 1：固化当前 baseline

产物：

- `benchmark/baselines/memory_recall_baseline.json`
- `benchmark/baselines/memory_recall_baseline.md`

验收：

- baseline 文件存在。
- pytest 通过。
- benchmark 可运行。

### 任务 2：实现 benchmark compare report

产物：

- compare 数据结构。
- compare markdown 输出。
- CLI 参数 `--baseline-json` 和 `--compare-output-md`。
- pytest 覆盖。

验收：

- 能识别 metric delta。
- 能识别 regressed cases。
- 能识别 improved/fixed cases。

### 任务 3：实现失败诊断第一版

产物：

- case result 中增加 diagnosis。
- Markdown 中展示 diagnosis。
- pytest 覆盖。

验收：

- failed case 不再只是显示 failed，而是有原因分类。

---

## 9. 不建议立即做的事情

短期不建议：

1. 不建议重写整个 memory system。
2. 不建议马上做 GraphIndex。
3. 不建议盲目调权重。
4. 不建议直接换外部 embedding 服务。
5. 不建议为了提升当前 15 个 case 的指标而过拟合。
6. 不建议让 session summary 无门槛进入长期记忆。

---

## 10. 最终目标形态

长期目标是让记忆系统具备以下能力：

- 能稳定召回项目历史决策。
- 能稳定召回文件修改历史。
- 能稳定召回错误修复经验。
- 能记住用户偏好和工作流。
- 能解释为什么召回某条记忆。
- 能解释为什么没召回某条记忆。
- 能在检索改动后自动发现退化。
- 能控制长期记忆写入质量。
- 能在未来通过 GraphIndex 支持多跳关系查询。

最终，长期记忆不应只是“能搜到一些历史”，而应该成为 agent 的可靠工程经验库。
