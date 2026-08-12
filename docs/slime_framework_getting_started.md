# slime 框架入门理解文档

> 目标：帮助快速理解 `D:\LLM\Agentic-RL\slime` 项目的定位、代码结构、训练/rollout 主流程，以及后续二次开发时应该从哪里入手。

## 1. 项目一句话理解

`slime` 是一个面向大模型强化学习训练的分布式框架，核心目标是把 **训练后端 Megatron**、**推理/rollout 后端 SGLang**、**Ray 分布式编排** 和 **RL 数据流** 连接起来，用于 GRPO、DAPO、tool-use、多轮 agent、VLM、多任务评测等场景。

从工程视角看，它不是一个单纯算法仓库，而是一个“训练-推理解耦/协同”的 RL 系统框架：

```text
数据集 / prompt
   ↓
Ray Rollout Manager
   ↓
SGLang 推理服务生成 response
   ↓
Reward / Filter / Advantage 处理
   ↓
Ray Train Actors
   ↓
Megatron 后端训练更新 actor 模型
   ↓
权重同步到 SGLang rollout 引擎
   ↓
进入下一轮 rollout
```

## 2. 适合先建立的心智模型

理解 slime 时建议抓住 4 个关键词：

1. **Ray 编排**：负责创建训练 actor、rollout actor、placement group、远程调用和资源分配。
2. **Megatron 训练**：负责真正的分布式模型训练、并行配置、checkpoint、权重更新。
3. **SGLang rollout**：负责高吞吐生成 response，并返回 token、logprob、meta 信息。
4. **Sample 数据流**：prompt、response、tokens、reward、loss mask、truncated/aborted 状态都围绕 `Sample` 对象流转。

如果只看算法公式会比较难入手；更有效的方式是沿着一次 rollout + train 迭代追踪数据如何流动。

## 3. 顶层目录速览

仓库主要目录大致如下：

```text
slime/
  slime/
    backends/        # 训练/推理后端适配，尤其是 Megatron、SGLang 相关逻辑
    ray/             # Ray actor、资源组、训练/rollout manager、主流程编排
    rollout/         # rollout 函数、reward model、filter、SGLang 生成逻辑
    utils/           # 参数、数据、类型、分布式、HTTP、tokenizer/processor 等工具
  examples/          # 不同任务/特性的示例脚本
  scripts/           # 启动、部署、辅助脚本
  tests/             # 测试
  docs/              # 官方文档
```

最值得优先看的目录是：

- `slime/ray/`：理解系统如何跑起来。
- `slime/rollout/`：理解样本如何生成、打分、过滤。
- `slime/backends/`：理解训练/推理后端如何接入。
- `examples/`：理解实际任务如何配置和启动。

## 4. 核心模块说明

### 4.1 `slime/ray/`：分布式控制层

这个目录是 slime 的“调度大脑”。

重点文件：

- `slime/ray/actor_group.py`：封装一组 Ray actors，提供批量调用、并行执行、资源绑定等能力。
- `slime/ray/placement_group.py`：负责 Ray placement group 资源规划，让训练和 rollout actors 按 GPU/节点布局。
- `slime/ray/train_actor.py`：训练 actor 抽象基类，初始化 torch distributed、设置 rank/world size/local rank、提供训练/保存/权重更新接口。
- `slime/ray/rollout.py`：rollout manager 侧逻辑，负责调用 rollout 函数、管理生成、评测、权重同步相关流程。
- `slime/ray/ray_actor.py`：Ray actor 的基础能力封装。

可以把它理解为：

```text
placement_group.py 决定资源怎么摆
actor_group.py 管一组远程 actors 怎么调
train_actor.py 定义训练 worker 怎么初始化和工作
rollout.py 管生成、评测、训练数据准备
```

### 4.2 `slime/rollout/`：生成与奖励数据层

这个目录负责把 prompt 变成 RL 训练需要的样本。

重点文件：

- `slime/rollout/sglang_rollout.py`：通过 SGLang router/server 发起 `/generate` 请求，拿到 response tokens、logprobs、meta_info，并调用 reward/filter。
- `slime/rollout/base_types.py`：定义 rollout 函数的标准输出类型：`RolloutFnTrainOutput` 和 `RolloutFnEvalOutput`。
- `slime/rollout/rm_hub/`：reward model / reward function 相关实现。
- `slime/rollout/filter_hub/`：动态过滤逻辑，例如按 reward、长度、完成状态过滤样本。

`sglang_rollout.py` 是理解 rollout 的关键：

1. 用 tokenizer/processor 准备 prompt ids 或多模态输入。
2. 向 SGLang router 的 `/generate` 发送请求。
3. 解析生成文本、output token logprobs、停止原因、路由专家等 meta 信息。
4. 更新 `Sample` 的 `tokens`、`response`、`response_length`、`rollout_log_probs`。
5. 调 reward 函数或 batched reward。
6. 返回训练或评测格式的数据。

### 4.3 `slime/backends/`：后端适配层

后端目录承担“对接具体训练/推理系统”的职责。

常见关注点包括：

- Megatron 训练 actor 的具体实现。
- SGLang server/router 的启动与控制。
- 权重同步：训练后的 actor 权重如何更新到 rollout 引擎。
- 不同精度、并行策略、训练推理解耦部署。

如果你要改训练行为，通常会进入 Megatron backend；如果你要改推理服务控制或 SGLang 交互，通常会进入 SGLang backend/util。

### 4.4 `slime/utils/`：公共工具层

这个目录包含大量胶水能力：

- 参数解析与配置。
- dataset/sample 类型。
- tokenizer/processor 加载。
- HTTP 请求封装。
- torch/ray 分布式工具。
- tracing/logging/memory 工具。

其中 `slime/utils/types.py` 里的 `Sample` 很重要，它是 rollout 与训练之间传递样本状态的核心结构。

## 5. 一次训练迭代的大致流程

从宏观上看，一轮 RL 训练可以拆成以下步骤：

```text
1. 初始化 Ray 集群资源
2. 创建训练 actors 和 rollout actors/manager
3. 启动或连接 SGLang rollout 服务
4. 从 dataset 取 prompt batch
5. rollout 函数生成多个 response
6. reward function / reward model 打分
7. filter 过滤无效或低质量样本
8. 组织成训练 batch
9. Megatron actor 执行 train
10. 保存 checkpoint 或同步权重
11. rollout 引擎加载/接收新权重
12. 进入下一轮
```

对应代码心智图：

```text
Ray 层
  ├─ 创建资源：placement_group.py
  ├─ 管理 actors：actor_group.py
  ├─ 训练 worker：train_actor.py + backend actor
  └─ rollout manager：rollout.py

Rollout 层
  ├─ 生成：sglang_rollout.py
  ├─ 样本结构：utils/types.py::Sample
  ├─ 输出协议：rollout/base_types.py
  ├─ 奖励：rollout/rm_hub/
  └─ 过滤：rollout/filter_hub/

Backend 层
  ├─ Megatron 训练
  ├─ SGLang 服务控制
  └─ 权重同步
```

## 6. `Sample` 是理解数据流的关键

在 slime 中，训练数据不是简单的字符串列表，而是带状态的 `Sample`。

它通常会承载：

- `prompt`：输入问题或对话上下文。
- `response`：模型生成内容。
- `tokens`：prompt + response token ids。
- `response_length`：生成长度。
- `reward`：奖励分数。
- `loss_mask`：哪些 token 参与 loss。
- `rollout_log_probs`：rollout 模型生成 token 时的 logprob。
- `status`：PENDING、COMPLETED、TRUNCATED、ABORTED 等状态。
- `multimodal_inputs`：图像等多模态输入。

二次开发时，如果你要新增字段、改变 reward、支持多轮 tool 调用，通常都要理解 `Sample` 如何被 rollout 函数更新。

## 7. 如何从零开始阅读这个项目

推荐阅读顺序：

### 第一步：先看 examples

从 `examples/README.md` 开始，选择和自己任务最接近的示例：

- 单轮文本 RL：看基础训练示例或 GRPO/DAPO 相关脚本。
- 多轮 agent/tool use：看 `examples/search-r1`、`examples/tau-bench`、`examples/retool`。
- 多模态 VLM：看 `examples/geo3k_vlm` 和 `examples/geo3k_vlm_multi_turn`。
- 异步 rollout：看 `examples/fully_async`。
- 训练/推理解耦和权重同步：看 `examples/delta_weight_sync`。

### 第二步：追启动脚本

从示例里的 shell 脚本或配置文件开始，看它传了哪些参数：

- 模型路径：HF checkpoint / Megatron checkpoint。
- rollout 参数：temperature、top_p、max_response_len、n_samples_per_prompt。
- Ray 资源参数：节点数、每节点 GPU 数。
- SGLang 参数：server 数、router、dp/tp 配置。
- 训练参数：batch size、micro batch、并行策略、学习率、checkpoint。

### 第三步：追 Ray 主流程

重点看 `slime/ray/` 下的 manager/actor 代码，理解：

- actors 在哪里创建。
- remote 方法如何调用。
- rollout 和 train 如何串起来。
- 权重同步在哪里触发。

### 第四步：追 rollout 函数

重点看 `slime/rollout/sglang_rollout.py`：

- prompt 怎么 tokenize。
- 如何请求 SGLang `/generate`。
- 返回 token/logprob 怎么写回 `Sample`。
- reward 和 filter 什么时候调用。
- train output 和 eval output 有什么差异。

### 第五步：再看 backend

最后再深入 `slime/backends/`，否则容易被 Megatron/SGLang 的细节淹没。

## 8. 常见二次开发入口

### 8.1 想换 reward 逻辑

优先看：

```text
slime/rollout/rm_hub/
slime/rollout/sglang_rollout.py
examples/* 中 reward function 的配置方式
```

你通常需要实现一个 reward function，并通过参数或配置让 rollout 阶段调用它。

### 8.2 想做自定义 rollout / tool use / agent 环境

优先看：

```text
slime/rollout/base_types.py
slime/rollout/sglang_rollout.py
examples/search-r1/
examples/tau-bench/
examples/retool/
```

核心是让自定义 rollout 函数最终返回标准的 `RolloutFnTrainOutput` 或 `RolloutFnEvalOutput`。

### 8.3 想改训练算法

优先看：

```text
slime/backends/
slime/ray/train_actor.py
slime/ray/rollout.py
```

训练算法通常涉及：

- advantage/reward 处理。
- loss 计算。
- old logprob / rollout logprob 的使用。
- reference model 或 teacher model。
- 权重同步时机。

### 8.4 想改资源布局或扩展多机

优先看：

```text
slime/ray/placement_group.py
slime/ray/actor_group.py
启动脚本里的 Ray/GPU 参数
```

重点理解每个 actor 需要多少 GPU、如何 colocate、如何拆分 train 和 rollout 资源。

### 8.5 想接入新的推理后端

优先看：

```text
slime/rollout/sglang_rollout.py
slime/backends/sglang_utils/
slime/utils/http_utils.py
```

你需要实现类似 SGLang 的 generate 协议：输入 prompt/token ids，输出文本、token ids、logprobs 和 meta 信息。

## 9. 关键文件索引

建议先打开这些文件：

```text
slime/ray/actor_group.py
slime/ray/placement_group.py
slime/ray/train_actor.py
slime/ray/rollout.py
slime/rollout/sglang_rollout.py
slime/rollout/base_types.py
slime/utils/types.py
examples/README.md
```

阅读时可以带着这些问题：

1. Ray actor 是在哪里创建的？
2. rollout manager 如何拿到 prompt batch？
3. SGLang 生成结果如何变成 `Sample`？
4. reward 是单样本调用还是 batch 调用？
5. 训练 actor 从 rollout 侧拿到的 batch 长什么样？
6. 模型权重什么时候从训练端同步到推理端？
7. checkpoint 保存和加载由哪个 backend 负责？

## 10. 初学者最容易混淆的点

### 10.1 rollout engine 不等于训练模型对象

SGLang 负责生成，Megatron 负责训练。两边可能是不同进程、不同显存布局、甚至不同节点。训练后需要同步权重，否则 rollout 用的还是旧模型。

### 10.2 Ray actor 是进程级抽象

看到 `actor.method.remote()` 时，要意识到这是跨进程/跨节点调用，不是普通 Python 函数调用。返回值通常需要 `ray.get()` 才真正取回。

### 10.3 rollout 输出不是最终训练 batch

rollout 阶段先得到 `Sample` 列表，随后还可能经过 reward、filter、advantage、padding、packing 等处理，最后才喂给训练后端。

### 10.4 多模态输入会走 processor

`sglang_rollout.py` 中对 image/multimodal inputs 有特殊处理。文本任务只看 tokenizer 不够，多模态任务还要理解 processor 输出和 `multimodal_train_inputs`。

### 10.5 partial rollout 会影响 loss mask

如果启用 partial rollout 或 off-policy mask，已有 response 的 token 可能不参与 loss，需要关注 `loss_mask` 的更新逻辑。

## 11. 建议的上手实验路径

如果你准备真正运行或改 slime，建议按这个顺序：

1. 先找一个最小 example，只跑很小模型或 mock/CI 参数。
2. 只改 rollout temperature/max tokens，确认生成链路正常。
3. 加一个简单 reward function，比如 response 长度或格式判断。
4. 打印/保存一批 `Sample`，确认 prompt、response、reward、tokens、status 正确。
5. 再打开训练，观察一次 train 后是否触发权重同步。
6. 最后再尝试多机、多卡、异步 rollout、tool-use 等复杂能力。

## 12. 如果要把 slime 用到自己的 Agentic-RL 项目

可以优先考虑这条迁移路线：

```text
自己的任务环境 / tool environment
   ↓
封装成 rollout function
   ↓
输出 Sample 或 RolloutFnTrainOutput
   ↓
接 reward / filter
   ↓
复用 slime 的 Ray + Megatron + SGLang 训练推理框架
```

也就是说，不一定一开始就改训练后端。更低风险的方式是先把自己的任务接到 rollout 层，让 slime 继续负责分布式生成、训练和权重同步。

## 13. 最小阅读结论

如果只记住三句话：

1. `slime/ray/` 管分布式编排和 actor 生命周期。
2. `slime/rollout/` 管 prompt 到 response/reward/sample 的生成数据流。
3. `slime/backends/` 管 Megatron/SGLang 等实际训练推理后端。

真正入手时，建议从 `examples/README.md` 选任务，再沿着 `slime/ray/rollout.py` 和 `slime/rollout/sglang_rollout.py` 追一次完整数据流。
