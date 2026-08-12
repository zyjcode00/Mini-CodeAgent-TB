# Terminal-Bench 评测通过复盘

## 背景
本次修改的目标，是让 mini-claude-code-cli 作为 Terminal-Bench 的非交互式 agent，在真实评测环境中更稳妥地完成任务启动前准备，并修复此前 Debian 12 / uv 镜像相关的环境兼容问题。

## 做了什么修改

### 1. 增强任务前环境初始化命令
在 `terminal_bench_adapter.py` 中，将原来的单一 apt 换源命令扩展为一段完整的 setup 脚本：

- 保留任务执行前的环境准备入口
- 兼容 Debian 12 常见的两种源配置：
  - `/etc/apt/sources.list`
  - `/etc/apt/sources.list.d/debian.sources`
- 将 `deb.debian.org` / `deb.debian.org/debian-security` 替换为国内镜像
- 同步创建 `/root/.config/uv/uv.toml`
- 为 uv 指定 PyPI 镜像，减少安装依赖时的网络失败概率

### 2. 补充测试覆盖
在 `tests/test_terminal_bench_adapter.py` 中新增测试，验证：

- setup 命令中包含 `set -e`
- 命令同时覆盖 `sources.list` 和 `debian.sources`
- 命令包含 apt 镜像替换内容
- 命令会写入 uv 配置文件
- uv 配置里包含镜像地址

### 3. 保持原有行为不变
除了增强启动前 setup 命令外，其他 agent 行为保持不变：

- 仍然通过 Terminal-Bench 兼容的 import path 暴露
- 仍然支持 `max_turns`、`model`、`task_ids` 等参数
- 仍然会在执行任务前先跑 setup 命令，再进入主推理流程

## 验证结果
执行以下测试通过：

```bash
pytest tests/test_terminal_bench_adapter.py
```

结果：

- 14 passed

另外，`python -m py_compile terminal_bench_adapter.py` 也已通过。

## 这次修复的关键点
之前评测失败的核心原因，不是业务逻辑本身，而是运行环境准备不够稳：

- Debian 12 下 apt 源配置形式可能不是传统的 `sources.list`
- uv 拉包会受默认网络环境影响
- 所以前置 setup 需要同时兼顾 apt 和 uv 的镜像配置

## 后续建议
如果后面还要继续优化 Terminal-Bench 适配，建议继续关注：

- 更细粒度的环境探测与换源策略
- 对不同 Debian/Ubuntu 镜像格式的兼容性
- 真实评测中各阶段日志的可读性与可追踪性
