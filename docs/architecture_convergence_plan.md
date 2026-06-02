# mini-claude-code-cli 架构收敛改进计划

> 目标：在不牺牲当前 CLI Agent 能力的前提下，收敛核心边界、降低模块耦合、稳定上下文压缩与长期记忆链路，让项目从“功能持续叠加”进入“可维护、可验证、可扩展”的架构阶段。

## 1. 当前判断

项目已经具备一个可用的 CLI 软件工程代理雏形：

- `main.py` 负责 CLI 入口与会话启动。
- `core/engine.py` 承载 Agent 主循环、模型调用、工具调用、计划状态、上下文拼装与错误恢复等核心流程。
- `tools/` 提供文件、Bash、Git、测试、记忆、计划等工具能力。
- `memory/` 承载短期/长期记忆、索引、召回、压缩与生命周期管理。
- `tests/` 已覆盖较多记忆、压缩、工具与上下文预算行为。
- `docs/` 已开始沉淀上下文压缩、read_file 防空转、长期记忆质量控制等局部改进方案。

主要问题不是“功能不足”，而是核心职责逐渐集中到少数模块，导致新增能力、修复 bug、压缩上下文、工具协议适配和状态恢复之间相互影响。

## 2. 架构收敛目标

### 2.1 短期目标

1. 明确 Agent 运行时主链路，把“对话循环、工具调用、上下文构建、记忆注入、计划管理、错误恢复”拆成可测试组件。
2. 将工具协议、Provider 消息协议、内部事件模型分层，减少 OpenAI/Claude strict tool-call 约束泄漏到业务逻辑。
3. 固化上下文压缩与长期记忆的数据契约，避免压缩结果破坏 tool call 配对或引入重复/低质记忆。
4. 让每次架构调整都有最小测试闭环，防止核心启动链路再次出现 SyntaxError、属性缺失、消息格式不合法等回归。

### 2.2 中期目标

1. 形成稳定的 `AgentRuntime` + `ContextPipeline` + `ToolRuntime` + `MemoryRuntime` 分层。
2. 让计划系统、记忆系统、工具系统都通过统一事件或状态快照交互，而不是彼此直接读写内部字段。
3. 建立架构边界测试：模块导入、协议转换、上下文预算、压缩安全、工具调用配对、会话恢复。
4. 将文档中的改进计划变成可分阶段执行的迁移路线，而不是一次性大重构。

## 3. 建议的目标架构

```text
main.py
  └── core/
      ├── runtime.py              # AgentRuntime：主循环编排，不放具体策略细节
      ├── engine.py               # 兼容层/旧入口，逐步瘦身
      ├── conversation.py         # 会话消息、turn、provider 消息转换
      ├── context_pipeline.py     # 上下文组装、预算、压缩、记忆注入
      ├── tool_runtime.py         # tool call 执行、结果配对、错误包装
      ├── plan_runtime.py         # plan 状态机、任务完成记录、恢复
      └── error_recovery.py       # 可恢复错误分类与自愈策略

memory/
  ├── manager.py                  # 对外门面
  ├── long_term/                  # 长期记忆、索引、召回、质量控制
  ├── compression/                # 压缩策略、摘要、晋升规则
  └── models.py                   # 统一数据模型

tools/
  ├── base.py                     # 工具协议与 schema
  ├── registry.py                 # 工具注册与发现
  └── *_tool.py                   # 具体工具实现

tests/
  ├── test_runtime_*.py
  ├── test_context_*.py
  ├── test_tool_runtime_*.py
  ├── test_memory_*.py
  └── test_startup_smoke.py
```

核心原则：

- `core/runtime.py` 只负责编排，不直接实现压缩、召回、工具细节。
- `context_pipeline.py` 输出 Provider 可接受的消息列表，必须保证 tool-call 配对完整。
- `tool_runtime.py` 负责工具调用生命周期，所有工具错误都转成结构化结果。
- `memory/manager.py` 是记忆系统对外唯一稳定入口，内部索引文件属于运行时产物，不应污染 Git。
- `plan_runtime.py` 负责计划状态与任务记录，避免计划字段散落在 AgentEngine 对象上。

## 4. 当前架构发散点

### 4.1 AgentEngine 职责过宽

`core/engine.py` 容易同时承担：

- CLI 会话状态。
- LLM 请求和响应处理。
- 工具调用分发。
- 上下文压缩与长期记忆注入。
- plan 创建、恢复、完成标记。
- 错误处理与自愈。

这会带来两个问题：

1. 任一子系统改动都可能影响启动和主循环。
2. 很难对单一职责写低成本测试，只能依赖较重的集成测试。

### 4.2 上下文压缩与消息协议耦合过深

历史问题已经显示：压缩后的会话状态如果包含半截 assistant tool call，可能违反 provider strict tool-call 协议。因此压缩系统需要从“文本摘要器”升级成“协议感知的上下文构建管线”。

### 4.3 长期记忆质量控制需要边界化

长期记忆已经有 BM25/vector/metadata 召回能力，但如果缺少统一的晋升、降噪、去重和索引生命周期约束，容易导致：

- 重复召回历史噪音。
- 把测试输出、半截 traceback、临时文件状态过度写入长期记忆。
- 运行时索引文件和项目源码边界不清。

### 4.4 工具层缺少统一运行时语义

各工具本身能力较强，但工具调用链需要统一回答这些问题：

- schema 校验失败怎么包装？
- 工具异常是否可恢复？
- tool call id 与 tool result 如何严格配对？
- 并行工具是否允许操作同一文件？
- 文件读取/编辑防空转策略由工具自己负责，还是 runtime 统一治理？

### 4.5 Plan 状态和会话压缩恢复耦合

计划管理是 Agent 行为稳定性的核心，但它不应作为零散字段挂在主 Engine 上。建议将它抽成独立状态机，支持：

- 创建计划。
- 恢复未完成步骤。
- 标记完成。
- 归档已完成任务。
- 压缩时只保留可恢复的最小状态。

## 5. 分阶段改进路线

## Phase 0：建立架构护栏（优先级最高）

目标：在重构前先防止继续发散。

行动：

1. 新增 `tests/test_startup_smoke.py`：验证 `main.py`、`core.engine.AgentEngine` 可导入，核心依赖无语法错误。
2. 新增 provider message validator 测试集合：确保压缩后消息不包含未配对 tool call。
3. 新增工具协议测试：每个工具至少覆盖 schema、成功结果、异常结果。
4. 固化 Git 忽略策略：运行时索引、缓存、session 临时文件不得进入版本控制。
5. 为 `core/engine.py` 增加“禁止继续膨胀”的约束：新功能优先进入独立模块，通过 Engine 编排。

交付物：

- 启动冒烟测试。
- 消息协议测试。
- 工具协议测试基线。
- 一份模块边界说明文档。

## Phase 1：抽出 ToolRuntime

目标：先把高风险的工具调用生命周期从 AgentEngine 中拿出来。

行动：

1. 新建 `core/tool_runtime.py`。
2. 定义 `ToolCallRequest`、`ToolCallResult`、`ToolExecutionError` 等内部模型。
3. 将工具查找、参数校验、执行、异常包装、结果序列化集中到 ToolRuntime。
4. AgentEngine 只调用 `tool_runtime.execute(call)`，不直接处理具体工具异常。
5. 增加测试：
   - 正常工具调用返回结构化结果。
   - 工具异常被包装成可注入 provider 的 tool result。
   - 多个 tool call 的 id 与 result 顺序/配对正确。

收益：

- 降低 provider strict tool-call 错误概率。
- 让工具层错误恢复独立可测。
- 为后续并行工具和权限控制打基础。

## Phase 2：抽出 ContextPipeline

目标：将上下文构建、预算控制、记忆注入、压缩安全统一为一个管线。

行动：

1. 新建 `core/context_pipeline.py`。
2. 将输入统一为：当前会话消息、系统提示、工具 schema、长期记忆候选、plan 状态。
3. 将输出统一为：provider-ready messages + context diagnostics。
4. 在管线内部划分阶段：
   - 原始消息清洗。
   - tool-call 配对校验。
   - 预算估算。
   - 长期记忆注入。
   - 压缩策略选择。
   - 最终 provider 消息校验。
5. 增加测试：
   - 超预算时触发压缩。
   - 压缩不破坏 tool-call 配对。
   - 长期记忆注入不挤掉当前用户任务和未完成 plan。
   - 召回噪音过高时降权或丢弃。

收益：

- 上下文相关问题可集中定位。
- 压缩系统从“事后补丁”变成“构建管线中的受控阶段”。
- 便于将来支持多 provider。

## Phase 3：收敛 MemoryRuntime/MemoryManager

目标：让记忆系统成为稳定服务，而不是散落在上下文和压缩逻辑中的辅助函数。

行动：

1. 明确 `memory/manager.py` 对外 API：`save`、`recall`、`file_history`、`error_history`、`promote_summary`、`cleanup`。
2. 将 BM25/vector/metadata 召回结果统一成 `MemoryCandidate`。
3. 引入质量门控：去重、过期、重要性、来源、测试噪音识别。
4. 明确索引生命周期：源码只保存逻辑，运行时索引文件由 `.gitignore` 管理。
5. 增加测试：
   - 相似任务不重复晋升。
   - traceback 查询能召回真实修复经验。
   - 噪音测试输出不会压过高价值架构/bug 记忆。

收益：

- 降低长期记忆污染。
- 提升跨会话恢复质量。
- 支撑更可靠的“继续执行”语义。

## Phase 4：抽出 PlanRuntime

目标：把计划系统做成明确状态机，减少 AgentEngine 属性漂移问题。

行动：

1. 新建 `core/plan_runtime.py`。
2. 定义 `PlanState`、`PlanStep`、`PlanArchiveRecord`。
3. 所有计划变更都通过状态机方法完成：`create_plan`、`mark_done`、`next_pending`、`archive_if_completed`。
4. 压缩会话时只写入最小可恢复状态：目标、步骤、完成状态、下一步。
5. 增加测试：
   - 中断后恢复下一个未完成步骤。
   - 已完成任务不会重复创建 plan。
   - mark_task_done 后状态立即持久化。

收益：

- 解决计划字段缺失、恢复混乱、重复创建计划的问题。
- 让“继续”指令稳定可预测。

## Phase 5：Engine 瘦身与兼容迁移

目标：保留现有外部行为，逐步让 `core/engine.py` 退化为兼容层/编排层。

行动：

1. 在不改 CLI 使用方式的前提下，引入 `AgentRuntime`。
2. `AgentEngine` 内部委托给 `AgentRuntime`，保留旧方法名兼容测试和调用方。
3. 每迁移一类职责，就减少 Engine 中对应代码。
4. 建立导入边界测试，防止 runtime 反向依赖 tools 具体实现或 memory 内部索引细节。
5. 最终形成：
   - `main.py` 创建 runtime。
   - runtime 编排上下文、工具、记忆、计划。
   - 各子系统独立测试。

收益：

- 后续新增能力不会继续堆到 Engine。
- 主循环变简单，错误定位成本下降。

## 6. 推荐执行顺序

建议不要一次性大改，而是按风险从低到高迁移：

1. **先补护栏测试**：启动、provider 消息、tool result 配对。
2. **再抽 ToolRuntime**：边界清晰，收益直接。
3. **再抽 ContextPipeline**：解决最核心的上下文压缩风险。
4. **再收敛 MemoryManager**：减少长期记忆噪音和索引污染。
5. **再抽 PlanRuntime**：稳定任务恢复和压缩态。
6. **最后瘦身 Engine**：避免大爆炸式重构。

每个阶段都应满足：

- 有文档变更。
- 有测试变更。
- 有小步 commit。
- 不破坏 `python main.py --session test` 或等价启动链路。

## 7. 验收标准

### 7.1 架构验收

- AgentEngine 不再直接包含具体工具异常处理细节。
- 上下文构建只有一个主入口。
- 长期记忆召回和压缩晋升只有一个对外门面。
- Plan 状态由状态机维护，而不是散落字段。
- Provider 消息最终输出前必须经过 validator。

### 7.2 测试验收

最低测试集合：

```text
tests/test_startup_smoke.py
tests/test_tool_runtime.py
tests/test_context_pipeline.py
tests/test_provider_message_validator.py
tests/test_plan_runtime.py
tests/test_memory_recall_quality.py
```

验收命令建议：

```bash
pytest tests/test_startup_smoke.py tests/test_tool_runtime.py tests/test_context_pipeline.py tests/test_provider_message_validator.py tests/test_plan_runtime.py tests/test_memory_recall_quality.py
```

如果阶段涉及 `core/` 或 `tools/` 逻辑改动，必须运行对应单测；如果涉及消息协议或压缩，必须运行 provider message validator 相关测试。

## 8. 风险与控制

| 风险 | 表现 | 控制方式 |
| --- | --- | --- |
| 大重构导致启动失败 | main.py 无法导入或运行 | 先加 startup smoke test，每步运行 |
| 压缩破坏 tool-call 协议 | provider 报 tool_calls/tool result 不配对 | ContextPipeline 最终 validator |
| 长期记忆污染 | 重复、低质、过期内容反复注入 | MemoryManager 质量门控 |
| Plan 恢复混乱 | “继续”执行错步骤或重复建计划 | PlanRuntime 状态机 + 恢复测试 |
| 工具异常泄漏 | 工具异常中断主循环 | ToolRuntime 统一异常包装 |
| 模块循环依赖 | 新分层后 import 混乱 | 导入边界测试 + 依赖方向约束 |

## 9. 近期最小落地建议

如果只做一轮架构收敛，建议范围控制在以下 5 件事：

1. 新增启动冒烟测试，锁住项目可启动性。
2. 新增/强化 provider message validator，锁住 tool-call 配对安全。
3. 抽出 `core/tool_runtime.py`，把工具调用生命周期集中起来。
4. 抽出 `core/context_pipeline.py` 的最小版本，先做消息清洗、预算诊断和最终校验。
5. 在 `docs/` 维护模块边界和迁移进度，后续所有核心改动都引用该边界。

这 5 件事完成后，项目会从“能跑的 Agent”进一步变成“可持续演进的 Agent Runtime”。

## 10. 建议的首个开发任务拆分

首个可执行任务建议为：

> 建立架构护栏测试，并抽出最小 ToolRuntime。

步骤：

1. 创建 `tests/test_startup_smoke.py`，验证核心模块导入。
2. 创建 `core/tool_runtime.py`，先包装现有工具 registry 调用，不改变外部行为。
3. 创建 `tests/test_tool_runtime.py`，覆盖成功、异常、未知工具、tool_call_id 保留。
4. 修改 `core/engine.py` 中工具调用路径，委托 ToolRuntime。
5. 运行相关测试和现有工具测试。
6. 文档记录迁移完成范围与后续 ContextPipeline 计划。

这样切入点最稳，风险低，同时能立刻降低 `core/engine.py` 的复杂度。
