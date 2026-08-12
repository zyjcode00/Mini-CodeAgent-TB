# Terminal-Bench 接入进展执行清单

> 目标：将当前 Terminal-Bench 接入状态整理为一页可执行清单，便于后续联调、验证和推进。

## 一、当前进展

Mini Claude Code CLI 已完成 Terminal-Bench 最小适配闭环，具备作为非交互式 agent runner 的基础能力：

- 支持通过 `--task` / `--task-file` 输入任务
- 支持指定 `--workspace`
- runner 会切换到 workspace 内执行
- runner 会调用真实 `AgentEngine.run_single_task(...)`
- 支持 `--output-json` 输出结构化结果
- 支持 `--disable-memory`、`--disable-auto-commit` 降低副作用
- 已有默认跳过、可显式开启的真实 smoke test
- 真实 smoke 中的 `No module named 'core'` 导入问题已修复

## 二、已完成事项

1. 已实现非交互式 runner：`scripts/run_terminal_bench_agent.py`
2. 已补充核心单测：
   - `tests/test_terminal_bench_runner.py`
   - `tests/test_engine_single_task.py`
   - `tests/test_terminal_bench_real_smoke.py`
3. 已验证真实 smoke 通过
4. 已修复脚本模式下项目根目录导入问题
5. 已补齐本地运行、JSON 输出、Docker/Linux 兼容和排障文档

## 三、待完成事项

### 1. 真实 Terminal-Bench harness 联调
需要在真正的 Terminal-Bench 执行环境中验证：

- 任务变量注入是否正确
- workspace 挂载是否正确
- cwd 是否正确
- hidden tests 是否可正常触发
- `agent_result.json` 是否可被收集

### 2. 1-3 个样例任务验证
建议先跑最小样例，再扩展到官方或本地样例任务：

- 任务是否完成
- 是否写到了正确目录
- 是否出现超时
- 是否出现 API / 网络 / 路径 / artifact 问题

### 3. 副作用隔离进一步确认
重点确认 benchmark 模式下默认关闭：

- 长期记忆写入
- 自动 Git 提交

### 4. 进一步增强 workspace 安全
后续可继续补强：

- 文件工具防止 `..` 越界
- Bash cwd 显式可控
- 日志路径相对 workspace 记录

## 四、下一步执行计划

### Step 1：本地最小环境复核
用 toy workspace 再跑一次 runner，确认：

- `--task-file`
- `--workspace`
- `--max-turns`
- `--timeout`
- `--output-json`

都工作正常。

### Step 2：接入 Terminal-Bench harness
将 agent command 指向：

```bash
python scripts/run_terminal_bench_agent.py ...
```

先只跑 1 个最小样例任务。

### Step 3：分类记录失败原因
如果失败，按以下维度记录：

- 路径错误
- cwd 错误
- timeout
- API / 网络错误
- artifact 未收集
- hidden tests 失败

### Step 4：根据联调结果补强
如发现问题，再补：

- workspace 越界限制
- 更严格退出条件
- 更稳定的日志与 JSON 输出
- 记忆 / Git 副作用控制

## 五、推荐验收标准

满足以下条件可认为接入推进到下一阶段：

- harness 能非交互式启动 runner
- runner 能在外层超时前退出
- workspace 内修改可被 scorer 或 hidden tests 识别
- `agent_result.json` 能保留
- 至少 1 个样例任务在完整链路中通过

## 六、当前结论

当前 Mini Claude Code CLI 已具备 Terminal-Bench 最小接入能力，下一阶段重点不在于继续补基础功能，而在于：

1. 真实 harness 联调
2. 样例任务验证
3. 副作用隔离与稳定性增强
