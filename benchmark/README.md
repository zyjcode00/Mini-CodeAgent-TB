# Benchmark 说明

本目录保存项目当前的评测脚本、固定基线、最新评测报告和对比报告。现阶段 benchmark 的核心目标是：**用可重复的量化指标约束长期记忆 / memory recall 的检索质量，避免后续优化只凭主观感受或单次样例判断。**

后续任何修改 benchmark case、指标算法、召回排序、长期记忆索引或相关权重时，都必须同步更新本文档中的指标解释、当前数值和质量判读。

## 1. 当前评测范围

当前主要覆盖长期记忆召回质量，入口位于：

- `benchmark/memory_recall_benchmark.py`：memory recall benchmark 主脚本。
- `benchmark/memory_recall_latest.json`：最近一次 benchmark 的机器可读结果。
- `benchmark/memory_recall_latest.md`：最近一次 benchmark 的人类可读报告。
- `benchmark/baselines/memory_recall_baseline.json`：已固化的 baseline 结果。
- `benchmark/baselines/memory_recall_baseline.md`：baseline 的人类可读报告。
- `benchmark/memory_recall_compare.md`：当前结果与 baseline 的对比报告。
- `tests/test_memory_recall_benchmark.py`：benchmark 结构、指标和回归行为测试。
- `scripts/run_evaluation.py`：统一评测入口，Phase 2 起支持 `baseline` 模式，并将 baseline comparison 纳入 `all`。

评测用例当前共 **26 个**，覆盖以下类别：

| 类别 | 用例数 | 说明 |
| --- | ---: | --- |
| `architecture` | 3 | 架构决策、上下文压缩、长期记忆演进方向等召回质量。 |
| `benchmark_coverage` | 1 | benchmark 自身覆盖与质量门禁相关记忆。 |
| `chinese_query` | 2 | 中文查询表达下的召回稳定性。 |
| `diagnostics` | 1 | 诊断信息、报告解释能力相关召回。 |
| `error_history` | 5 | 错误历史、traceback、历史修复经验召回。 |
| `file_history` | 2 | 指定文件相关历史召回。 |
| `lifecycle` | 1 | 生命周期、阶段推进相关记忆召回。 |
| `phase_task` | 2 | Phase 任务、阶段性执行记录召回。 |
| `planning_protocol` | 1 | 计划协议、任务清单相关记忆召回。 |
| `preference` | 2 | 用户偏好、长期约定召回。 |
| `rerank_quality` | 1 | rerank / 排序质量相关用例。 |
| `semantic_rewrite` | 1 | 查询改写、语义补全相关用例。 |
| `specialized_recall` | 1 | 专用召回入口能力。 |
| `tool_guard` | 1 | 工具调用、防误操作约束召回。 |
| `workflow` | 2 | 工程工作流、测试驱动、自愈流程召回。 |

## 2. 运行方式

推荐使用统一评测入口运行：

```bash
python scripts/run_evaluation.py --suite benchmark
```

也可以直接运行 memory recall benchmark：

```bash
python benchmark/memory_recall_benchmark.py
```

运行回归测试：

```bash
python -m pytest tests/test_memory_recall_benchmark.py -q
```

如果修改了长期记忆召回逻辑、索引结构、排序权重或 benchmark case，应至少运行：

```bash
python benchmark/memory_recall_benchmark.py
python -m pytest tests/test_memory_recall_benchmark.py -q
```

必要时再运行完整测试：

```bash
python -m pytest -q
```

## 3. 指标定义

当前 benchmark 使用以下核心指标衡量 memory recall 质量：

| 指标 | 当前值 | 含义 | 质量判读 |
| --- | ---: | --- | --- |
| `total_cases` | 26 | 当前参与评测的用例总数。 | 用例数越多覆盖越充分，但必须保持 case 有明确期望结果。 |
| `hit_at_1` | 1.0 | 期望记忆是否出现在第 1 条结果中。 | 最严格的排序指标；1.0 表示所有 case 的首条结果都命中。 |
| `hit_at_3` | 1.0 | 期望记忆是否出现在前 3 条结果中。 | 衡量用户在少量结果中能否看到正确记忆。 |
| `hit_at_5` | 1.0 | 期望记忆是否出现在前 5 条结果中。 | 衡量召回池是否稳定包含正确记忆。 |
| `mrr` | 1.0 | Mean Reciprocal Rank，期望结果排名倒数的平均值。 | 1.0 表示所有期望结果均排第 1。 |
| `forbidden_violation_rate` | 0.0 | 禁止出现的错误记忆或污染结果的违规比例。 | 越低越好；0.0 表示未发现 forbidden 违规。 |
| `expected_file_hit_rate` | 1.0 | 指定 expected file 的用例中，结果是否命中文件来源。 | 衡量 file history / 文件相关召回是否精准。 |
| `expected_kind_hit_rate` | 1.0 | 指定 expected kind 的用例中，结果是否命中记忆类型。 | 衡量 task / decision / bug 等类型过滤与排序是否正确。 |

### 3.1 检索信号覆盖

当前最近 baseline 中，各检索信号贡献计数如下：

| 信号 | 计数 | 说明 |
| --- | ---: | --- |
| `bm25` | 26 | 关键词 / 稀疏检索信号，所有 26 个 case 均有贡献。 |
| `vector` | 26 | 向量 / 语义检索信号，所有 26 个 case 均有贡献。 |
| `metadata` | 26 | metadata 排序信号，所有 26 个 case 均有贡献。 |
| `file` | 4 | 文件专用召回信号，在文件相关 case 中触发。 |
| `error` | 7 | 错误历史专用召回信号，在错误相关 case 中触发。 |

这说明当前 memory recall 不是单一路径命中，而是由 BM25、向量、metadata、文件专用召回和错误专用召回共同参与。后续改动如果导致某类信号计数异常下降，需要检查是否误伤了索引加载、query 改写、专用召回入口或融合排序逻辑。

## 4. 当前数值质量结论

以当前 baseline 为准，memory recall benchmark 的总体结果为：

```json
{
  "total_cases": 26,
  "hit_at_1": 1.0,
  "hit_at_3": 1.0,
  "hit_at_5": 1.0,
  "mrr": 1.0,
  "forbidden_violation_rate": 0.0,
  "expected_file_hit_rate": 1.0,
  "expected_kind_hit_rate": 1.0,
  "retrieval_signal_counts": {
    "bm25": 26,
    "vector": 26,
    "metadata": 26,
    "file": 4,
    "error": 7
  }
}
```

质量解释：

1. **排序质量当前为满分**：`hit_at_1 = 1.0` 和 `mrr = 1.0` 表示所有 case 的期望记忆都排在第 1 位。
2. **召回质量当前为满分**：`hit_at_3 = 1.0`、`hit_at_5 = 1.0` 表示即使只看少量候选结果，也不会漏掉目标记忆。
3. **污染控制当前良好**：`forbidden_violation_rate = 0.0` 表示当前评测未发现明确禁止结果混入。
4. **文件与类型约束当前稳定**：`expected_file_hit_rate = 1.0`、`expected_kind_hit_rate = 1.0` 表示文件来源与记忆类型约束都能被满足。
5. **专用召回链路仍在工作**：`file = 4`、`error = 7` 表明文件历史和错误历史专用路径没有退化为普通关键词检索。

需要注意：当前数值为满分，并不代表系统已经完成所有评测建设。它只代表**现有 26 个用例覆盖范围内**表现稳定。后续仍应继续增加更难的负例、近似语义混淆 case、跨项目污染 case、陈旧记忆与近期低质量 summary 竞争 case。

## 5. Baseline 与对比规则

当前 baseline 文件：

```text
benchmark/baselines/memory_recall_baseline.json
benchmark/baselines/memory_recall_baseline.md
```

对比报告文件：

```text
benchmark/memory_recall_compare.md
```

建议规则：

1. 修改召回排序、权重、索引、query rewrite、metadata scoring、错误历史召回或文件历史召回后，必须重新跑 benchmark 并查看 compare 报告。
2. 如果 `hit_at_1`、`mrr`、`expected_file_hit_rate`、`expected_kind_hit_rate` 下降，应视为高风险回归。
3. 如果 `forbidden_violation_rate` 上升，应优先排查负例污染、跨项目污染、过度语义召回或 metadata 加权问题。
4. 如果新增 case 导致总分下降，需要区分是系统真实缺陷还是 case 期望设置不合理；不能直接删除失败 case 来维持满分。
5. 当 benchmark case 有实质扩充，且新结果被确认可接受时，应重新固化 baseline，并同步更新本文档。

## 6. 后续维护规范

后续修改 benchmark 时，必须同步维护以下内容：

1. **新增 / 删除 / 修改 case**
   - 更新 `total_cases`。
   - 更新分类表中的类别和用例数。
   - 说明新增 case 主要覆盖什么风险。

2. **修改指标计算逻辑**
   - 更新“指标定义”章节。
   - 说明新旧指标是否可直接比较。
   - 如果不可比较，应重新生成 baseline。

3. **修改召回链路或排序权重**
   - 重新运行 benchmark。
   - 检查 `memory_recall_compare.md`。
   - 如果结果变化，记录变化原因和是否接受。

4. **修改 baseline**
   - 同步更新当前数值。
   - 说明 baseline 更新原因，例如新增 case、修复 bug、调整指标算法或接受新的排序策略。

5. **修改统一评测入口**
   - 更新本文档的运行方式。
   - 确保 `scripts/run_evaluation.py --suite benchmark` 仍可使用，或说明替代命令。

## 7. 统一评测入口与 baseline 模式

Phase 2 已将 memory recall baseline comparison 接入统一评测入口：

```bash
python scripts/run_evaluation.py baseline
```

该模式等价于运行：

```bash
python benchmark/memory_recall_benchmark.py --compare-baseline benchmark/baselines/memory_recall_baseline.json
```

`baseline` 模式用于把当前 memory recall benchmark 结果与已登记的 `benchmark/baselines/memory_recall_baseline.json` 做回归对比，并刷新/生成对比报告。`all` 模式现在会依次运行 fast、memory 与 baseline 检查：

```bash
python scripts/run_evaluation.py all
```

如果只想确认命令计划而不执行，可使用：

```bash
python scripts/run_evaluation.py baseline --dry-run
```

维护要求：

- 修改 benchmark case、评分指标或召回排序逻辑后，需要运行 `python scripts/run_evaluation.py baseline` 检查相对基线变化。
- 如果质量变化符合预期，应同步更新 baseline artifact 与本文档中的指标说明、当前数值或质量判读。
- 如果 baseline 对比暴露退化，应优先分析 case 级别差异，再决定修复召回逻辑还是更新基线。
- 旧的 `scripts/run_evaluation.py --suite benchmark` 形式不是当前入口；当前统一入口使用位置参数模式，例如 `python scripts/run_evaluation.py memory` 或 `python scripts/run_evaluation.py baseline`。

## 8. 建议的质量门禁

当前建议把以下条件作为 memory recall benchmark 的最低质量门禁：

| 指标 | 建议门禁 |
| --- | ---: |
| `hit_at_1` | >= 0.95 |
| `hit_at_3` | >= 0.98 |
| `hit_at_5` | >= 1.00 |
| `mrr` | >= 0.95 |
| `forbidden_violation_rate` | == 0.00 |
| `expected_file_hit_rate` | >= 0.95 |
| `expected_kind_hit_rate` | >= 0.95 |

当前结果全部满足上述门禁。若后续用例显著增加，可根据 case 难度重新讨论门禁，但不能在未解释原因的情况下放宽门槛。

## 9. 面向后续完善的方向

当前 benchmark 已经可以防止明显回归，但还可以继续增强：

1. 增加更强负例：相似标题、相似文件、相似错误但不同修复方案。
2. 增加跨项目污染 case：确保其他项目记忆不会压过当前项目记忆。
3. 增加时间衰减 case：验证高质量旧决策不会被低质量近期 summary 淹没。
4. 增加诊断维度：区分失败来自 BM25、vector、metadata、query rewrite、rerank 还是索引数据质量。
5. 增加性能指标：记录 benchmark 耗时、索引加载耗时、单 query 平均耗时。
6. 增加 CI 门禁：在关键 PR 或提交前自动运行 benchmark 回归测试。

---

最后更新依据：当前 `benchmark/baselines/memory_recall_baseline.json` 中的 26 个 memory recall benchmark case 与对应满分 baseline 结果。
