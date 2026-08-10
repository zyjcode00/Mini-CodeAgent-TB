# Mini Claude Code CLI 接入 Terminal-Bench 改造方案

> 文档目标：作为后续逐步接入 Terminal-Bench 评测的实施蓝图，明确当前项目可复用能力、接口差距、最小可行改造路径、测试验证方式与后续演进计划。

## 1. 背景与目标

Terminal-Bench 是面向终端环境中 agentic coding / debugging / tool-use 能力的评测框架。它通常会为每个任务准备一个隔离工作目录，提供任务描述，并通过测试脚本、文件状态检查或 hidden tests 判断 agent 是否完成任务。

`mini-claude-code-cli` 当前已经具备较完整的代码 Agent 能力：

- CLI 入口与交互式会话能力；
- Bash / 文件读写 / 代码搜索 / pytest 等工具调用能力；
- ReAct 风格主循环；
- 任务规划、长期记忆、会话压缩、Git 快照等工程化能力；
- 可运行测试并根据 Traceback 自愈修复。

因此，本项目可以接入 Terminal-Bench，但需要增加一层面向 benchmark harness 的非交互式适配入口，使其能够被外部评测系统稳定调用。

## 2. 接入结论

结论：**可以接入，但不是零改造直接接入。**

当前项目更接近一个交互式 Claude Code Lite CLI，而 Terminal-Bench 需要的是一个可被自动化 harness 调用的 agent runner。需要补齐以下能力：

1. 非交互式任务输入；
2. 指定 workspace / working directory；
3. 固定最大轮数、超时时间和退出条件；
4. 明确 stdout / stderr / exit code 协议；
5. 隔离或可控地使用长期记忆、Git 快照等副作用功能；
6. 提供 smoke test，确认适配入口可以在临时目录中完成任务。

## 3. Terminal-Bench 对 Agent 的典型要求

不同版本或不同集成方式的 Terminal-Bench 细节可能不同，但通常有以下共同点：

### 3.1 输入

- 一个任务描述，例如 `task.txt`、环境变量或命令行参数；
- 一个任务工作目录，里面包含待修改项目、测试脚本和说明文件；
- 可能还会提供 timeout、max-steps、model config 等参数。

### 3.2 执行

Agent 需要在任务工作目录内：

- 查看文件；
- 修改代码或配置；
- 运行命令；
- 执行测试；
- 根据失败结果迭代修复；
- 在认为完成后退出。

### 3.3 输出

Benchmark harness 更关心最终文件状态和测试结果，但 agent runner 仍应提供：

- 标准输出日志；
- 标准错误日志；
- 进程退出码；
- 可选的结构化结果文件，例如 `agent_result.json`。

建议约定：

- `exit code = 0`：agent 正常完成自身执行流程，不代表 hidden tests 必定通过；
- `exit code = 1`：agent 内部异常、参数错误或执行失败；
- `exit code = 124`：超时退出。

## 4. 当前项目可复用能力

### 4.1 CLI 与 Agent 主循环

当前项目已有主入口和 Agent Engine，可复用其对话循环、工具分发与模型调用逻辑。后续不应重新实现一个独立 agent，而应该新增 runner，将 Terminal-Bench 的 task/workspace 转换成当前 Engine 可消费的初始用户消息和运行上下文。

### 4.2 工具系统

可复用工具包括：

- Bash 命令执行；
- 文件读取；
- 文件编辑；
- 全文搜索；
- pytest 执行；
- Git 状态/快照；
- 长期记忆召回与保存。

Terminal-Bench 的核心任务正是要求 agent 能通过 shell 与文件系统解决问题，因此这些能力是接入的基础。

### 4.3 TDD 与自愈流程

项目已有“运行测试 → 分析 Traceback → 读取相关代码 → 修改 → 重跑测试”的工作流要求。该能力非常契合 Terminal-Bench 的评测目标，应在非交互式 runner 中保留。

## 5. 主要差距

### 5.1 缺少 benchmark 专用入口

当前交互式 CLI 通常需要用户多轮输入，而 Terminal-Bench 需要一次性启动进程执行任务。因此需要新增入口，例如：

```bash
python scripts/run_terminal_bench_agent.py \
  --task-file /path/to/task.txt \
  --workspace /path/to/workspace \
  --max-turns 40 \
  --timeout 1800
```

或模块形式：

```bash
python -m scripts.run_terminal_bench_agent \
  --task-file /path/to/task.txt \
  --workspace /path/to/workspace
```

### 5.2 工作目录控制不足

Terminal-Bench 的每个任务都有自己的 workspace。Agent 的所有 Bash、读写、搜索、pytest 操作都应默认发生在该 workspace 内。

需要确认并改造：

- 启动 runner 时 `os.chdir(workspace)`；
- Bash 工具默认 cwd 为 workspace；
- 文件工具限制或默认相对 workspace；
- 日志和记忆文件不要污染任务目录，除非显式指定。

### 5.3 退出条件不够明确

交互式 agent 可以等待用户继续输入，但 benchmark 需要自动结束。应支持：

- 最大轮数 `--max-turns`；
- 总超时 `--timeout`；
- agent 输出完成信号后退出；
- 连续空响应或无工具调用时提前终止；
- 异常时返回非零退出码。

### 5.4 记忆与 Git 副作用需要控制

长期记忆、Git 快照、历史任务召回等能力对日常编码有帮助，但在 benchmark 中可能引入污染：

- 不同任务之间可能信息泄漏；
- 自动 Git 操作可能改变评测目录状态；
- 记忆召回可能让结果不可复现。

建议为 Terminal-Bench runner 增加模式开关：

```bash
--disable-memory
--disable-auto-commit
--session-id terminal-bench-<task-id>
--artifact-dir /tmp/agent-artifacts/<task-id>
```

初期建议默认关闭长期记忆写入和自动提交，只保留必要的上下文内记忆。

## 6. 推荐目标架构

```text
Terminal-Bench Harness
        |
        | calls
        v
scripts/run_terminal_bench_agent.py
        |
        | parse args: task-file, workspace, timeout, max-turns
        | chdir(workspace)
        | build initial prompt
        v
core.engine.AgentEngine
        |
        | uses tools under workspace
        v
Bash / File / Search / Pytest Tools
        |
        v
Task workspace files modified
        |
        v
Terminal-Bench scorer / hidden tests
```

runner 只负责适配协议，不替代现有 Engine。

## 7. 最小可行改造方案 MVP

### 阶段 1：新增非交互式 runner

新增文件：

```text
scripts/run_terminal_bench_agent.py
```

职责：

1. 解析参数：
   - `--task`：直接传入任务文本；
   - `--task-file`：从文件读取任务；
   - `--workspace`：任务工作目录；
   - `--max-turns`：最大循环轮数；
   - `--timeout`：总超时秒数；
   - `--output-json`：可选结构化结果输出路径。
2. 校验 workspace 存在；
3. 切换当前工作目录到 workspace；
4. 构造初始 prompt；
5. 调用现有 Agent Engine 执行单任务；
6. 捕获异常并返回标准退出码。

建议初始 prompt：

```text
你正在 Terminal-Bench 任务工作目录中运行。
请阅读任务说明，使用 shell、文件编辑、测试运行等工具完成任务。
所有修改必须发生在当前 workspace 内。
完成后请停止，不要等待用户继续输入。

任务说明：
<task content>
```

### 阶段 2：为 Engine 增加单任务运行接口

如果当前 Engine 只有交互式循环，建议新增方法：

```python
async def run_single_task(
    self,
    task_prompt: str,
    max_turns: int = 40,
    timeout_seconds: int | None = None,
) -> AgentRunResult:
    ...
```

返回结构：

```python
@dataclass
class AgentRunResult:
    success: bool
    stop_reason: str
    turns: int
    message: str
    error: str | None = None
```

`stop_reason` 可选值：

- `completed`；
- `max_turns`；
- `timeout`；
- `model_error`；
- `tool_error`；
- `empty_response`；
- `exception`。

### 阶段 3：workspace 安全与 cwd 传递

需要检查所有工具是否遵循当前工作目录。最低要求：

- runner 中 `os.chdir(workspace)`；
- Bash 工具继承当前 cwd；
- 文件读写工具接受相对路径时基于 cwd；
- 不强制访问项目根目录。

增强要求：

- 新增 `workspace_root` 配置；
- 文件工具拒绝越界路径，例如 `..` 逃逸；
- Bash 工具可配置 cwd；
- 所有工具日志记录相对 workspace 的路径。

### 阶段 4：日志与结果输出

建议 runner 输出 JSON：

```json
{
  "success": true,
  "stop_reason": "completed",
  "turns": 23,
  "workspace": "/path/to/workspace",
  "duration_seconds": 532.1,
  "error": null
}
```

同时保留 stdout/stderr，方便 Terminal-Bench 或本地排障查看。

### 阶段 5：本地 smoke test

新增测试或脚本：

```text
tests/test_terminal_bench_runner.py
```

验证内容：

1. 创建临时 workspace；
2. 写入一个简单 Python 文件和失败测试；
3. 提供任务：修复函数使测试通过；
4. 调用 runner；
5. 检查 runner 正常退出；
6. 检查文件被修改；
7. 检查 pytest 通过。

如果不希望真实调用大模型，可先对 Engine 做 mock，验证 runner 的参数解析、cwd 切换和结果输出。

## 8. 详细实施清单

### 8.1 新增配置项

建议支持环境变量和命令行参数：

| 参数 | 默认值 | 说明 |
|---|---:|---|
| `--workspace` | 必填 | Terminal-Bench 任务目录 |
| `--task-file` | 可选 | 任务说明文件 |
| `--task` | 可选 | 直接传入任务文本 |
| `--max-turns` | `40` | 最大 agent 轮数 |
| `--timeout` | `1800` | 最大运行时间，秒 |
| `--output-json` | 可选 | 写入结构化结果 |
| `--disable-memory` | `true` | benchmark 下默认禁用长期记忆写入 |
| `--disable-auto-commit` | `true` | benchmark 下默认禁用自动提交 |
| `--log-level` | `INFO` | 日志级别 |

### 8.2 Runner 伪代码

```python
import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

async def main_async():
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    if not workspace.exists() or not workspace.is_dir():
        print(f"Invalid workspace: {workspace}", file=sys.stderr)
        return 1

    task_text = load_task(args)
    old_cwd = Path.cwd()
    start = time.time()

    try:
        os.chdir(workspace)
        engine = build_engine_for_terminal_bench(args)
        prompt = build_prompt(task_text)
        result = await asyncio.wait_for(
            engine.run_single_task(prompt, max_turns=args.max_turns),
            timeout=args.timeout,
        )
        exit_code = 0 if result.success else 1
    except asyncio.TimeoutError:
        result = make_timeout_result(args.max_turns)
        exit_code = 124
    except Exception as exc:
        result = make_exception_result(exc)
        exit_code = 1
    finally:
        os.chdir(old_cwd)

    write_output_json_if_needed(args.output_json, result, time.time() - start)
    return exit_code

if __name__ == "__main__":
    raise SystemExit(asyncio.run(main_async()))
```

### 8.3 Engine 改造点

如果当前 Engine 的运行循环直接绑定用户交互，需要拆出公共逻辑：

```text
交互式 CLI:
  while True:
    user_input = input(...)
    await engine.run_single_task(user_input)

Terminal-Bench runner:
  task = read_task(...)
  await engine.run_single_task(task, max_turns=N)
```

目标是让交互式 CLI 和 benchmark runner 复用同一套执行核心。

## 9. 验证策略

### 9.1 单元测试

- 参数解析测试；
- task 文件读取测试；
- workspace 不存在时报错；
- output json 格式测试；
- timeout 映射到 exit code 124。

### 9.2 Mock Engine 集成测试

用 fake engine 替代真实模型：

- 验证 runner 会切换 cwd；
- 验证 prompt 包含任务内容；
- 验证 max-turns 被传入；
- 验证结果 JSON 被写入。

### 9.3 真实模型 smoke test

构造一个非常简单任务：

```text
workspace/
  app.py       # add(a, b) 返回错误结果
  test_app.py  # pytest 测试 add(1, 2) == 3
  task.txt     # 请修复 app.py 并运行 pytest
```

执行：

```bash
python scripts/run_terminal_bench_agent.py \
  --task-file workspace/task.txt \
  --workspace workspace \
  --max-turns 20 \
  --timeout 600 \
  --output-json workspace/agent_result.json
```

期望：

- runner exit code 为 0；
- `pytest` 通过；
- `agent_result.json` 存在；
- 文件修改只发生在 workspace 内。

## 10. 与 Terminal-Bench 的集成方式建议

### 10.1 本地手动运行

先不直接改 Terminal-Bench，只在本项目内验证 runner：

```bash
python scripts/run_terminal_bench_agent.py \
  --task-file D:/path/to/task.txt \
  --workspace D:/path/to/workspace
```

### 10.2 封装为 agent command

在 Terminal-Bench 配置中，将 agent 命令指向本项目 runner：

```bash
python D:/LLM/mini-claude-code-cli/scripts/run_terminal_bench_agent.py \
  --task-file $TASK_FILE \
  --workspace $WORKSPACE \
  --max-turns 40 \
  --timeout 1800
```

实际变量名以 Terminal-Bench 当前版本为准。

### 10.3 Docker / Linux 兼容

Terminal-Bench 常在 Linux / Docker 环境中运行。当前项目在 Windows 路径下开发，后续需要注意：

- 路径使用 `pathlib.Path`，避免硬编码 `D:\...`；
- shell 命令不要依赖 Windows 专有语法；
- 如果工具内部调用 `cmd.exe`，需要改为可配置 shell；
- requirements 应能在 Linux 环境安装；
- pytest 与文件编码使用 UTF-8。

## 11. 风险与应对

| 风险 | 影响 | 应对 |
|---|---|---|
| Agent 无法自动停止 | benchmark 超时 | max-turns + timeout + 完成信号检测 |
| 长期记忆导致任务泄漏 | 评测不公平 | benchmark 模式默认禁用长期记忆写入 |
| 文件工具越界访问 | 污染环境 | workspace root 限制 |
| Bash cwd 不一致 | 修改错目录 | runner chdir + 工具 cwd 参数 |
| Windows/Linux 差异 | Docker 运行失败 | pathlib + shell 可配置 + CI smoke test |
| 模型输出空响应 | 进程卡住 | 连续空响应阈值，返回 empty_response |
| hidden tests 无法感知 | 自评不准确 | 明确 exit code 只代表 agent 流程完成，最终由 scorer 判定 |

## 12. 推荐分阶段里程碑

### Milestone 1：Runner 骨架

- 新增 `scripts/run_terminal_bench_agent.py`；
- 支持 `--task-file`、`--workspace`、`--max-turns`、`--timeout`；
- 能构造 prompt 并调用 Engine；
- 有基本异常处理。

验收：mock engine 测试通过。

### Milestone 2：Engine 单任务接口

- 新增或抽取 `run_single_task`；
- 支持 max-turns；
- 支持完成后返回结构化结果。

验收：交互式 CLI 不回退；runner 可以跑完简单任务。

### Milestone 3：Workspace 与副作用隔离

- Bash/File/Pytest 工具确认运行在 workspace；
- benchmark 模式禁用长期记忆写入和自动 Git 提交；
- 输出 artifact 到指定目录。

验收：临时 workspace 测试中无越界修改。

### Milestone 4：Terminal-Bench 真实接入

- 根据 Terminal-Bench 当前版本配置 agent command；
- 跑 1-3 个样例任务；
- 收集日志、失败案例和耗时。

验收：至少一个公开样例任务完成闭环评测。

### Milestone 5：质量优化

- 优化 prompt；
- 加强 Traceback 解析；
- 控制 token 与轮数；
- 加入任务级日志分析；
- 建立 benchmark regression 表。

## 13. 首次实施建议

建议下一步按以下顺序动手：

1. 先新增 runner 文件，但使用 mock / 最小 Engine 调用跑通参数和 cwd；
2. 再抽取 Engine 的 `run_single_task`；
3. 然后写 `tests/test_terminal_bench_runner.py`；
4. 最后构造一个本地 toy workspace 做真实模型 smoke test。

不要一开始就直接接完整 Terminal-Bench harness，否则问题来源会混杂在：Terminal-Bench 配置、runner 参数、Engine 退出、工具 cwd、模型能力等多个层面，排障成本较高。

## 14. 最小验收标准

当以下条件全部满足时，可以认为本项目已完成 Terminal-Bench 最小适配：

- 可以用一条非交互式命令启动 agent；
- 可以指定 task-file 和 workspace；
- agent 所有文件/命令操作默认发生在 workspace；
- agent 能在 max-turns 或 timeout 内退出；
- runner 能输出明确 exit code；
- 有结构化结果 JSON；
- 至少一个本地 toy benchmark 任务通过；
- 有测试覆盖 runner 的关键行为。

## 15. 后续文档更新约定

后续每完成一个里程碑，建议在本文档末尾追加记录：

```text
## 实施记录

### YYYY-MM-DD Milestone X
- 修改文件：...
- 新增测试：...
- 运行命令：...
- 结果：...
- 遗留问题：...
```

这样本文档可以持续作为 Terminal-Bench 接入的工程追踪文档，而不只是一次性方案说明。
