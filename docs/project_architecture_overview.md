# Mini Claude Code CLI — 项目架构总览

> 本文档基于 2026-06-03 项目现状梳理，涵盖整体架构、核心模块、数据流与设计思想。

---

## 1. 项目定位

Mini Claude Code CLI 是一个 **带工具调用、上下文压缩、长期记忆、测试闭环和 Git 快照能力的 CLI Agent 框架**。

它不是单纯的聊天 CLI，而是一个小型 Claude Code / Cursor Agent 风格的本地工程代理。

核心定位：

```
LLM 是大脑；
AgentEngine 是神经中枢；
Tools 是手脚；
Memory 是长期经验；
Context Compression 是短期注意力管理；
Tests / Git 是工程安全网。
```

---

## 2. 总体架构图

```
┌──────────────────────────────────────────────────────────────────────┐
│                              用户输入                                 │
│                  CLI 交互 / 自然语言任务 / 继续执行                   │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                              main.py                                  │
│  - CLI 入口                                                           │
│  - 初始化 AgentEngine                                                  │
│  - 加载配置 / 工具 / 记忆系统                                           │
│  - 进入交互循环                                                        │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         Agent Engine 核心调度层                       │
│                         core/engine.py                                │
│                                                                      │
│  职责：                                                               │
│  - 接收用户任务                                                       │
│  - 组装上下文                                                         │
│  - 调用 LLM                                                           │
│  - 解析 tool_calls                                                    │
│  - 执行工具                                                           │
│  - 保存记忆                                                           │
│  - 控制多轮 ReAct 循环                                                 │
│  - 处理 read_file 防重复读取                                           │
│  - 触发上下文压缩                                                     │
└──────────────────────────────────────────────────────────────────────┘
              │                    │                    │
              │                    │                    │
              ▼                    ▼                    ▼
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│      LLM Client       │ │     Tool System       │ │    Memory System     │
│  OpenAI兼容接口        │ │  文件/测试/Git/记忆工具 │ │  长短期记忆/召回/注入 │
└──────────────────────┘ └──────────────────────┘ └──────────────────────┘
              │                    │                    │
              ▼                    ▼                    ▼
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│  Chat Completion      │ │ tools/*.py            │ │ memory/*.py          │
│  tool_calls            │ │ read/edit/search/test │ │ BM25/Vector/RRF      │
│  OpenAI tool protocol  │ │ git/symbol/memory     │ │ persistence/indexes  │
└──────────────────────┘ └──────────────────────┘ └──────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         Context Compression                           │
│  - 上下文过长时压缩历史消息                                            │
│  - 保留关键帧：代码修改、测试、错误、Git、用户决策                      │
│  - 保护 OpenAI tool_calls/tool responses 成对不被截断                  │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          输出给用户 / 继续循环                         │
│  - 最终回答                                                           │
│  - 工具结果                                                           │
│  - 测试结果                                                           │
│  - 下一步建议                                                         │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. 按目录拆分的项目结构

```
mini-claude-code-cli/
│
├── main.py                    # CLI 程序入口
│
├── core/
│   ├── engine.py              # Agent 主循环 / ReAct 调度 / LLM 调用 / 工具执行
│   ├── context_manager.py     # 上下文管理 / 压缩触发 / 消息预算控制
│   ├── compression_engine.py  # 上下文压缩策略
│   ├── compressed_session_state.py  # 压缩后的结构化会话状态
│   ├── turn_builder.py        # 将消息按 turn 原子化建模，保护 tool pair
│   └── 其他核心运行模块
│
├── tools/
│   ├── base.py                # 工具基类
│   ├── file_tool.py           # read_file / edit_file / write_full_file / list_files
│   ├── search_tool.py         # search_code
│   ├── symbol_tool.py         # list_all_symbols / find_symbol_definition
│   ├── pytest_tool.py         # run_pytest
│   ├── git_tool.py            # git status / commit snapshot / rollback
│   └── memory_tool.py         # memory_save / recall / file_history / error_history / stats
│
├── memory/
│   ├── memory_manager.py      # 记忆系统总入口
│   ├── memory_models.py       # MemoryItem / SessionSummary / FileChange / ErrorRecord 等模型
│   ├── memory_layers.py       # Working / Episodic / LongTerm 三层记忆
│   ├── memory_retrieval.py    # 检索层：多层检索 / BM25 / 文件历史 / 错误历史
│   ├── memory_bm25_index.py   # BM25 关键词索引
│   ├── memory_vector_index.py # embedding / vector index 语义索引
│   ├── memory_context_builder.py  # 构造要注入 system prompt 的记忆上下文
│   └── long_term/
│       ├── memory_items.json
│       ├── session_summaries.json
│       └── indexes/
│           ├── bm25_index.json
│           └── vector_index.json
│
├── tests/
│   ├── test_read_guard.py
│   ├── test_openai_tool_pairing.py
│   ├── test_compression_engine.py
│   ├── test_memory_*.py
│   ├── test_turn_builder.py
│   ├── test_symbol_tool.py
│   └── ...
│
├── requirements.txt           # 项目依赖
├── README.md                  # 项目说明
└── CLAUDE.md                  # 工程规范
```

---

## 4. 核心运行链路

用户输入一个任务后，大致会走下面这条链路：

```
用户输入
   │
   ▼
main.py 接收输入
   │
   ▼
AgentEngine.run()
   │
   ├── 1. 读取当前会话状态
   ├── 2. 判断是否需要召回长期记忆
   ├── 3. 通过 MemoryManager 检索相关 memory
   ├── 4. 组装 system prompt + memory context + recent messages
   ├── 5. 调用 LLM
   ├── 6. 如果 LLM 返回普通文本 → 输出给用户
   └── 7. 如果 LLM 返回 tool_calls → Tool Registry 匹配工具 → 执行工具 → 结果写入 messages → 回到 LLM 继续推理
```

典型的 ReAct Agent 模式：

```
Thought → Tool Call → Observation → Thought → Tool Call → Observation → Final Answer
```

---

## 5. Agent Engine 中枢详细架构

`core/engine.py` 是项目的大脑，负责串联所有子系统：

```
┌──────────────────────────────────────────────────────────────────┐
│                         AgentEngine                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  用户输入                                                        │
│    │                                                             │
│    ▼                                                             │
│  构造上下文 ────────┬──────── 召回长期记忆                         │
│    │                │                                            │
│    ▼                ▼                                            │
│  调用 LLM        MemoryManager                                   │
│    │                                                             │
│    ▼                                                             │
│  解析 tool_calls                                                 │
│    │                                                             │
│    ▼                                                             │
│  执行工具                                                        │
│    │                                                             │
│    ▼                                                             │
│  记录工具结果 / 错误 / 文件变化 / 测试结果                         │
│    │                                                             │
│    ▼                                                             │
│  判断是否继续循环或输出最终答案                                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

关键能力：

- 调 LLM
- 管消息
- 管工具调用
- 管记忆召回
- 管上下文压缩
- 管 read_file 防重复读取
- 管测试结果
- 管错误恢复提示
- 管计划 / 任务状态

---

## 6. 工具系统架构

### 6.1 工具清单

```
┌─────────────────────────────────────────────────────────────┐
│                         Tool Registry                        │
│  将工具暴露给 LLM，并根据 tool_call name 找到对应工具执行       │
└─────────────────────────────────────────────────────────────┘
           │
           ├── read_file
           ├── edit_file
           ├── write_full_file
           ├── list_files_recursive
           ├── search_code
           ├── list_all_symbols
           ├── find_symbol_definition
           ├── run_pytest
           ├── get_git_status
           ├── commit_snapshot
           ├── git_rollback
           ├── memory_save
           ├── memory_recall
           ├── memory_file_history
           ├── memory_error_history
           └── memory_stats
```

### 6.2 工具分类

| 类别       | 文件               | 工具                                              | 作用                                |
|-----------|--------------------|--------------------------------------------------|-------------------------------------|
| 文件工具   | `tools/file_tool.py`  | read_file / edit_file / write_full_file / list_files | 读代码 → 修改代码 → 创建文件 → 查看结构 |
| 搜索与符号 | `tools/search_tool.py` + `tools/symbol_tool.py` | search_code / list_all_symbols / find_symbol_definition | 全局搜索 / 定位定义 / 理解代码结构 |
| 测试工具   | `tools/pytest_tool.py` | run_pytest                                       | 运行 pytest / 捕获失败 / 辅助自愈    |
| Git 工具   | `tools/git_tool.py`    | get_git_status / commit_snapshot / git_rollback   | 查看状态 / 自动快照 / 回滚           |
| 记忆工具   | `tools/memory_tool.py` | memory_save / recall / file_history / error_history / stats | 保存经验 / 召回历史 / 查统计        |

---

## 7. 记忆系统详细架构

### 7.1 三层记忆 + 检索索引 + 注入上下文

```
┌────────────────────────────────────────────────────────────────────┐
│                         MemoryManager                               │
│                   memory/memory_manager.py                          │
└────────────────────────────────────────────────────────────────────┘
                │
       ┌────────┼────────┐
       │        │        │
       ▼        ▼        ▼
┌──────────┐ ┌──────────┐ ┌────────────────┐
│ Working  │ │ Episodic │ │ Long-term       │
│ Memory   │ │ Memory   │ │ Memory          │
└──────────┘ └──────────┘ └────────────────┘
       │        │                 │
       │        │                 ▼
       │        │        ┌──────────────────────┐
       │        │        │ MemoryItem Store      │
       │        │        │ SessionSummary Store  │
       │        │        └──────────────────────┘
       │        │                 │
       │        │                 ▼
       │        │        ┌──────────────────────┐
       │        │        │ Indexes               │
       │        │        │ - BM25 Index          │
       │        │        │ - Vector Index        │
       │        │        │ - Metadata            │
       │        │        └──────────────────────┘
       │        │                 │
       └────────┴─────────────────┘
                │
                ▼
┌────────────────────────────────────────────────────────────────────┐
│                         Hybrid Recall                               │
│  BM25 + Vector + Metadata + Lifecycle + RRF Fusion                   │
└────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────────────────────────────┐
│                     Memory Context Builder                           │
│  将召回结果裁剪、去重、排序，变成可注入 prompt 的记忆上下文             │
└────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────────────────────────────┐
│                           Agent Prompt                               │
│  System Prompt + Memory Context + Recent Conversation + User Input    │
└────────────────────────────────────────────────────────────────────┘
```

### 7.2 三层记忆说明

| 层级          | 保存内容                                    | 特点                     | 比喻                  |
|--------------|---------------------------------------------|-------------------------|----------------------|
| Working      | 最近用户/assistant/tool消息                  | 生命周期短、容量有限、偏当前 | "正在想的东西"        |
| Episodic     | 会话总结/任务进展/文件修改/错误记录           | 阶段性摘要、比 working 长 | "对某次经历的摘要"    |
| Long-term    | 用户偏好/架构决策/Bug经验/工作流/文件/错误历史 | 持久化、跨会话、有生命周期 | "长期经验库"          |

### 7.3 记忆检索架构

```
用户当前问题 / 当前任务
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                     Memory Retrieval                         │
└─────────────────────────────────────────────────────────────┘
        │
        ├────────────────────┬────────────────────┬────────────────────┐
        │                    │                    │                    │
        ▼                    ▼                    ▼                    ▼
┌──────────────┐   ┌────────────────┐   ┌────────────────┐   ┌──────────────┐
│ BM25 Search  │   │ Vector Search  │   │ Metadata Match │   │ Lifecycle    │
│ 关键词匹配    │   │ embedding 语义 │   │ 文件/错误/类型 │   │ 过滤归档/过期 │
└──────────────┘   └────────────────┘   └────────────────┘   └──────────────┘
        │                    │                    │                    │
        └────────────────────┴────────────────────┴────────────────────┘
                                   │
                                   ▼
                       ┌────────────────────┐
                       │ RRF Fusion          │
                       │ 多路结果融合排序     │
                       └────────────────────┘
                                   │
                                   ▼
                       ┌────────────────────┐
                       │ Top-K Memory Items  │
                       └────────────────────┘
                                   │
                                   ▼
                       ┌────────────────────┐
                       │ Prompt Injection    │
                       └────────────────────┘
```

#### BM25 的作用

适合：文件名、函数名、错误类型、精确关键词、代码符号、traceback 片段

#### Vector / Embedding 的作用

适合：语义相似、表达不同但意思接近、中英混合、模糊查询、历史决策类查询

> 当前 embedding 模块偏简单（hash / 伪向量），是工程占位实现。接入真实 embedding API 后将显著提升语义召回质量。

#### Metadata 的作用

增强排序：文件路径、任务类型、memory kind、importance、confidence、created_at、last_accessed_at、access_count、是否 archived / superseded

#### RRF Fusion 的作用

把多个检索通道的结果融合排序，比单靠某一种检索方式更稳定。

---

## 8. 上下文压缩系统架构

解决对话越来越长、不能无限塞进 LLM 上下文的问题。

```
┌────────────────────────────────────────────────────────────────────┐
│                        Conversation Messages                        │
│  user / assistant / tool / tool_calls                               │
└────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                         TurnBuilder                                 │
│  - 将消息按 turn 原子化建模                                          │
│  - assistant tool_call + tool response 必须成对处理                   │
│  - 避免截断出非法 OpenAI message                                      │
└────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                     Compression Engine                              │
│  策略：                                                              │
│  - sliding window                                                    │
│  - keyframe compression                                              │
│  - LLM summary                                                       │
│  - structured compressed session state                               │
└────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                  CompressedSessionState                              │
│  保存：                                                              │
│  - 当前目标                                                          │
│  - 已完成任务                                                        │
│  - 未完成任务                                                        │
│  - 文件变更                                                          │
│  - 已读取文件                                                        │
│  - 测试结果                                                          │
│  - 关键错误                                                          │
│  - 关键决策                                                          │
│  - 注意事项                                                          │
└────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                      Inject Back to Prompt                           │
│  将压缩后的结构化状态重新注入后续上下文                               │
└────────────────────────────────────────────────────────────────────┘
```

设计重点：**压缩不是简单删消息，而是保留工程任务的关键状态。**

---

## 9. OpenAI Tool Pair 安全机制

OpenAI tool calling 严格要求：assistant message 里如果有 `tool_calls`，后面必须紧跟对应的 `tool response`。

```
原始 messages
    │
    ▼
TurnBuilder
    │
    ├── 普通 user/assistant 消息
    ├── 完整 assistant tool_call + tool response
    ├── 缺失 tool response 的不完整 turn
    └── 孤立 tool message
    │
    ▼
过滤 / 修复非法 turn
    │
    ▼
发送给 OpenAI 的合法 messages
```

核心目标：**任何上下文裁剪、压缩、插入 memory，都不能破坏 tool pair。**

---

## 10. read_file 防重复读取机制

```
LLM 请求 read_file(path, start_line, end_line)
        │
        ▼
Runtime Read Ledger 检查
        │
        ├── 如果是新范围：允许真实读取
        ├── 如果是向后分页：允许
        └── 如果是重复/包含范围：短路返回提醒
```

目的：减少无效工具调用，防止模型卡在重复 read_file，节省上下文和调用轮次。

同时还有 **read-only streak guard**：连续多轮只读不写时，提醒 Agent 应该总结、计划或采取行动。

---

## 11. 测试系统架构

当前全量测试 **219 passed**，覆盖：

| 测试文件                          | 覆盖内容                              |
|----------------------------------|--------------------------------------|
| `test_compression_engine.py`     | 上下文压缩策略                        |
| `test_compressed_session_state.py` | 压缩状态结构化保存与渲染              |
| `test_context_assembly_budget.py`  | 上下文预算控制 / memory 注入位置     |
| `test_openai_tool_pairing.py`    | OpenAI tool_calls/tool response 配对安全 |
| `test_turn_builder.py`           | turn 原子化建模                       |
| `test_read_guard.py`             | read_file 防重复读取                  |
| `test_memory_*.py`               | 记忆系统、召回、生命周期、benchmark   |
| `test_symbol_tool.py`            | 符号工具                              |
| `test_shared_memory_manager.py`  | Engine 与 memory tools 共享 MemoryManager |

项目已经重视：Agent 行为稳定性、记忆召回质量、上下文压缩安全、工具协议合法性、工程自愈流程。

---

## 12. 一次完整任务的数据流

示例：用户说"帮我修复 pytest 失败的问题"

```
用户输入
   │
   ▼
AgentEngine 接收任务
   │
   ▼
MemoryManager 召回历史经验
   │
   ├── 有没有类似 pytest 错误？
   ├── 有没有相关文件历史？
   └── 有没有用户偏好？
   │
   ▼
组装 prompt (system + memory + compressed state + recent messages + user input)
   │
   ▼
调用 LLM → LLM 决定先运行测试
   │
   ▼
tool_call: run_pytest → PytestTool 执行 → 返回失败 traceback
   │
   ▼
AgentEngine 把结果加入 messages → LLM 分析 traceback → 决定读取文件
   │
   ▼
tool_call: read_file → Read Guard 检查 → 读取相关代码
   │
   ▼
LLM 决定修改代码 → tool_call: edit_file / write_full_file
   │
   ▼
再次 run_pytest → 测试通过
   │
   ▼
memory_save 保存修复经验 → git commit snapshot → 最终答复用户
```

---

## 13. 当前项目完成度评估

### ✅ 已完成

| 能力维度          | 完成度  | 说明                                    |
|------------------|--------|----------------------------------------|
| 工具调用体系      | 高     | 文件/搜索/符号/测试/Git/记忆工具完整     |
| 测试覆盖         | 高     | 219 tests passed，覆盖核心路径          |
| 长期记忆系统      | 高     | 三层记忆 + BM25 + Vector + RRF + 生命周期 |
| 上下文压缩        | 高     | 关键帧 + tool pair 保护 + 结构化状态     |
| OpenAI 协议安全   | 高     | TurnBuilder + sanitizer 机制             |
| read_file 防护    | 高     | Read Ledger + streak guard               |

### ⚠️ 需要继续改进

| 优先级 | 改进方向                          | 说明                                      |
|-------|----------------------------------|------------------------------------------|
| P0    | CLI 端到端回归测试               | 防止"单测全绿但 CLI 实际不可用"            |
| P1    | 记忆召回质量可视化与调试命令      | 降低记忆系统黑盒程度                       |
| P1    | Plan 持久化与恢复增强             | 会话重启后恢复未完成 plan                  |
| P2    | 工具错误自愈能力标准化            | 统一错误结构存入 memory                    |
| P2    | 性能与依赖治理                    | 区分 fast/integration/benchmark 测试       |
| P2    | 接入真实 Embedding API            | 当前 hash embedding 是占位实现             |

### 主要风险点

1. **真实 LLM/CLI 端到端场景仍需更多验证** — 单测很强但集成场景覆盖不足
2. **记忆系统复杂度较高** — 召回噪音、ranking 难解释、历史记忆污染当前任务
3. **Agent 行为稳定性** — 历史上出现过 read_file 反复调用、压缩残留非法 tool pair 等问题
4. **文档与实际能力同步** — README 展示较完整但随模块演进容易滞后

---

## 14. 核心设计思想

### 1. 工具化

让模型可以：读文件 → 改文件 → 跑测试 → 查符号 → 查 Git → 保存记忆 → 召回经验

### 2. 可恢复

通过 compressed session state + memory + plan + git snapshot，让长任务不会因上下文变长或会话重启而完全丢失状态。

### 3. 可验证

通过 pytest + py_compile + 测试失败后自愈，让 Agent 不只是"写代码"，而是必须验证代码。

### 4. 可控上下文

通过 context budget + compression + turn builder + tool pair sanitizer + memory context builder，控制 LLM 输入质量。

### 5. 长期学习

通过 memory_save/recall + file_history + error_history + BM25/Vector/RRF，让 Agent 跨会话积累经验。

---

## 15. 推荐代码阅读顺序

| 优先级 | 模块             | 文件                                | 理解目标                              |
|-------|-----------------|-------------------------------------|--------------------------------------|
| 1     | Agent 主流程     | `main.py` + `core/engine.py`       | 用户输入如何进入 → LLM 调用 → 工具执行 |
| 2     | 工具系统         | `tools/base.py` + `tools/file_tool.py` + `tools/pytest_tool.py` | 工具定义/调用/返回                    |
| 3     | 记忆系统         | `memory/memory_manager.py` + `memory_layers.py` + `memory_retrieval.py` | 保存/索引/召回/注入                  |
| 4     | 上下文压缩       | `core/compression_engine.py` + `turn_builder.py` + `compressed_session_state.py` | 裁剪/摘要/tool pair 保护/状态保留     |
| 5     | 测试             | `tests/test_openai_tool_pairing.py` + `test_read_guard.py` + `test_memory_*.py` | 反推设计意图                          |

---

## 16. 一句话总结

> **Mini Claude Code CLI = LLM 大脑 + AgentEngine 中枢 + Tools 手脚 + Memory 长期经验 + Context Compression 注意力管理 + Tests/Git 安全网**