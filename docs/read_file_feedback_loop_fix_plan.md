# read_file 反馈回路问题诊断与修复方案

## 背景

近期在使用本项目作为 code agent 展开较长任务时，出现过一种典型失效模式：Agent 在已有 Plan 的情况下，持续调用 `read_file` 阅读文件，但迟迟不产出分析、方案或代码修改；重开会话后又能继续推进。

结合本轮代码阅读与 Codex 诊断，可以判断该问题不是单个 `read_file` 工具实现错误，而是多个机制叠加形成的“读文件反馈回路”：

1. 主循环允许连续多轮只执行工具而不要求中间产出。
2. `read_file` 默认可返回较大原文内容，容易吞噬上下文预算。
3. 压缩会保留摘要和最近消息，但可能丢失“已读过哪些文件/为什么读/下一步要做什么”的可执行状态。
4. 长期记忆会把工具结果、压缩摘要、失败经验等沉淀并在后续任务召回，可能把旧的 `read_file` 轨迹再次注入 prompt。
5. 提示词与开发者工作流强调“需要读文件就读”“修改前查历史”“失败后查历史”，但缺少足够强的工具循环刹车与产出约束。

本文档只给出诊断和修复方案，不修改业务代码。

## 关键相关模块

### 1. Agent 主循环：`core/engine.py`

当前主循环大致行为是：

- 向模型发送上下文。
- 如果模型返回 tool calls，则执行工具。
- 将工具结果写入上下文。
- 保存 session。
- 继续下一轮，直到模型返回最终文本或达到 `max_steps`。

该结构本身是常见 agent loop，但当前缺少对“连续只读文件、没有任务推进”的显式检测。例如：

- 连续 N 轮都只调用 `read_file` 时，没有强制要求模型总结发现并推进 Plan。
- 多次读取同一个文件/相同行范围时，没有自动拦截或降级为提醒。
- 工具结果被加入上下文后，下一轮模型仍可能认为“信息还不够”，继续读文件。

主循环中已有一些安全机制，例如工具执行异常时清理 OpenAI tool pair、`mark_task_done` 后自动快照、编辑失败回滚等，但这些主要处理一致性与代码安全，不处理“只读不产出”的行为退化。

### 2. 上下文与压缩：`core/context.py`、`core/compression_engine.py`

`ContextManager.compress()` 会在消息长度超过阈值或工作记忆达到上限时触发压缩。压缩成功后：

- 使用 `result.compressed_messages + appended_messages` 替换上下文。
- 重建 working memory。
- 将结构化摘要写入 episodic/session summary。
- `task_status` 会参考 Plan 状态做覆盖，避免 LLM 错判完成状态。

这一机制解决了长上下文成本问题，但对 read loop 有两个副作用：

1. 大段工具输出很容易触发压缩。
2. 压缩摘要如果没有稳定记录“已经读过什么、结论是什么、下一步是什么”，模型会在压缩后重新探索。

特别需要注意：压缩不能只保存自然语言总结，还应保存可执行的任务状态，例如文件阅读清单、关键结论、待验证假设、下一步动作。

### 3. 记忆系统：`core/memory_manager.py`、`core/memory_retrieval.py`、`core/memory_context_builder.py`

当前记忆系统具备：

- WorkingMemory
- EpisodicMemory
- LongTermMemory
- Hybrid Recall
- 主动记忆注入
- 文件编辑前历史召回
- 工具失败后错误历史召回
- prompt submit / tool result observation 晋升

这些能力能提升跨会话连续性，但在 read loop 场景中也可能放大问题：

- 如果长期记忆中沉淀了大量低质量工具输出或“工具执行成功: read_file”，召回结果会把模型重新拉回阅读动作。
- 召回内容中如果包含旧会话的半截执行轨迹，而不是结论型知识，会污染当前任务。
- 对简单“继续”已跳过主动记忆注入，但 Plan 恢复任务本身通常不属于简单交互，仍可能注入大量历史。

因此，需要对记忆写入和召回都增加质量门槛。

### 4. 文件工具：`tools/file_tool.py`

`read_file` 支持按行范围读取，也支持 `raw_mode`。这对工程任务很有用，但如果模型不主动控制读取范围，单次工具输出可能很大，导致：

- 当前 turn 上下文被工具结果占据。
- 很快触发压缩。
- 压缩摘要又不足以替代原文阅读状态。

因此，工具层也应承担一部分“防重复”和“鼓励范围化阅读”的职责。

### 5. 提示词与计划机制：`core/prompts.py`、PlanManager、系统提示

当前提示词和系统规范中强调：

- 多步骤任务必须使用 Plan。
- 完成步骤后调用 `mark_task_done`。
- 需要读文件时使用工具。
- 修改前查询文件历史。
- 出错后查询错误历史。

这些规则提升了执行可靠性，但对 read loop 来说缺少几条反向约束：

- 读取若干文件后必须产出阶段性结论。
- 不能连续读取无关文件。
- 不能重复读取同一路径/同一范围，除非说明原因。
- 当前 Plan 有未完成步骤时，应优先推进下一个步骤，而不是无限探索。

## 根因判断

该问题更像是“闭环控制缺失”，而不是某个模块的单点 bug。

可以概括为：

> 工具输出扩大上下文 → 压缩丢失精确阅读轨迹 → 记忆召回注入旧阅读轨迹 → prompt 鼓励继续读取 → 主循环无连续读取刹车 → 再次读取。

在这个链路中，任何一个点都可能触发或放大循环：

- 工具输出过大。
- 压缩摘要不可执行。
- 记忆质量控制不足。
- prompt 缺少 stop rule。
- agent loop 缺少进展检测。

## 修复目标

建议把修复目标定义为：

1. 保留必要的文件阅读能力。
2. 防止重复读取和无产出读取。
3. 让压缩后仍能知道已读内容和下一步。
4. 让长期记忆更多保存结论和决策，少保存原始工具轨迹。
5. 当出现疑似循环时，自动打断并要求模型总结/决策/推进 Plan。

## 建议方案 A：Agent Loop 增加“工具循环刹车”

优先级：高。

在 `AgentEngine.execute_query()` 的循环中增加轻量状态跟踪：

- 记录最近 K 个 tool call。
- 统计连续 tool-only 轮数。
- 统计连续 `read_file` 次数。
- 统计重复读取的 `(path, start_line, end_line, raw_mode)`。

建议策略：

1. 连续 3 轮只有 `read_file`，无 assistant 文本产出：向上下文追加系统/用户提醒，要求模型先总结已读内容并给出下一步，而不是继续读。
2. 连续 5 次 `read_file`：强制进入“反思 turn”，本轮不再执行新工具，要求输出阶段性结论。
3. 重复读取同一文件同一范围：返回短提示，例如“该范围刚刚读过，请基于已有内容推进；如必须重读，请说明原因并读取更小范围”。
4. 如果当前有未完成 Plan：提醒模型必须围绕下一个未完成 task 产出或执行相关工具。

伪代码示意：

```python
if tool_name == "read_file":
    key = (path, start_line, end_line, raw_mode)
    read_counts[key] += 1
    consecutive_read_file_calls += 1

if consecutive_read_file_calls >= READ_FILE_SOFT_LIMIT:
    context.add_message({
        "role": "user",
        "content": "你已经连续多次读取文件。请停止继续读取，先总结已读结论、未解决问题和下一步，并推进当前 Plan。"
    })
    continue
```

实现时要注意 OpenAI tool pair 完整性：提醒消息必须在 assistant tool_calls 对应 tool responses 之后追加，不能插入 tool call 和 tool response 中间。

## 建议方案 B：`read_file` 工具增加重复读取与大输出保护

优先级：高。

在工具层增加保护比完全依赖模型更稳定。

可选改动：

1. 默认限制最大返回字符数或行数。
2. 当未指定范围且文件较大时，只返回文件头部、结构提示和建议读取范围。
3. 对相同路径/范围的短期重复读取做提示。
4. 对 `raw_mode=false` 的装饰输出控制长度，避免额外膨胀。
5. 返回结果中附带简短元信息：路径、行范围、总行数、是否截断。

建议返回格式：

```text
文件: core/engine.py
范围: 240-520 / 共 620 行
状态: 已截断，建议继续读取 521-620 或使用 search_code 定位关键词

<内容>
```

如果担心改变现有工具行为，可以先只在超大输出或重复读取时启用。

## 建议方案 C：压缩摘要加入“阅读状态 Ledger”

优先级：高。

压缩 prompt 和 `SessionSummary` 结构中应加入明确字段：

- `files_read`: 已阅读文件与范围。
- `facts_learned`: 从阅读中得到的事实。
- `open_questions`: 未解决问题。
- `next_action`: 压缩后恢复时应执行的下一步。
- `avoid_repeating`: 不应重复执行的工具/读取范围。

压缩摘要示例：

```json
{
  "task_goal": "定位 read_file 反馈回路",
  "task_status": "in_progress",
  "files_read": [
    {"path": "core/engine.py", "ranges": ["240-520"], "reason": "检查工具主循环"},
    {"path": "core/context.py", "ranges": ["200-520"], "reason": "检查压缩替换逻辑"}
  ],
  "facts_learned": [
    "工具结果会在执行后加入上下文",
    "压缩后会重建 working memory",
    "Plan 未完成时 task_status 会被覆盖为 in_progress"
  ],
  "next_action": "编写 docs/read_file_feedback_loop_fix_plan.md",
  "avoid_repeating": [
    "不要再次完整读取 core/engine.py 240-520，除非需要核对具体行"
  ]
}
```

这样即使发生压缩，恢复后的 agent 也不需要重新阅读相同内容。

## 建议方案 D：记忆写入质量门控

优先级：中高。

建议对工具 observation 晋升长期记忆增加过滤：

1. 默认不要把成功的 `read_file` 原始输出晋升为长期 MemoryItem。
2. 只保存从 read_file 中提炼出的结论，而不是完整内容。
3. 对标题为“工具执行成功: read_file”或内容主要是文件原文的记忆降权或不召回。
4. 对 `mark_task_done`、`list_all_symbols` 等工具结果也避免无脑晋升。
5. 长期记忆中保留：架构决策、bug 修复经验、测试失败原因、用户偏好、任务完成摘要。

可采用规则：

```python
if observation.event_type == POST_TOOL_USE and observation.tool_name == "read_file":
    promote = False
```

或者只在满足以下条件时晋升：

- 用户明确要求保存。
- 工具结果被后续 assistant 总结为结论。
- 与文件修改/bug 修复直接相关。

## 建议方案 E：记忆召回降噪与预算控制

优先级：中。

当前 `build_prompt_memory_context()` 会进行 hybrid recall 并构建 prompt 记忆上下文。建议增加：

1. 对低质量工具轨迹类记忆降权。
2. 对当前任务高度相似但状态为 completed 的旧任务，只注入最终结论，不注入执行过程。
3. 对 `read_file`、`工具执行成功`、原始文件内容类记忆设置黑名单或低权重。
4. 对“继续”且已有 Plan 的场景，优先注入当前 Plan 和压缩 ledger，而不是广泛召回长期记忆。
5. 对召回结果做多样性约束，避免 top_k 都来自同一旧会话/同一工具。

## 建议方案 F：提示词补充反循环规则

优先级：中。

在系统提示或 developer prompt 中增加明确约束：

```text
当你连续读取 2 个以上文件后，必须先用简短文字总结已获得的信息，并判断是否足以推进当前 Plan。
禁止重复读取同一文件同一范围；如必须重复读取，必须说明新的读取目的。
当前 Plan 有未完成步骤时，优先完成下一个未完成步骤，不要进行无边界探索。
如果你发现自己还想继续 read_file，请先列出：已读文件、缺口、下一次读取的必要性。
```

这类规则不能单独解决问题，但配合 loop guard 和工具保护会更有效。

## 建议方案 G：Plan 状态和执行恢复强化

优先级：中。

当前系统提示已经包含 Plan 恢复规则，但可以进一步让运行时上下文显式注入：

- 当前目标。
- 已完成步骤。
- 下一个未完成步骤。
- 最近已读文件摘要。
- 强制要求本轮围绕下一个步骤行动。

例如在每轮模型调用前，如果存在未完成 Plan，可注入短上下文：

```text
当前 Plan 下一个步骤是：编写修复方案文档到 docs 目录。
你已经完成了代码阅读，不要继续阅读文件，除非必须核对文档路径。
本轮应产出文档或调用写文件工具。
```

这能显著降低恢复时重新探索的概率。

## 分阶段落地建议

### Phase 1：最小闭环刹车

目标：最快降低死循环概率。

- 在 agent loop 增加连续 `read_file` 计数。
- 达到阈值后追加提醒，要求总结并推进。
- 对重复读取同一范围给出提醒。
- 在 prompt 中增加反循环规则。

验证方式：

- 构造一个 mock LLM 连续返回 `read_file`，确认第 N 次后被提醒。
- 确认 OpenAI tool pair 仍完整。
- 确认正常读取 1-2 个文件不受影响。

### Phase 2：压缩可恢复性

目标：压缩后不重复探索。

- 修改压缩 prompt，要求输出 files_read / facts_learned / next_action / avoid_repeating。
- `SessionSummary` 或 metadata 中保存这些字段。
- 恢复上下文时优先注入这部分 ledger。

验证方式：

- 构造包含多次 read_file 的消息历史，触发压缩。
- 检查摘要包含已读文件与下一步。
- 压缩后继续任务时，模型不再重复读取相同范围。

### Phase 3：记忆质量治理

目标：长期降低旧工具轨迹污染。

- 禁止成功 `read_file` 原始结果直接晋升长期记忆。
- 对旧的低质量 read_file/tool success 记忆做审计和降权/清理。
- 召回时过滤工具轨迹类记忆。

验证方式：

- 使用 `memory_recall` 查询 read_file 相关任务，确认召回的是结论型记忆，而不是大段工具输出。
- 检查 token budget 中低质量记忆占比下降。

### Phase 4：工具输出预算优化

目标：降低上下文膨胀。

- `read_file` 默认范围化。
- 大文件自动截断。
- 输出包含总行数、范围、截断提示。
- 鼓励 `search_code` / `find_symbol_definition` 先定位再读。

验证方式：

- 读取大文件时输出不会超过预算。
- 指定范围时仍能完整返回该范围。
- 旧测试兼容或明确更新预期。

## 测试建议

建议补充以下测试：

1. `test_agent_loop_read_file_guard.py`
   - mock LLM 连续请求 read_file。
   - 验证达到阈值后系统注入反思提示。
   - 验证不会破坏 tool call/tool response 配对。

2. `test_read_file_dedup.py`
   - 重复读取相同路径和范围。
   - 验证工具或 engine 返回重复提醒。

3. `test_compression_read_ledger.py`
   - 构造含多个 read_file 的上下文。
   - 触发压缩。
   - 验证摘要中包含 files_read、next_action、avoid_repeating。

4. `test_memory_no_promote_read_file_raw_output.py`
   - 执行 read_file 成功 observation。
   - 验证不会晋升为长期 MemoryItem，或被标记为低优先级。

5. `test_memory_recall_filters_tool_traces.py`
   - 构造工具轨迹类和结论类记忆。
   - 验证召回优先结论类记忆。

## 风险与注意事项

1. 不能过度限制 `read_file`，否则会影响正常代码理解。
2. 反循环提醒必须放在 tool responses 之后，避免 OpenAI 兼容接口报 tool_calls 不匹配。
3. 压缩摘要字段扩展要兼容旧 SessionSummary。
4. 记忆清理要谨慎，最好先降权和过滤，再考虑删除。
5. 对“只读分析任务”不能强制要求修改代码，但应要求阶段性分析产出。

## 推荐优先级结论

最推荐先做三件事：

1. **Agent loop 连续 read_file guard**：最快阻断死循环。
2. **压缩摘要加入阅读 ledger**：解决重开/压缩后重复探索。
3. **禁止 read_file 原始工具输出晋升长期记忆**：减少跨会话污染。

这三项组合后，基本可以切断主要反馈回路：

> 重复读取被 guard 打断；压缩后有状态可恢复；长期记忆不再反复注入旧阅读轨迹。
