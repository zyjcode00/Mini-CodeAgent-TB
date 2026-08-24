# Executor Shutdown Recovery 修复说明

## 背景

Terminal-Bench 非交互任务中曾出现 `cannot schedule new futures after shutdown`。该错误并非普通命令失败，而是底层 `ThreadPoolExecutor` 已进入关闭状态，后续工具调用仍尝试提交新的 future。若继续重试，会重复触发同一错误并消耗任务超时时间，最终表现为 Agent 超时且没有生成可评测产物。

## 根因

工具执行层在发现 executor 已关闭后，需要把底层 `RuntimeError` 转换为明确的、不可重试的领域异常。上层 Agent 还需要识别该异常并立即结束当前任务。此前 `AgentEngine.run_single_task()` 只返回通用错误字段，没有稳定的停止原因，因此调用方无法区分：

- 正常完成；
- Agent 达到内部思考步数上限；
- executor 已关闭且无法继续执行；
- 其他执行异常。

## 修改内容

### 1. executor 错误快速失败

`tools/execution_backend.py` 定义并抛出 `ExecutorShutdownError`。只有错误消息明确包含 `cannot schedule new futures after shutdown` 时才进行转换，其他 `RuntimeError` 保持原样抛出，避免误分类。

该异常表示执行器生命周期已经结束，不应由上层重新提交命令或进行无条件重试。

### 2. 单任务结果契约稳定化

`core/engine.py` 的 `run_single_task()` 现在始终提供 `stop_reason`：

- `completed`：任务正常返回；
- `max_turns`：Agent 返回内部思考步数限制结果；
- `executor_shutdown`：底层 executor 已关闭；
- `execute_query_error`：其他执行异常。

对于 shutdown 错误，结果保留完整的 `ExecutorShutdownError: ...` 错误信息，并将 `success` 设为 `False`。该路径不再触发重试。

### 3. 内部步数上限显式失败

当真实执行返回 `任务达到最大思考步数限制。` 时，单任务 API 将其标记为失败，并返回稳定的英文错误说明，避免把未完成任务误报为成功。

## 回归测试

执行命令：

```bash
pytest tests/test_engine_single_task.py
```

结果：`11 passed`。

覆盖范围包括：

- 成功任务的结果封装与 prompt 清理；
- 内部思考步数上限识别；
- 普通 `execute_query` 异常；
- `ExecutorShutdownError` 的不可重试快速失败；
- 空 prompt 和非法 `max_turns` 参数校验。

## 运维建议

1. 将 `executor_shutdown` 视为任务级终止信号，不要在同一已关闭 session 上继续提交工具调用。
2. 评测 runner 在收到 `executor_shutdown` 后应停止当前 Agent，记录错误，并创建新的 session 或新的 executor 后再做有限次数重试。
3. 每个阶段都验证产物：构建完成、安装完成、命令可用、输出文件存在。不要只依赖总超时判断任务结果。
4. 对 `execute_query_error` 和 `executor_shutdown` 分开统计，以便区分业务错误与执行器生命周期错误。
5. 长时间 LLM 或工具调用仍应有独立 timeout；timeout 清理后必须保证不会继续向已关闭 executor 提交工作。

## 影响范围

本修复只改变非交互单任务 API 的结果分类和 executor 关闭错误的传播方式，不改变正常 `execute_query()` 的执行流程。调用方如果只依赖 `success`、`final_answer`、`error` 字段，仍可兼容运行；需要可靠调度和重试策略的调用方应使用新增的 `stop_reason` 字段。
