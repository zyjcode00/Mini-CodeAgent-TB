# Terminal-Bench 适配与评测流程指南

本文档记录 Mini Claude Code CLI 作为 Terminal-Bench 非交互式 agent 的实际接入方式、真实 smoke 验证命令、评测环境配置建议与排障流程。

相关实现文件：

- `scripts/run_terminal_bench_agent.py`：Terminal-Bench 非交互式 runner。
- `tests/test_terminal_bench_runner.py`：runner 参数、JSON、异常、超时等单元测试。
- `tests/test_engine_single_task.py`：真实 `AgentEngine.run_single_task` 接口测试。
- `tests/test_terminal_bench_real_smoke.py`：默认跳过、需显式开启的真实端到端 smoke test。
- `docs/terminal_bench_adaptation_plan.md`：较完整的适配方案蓝图。

## 1. 当前适配状态

当前项目已经具备 Terminal-Bench 最小接入闭环：

1. 支持通过命令行传入 task 或 task file。
2. 支持指定任务 workspace。
3. runner 会切换到 workspace 内执行任务。
4. runner 会调用真实 `AgentEngine.run_single_task(...)`。
5. 支持 `--output-json` 输出结构化结果，便于 harness 或 CI 收集。
6. 支持 `--disable-memory` 和 `--disable-auto-commit`，降低 benchmark 运行时的副作用。
7. 已提供默认跳过的真实 smoke test，可在具备模型/API 配置时显式开启。

## 2. 环境变量

真实运行需要可用的模型 API 配置。runner 会按以下顺序读取 API key：

1. `MINI_CLAUDE_API_KEY`
2. `OPENAI_API_KEY`
3. `ANTHROPIC_API_KEY`

可选配置：

| 变量 | 说明 | 默认值 |
|---|---|---|
| `MINI_CLAUDE_API_KEY` | 推荐使用的 API key 变量 | 无 |
| `OPENAI_API_KEY` | OpenAI-compatible key fallback | 无 |
| `ANTHROPIC_API_KEY` | Anthropic key fallback | 无 |
| `MINI_CLAUDE_BASE_URL` | OpenAI-compatible endpoint | `https://api.openai.com/v1` |
| `MINI_CLAUDE_MODEL` | 模型名称 | `gpt-5.5` |
| `MINI_CLAUDE_SESSION` | session id | `terminal-bench` |
| `TERMINAL_BENCH_REAL_SMOKE` | 是否开启真实 smoke test | 默认不开启 |

示例，Windows CMD：

```bat
set MINI_CLAUDE_API_KEY=your_api_key
set MINI_CLAUDE_BASE_URL=https://your-openai-compatible-endpoint/v1
set MINI_CLAUDE_MODEL=your_model_name
```

PowerShell：

```powershell
$env:MINI_CLAUDE_API_KEY="your_api_key"
$env:MINI_CLAUDE_BASE_URL="https://your-openai-compatible-endpoint/v1"
$env:MINI_CLAUDE_MODEL="your_model_name"
```

Linux/macOS：

```bash
export MINI_CLAUDE_API_KEY=your_api_key
export MINI_CLAUDE_BASE_URL=https://your-openai-compatible-endpoint/v1
export MINI_CLAUDE_MODEL=your_model_name
```

## 3. 本地真实 smoke 流程

真实 smoke test 默认跳过，避免普通单测或 CI 意外调用真实模型。需要显式设置：

Windows CMD：

```bat
set TERMINAL_BENCH_REAL_SMOKE=1
pytest tests\test_terminal_bench_real_smoke.py -q
```

PowerShell：

```powershell
$env:TERMINAL_BENCH_REAL_SMOKE="1"
pytest tests/test_terminal_bench_real_smoke.py -q
```

Linux/macOS：

```bash
TERMINAL_BENCH_REAL_SMOKE=1 pytest tests/test_terminal_bench_real_smoke.py -q
```

本轮实测结果：

```text
1 passed in 16.45s
```

说明：首次运行曾发现脚本模式下无法导入项目包 `core`。已在 `scripts/run_terminal_bench_agent.py` 中补充项目根目录到 `sys.path`，修复后真实 smoke 通过。

## 4. 直接运行 runner 的方式

使用内联 task：

```bash
python scripts/run_terminal_bench_agent.py \
  --task "Create a file named hello.txt containing exactly: hello from terminal bench smoke" \
  --workspace /path/to/workspace \
  --max-turns 6 \
  --timeout 120 \
  --output-json /path/to/agent_result.json \
  --disable-memory \
  --disable-auto-commit
```

使用 task file：

```bash
python scripts/run_terminal_bench_agent.py \
  --task-file /path/to/task.txt \
  --workspace /path/to/workspace \
  --max-turns 40 \
  --timeout 1800 \
  --output-json /path/to/agent_result.json \
  --disable-memory \
  --disable-auto-commit
```

Windows 示例：

```bat
python scripts\run_terminal_bench_agent.py ^
  --task-file D:\tmp\tb-task\task.txt ^
  --workspace D:\tmp\tb-task\workspace ^
  --max-turns 40 ^
  --timeout 1800 ^
  --output-json D:\tmp\tb-task\agent_result.json ^
  --disable-memory ^
  --disable-auto-commit
```

## 5. JSON 输出协议

`--output-json` 会写出结构化结果，便于评测 harness 消费。典型字段包括：

```json
{
  "success": true,
  "stop_reason": "completed",
  "turns": 1,
  "message": "...",
  "error": null,
  "workspace": "/path/to/workspace",
  "duration_seconds": 12.34
}
```

建议 harness 至少关注：

- 进程退出码：`0` 表示 runner 认为任务完成。
- `success`：runner 归一化后的成功标记。
- `error`：失败时的错误摘要。
- `workspace`：确认 agent 在正确任务目录内运行。

注意：Terminal-Bench 最终评分通常仍应以任务测试脚本、hidden tests 或文件状态为准，runner JSON 只代表 agent 运行层面的状态。

## 6. Terminal-Bench harness 接入建议

在 Terminal-Bench 配置中，将 agent command 指向本项目 runner。不同版本 Terminal-Bench 的变量名可能不同，以下是模板：

```bash
python /path/to/mini-claude-code-cli/scripts/run_terminal_bench_agent.py \
  --task-file "$TASK_FILE" \
  --workspace "$WORKSPACE" \
  --max-turns 40 \
  --timeout 1800 \
  --output-json "$WORKSPACE/agent_result.json" \
  --disable-memory \
  --disable-auto-commit
```

如果 harness 直接把任务描述作为字符串传入，也可以使用：

```bash
python /path/to/mini-claude-code-cli/scripts/run_terminal_bench_agent.py \
  --task "$TASK" \
  --workspace "$WORKSPACE" \
  --max-turns 40 \
  --timeout 1800 \
  --output-json "$WORKSPACE/agent_result.json" \
  --disable-memory \
  --disable-auto-commit
```

推荐顺序：

1. 先跑普通 runner 单测。
2. 再显式开启真实 smoke test。
3. 然后用本地 toy workspace 直接运行 runner。
4. 最后接完整 Terminal-Bench harness / Docker。

不要一开始直接接完整 harness，否则失败来源会混在 Terminal-Bench 配置、Docker 路径、runner 参数、模型配置、工具 cwd、项目导入路径等多个层面。

## 7. Docker / Linux 注意事项

Terminal-Bench 常在 Linux 或 Docker 环境中运行，而当前项目目录在 Windows 下开发。迁移到 Docker/Linux 时重点检查：

1. 路径分隔符：使用 `/path/to/...`，不要硬编码 Windows 盘符。
2. Python 入口：优先使用容器内的 `python` 或绝对解释器路径。
3. 项目挂载：确保 `/path/to/mini-claude-code-cli` 在容器内可读。
4. workspace 权限：确保 agent 对 workspace 有读写权限。
5. API 环境变量：通过 Docker `-e` 或 harness secret 注入。
6. 网络访问：容器需要能访问模型 endpoint。
7. 输出文件：`--output-json` 路径应位于 workspace 或 harness artifacts 目录中。

Docker 命令模板：

```bash
docker run --rm \
  -e MINI_CLAUDE_API_KEY="$MINI_CLAUDE_API_KEY" \
  -e MINI_CLAUDE_BASE_URL="$MINI_CLAUDE_BASE_URL" \
  -e MINI_CLAUDE_MODEL="$MINI_CLAUDE_MODEL" \
  -v /host/mini-claude-code-cli:/app \
  -v /host/task-workspace:/workspace \
  -w /app \
  python:3.11 \
  python scripts/run_terminal_bench_agent.py \
    --task-file /workspace/task.txt \
    --workspace /workspace \
    --output-json /workspace/agent_result.json \
    --disable-memory \
    --disable-auto-commit
```

## 8. 推荐校验命令

常规单测，不触发真实模型：

```bash
pytest tests/test_terminal_bench_runner.py tests/test_engine_single_task.py tests/test_terminal_bench_real_smoke.py -q
```

预期：真实 smoke 被 skip，例如：

```text
14 passed, 1 skipped
```

真实 smoke：

```bash
TERMINAL_BENCH_REAL_SMOKE=1 pytest tests/test_terminal_bench_real_smoke.py -q
```

Windows CMD：

```bat
cmd /c "set TERMINAL_BENCH_REAL_SMOKE=1&& pytest tests\test_terminal_bench_real_smoke.py -q"
```

## 9. 常见问题排障

### 9.1 `No module named 'core'`

现象：

```text
RuntimeError: Unable to import project AgentEngine dependencies: No module named 'core'
```

原因：直接以脚本路径运行 `scripts/run_terminal_bench_agent.py` 时，Python 默认把 `scripts/` 加入 `sys.path`，但不一定包含项目根目录。

当前状态：已修复。runner 启动时会将项目根目录加入 `sys.path`。

### 9.2 缺少 API key

现象：

```text
Missing API key for AgentEngine. Set MINI_CLAUDE_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY.
```

解决：设置 `MINI_CLAUDE_API_KEY`，或设置兼容的 `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`。

### 9.3 模型 endpoint 不兼容

检查：

- `MINI_CLAUDE_BASE_URL`
- `MINI_CLAUDE_MODEL`
- API key 是否匹配 endpoint
- endpoint 是否为 OpenAI-compatible chat/completions 或项目当前 Engine 支持的格式

### 9.4 任务通过 runner 但 Terminal-Bench 评分失败

runner 成功只说明 agent 进程完成，不等于 benchmark 任务通过。需要检查：

1. workspace 中实际文件是否符合任务要求。
2. Terminal-Bench 的 visible tests / hidden tests 是否通过。
3. agent 是否把文件写到了错误目录。
4. harness 传入的 workspace 变量是否正确。
5. 是否有权限或路径挂载问题。

## 10. 正式 harness 接入前检查清单

在接入 Terminal-Bench 官方或自建 harness 前，建议先确认以下配置项，避免把 runner、Docker、任务变量和模型配置问题混在一起排查。

### 10.1 Agent command 模板

优先使用 `--task-file` 方式传入任务说明，并把 `--output-json` 写到 harness 可收集的 artifacts 目录或 workspace 内：

```bash
python /path/to/mini-claude-code-cli/scripts/run_terminal_bench_agent.py   --task-file "${TASK_FILE}"   --workspace "${WORKSPACE}"   --max-turns "${MAX_TURNS:-40}"   --timeout "${AGENT_TIMEOUT:-1800}"   --output-json "${ARTIFACT_DIR:-${WORKSPACE}}/agent_result.json"   --disable-memory   --disable-auto-commit
```

如果当前 harness 不提供 `TASK_FILE`，可以在 harness wrapper 中先把任务描述写入临时文件，再调用上述命令；也可以使用 `--task "${TASK}"`，但需要注意 shell quoting 和多行文本转义。

### 10.2 必填变量映射

| 变量 | 来源 | 传给 runner 的参数 | 检查点 |
|---|---|---|---|
| 任务说明文件 | Terminal-Bench task instruction / prompt file | `--task-file` | 文件在容器内可读，内容非空 |
| 任务工作目录 | Terminal-Bench task workspace / repo path | `--workspace` | 目录存在且可读写 |
| 结果目录 | harness artifacts 目录或 workspace | `--output-json` | 父目录存在且 harness 会保留该文件 |
| 最大轮数 | harness 配置或默认值 | `--max-turns` | 建议先用 20-40 做样例验证 |
| 超时时间 | harness 配置或默认值 | `--timeout` | 应小于外层 harness/container 超时 |
| 模型凭据 | secret/env 注入 | 环境变量 | 至少设置 `MINI_CLAUDE_API_KEY` 或兼容 fallback |

### 10.3 首次正式验证步骤

1. 选择 1 个最小样例任务，确认 workspace 中 visible tests 可手动运行。
2. 在同一个 workspace 内手动执行 agent command，确认 `agent_result.json` 能生成。
3. 检查 JSON 中的 `workspace` 是否等于 harness 传入目录，避免 cwd 错位。
4. 再由 Terminal-Bench harness 调用同一条命令，比较手动运行与 harness 运行的环境变量、挂载路径和退出码。
5. 扩展到 1-3 个官方或本地样例任务，记录失败类型：任务未完成、测试失败、路径错误、超时、API/网络错误或 artifact 未收集。

### 10.4 推荐验收标准

正式 harness 接入可视为跑通的最低标准：

- harness 能以非交互方式启动 `scripts/run_terminal_bench_agent.py`；
- runner 进程能在外层超时前退出；
- workspace 内的文件变更由 Terminal-Bench scorer / hidden tests 正常检测；
- `agent_result.json` 被保留下来，失败时包含 `error` 字段；
- 至少 1 个 toy task 或官方样例任务在完整 harness 链路中通过。

## 11. 当前结论

当前 Mini Claude Code CLI 已完成 Terminal-Bench 最小适配：

- 非交互 runner 可直接作为 harness agent command。
- 单元测试覆盖 runner 的核心行为。
- 真实 smoke test 在本地显式开启后通过。
- 文档已补齐本地验证、真实 smoke、JSON 输出、harness 接入、Docker/Linux 注意事项与排障流程。

下一阶段建议选取 1-3 个 Terminal-Bench 官方或本地样例任务，在真实 harness 中验证：

1. 任务注入变量是否正确。
2. workspace 权限和 cwd 是否正确。
3. hidden tests 执行链路是否正确。
4. runner JSON artifact 是否被保存。
5. 失败时日志是否足以定位问题。
