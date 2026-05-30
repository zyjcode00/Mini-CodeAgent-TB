# Mini Claude Code CLI 项目简历素材与多版本模板

> 适用项目：`D:\LLM\mini-claude-code-cli`
> 项目定位：面向软件工程任务的 AI Coding Agent / CLI 工程代理，支持异步工具调用、显式规划、TDD 自愈、长期记忆、上下文压缩、符号检索与 Git 保护机制。

---

## 1. 项目一句话概括

Mini Claude Code CLI 是一个类 Claude Code 的本地命令行 AI 工程代理，围绕“规划 → 工具执行 → 测试验证 → 错误自愈 → 记忆沉淀”的闭环工作流，构建了具备异步并发工具调用、三层记忆系统、长期记忆 Hybrid Recall、上下文压缩、AST 符号导航和 Git 影子分支保护能力的 Agentic Coding 系统。

---

## 2. 推荐简历项目命名

可根据目标岗位选择不同名称：

1. **Mini Claude Code CLI：面向软件工程任务的 AI Coding Agent**
2. **基于 ReAct + Tool Calling 的本地智能编程代理系统**
3. **具备长期记忆与自愈能力的 AI 工程 Agent 平台**
4. **面向代码修改与测试闭环的 Agentic CLI 开发工具**
5. **类 Claude Code 的多工具协同代码代理系统**

---

## 3. 技术栈关键词

### Agent / LLM 工程

- ReAct Agent
- Tool Calling / Function Calling
- OpenAI-compatible API
- System Prompt 动态注入
- 多工具编排
- 异步并发工具执行
- 上下文预算管理
- Agent 自愈闭环

### Python 工程

- Python 3.9+
- asyncio
- dataclass / pydantic 风格结构化模型
- CLI / REPL
- pytest
- JSON 持久化
- AST 解析
- 正则搜索

### 记忆与检索

- 三层记忆架构：工作记忆、情景记忆、长期记忆
- BM25 检索
- 向量索引 / Hash Embedding 降级
- Hybrid Recall
- RRF 融合排序
- 文件历史召回
- 错误历史召回
- 记忆压缩与长期晋升

### 软件工程能力

- 测试驱动开发 TDD
- Traceback 驱动修复
- Git 快照 / 回滚
- 影子分支保护
- 代码符号索引
- 工具抽象与插件化设计
- 上下文压缩与 provider message validation

---

## 4. 项目职责与亮点拆解

### 4.1 Agent 执行引擎

- 设计并实现异步 Agent Engine，支持 LLM 在单轮响应中发起多个工具调用，并通过 `asyncio.gather` 并行执行 Bash、File、Search、Symbol、Pytest、Git、Memory 等工具。
- 构建类 ReAct 的循环决策流程，将“模型思考、工具执行、结果回传、继续推理”封装为稳定的 CLI 交互体验。
- 接入 OpenAI-compatible API，支持 system prompt、历史消息、工具 schema 和 tool result 的统一消息编排。

### 4.2 显式规划系统

- 实现 PlanManager，将复杂用户任务拆解为结构化计划清单，并在 system prompt 中持续注入当前计划状态。
- 支持任务步骤的创建、进度更新、完成归档和中断恢复，降低长任务中 Agent 遗忘目标或重复执行的概率。
- 将计划状态与工具执行强绑定，确保每完成一个阶段都可被追踪和恢复。

### 4.3 工具系统与工程执行能力

- 抽象统一 Tool 基类与 schema 规范，封装文件读写、Shell 执行、Git 操作、代码搜索、AST 符号定位、pytest 执行、记忆检索等工具。
- 针对 Windows 环境实现 Bash 编码自愈和文件换行符归一化，降低本地 CLI 在中文路径、CMD 编码、CRLF/LF 差异下的失败率。
- 实现 `read_file` 行范围读取、`edit_file` 精准替换、`write_full_file` 全量写入等安全文件编辑能力。

### 4.4 TDD 自愈闭环

- 将代码修改与 pytest 测试验证绑定：Agent 修改核心逻辑后必须运行对应测试，失败时根据 Traceback 自动定位代码并再次修复。
- 封装 pytest 工具，结构化捕获 STDOUT、STDERR、失败用例和 Traceback，为自动修复提供可解析反馈。
- 形成“生成测试 → 修改代码 → 运行测试 → 读取错误 → 修复 Bug → 重新验证”的确定性工程闭环。

### 4.5 三层记忆与长期记忆系统

- 设计工作记忆、情景记忆、长期记忆三层架构：短期对话保留最近上下文，中期摘要保存任务过程，长期记忆沉淀可复用经验。
- 实现 `MemoryItem`、`RawObservation` 等结构化记忆模型，将任务完成、文件变更、错误修复、架构决策等事件保存为可检索知识。
- 构建 Hybrid Recall 检索流程，融合 BM25、关键词、时间新鲜度、重要性、来源等信号，并通过 RRF 进行排序融合。
- 提供 `memory_recall`、`memory_file_history`、`memory_error_history`、`memory_stats` 等工具接口，让 Agent 在编辑文件或修复错误前主动召回历史经验。

### 4.6 上下文压缩与预算控制

- 实现面向长对话的智能压缩引擎，支持 keyframe、semantic、hybrid、timeline 等策略，根据任务类型保留关键工程状态。
- 将代码修改、测试结果、错误 Traceback、Git 操作、用户决策等高价值节点识别为关键帧，降低上下文截断导致的任务状态丢失。
- 设计 `CompressedSessionState` 结构化压缩状态，记录任务状态、文件变更、测试状态、错误记录、关键决策和可复用经验。
- 构建 ContextAssembler，对 system、memory、compressed state、recent turns、current request 进行预算化装配，保证上下文窗口紧张时仍优先保留当前请求与关键状态。
- 处理 OpenAI-compatible tool message 的原子性，避免压缩或截断后出现 assistant.tool_calls 与 tool result 不匹配的问题。

### 4.7 代码检索与符号导航

- 基于 Python AST 构建项目级符号地图，支持按函数名/类名定位定义文件、起止行号、docstring 和代码片段。
- 实现正则搜索工具，支持上下文行展示、glob 文件过滤和跨文件影响评估，为大规模重构提供定位能力。
- 将符号导航与文件编辑工具结合，减少盲目 grep 和误改风险。

### 4.8 Git 保护与影子分支机制

- 封装 Git 状态查看、快照提交和回滚能力，为 Agent 代码修改提供物理级安全保护。
- 设计影子分支思路，将实验性修改与主分支隔离，降低自动化重构对主分支的破坏风险。
- 在连续失败或编辑错误时支持回滚到安全提交，提升 Agent 自愈过程的可靠性。

---

## 5. 简历模板一：AI Agent / LLM 应用工程师方向

### 项目名称

**Mini Claude Code CLI：面向软件工程任务的 AI Coding Agent**

### 项目描述

基于 Python 构建类 Claude Code 的本地命令行 AI 工程代理，支持 ReAct 推理、多工具调用、异步并发执行、显式任务规划、TDD 自愈、长期记忆召回和上下文压缩，可完成项目阅读、代码修改、测试运行、错误修复、Git 回滚和文档生成等软件工程任务。

### 简历写法

- 负责设计并实现 AI Coding Agent 核心执行引擎，基于 OpenAI-compatible Tool Calling 协议封装 Bash、File、Search、Symbol、Pytest、Git、Memory 等工具，实现 LLM 推理与本地工程操作的闭环联动。
- 基于 `asyncio.gather` 实现多工具并发执行能力，使模型在单轮响应中发起的多个工具调用可并行落地，减少串行工具调用带来的交互轮次和等待时间。
- 设计显式 PlanManager，将复杂任务拆解为可追踪步骤，并将计划状态动态注入 system prompt，支持任务中断恢复、步骤完成标记和长任务目标保持。
- 构建 TDD 自愈流程，封装 pytest 执行与 Traceback 捕获能力，使 Agent 能在测试失败后自动读取报错位置、修改代码并重新验证。
- 设计三层记忆架构与长期记忆工具，支持任务经验、文件历史、错误修复记录的结构化保存和 Hybrid Recall 召回，提升跨会话任务连续性。
- 实现上下文压缩与预算化装配，将代码修改、测试结果、错误记录和用户决策抽取为结构化压缩状态，降低长对话下关键信息丢失风险。

### 可突出关键词

`LLM Agent`、`Tool Calling`、`ReAct`、`asyncio`、`TDD`、`Hybrid Recall`、`Context Compression`、`AST Symbol Map`

---

## 6. 简历模板二：后端 / Python 工程方向

### 项目名称

**基于 Python 的多工具协同智能 CLI 工程代理系统**

### 项目描述

一个面向本地软件工程工作流的 Python CLI 系统，采用模块化工具架构封装 Shell、文件、搜索、符号解析、测试、Git 与记忆管理能力，并通过 Agent Engine 统一调度，支持自动化代码修改、测试验证和任务状态持久化。

### 简历写法

- 负责项目核心后端架构设计，将系统拆分为 `core/` 引擎层、`tools/` 工具层、`memory/` 持久化层、`tests/` 测试层和 `docs/` 文档层，提升模块边界清晰度与可维护性。
- 设计统一 Tool 抽象与 schema 注册机制，将 Bash、文件读写、Git、pytest、搜索、符号导航等能力封装为可扩展工具插件，降低新增工具接入成本。
- 实现 SessionManager 与 Context 管理模块，将会话历史、计划状态、压缩摘要和长期记忆以 JSON 方式持久化，支持 CLI 跨会话恢复。
- 优化 Windows 本地运行兼容性，处理 Shell 编码、中文输出、CRLF/LF 换行差异和文件精准替换问题，提高工具在真实开发环境下的稳定性。
- 使用 pytest 建立覆盖核心引擎、上下文装配、记忆检索、压缩策略、工具调用消息合法性等模块的测试体系，保障重构过程可验证。
- 封装 Git 快照和回滚工具，为自动化文件修改提供工程级安全兜底。

### 可突出关键词

`Python`、`CLI`、`asyncio`、`pytest`、`AST`、`JSON Persistence`、`Git Automation`、`Modular Tool System`

---

## 7. 简历模板三：RAG / 记忆系统 / 检索方向

### 项目名称

**面向 Code Agent 的长期记忆与 Hybrid Recall 检索系统**

### 项目描述

为 AI Coding Agent 构建长期记忆系统，将任务过程中的文件变更、Bug 修复、架构决策、用户偏好和测试反馈转化为结构化 MemoryItem，并通过关键词、BM25、向量索引、重要性和时间新鲜度等多信号融合实现跨会话召回。

### 简历写法

- 设计并实现面向 Code Agent 的三层记忆架构，包含工作记忆、情景记忆和长期记忆，实现从短期对话到长期经验沉淀的自动化链路。
- 定义 `MemoryItem`、`RawObservation` 等结构化数据模型，对任务、文件、错误、决策、测试结果等工程事件进行统一表达和持久化。
- 构建 Hybrid Recall 检索模块，融合关键词匹配、BM25 排序、向量相似度、时间新鲜度、重要性和来源权重，并使用 RRF 进行多路结果融合。
- 实现文件历史和错误历史召回工具，使 Agent 在编辑特定文件或遇到 Traceback 时可主动检索历史修复经验，降低重复踩坑概率。
- 设计 MemoryContextBuilder，对召回结果进行排序、去重、截断和 token budget 控制，避免长期记忆过量注入污染当前上下文。
- 编写记忆生命周期、索引持久化、召回质量、BM25 检索、向量索引和 RRF 融合等测试，保障记忆系统可持续演进。

### 可突出关键词

`RAG`、`Hybrid Recall`、`BM25`、`Vector Index`、`RRF`、`Memory System`、`Context Budget`、`Agent Memory`

---

## 8. 简历模板四：Agent 平台 / 工程架构方向

### 项目名称

**类 Claude Code 的 Agentic 工程自动化平台**

### 项目描述

围绕软件工程任务自动化构建的 Agentic 平台，具备规划、执行、验证、自愈、记忆和回滚能力。系统通过显式计划管理、工具层抽象、上下文压缩、长期记忆和 Git 保护机制，提高 AI Agent 在真实代码仓库中的可靠性。

### 简历写法

- 主导类 Claude Code CLI Agent 的整体架构设计，构建从用户输入、Agent Engine、工具执行、测试反馈、记忆沉淀到会话持久化的完整闭环。
- 设计显式规划协议，将任务执行拆分为多步骤状态机，支持计划创建、进度更新、中断恢复和完成归档，解决长任务执行过程中的目标漂移问题。
- 构建上下文压缩系统，对长对话进行关键帧识别和结构化摘要，保留文件变更、测试状态、错误记录和关键决策，并通过预算化装配控制上下文长度。
- 实现 provider message validation，保证 OpenAI-compatible 工具调用链中 assistant.tool_calls 与 tool result 的原子性，避免非法消息序列导致模型 API 报错。
- 设计 Git 快照、回滚和影子分支保护流程，为 Agent 自动化修改代码提供安全边界。
- 建立文档化架构沉淀，输出长期记忆系统、上下文压缩策略、影子分支系统等设计文档，提升项目可交接性和可维护性。

### 可突出关键词

`Agentic Workflow`、`State Machine`、`Context Engineering`、`Tool Orchestration`、`Message Validation`、`Git Safety`、`Architecture Design`

---

## 9. 简历模板五：测试平台 / 自动化质量保障方向

### 项目名称

**面向 AI Coding Agent 的 TDD 自愈与测试验证系统**

### 项目描述

在 AI Coding Agent 中引入测试驱动开发规范，将代码修改与 pytest 验证强绑定，并通过 Traceback 解析、文件定位、自动修复和重新测试形成确定性自愈闭环。

### 简历写法

- 负责构建 Agent 的 TDD 执行规范，规定核心逻辑修改必须伴随测试用例，并以 pytest 通过作为任务完成标准。
- 封装 pytest 工具，自动捕获测试输出、失败用例、错误栈和返回码，为 Agent 提供结构化错误反馈。
- 设计 Traceback 驱动修复流程：测试失败后自动读取报错文件和行号，分析异常原因，修改代码并重新运行测试，直到验证通过。
- 针对上下文装配、记忆索引、压缩状态、工具消息合法性、OpenAI tool pairing 等高风险模块补充测试，提升系统重构稳定性。
- 将 Git 快照与测试闭环结合，在关键阶段保存可回滚状态，降低自动化修改造成不可恢复错误的风险。

### 可突出关键词

`TDD`、`pytest`、`Traceback Analysis`、`Self-healing Agent`、`Regression Test`、`Quality Assurance`

---

## 10. 简历模板六：一段式项目经历

**Mini Claude Code CLI：AI Coding Agent 工程代理系统**
基于 Python 设计并实现类 Claude Code 的本地命令行 AI 工程代理，支持 ReAct 推理、OpenAI-compatible Tool Calling、多工具异步并发执行、显式任务规划、TDD 自愈、长期记忆召回、上下文压缩、AST 符号导航和 Git 回滚保护。项目中负责 Agent Engine、工具抽象、PlanManager、MemoryManager、ContextAssembler 和 pytest 自愈链路等核心模块开发；通过结构化计划看板解决长任务目标漂移问题，通过 Hybrid Recall 将文件历史、错误修复和架构决策沉淀为长期记忆，通过关键帧压缩和预算化上下文装配降低长对话信息丢失风险，并建立覆盖记忆检索、上下文装配、压缩状态和工具消息合法性的测试体系，提升 AI Agent 在真实代码仓库中的可靠性和可维护性。

---

## 11. 简历模板七：精简项目经历（适合简历 3-5 行）

**Mini Claude Code CLI｜AI Coding Agent / Python CLI**

- 基于 Python + OpenAI-compatible Tool Calling 实现本地 AI Coding Agent，封装 Bash、File、Search、Symbol、Pytest、Git、Memory 等工具，实现代码修改、测试验证、错误修复和文档生成闭环。
- 设计异步 Agent Engine 与显式 PlanManager，支持多工具并发执行、任务步骤追踪、中断恢复和长任务状态保持。
- 构建三层记忆与 Hybrid Recall 检索系统，将文件变更、错误修复、架构决策等沉淀为长期记忆，并支持文件/错误历史召回。
- 实现上下文压缩与预算化装配，保留关键帧、测试状态和工具调用原子性，提升长对话下 Agent 的稳定性。
- 接入 pytest 自愈流程和 Git 快照/回滚机制，形成“修改 → 测试 → 失败分析 → 修复 → 验证”的工程闭环。

---

## 12. 面试可讲的技术难点

### 难点一：如何保证 Agent 长任务不跑偏？

可回答：

- 通过 PlanManager 将任务拆成显式步骤。
- 每轮 system prompt 注入当前计划状态。
- 工具执行完成后必须更新任务状态。
- 会话中断后可从下一个未完成步骤恢复。

### 难点二：如何处理长上下文导致的信息丢失？

可回答：

- 引入上下文压缩，不是简单截断。
- 先识别 turn 元数据和关键帧，包括代码修改、测试反馈、Traceback、Git 操作、用户决策。
- 将压缩结果保存为结构化 `CompressedSessionState`。
- 使用 ContextAssembler 按预算装配 system、memory、compressed state、recent turns 和 current request。

### 难点三：长期记忆和普通 RAG 有什么区别？

可回答：

- 普通 RAG 多用于外部知识文档检索；本项目长期记忆面向 Agent 自身执行经验。
- 记忆对象包括文件变更、错误修复、架构决策、用户偏好和测试结果。
- 检索时不仅看文本相似度，还融合重要性、时间新鲜度、来源和文件/错误维度。
- 召回结果会受 token budget 控制，避免污染当前任务。

### 难点四：如何保证 Tool Calling 消息合法？

可回答：

- OpenAI-compatible API 要求 `assistant.tool_calls` 后必须跟对应的 `tool` 结果。
- 上下文压缩和截断不能破坏 tool pair。
- 项目中在 ContextAssembler 阶段进行 provider message validation，清理不完整工具链，保证工具调用原子性。

### 难点五：如何让 Agent 真正具备自愈能力？

可回答：

- 不是只让模型“猜测修复”，而是接入 pytest 物理验证。
- 测试失败后读取 Traceback 指向的文件和行号。
- 结合文件工具精准修改。
- 重新运行测试，直到通过。
- 必要时使用 Git 回滚恢复到安全状态。

---

## 13. 不同岗位推荐使用版本

| 目标岗位 | 推荐模板 | 重点突出 |
|:---|:---|:---|
| LLM 应用工程师 | 模板一 | Agent、Tool Calling、ReAct、上下文工程 |
| AI Agent 工程师 | 模板一 + 模板四 | 规划、工具编排、记忆、自愈 |
| Python 后端工程师 | 模板二 | 模块化架构、CLI、异步、测试、Git |
| RAG / 检索工程师 | 模板三 | Hybrid Recall、BM25、长期记忆、排序融合 |
| 测试开发工程师 | 模板五 | pytest、自愈、Traceback、质量保障 |
| 简历篇幅有限 | 模板七 | 3-5 行精简表达 |

---

## 14. 最推荐放入简历的版本

如果只能放一个版本，建议使用下面这个，兼顾 AI Agent、工程架构和测试闭环：

**Mini Claude Code CLI｜面向软件工程任务的 AI Coding Agent**

- 基于 Python + OpenAI-compatible Tool Calling 构建本地 AI Coding Agent，封装 Bash、File、Search、Symbol、Pytest、Git、Memory 等工具，实现代码阅读、文件修改、测试运行、错误修复、Git 回滚和文档生成等工程任务自动化。
- 设计异步 Agent Engine 与显式 PlanManager，支持多工具并发执行、复杂任务步骤拆解、进度追踪和中断恢复，降低长任务中的目标漂移与重复执行问题。
- 构建三层记忆与长期记忆 Hybrid Recall 系统，将文件变更、Bug 修复、架构决策和用户偏好沉淀为结构化 MemoryItem，并支持文件历史/错误历史主动召回。
- 实现上下文压缩与预算化装配，将代码修改、测试结果、Traceback、Git 操作等关键帧保存为结构化状态，并保证 tool calling 消息原子性，提升长对话稳定性。
- 接入 pytest 驱动的自愈闭环和 Git 快照/回滚机制，使 Agent 在测试失败后可自动定位、修复并重新验证，提高自动化代码修改的可靠性。

---

## 15. 分模块实现拆解：Tool、Agent Loop、Plan、Memory、Session、Context 与安全性

这一部分适合在面试中展开讲项目实现。可以按“用户输入进入 Agent 后，系统如何规划、组装上下文、调用模型、执行工具、保存会话、沉淀记忆、保障安全”这条主链路来讲。

### 15.1 Tool 工具系统：把本地工程能力标准化暴露给 Agent

Tool 模块的核心作用是把本地开发环境中的操作能力封装成 LLM 可调用的结构化函数。系统不是让模型直接“凭空修改代码”，而是通过统一的工具协议把文件读写、Shell 执行、代码搜索、符号定位、测试运行、Git 操作和记忆检索都纳入可控边界。

实现上一般包含三层：

1. **工具抽象层**：每个工具都有固定的名称、描述、参数 schema 和执行函数，便于转换成 OpenAI-compatible tool/function calling 格式。
2. **工具注册层**：启动时将 Bash、ReadFile、EditFile、WriteFile、Search、Symbol、Pytest、Git、Memory 等工具注册到统一工具表，Agent Loop 根据模型返回的 tool name 路由到对应实现。
3. **工具执行层**：接收模型生成的 JSON 参数，做参数校验、路径处理、异常捕获和结果格式化，再把执行结果作为 tool message 回传给模型。

比较关键的工程点：

- **文件工具**：`read_file` 支持按行读取，避免大文件一次性塞满上下文；`edit_file` 通过精确字符串替换降低误改风险；`write_full_file` 用于新建文件或复杂整体重写。
- **搜索与符号工具**：正则搜索负责跨文件定位文本模式，AST 符号工具负责按函数/类名直接定位定义、行号、docstring 和代码片段。
- **测试工具**：pytest 工具不只是运行命令，还会结构化返回 stdout、stderr、失败用例和 Traceback，供下一轮修复使用。
- **Git 工具**：封装 status、snapshot、rollback，让 Agent 的自动修改有可回退边界。
- **Memory 工具**：提供 recall、file history、error history、stats 等接口，使 Agent 在编辑文件或修复错误前主动查询历史经验。

简历/面试可以这样讲：

> 我把工具系统设计成 Agent 和真实操作系统之间的“安全适配层”。模型只能通过声明式 tool schema 发起操作，工具层负责参数校验、异常捕获、结果裁剪和结构化回传，从而把不可控的自然语言意图转成可追踪、可测试、可回滚的工程动作。

### 15.2 Agent Loop：ReAct 式决策、工具执行与反馈闭环

Agent Loop 是整个系统的调度中枢，负责把用户需求变成多轮“模型决策 → 工具调用 → 结果观察 → 再决策”的闭环。

典型流程如下：

1. 接收用户输入。
2. 读取当前 session、plan、memory、compressed context 等状态。
3. 通过 ContextAssembler 组装 system prompt、历史消息、长期记忆、压缩摘要和当前请求。
4. 调用 LLM，携带工具 schema。
5. 如果模型返回普通文本，则输出给用户。
6. 如果模型返回 tool calls，则解析工具名和参数。
7. 并发或串行执行对应工具。
8. 将 tool result 追加回消息历史。
9. 再次调用 LLM，让模型基于真实执行结果继续推理。
10. 直到模型给出最终回答或达到轮次/预算限制。

项目里的亮点是：

- **异步并发工具调用**：当模型一轮返回多个互不依赖的工具调用时，可以用 `asyncio.gather` 并行执行，例如同时读取文件和搜索代码，减少等待时间。
- **观察驱动修复**：工具结果不是日志而已，而是下一轮推理的 observation。比如 pytest 失败后，Traceback 会进入下一轮上下文，指导模型读取具体文件行并修复。
- **工具调用原子性**：Agent Loop 与 Context 模块需要保证 `assistant.tool_calls` 后面必须跟对应的 tool result，不能在压缩或截断时拆散。
- **失败自愈**：工具异常会被包装成结构化错误返回给模型，而不是直接中断进程，模型可以根据错误换一种方式继续完成任务。

可以用下面这句话概括：

> Agent Loop 本质上是一个工程化 ReAct 状态机：LLM 负责决策，Tool 负责真实执行，Observation 负责反馈校正，Plan/Memory/Session/Context 共同负责让多轮执行保持连续、可恢复和可验证。

### 15.3 Plan 规划系统：让长任务显式化、可追踪、可恢复

Plan 模块解决的是长任务中 Agent 容易遗忘目标、重复执行、跳步骤的问题。系统要求复杂任务开始前先创建计划，把用户目标拆成多个明确步骤，并在每一步完成后更新状态。

实现上包含：

- **Plan 数据结构**：包含 goal、steps、status、task_id、created_at、updated_at 等字段。
- **PlanManager**：负责任务创建、步骤完成标记、计划更新、完成归档和查询当前未完成步骤。
- **Prompt 注入**：当前计划会被动态注入 system prompt，例如展示为“1. ✅ 已完成；2. ⏳ 待执行”。
- **中断恢复**：如果会话被压缩或用户隔一段时间说“继续”，Agent 可以从下一个未完成步骤恢复，而不是重新开始。
- **完成记录**：已完成任务会进入历史记录，避免用户重复提出相似任务时重复执行。

Plan 的关键不是“列 TODO”，而是把 TODO 变成 Agent 执行协议的一部分：

- 开始复杂任务前必须有计划。
- 完成一个步骤后必须调用工具标记完成。
- 如果计划变化，必须更新计划，而不是在自然语言里随口改。
- 当前计划会进入上下文，影响后续决策。

面试表达：

> 我把规划系统做成显式状态机，而不是只靠 prompt 里一句“请逐步思考”。Plan 状态会持久化并注入每轮上下文，因此 Agent 在长对话、工具失败或会话恢复后仍能知道当前目标、已完成步骤和下一步应该做什么。

### 15.4 Memory 记忆系统：从一次性对话升级为跨会话经验复用

Memory 模块解决跨会话连续性问题。普通 Chatbot 的历史只存在当前上下文里，一旦截断或换会话就丢失；这个项目把任务经验、文件修改、Bug 修复、架构决策等沉淀为长期记忆，并在后续任务中主动召回。

整体可以分为三层：

1. **工作记忆**：当前窗口内最近的对话、工具调用和执行结果。
2. **情景记忆**：一次任务或一次会话的结构化摘要，例如目标、完成状态、文件变更、测试结果、错误记录。
3. **长期记忆**：跨会话保存的 `MemoryItem`，包括任务经验、Bug 修复、用户偏好、架构决策、工作流规范等。

长期记忆通常包含这些字段：

- title / content：记忆标题和正文。
- kind：task、bug、decision、workflow、preference 等类型。
- files：关联文件。
- concepts：关键词。
- importance / confidence：重要性和置信度。
- metadata：额外结构化信息。
- timestamp：创建或更新时间。

检索上采用 Hybrid Recall：

- **关键词 / BM25**：适合精确召回文件名、函数名、错误信息。
- **向量相似度**：适合语义相近但措辞不同的任务。
- **时间新鲜度**：近期经验适当加权。
- **重要性权重**：架构决策、已解决 Bug、用户偏好优先级更高。
- **文件/错误维度召回**：编辑某文件前查 file history，遇到 traceback 时查 error history。
- **RRF 融合排序**：把多路检索结果稳定融合，避免单一检索器偏差。

面试可以这样讲：

> 这个 Memory 不是传统文档 RAG，而是 Agent 自身执行经验的 RAG。它召回的不只是知识文本，还包括某个文件以前怎么改过、某类错误以前怎么修过、用户偏好是什么、哪些架构决策不能破坏。这样 Agent 才能在跨会话任务里表现得像一个持续工作的工程师。

### 15.5 Session 会话管理：保存对话、工具轨迹和可恢复状态

Session 模块负责把一次 CLI 交互过程持久化。它关注的不是“长期知识”，而是当前会话能否恢复、审计和继续执行。

通常保存的信息包括：

- session_id、创建时间、更新时间。
- 用户消息、assistant 消息、tool call、tool result。
- 当前 plan 状态。
- 已读文件、已改文件、测试运行记录、错误信息。
- 压缩摘要或 `CompressedSessionState`。
- 当前工作目录、环境信息、模型配置等。

Session 和 Memory 的区别：

| 模块 | 关注点 | 生命周期 | 内容 |
|:---|:---|:---|:---|
| Session | 当前会话过程 | 中短期，可恢复 | 完整消息、工具轨迹、计划状态 |
| Memory | 可复用经验 | 长期，跨会话 | Bug 修复、架构决策、用户偏好、任务总结 |

实现上，SessionManager 会在关键节点保存状态：

- 用户输入后保存 turn。
- 模型返回 tool call 后保存 assistant 消息。
- 工具执行完成后保存 tool result。
- 文件修改、测试运行、Git 操作后记录关键事件。
- 会话过长时触发压缩，并保存压缩后的结构化状态。

这个模块的价值：

- CLI 退出后可以继续上次任务。
- 出错后可以回看工具轨迹。
- 压缩时可以基于完整历史提取关键帧。
- 长期记忆晋升时可以从 session 中抽取高价值事件。

面试表达：

> Session 是 Agent 的“短中期工作日志”，Memory 是“长期经验库”。Session 保证一次任务可以恢复和审计，Memory 负责把可复用经验沉淀到未来任务中。

### 15.6 Context / 压缩策略：在有限窗口里保留最重要的工程状态

Context 模块负责决定“每次请求模型时到底塞什么内容”。长任务里消息、工具输出、文件内容和测试日志会快速膨胀，如果简单截断，很容易丢掉任务目标、错误原因或工具调用配对关系。

ContextAssembler 一般按优先级组装：

1. System prompt：角色、工具协议、安全规则、规划要求。
2. 当前 Plan：目标、步骤、完成状态。
3. 相关 Memory：长期记忆召回结果。
4. CompressedSessionState：压缩后的任务状态。
5. Recent turns：最近若干轮用户/assistant/tool 消息。
6. Current request：用户当前输入，最高优先级保留。

压缩策略不是简单 summary，而是面向工程任务的结构化压缩：

- **keyframe 压缩**：优先保留代码修改、测试结果、Traceback、Git 操作、用户明确决策。
- **semantic 压缩**：对长讨论提取核心观点、约束和结论。
- **timeline 压缩**：按时间线记录任务推进过程。
- **hybrid 压缩**：结合关键帧和语义摘要，适合复杂工程任务。

`CompressedSessionState` 可以包含：

- 当前目标与完成状态。
- 已完成/未完成计划。
- 文件变更列表。
- 已读取文件与关键片段。
- 测试命令与结果。
- 错误 Traceback 摘要。
- 关键架构决策。
- 注意事项和禁止破坏的约束。

最关键的工程点是 **tool message pairing**：

- OpenAI-compatible 协议要求 assistant 返回 tool_calls 后，后续必须有对应 tool result。
- 压缩和截断不能留下半截 tool call。
- 因此 Context 模块需要做 provider message validation，必要时整组保留或整组丢弃工具调用链。

面试表达：

> 我把上下文管理从“截断聊天记录”升级成“工程状态装配”。模型每次看到的不一定是完整历史，但一定包含当前目标、计划状态、关键文件变更、测试错误、相关长期记忆和合法的工具调用链。

### 15.7 安全性：把 Agent 的自主性限制在可验证、可回滚边界内

安全性模块主要解决一个问题：让 Agent 能自主执行工程动作，但不能无限制破坏本地项目。

可以从几个层面讲：

#### 1. 工具边界安全

- 模型不能直接操作系统，只能调用已注册工具。
- 每个工具有明确参数 schema。
- 文件编辑工具要求明确路径和内容。
- 搜索/读取工具优先支持范围读取，避免一次性泄露或污染上下文。
- 工具异常会结构化返回，不让进程直接崩溃。

#### 2. 文件修改安全

- 小文件可全量写入，长文件优先精准替换。
- `edit_file` 必须匹配到唯一旧内容才替换，降低误改概率。
- 连续匹配失败时切换读取原文再重写，避免盲目 patch。
- 修改后通过读取文件核对实际落盘内容。

#### 3. 测试验证安全

- 核心逻辑修改必须配套测试。
- pytest 通过才视为任务真正完成。
- 测试失败时根据 Traceback 修复，而不是直接报告完成。

#### 4. Git 安全

- 修改前后查看 git status。
- 关键节点创建 snapshot commit。
- 连续失败或误改时支持 rollback。
- 通过影子分支/隔离分支思路降低主分支污染风险。

#### 5. 上下文与协议安全

- 压缩时不破坏 tool call/tool result 配对。
- 避免把半截工具调用发给 provider。
- 控制长期记忆注入长度，避免无关历史污染当前任务。
- 对 system prompt、plan、当前用户请求设置优先级，防止关键规则被挤出上下文。

#### 6. 任务流程安全

- 复杂任务必须先 plan。
- 每一步完成后标记状态。
- 已完成任务进入历史记录，避免重复执行。
- 会话恢复时从未完成步骤继续，避免重复写文件。

面试总结可以这样说：

> 这个项目的安全性不是单点权限控制，而是一套工程闭环：工具 schema 限制模型能做什么，文件编辑策略降低误改，pytest 验证保证结果正确，Git snapshot/rollback 提供恢复点，Context validation 保证模型协议合法，Plan/Session 则保证任务过程可追踪、可恢复。

### 15.8 一条完整执行链路示例

可以用一个“用户要求修改代码并补测试”的例子串起来：

1. 用户提出需求。
2. PlanManager 创建任务步骤。
3. ContextAssembler 组装 system prompt、plan、相关 memory、session 摘要和当前请求。
4. Agent Loop 调用模型。
5. 模型决定先读取文件和搜索符号。
6. Tool Registry 路由到 read/search/symbol 工具执行。
7. 工具结果返回给模型。
8. 模型调用 edit/write 工具修改代码，并调用 pytest 工具运行测试。
9. 如果测试失败，pytest tool 返回 Traceback。
10. Agent 根据 Traceback 再读取对应文件行，继续修复。
11. 测试通过后，PlanManager 标记步骤完成。
12. SessionManager 保存完整轨迹。
13. Memory 模块将关键 Bug 修复、文件经验或架构决策晋升为长期记忆。
14. Git 工具在关键节点创建快照，必要时可回滚。
15. 最终 Agent 向用户报告已完成，并说明修改与验证结果。

这条链路体现了整个项目的核心价值：

> 它不是一个只会聊天的代码助手，而是一个带有工具执行、规划管理、测试验证、长期记忆、上下文工程和安全回滚能力的本地 AI 软件工程代理。
