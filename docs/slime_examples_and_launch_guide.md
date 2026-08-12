# slime 官方 examples 与 train/train_async 启动代码详解

本文面向已经能找到 `D:\LLM\Agentic-RL\slime` 源码的读者，解释 slime 官方示例目录的组织方式，以及这些示例最终如何落到 `train.py` / `train_async.py` 两个启动入口上。

> 说明：本文是源码阅读笔记，重点帮助你建立“示例脚本参数 → 启动入口 → Ray 资源编排 → rollout/training actor → 数据与权重同步”的整体心智模型。

## 1. slime 是什么

slime 是一个面向大模型强化学习训练的框架，重点优化 **Megatron 训练后端 + SGLang rollout 后端** 的大规模 RL 工作流。它的核心设计不是把所有推理/训练后端都抽象成最小公共接口，而是围绕生产中常见的大规模 RL 需求，显式处理：

- Ray 资源调度与 placement group；
- actor / rollout worker 的生命周期；
- prompt 采样、response 生成、reward / advantage 计算；
- Megatron 训练循环；
- SGLang 推理服务、router、权重同步；
- 同步训练与异步训练两种执行模式；
- rollout-only / train-only 等调试模式。

## 2. examples 目录应该怎么看

官方 `examples` 目录通常不是“独立小 demo”，而是一组可运行训练配方。它们一般由 shell 脚本、任务定制代码和配置参数组成。

### 2.1 示例脚本的共同结构

典型 example 启动脚本通常会做这些事：

1. 设置基础路径：模型路径、数据路径、保存路径、日志路径。
2. 设置集群资源：节点数、每节点 GPU 数、训练 actor 数、rollout actor 数。
3. 选择运行入口：同步训练走 `python train.py`，异步训练走 `python train_async.py`。
4. 传入 Megatron 相关参数：tensor/pipeline parallel、micro/global batch、sequence length、optimizer、checkpoint 等。
5. 传入 rollout/SGLang 参数：rollout batch size、采样温度、top-p、最大生成长度、服务端口、router/engine 配置、权重同步策略等。
6. 传入 RL 算法参数：GRPO/PPO 类参数、advantage estimator、KL、reward、采样次数等。
7. 可选地传入任务自定义模块：例如自定义数据读取、reward function、agent workflow。

换句话说，examples 里大多数 shell 文件的价值不在“写了多少 Python 逻辑”，而在于把一次 RL 训练需要的几十到上百个参数固定成可复现的命令行配方。

### 2.2 示例类型

从 slime 的定位看，examples 可以粗略分成几类：

- **基础 RL 训练示例**：展示如何从模型、数据和算法参数启动一次完整训练。
- **rollout / train 分离调试示例**：帮助定位生成侧或训练侧问题，避免 RL 全链路过长导致难排错。
- **特定模型示例**：针对 DeepSeek、Kimi、Qwen 等模型族准备并行、权重转换、checkpoint 参数。
- **agentic workflow 示例**：在 rollout 中引入工具调用、环境交互、多轮 agent 过程，再把结果送回训练。
- **benchmark / eval 相关示例**：用于特定任务集的评测、reward 或数据格式适配。

### 2.3 读 example 的建议顺序

建议按如下顺序阅读一个官方示例：

1. 先看脚本最后一行到底调用 `train.py` 还是 `train_async.py`。
2. 再看数据、模型、保存目录相关变量。
3. 然后看资源参数：多少节点、多少 GPU、训练和 rollout 分别占多少。
4. 接着看 batch / sequence / generation 参数。
5. 最后看是否引用了自定义 Python 模块，例如 reward、dataset、agent、sandbox。

这样读能快速判断这个示例是“通用训练模板”，还是“某个任务/模型的定制配方”。

## 3. `train.py`：同步训练入口

`train.py` 是 slime 的同步训练入口。它的核心流程可以理解为：

```text
解析命令行参数
  ↓
初始化日志、Ray、随机种子等运行环境
  ↓
创建 Ray placement groups
  ↓
创建 rollout manager / training models
  ↓
进入同步 RL 训练循环
  ↓
每轮：rollout 生成 → 计算训练数据 → trainer 更新 → 同步新权重给 rollout
```

### 3.1 参数解析

入口会通过 `slime.utils.arguments.parse_args` 解析命令行。examples 中传入的大量 `--xxx` 参数都会汇总到一个 args 对象中。

这些参数大致分为：

- 训练参数：batch size、epoch、学习率、checkpoint、Megatron 并行策略；
- rollout 参数：每个 prompt 采样数、采样温度、最大 response 长度、SGLang 服务参数；
- Ray 参数：节点、GPU、placement group、actor 数；
- RL 参数：advantage、reward、KL、loss 相关开关；
- 调试参数：rollout-only、train-only、profile、trace、dump 数据等。

### 3.2 Ray 资源编排

`train.py` 会调用 `slime.ray.placement_group` 中的工具创建资源布局。核心思想是：

- 训练 worker 和 rollout worker 都是 Ray actor；
- placement group 用来保证这些 actor 按预期绑定 GPU/节点资源；
- 训练侧通常由 Megatron actor group 管理；
- rollout 侧通常由 SGLang engine/router/manager 相关 actor 管理。

这一步非常关键，因为大规模 RL 中“代码逻辑正确但资源摆放不对”会直接导致性能差、通信失败或权重同步异常。

### 3.3 创建 rollout manager

rollout manager 负责生成训练样本。它通常要处理：

- 从 prompt dataset 中取样；
- 调用 SGLang 服务生成 response；
- 管理多采样、多轮 agent、工具调用等复杂 rollout；
- 执行 reward function 或收集外部环境反馈；
- 组装最终训练需要的数据结构。

在同步模式里，rollout manager 每轮生成的数据会被训练侧消费，训练完成后再进入下一轮。

### 3.4 创建 training models

training models 对应 Megatron 后端。它们负责：

- 加载初始模型或 checkpoint；
- 接收 rollout 产生的数据；
- 执行 forward / loss / backward / optimizer step；
- 产出训练指标；
- 在必要时保存 checkpoint；
- 把更新后的权重同步给 rollout 侧。

### 3.5 同步模式的特点

同步训练的语义最容易理解：

```text
第 k 轮 rollout 使用第 k 版权重生成数据
第 k 轮 train 使用这些数据更新到第 k+1 版权重
第 k+1 轮 rollout 再使用新权重
```

优点：

- 数据和权重版本关系清晰；
- 调试简单；
- 更适合首次跑通 pipeline。

缺点：

- rollout 和 train 可能互相等待；
- 在生成很慢或训练很慢时，GPU 利用率可能不理想。

## 4. `train_async.py`：异步训练入口

`train_async.py` 面向更高吞吐的异步 RL 训练。它和 `train.py` 使用很多相同组件，但调度方式不同。

可以理解为：

```text
解析参数 / 初始化环境 / 创建资源
  ↓
启动训练 actor 与 rollout actor
  ↓
rollout 持续生成数据，放入队列或缓冲区
  ↓
training 持续消费数据并更新模型
  ↓
按策略将新权重同步给 rollout 侧
```

### 4.1 与同步入口的共同点

`train_async.py` 仍然会做：

- parse args；
- 初始化 Ray；
- 创建 placement groups；
- 创建 rollout manager；
- 创建 training actors；
- 管理日志、checkpoint、profile、trace。

因此，examples 中很多参数在同步/异步两种入口下是复用的。

### 4.2 异步模式的核心差异

异步模式的关键是解耦 rollout 和 train：

- rollout 不必等待每次训练 step 完成后再继续生成；
- train 不必等待完整一轮 rollout 全部完成后才开始训练；
- 数据通过队列、buffer 或 remote object 在 Ray actor 之间流动；
- 权重同步不一定每个 step 都做，而是按频率、版本或调度策略触发。

这能提高吞吐，但也带来新的工程问题：

- rollout 数据可能来自稍旧的 policy；
- 需要处理 policy version / stale data；
- 队列容量和 backpressure 会影响稳定性；
- 权重同步频率需要在性能和 on-policy 程度之间折中。

### 4.3 什么时候用异步入口

建议：

- 第一次跑官方示例：优先用 `train.py` 同步入口。
- 已经确认数据、reward、模型并行、SGLang 服务都能跑通：再切到 `train_async.py`。
- rollout 特别慢、训练侧经常等待：考虑异步。
- 需要最大化集群吞吐：考虑异步，但要额外关注指标稳定性。

## 5. examples 参数如何映射到启动代码

下面按功能解释常见参数最终会影响哪里。

### 5.1 资源类参数

这类参数影响 placement group 和 Ray actor 创建：

- 节点数；
- 每节点 GPU 数；
- training actor 数；
- rollout actor 数；
- 每个 actor 使用多少 GPU；
- colocate / disaggregate 策略。

它们最终决定：训练和推理是否共用节点、每个 worker 绑定哪些 GPU、是否能满足 Megatron/SGLang 的并行要求。

### 5.2 Megatron 类参数

这类参数进入 training actor：

- tensor model parallel；
- pipeline model parallel；
- expert parallel；
- sequence length；
- micro batch size；
- global batch size；
- optimizer / lr schedule；
- checkpoint load/save；
- bf16/fp8 等精度配置。

如果这些参数与模型结构或 GPU 数不匹配，通常会在训练初始化阶段报错。

### 5.3 SGLang / rollout 类参数

这类参数进入 rollout manager 或 SGLang 后端：

- prompt batch size；
- 每个 prompt 生成几个 response；
- max response length；
- temperature / top-p / top-k；
- SGLang server、router、engine 参数；
- weight sync endpoint / frequency；
- agent workflow 相关参数。

如果这些参数不合理，可能表现为生成过慢、OOM、response 截断、服务连接失败或吞吐异常。

### 5.4 RL 算法参数

这类参数影响 rollout 后处理和训练 loss：

- reward function；
- advantage estimator；
- KL coefficient；
- clip range；
- entropy / loss 相关系数；
- group size / samples per prompt。

例如 GRPO 类训练通常依赖同一 prompt 的多条 response 来做组内归一化或 advantage 计算，所以 examples 中的采样数量并不只是推理参数，也会改变训练语义。

## 6. 一次完整同步训练的链路

以 `train.py` 为例，完整链路可以概括为：

```text
example shell
  ↓ 传入命令行参数
train.py
  ↓ parse_args
args
  ↓ 创建 placement groups
Ray resources
  ↓ 创建 rollout manager + training actor group
rollout / trainer actors
  ↓ rollout 生成 samples
prompt + response + reward + metadata
  ↓ training actor 消费 batch
loss / backward / optimizer
  ↓ checkpoint + metrics
保存模型与日志
  ↓ weight sync
SGLang rollout 侧使用新权重
```

排错时也可以按这个链路反向定位：

- 启动即失败：看参数、环境、import、Ray 初始化。
- actor 创建失败：看 GPU 数、placement group、并行配置。
- rollout 失败：看 SGLang 服务、数据格式、reward/agent 代码。
- train 失败：看 Megatron 参数、batch/sequence、checkpoint。
- 指标异常：看 reward、advantage、KL、数据是否 stale。

## 7. 一次完整异步训练的链路

以 `train_async.py` 为例：

```text
example shell
  ↓
train_async.py
  ↓
初始化 Ray resources / actors
  ↓
rollout producer 持续生成数据
  ↓
数据进入 buffer / queue
  ↓
trainer consumer 持续取数据更新模型
  ↓
周期性 checkpoint / metric / weight sync
  ↓
rollout producer 使用较新权重继续生成
```

异步模式排错除了同步模式的问题外，还要额外关注：

- queue 是否堆积；
- rollout 是否跑得太快导致数据过旧；
- trainer 是否因为数据不足而等待；
- 权重同步是否成功；
- 版本号、step、metric 是否能对齐。

## 8. 如何新增自己的 example

可以按官方 example 的方式新建一个目录：

```text
examples/my-task/
  train.sh
  README.md
  reward.py          # 可选
  dataset.py         # 可选
  agent.py           # 可选
```

建议步骤：

1. 复制一个最接近的官方 shell 脚本。
2. 只改模型路径、数据路径、输出路径，先跑最小规模。
3. 保持同步入口 `train.py`，确认全链路能跑通。
4. 加入自己的 reward / agent 逻辑。
5. 打开 dump/trace/profile 之类调试开关检查中间样本。
6. 扩大 batch 和资源规模。
7. 最后再考虑切换到 `train_async.py`。

## 9. 常见坑

- **模型并行参数与 GPU 数不匹配**：Megatron 初始化失败或 hang。
- **rollout 和 train 资源抢占**：placement group 配置不合理导致 actor 起不来。
- **SGLang 权重未同步成功**：训练指标变化但生成质量不变。
- **reward 代码异常被吞掉或延迟暴露**：建议先 rollout-only 调试。
- **异步数据过旧**：吞吐提高但训练不稳定。
- **路径写死**：官方脚本常假设特定 Docker、挂载路径和模型目录，迁移到本机要逐项检查。

## 10. 阅读源码时的关键文件

建议结合以下文件理解：

- `train.py`：同步训练主入口。
- `train_async.py`：异步训练主入口。
- `slime/utils/arguments.py`：命令行参数定义与默认值。
- `slime/ray/placement_group.py`：Ray 资源布局。
- `slime/ray/actor_group.py`：Ray actor group 管理。
- `slime/ray/rollout.py`：rollout 管理、生成、后处理。
- `slime/backends/megatron_utils/actor.py`：Megatron training actor。
- `slime/backends/megatron_utils/model.py`：模型训练与权重相关逻辑。
- `examples/**`：官方训练配方。

## 11. 总结

- `examples` 是可复现训练配方，核心是参数组合和任务定制。
- `train.py` 是同步入口，适合先跑通和调试。
- `train_async.py` 是异步入口，适合提高吞吐，但需要关注 stale data、buffer 和权重同步。
- slime 的主线是：Ray 编排资源，SGLang 做 rollout，Megatron 做训练，二者通过数据流和权重同步形成 RL 闭环。
