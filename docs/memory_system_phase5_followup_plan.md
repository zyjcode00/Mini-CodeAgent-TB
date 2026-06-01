# Phase 5 后续记忆系统与检索缺陷改进方案

> 适用项目：mini-claude-code-cli  
> 关联文档：`docs/memory_system_next_architecture.md`  
> 目标：在不推倒重写现有记忆系统的前提下，补齐 Phase 5 之后的检索质量、写入质量、可观测性和长期演进能力。

---

## 1. 结论摘要

当前记忆系统已经具备继续演进的基础，不建议推倒重写。

优先级建议如下：

1. **先做质量测评与回归基线**：建立可重复运行的 benchmark，避免后续改动只凭主观感觉判断召回效果。
2. **再做写入质量治理**：减少低质量、临时、重复、异常记忆进入长期记忆库。
3. **补齐可观测性与调试能力**：让每一次召回能解释“为什么命中、为什么没命中”。
4. **随后增强检索链路**：包括 Hybrid 召回权重、rerank、真实 embedding provider、查询改写等。
5. **最后再考虑 GraphIndex**：Graph 适合解决实体关系、项目上下文迁移和跨记忆推理问题，但不应早于质量测评体系落地。

一句话：**下一步先做质量 benchmark，不要先做 Graph，也不要重写。**

---

## 2. 当前系统现状概览

根据当前代码与既有架构文档，系统已经包含以下能力：

- 长期记忆条目结构化保存。
- 支持 memory recall / file history / error history 等工具入口。
- 已有 BM25/关键词式索引能力。
- 已引入向量索引与 embedding provider 的方向设计。
- 已有 benchmark 文件雏形，用于评估 memory recall。
- 已有 memory maintenance / context builder / retrieval 等模块拆分。

这些能力说明系统已经进入“可优化架构”阶段，而不是“必须重写”阶段。

---

## 3. 核心问题清单

### 3.1 缺少稳定的召回质量基线

当前最大风险不是某个算法不够高级，而是缺少稳定指标回答以下问题：

- 修改检索权重后，召回是否真的变好？
- BM25、向量、metadata、error/file 专用召回各自贡献是多少？
- 某次失败是 query 理解问题、索引问题、数据质量问题，还是 rerank 问题？
- 长期记忆增长后，是否出现噪声淹没有效记忆？

如果没有 benchmark，后续引入 Graph、embedding 或 rerank 都难以客观判断收益。

### 3.2 长期记忆写入质量不稳定

长期记忆库容易混入以下低质量内容：

- 临时会话片段。
- 半截 traceback 或半截工具输出。
- 重复总结。
- 与项目无关的闲聊。
- 粒度过细、无法复用的事实。
- 缺少 project/files/concepts 元数据的孤立条目。
- 被压缩后的 session summary 噪声。

这些问题会直接影响召回质量：即使检索算法变强，也可能只是在更高效地召回噪声。

### 3.3 检索结果缺少解释性

当前需要进一步回答：

- 结果由哪个通道召回：BM25、vector、metadata、file、error？
- 每个通道原始分是多少？
- 融合权重是多少？
- 哪些 query token 命中了？
- 是否因为 project/file/error metadata 被提升？
- 被过滤掉的候选为什么被过滤？

缺少解释性会导致调参困难，也不利于定位“为什么没召回我想要的记忆”。

### 3.4 Hybrid 检索仍需系统性调权

当前 Hybrid 检索方向是正确的，但后续需要明确：

- BM25 对代码符号、错误消息、文件路径更敏感。
- Vector 对语义相近但字面不同的描述更有帮助。
- Metadata 对 project、file、concept、kind 的精确过滤很关键。
- Error/File 专用召回应保持强命中能力。

如果不通过 benchmark 调权，容易出现以下问题：

- 语义召回压过精确错误召回。
- 文件历史召回被普通记忆稀释。
- 高质量旧决策被近期低质量 session summary 淹没。
- query 很短时 vector 或 BM25 分数不稳定。

### 3.5 GraphIndex 尚未到最高优先级

GraphIndex 有价值，但不是当前第一优先级。

它适合解决：

- 项目、文件、错误、决策、任务之间的关系追踪。
- “这个 bug 以前在哪个文件修过”的多跳查询。
- 架构决策与后续实现之间的关联。
- 同一概念在多个模块中的演进关系。

但如果当前还没有质量 benchmark 和写入治理，GraphIndex 很可能把低质量节点和边也结构化保存，导致更复杂的噪声问题。

---

## 4. Phase 5 后续路线图

### Phase 5.1：召回质量 Benchmark 优先落地

目标：建立可以反复运行的召回质量评估体系。

建议任务：

1. 扩展 `benchmark/memory_recall_benchmark.py`。
2. 建立固定测试集，例如：
   - 项目架构决策查询。
   - 文件历史查询。
   - 错误修复经验查询。
   - 用户偏好查询。
   - 工作流查询。
   - 语义改写查询。
3. 为每条 query 标注 expected memory id/title/concepts。
4. 输出指标：
   - Recall@1
   - Recall@3
   - Recall@5
   - MRR
   - nDCG@k
   - 通道贡献占比
5. benchmark 输出 JSON 报告，便于 CI 或人工对比。

验收标准：

- 可以用一条命令运行 memory recall benchmark。
- benchmark 不依赖外部服务。
- 至少覆盖 file_history、error_history、general recall 三类任务。
- 后续检索权重修改必须能通过 benchmark 对比收益。

建议优先级：最高。

---

### Phase 5.2：长期记忆写入质量治理

目标：从源头减少低质量记忆进入长期库。

建议任务：

1. 在 memory save 前增加质量评分。
2. 评分维度包括：
   - 是否具有长期复用价值。
   - 是否包含明确项目或上下文。
   - 是否有 concepts/files/kind。
   - 是否重复。
   - 是否过短或过长。
   - 是否包含半截工具输出。
   - 是否包含明显异常格式。
3. 对低质量候选执行：
   - 拒绝写入。
   - 降级为 session summary。
   - 要求补充元数据。
   - 合并到已有 memory item。
4. 增加去重与合并逻辑。
5. 为 memory maintenance 增加质量巡检报告。

验收标准：

- 新增记忆至少包含 title/content/kind/project/concepts 中的核心字段。
- 明显重复或临时内容不会直接进入长期记忆。
- 可以生成低质量记忆清单。
- 清理操作保持 index 一致性。

建议优先级：最高。

---

### Phase 5.3：召回解释与调试日志

目标：让每次检索都可以解释和复现。

建议任务：

1. 为 recall 增加 debug/explain 模式。
2. 每个结果输出：
   - memory id/title/kind/project。
   - final_score。
   - bm25_score。
   - vector_score。
   - metadata_score。
   - recency_score。
   - file/error boost。
   - matched terms。
   - source channel。
3. 为被过滤候选记录 filter reason。
4. benchmark 中保存 explain 信息。

验收标准：

- 用户能看出每条结果为什么排名靠前。
- 调参时能判断哪个通道导致误召回。
- 错误/file 查询能看到专用 boost 是否生效。

建议优先级：高。

---

### Phase 5.4：Hybrid 检索权重调优与 rerank

目标：在 benchmark 基线之上优化排序质量。

建议任务：

1. 将融合权重配置化。
2. 区分 query 类型：
   - error query
   - file query
   - architecture query
   - preference query
   - workflow query
   - general semantic query
3. 不同 query 类型采用不同权重。
4. 引入轻量 rerank：
   - title/concepts 精确命中加权。
   - project 精确匹配加权。
   - file path 精确匹配加权。
   - error symbol 精确匹配加权。
   - 高质量记忆加权。
5. 在真实 embedding provider 可用前，保持 hash embedding 作为默认降级方案。

验收标准：

- 调权后 benchmark 指标不下降。
- error/file 专用查询 Recall@3 保持高水平。
- 普通语义查询不会显著干扰专用召回。

建议优先级：高。

---

### Phase 5.5：真实 Embedding Provider

目标：在不破坏本地可测试性的前提下接入更强语义向量。

建议任务：

1. 保留 `HashEmbeddingProvider` 作为默认、测试和离线降级实现。
2. 增加可选 provider：
   - OpenAI-compatible embedding。
   - 本地 sentence-transformers。
   - 其他兼容接口。
3. provider 必须满足：
   - 可配置。
   - 可禁用。
   - 可缓存。
   - 失败时自动降级。
   - 测试环境不依赖外部网络。
4. 为不同 provider 的向量维度、版本和模型名记录 metadata。
5. provider 变化时支持重建 vector index。

验收标准：

- 无 API key 时测试仍可通过。
- 有 provider 配置时可重建向量索引。
- benchmark 可比较 hash embedding 与真实 embedding 的差异。

建议优先级：中高。

---

### Phase 5.6：GraphIndex 设计与试点

目标：在质量体系稳定后，引入关系型记忆索引。

建议任务：

1. 定义节点类型：
   - MemoryItem
   - Project
   - File
   - Error
   - Concept
   - Decision
   - Task
   - Test
2. 定义边类型：
   - mentions
   - fixes
   - depends_on
   - supersedes
   - relates_to
   - occurred_in
   - implemented_by
3. 先做离线构建，不影响主召回链路。
4. Graph 结果作为 recall boost 或补充候选，而不是一开始替代现有检索。
5. 先覆盖少量高价值场景：
   - error -> file -> previous fix
   - file -> decisions -> related tasks
   - concept -> architecture decision -> implementation files

验收标准：

- GraphIndex 可独立构建和清理。
- 不影响现有 recall 功能。
- 至少一个多跳查询场景优于纯 Hybrid 检索。
- Graph 噪声可解释、可回滚。

建议优先级：中。

---

## 5. 推荐实施顺序

| 顺序 | 模块 | 目标 | 原因 |
|---|---|---|---|
| 1 | Benchmark | 建立质量基线 | 没有指标无法判断后续改动收益 |
| 2 | 写入质量治理 | 减少噪声 | 检索质量上限取决于记忆质量 |
| 3 | Explain/Debug | 提升可调试性 | 便于定位误召回和漏召回 |
| 4 | Hybrid 调权/Rerank | 提升排序 | 在基线之上优化更可靠 |
| 5 | 真实 Embedding | 提升语义召回 | 需要 benchmark 验证收益 |
| 6 | GraphIndex | 增强关系推理 | 等数据质量稳定后再结构化关系 |

---

## 6. 不建议做的事情

### 6.1 不建议推倒重写

原因：

- 当前模块边界已经可继续演进。
- 已有索引、检索、维护、benchmark 雏形。
- 重写会丢失已验证的 file/error/history 专用路径。
- 当前问题主要是质量治理和评估体系不足，而非架构完全错误。

### 6.2 不建议先做 GraphIndex

原因：

- Graph 会放大数据质量问题。
- 没有 benchmark 时难以证明 Graph 收益。
- Graph 构建和维护成本高于 Hybrid 调权。
- 当前更紧急的问题是“召回准不准”和“记忆干不干净”。

### 6.3 不建议立即强依赖外部 Embedding 服务

原因：

- 会破坏本地测试稳定性。
- API key、网络、模型版本都会引入不可控因素。
- 应保留 hash/local provider 作为测试和降级路径。

---

## 7. 最小可落地任务包

如果希望快速推进，建议先做以下 4 个小任务：

1. **完善 benchmark 测试集**
   - 新增 20~30 条固定 query。
   - 每条 query 标注 expected title/concepts/kind。

2. **为 recall 输出 explain JSON**
   - 不改变默认用户输出。
   - benchmark 和调试模式可启用。

3. **增加 memory save 质量评分**
   - 先只做 warn/report，不立即 hard reject。
   - 收集一轮低质量样本。

4. **调优 error/file 查询权重**
   - 确保错误和文件历史类召回不被普通语义召回稀释。

完成这 4 个任务后，再决定是否进入真实 embedding 或 GraphIndex。

---

## 8. 验收指标建议

### 8.1 召回指标

- General Recall@3 >= 0.75
- File History Recall@3 >= 0.85
- Error History Recall@3 >= 0.85
- Preference Recall@3 >= 0.80
- Workflow Recall@3 >= 0.80

上述阈值可根据初始 benchmark 结果调整，但应形成固定门槛。

### 8.2 写入质量指标

- 新增长期记忆中低质量条目比例 < 10%。
- 重复记忆比例 < 5%。
- 缺少 project/concepts/kind 的条目比例持续下降。
- maintenance 可列出候选清理项。

### 8.3 可观测性指标

- 召回结果可输出通道分数。
- benchmark 报告包含失败样例。
- 每个失败样例能区分：未入库、索引失败、召回失败、排序失败、过滤失败。

---

## 9. 风险与缓解

| 风险 | 表现 | 缓解 |
|---|---|---|
| benchmark 过拟合 | 指标提升但真实使用无改善 | 测试集分层，保留人工抽样 |
| 质量过滤过严 | 有价值记忆被拒绝 | 先 warn 后 enforce，保留人工 override |
| embedding 不稳定 | 不同环境结果不同 | hash provider 作为测试基线 |
| Graph 噪声 | 多跳结果变差 | Graph 先做补充候选，不替代主链路 |
| 权重调参混乱 | 改动后无法解释 | 所有召回保存 explain 信息 |

---

## 10. 最终建议

Phase 5 后续不应从“更复杂的索引”开始，而应从“质量可证明”开始。

推荐路线：

```text
Benchmark -> 写入质量治理 -> Explain/Debug -> Hybrid/Rerank -> Embedding -> GraphIndex
```

其中最关键的第一步是：

> 建立一套可以反复运行、覆盖 general/file/error/preference/workflow 的 memory recall benchmark，并把后续所有检索改动都纳入回归比较。

这样可以避免记忆系统进入“功能越来越多，但质量不可证明”的状态。
