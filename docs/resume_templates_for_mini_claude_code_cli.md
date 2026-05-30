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
