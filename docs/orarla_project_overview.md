# Orarla 项目理解文档

## 1. 项目定位

Orarla 是一个面向运筹优化（Operations Research, OR）任务的强化学习项目。它基于 `verl` 训练框架扩展，目标是让大语言模型在组合优化、数学建模、约束求解等 OR 场景中，通过可执行代码、求解器反馈和强化学习信号提升推理与求解能力。

从 README、示例脚本和源码结构看，项目核心关注点包括：

- 使用 PPO / Ray / vLLM 等组件训练大模型。
- 将 OR 问题转化为可评估的代码生成或求解任务。
- 通过 Gurobi 等优化求解器对模型输出进行打分。
- 支持 SIRL（Self-Improving Reinforcement Learning）类训练流程。
- 提供沙箱执行能力，用于运行模型生成的 Python 代码并收集结果。
- 包含数据构建、技能资料、评估与仪表盘相关模块。

一句话概括：Orarla 是一个把 `verl` 的大模型 RL 训练能力接到 OR 代码执行和求解器奖励上的项目。

## 2. 技术栈与依赖

项目使用 Python，构建配置主要在 `pyproject.toml` 中。核心技术栈包括：

- `verl`：强化学习训练框架，项目中保留并扩展了 `src/verl` 下的大量训练逻辑。
- `Ray`：分布式任务和 worker 编排，PPO trainer 基于 Ray actor/worker 运行。
- `vLLM` / Megatron / FSDP：用于高效生成和大模型训练。
- `Hydra`：训练入口的配置管理。
- `PyTorch`：模型训练基础框架。
- `Gurobi`：OR 任务求解和奖励计算的关键依赖。
- `datasets` / parquet：训练和验证数据通常以 parquet 形式组织。

需要注意：Gurobi 通常需要本地安装和许可证，相关 reward function 或测试在没有 Gurobi 环境时可能无法直接运行。

## 3. 顶层目录结构

根据已读文件和项目命名，Orarla 大致可以按以下模块理解：

```text
Orarla/
├── README.md / README.zh.md        # 项目介绍、安装、训练示例
├── pyproject.toml                  # Python 包、依赖、工具配置
├── examples/                       # 训练、评估、奖励函数示例
│   └── SIRL/                       # SIRL 相关脚本与 reward function
├── src/
│   ├── verl/                       # verl 原训练框架与 PPO/Ray 训练实现
│   └── orarla/                     # Orarla 自定义扩展
│       ├── reward_manager/         # 奖励管理，含 Gurobi 相关逻辑
│       ├── runtime/                # 代码执行运行时
│       └── sandbox/                # 沙箱与安全执行辅助函数
├── tests/                          # 测试脚本，例如 SIRL 测试
├── skills/                         # OR 数据集、任务技能、参考资料
└── dashboard / data pipeline        # 数据处理、展示或分析相关能力
```

理解这个项目时，可以先把 `src/verl` 看作通用 RL 基座，把 `src/orarla` 和 `examples/SIRL` 看作项目真正面向 OR 的业务扩展。

## 4. 训练入口

主要训练入口位于：

- `src/verl/trainer/main_ppo.py`

该文件是 PPO 训练的 Hydra 入口。典型职责包括：

1. 读取 Hydra 配置。
2. 初始化 Ray runtime。
3. 根据配置选择 tokenizer、模型、worker 类型和资源池。
4. 构造 reward manager。
5. 创建并启动 RayPPOTrainer。

训练脚本一般不会直接手写 Python 参数，而是通过 shell 脚本传入大量 Hydra override。`examples/SIRL/run_withoutKL.sh` 就是一个典型示例。

## 5. PPO / Ray 训练主流程

核心 trainer 位于：

- `src/verl/trainer/ppo/ray_trainer.py`

它承担实际训练编排。可以把流程理解为：

1. 初始化 actor、critic、reference policy、reward model 等 worker。
2. 建立 Ray resource pool，把不同角色分配到 GPU/节点资源。
3. 从训练数据集中读取 batch。
4. actor rollout 生成回答或代码。
5. reward manager 对生成结果打分。
6. 计算 advantage、policy loss、value loss 等 PPO 指标。
7. 更新 actor/critic。
8. 按配置执行验证、保存 checkpoint、日志上报。

Orarla 的业务价值主要插在第 5 步：模型输出不是只用文本规则评分，而是可以进入代码执行、Gurobi 求解和 OR-specific reward pipeline。

## 6. SIRL 示例脚本

示例脚本：

- `examples/SIRL/run_withoutKL.sh`

这个脚本展示了如何启动一个不使用 KL penalty 或弱化 KL 相关设置的 SIRL 训练流程。它通常会配置：

- 训练/验证数据路径。
- actor rollout 模型路径。
- rollout engine、采样数量、temperature、top-p 等生成参数。
- PPO batch size、mini batch size、micro batch size。
- Ray / GPU / tensor parallel 设置。
- reward function 路径或 reward manager 类型。
- checkpoint 和日志输出路径。

从使用方式看，Orarla 的训练高度依赖 Hydra override。排查训练问题时，应优先检查 shell 脚本中的配置覆盖项是否和本地资源、数据路径、模型路径匹配。

## 7. 奖励系统与 Gurobi

关键文件：

- `src/orarla/reward_manager/gurobi.py`
- `examples/SIRL/reward_func/batch_score_gurobi.py`

Gurobi reward 是 Orarla 区别于普通 LLM RL 项目的核心。整体思路是：

1. 模型针对 OR 问题生成 Python 代码、建模代码或求解过程。
2. reward function 提取、清洗或包装模型输出。
3. 在沙箱或受控 runtime 中执行生成代码。
4. 调用 Gurobi 求解目标问题。
5. 根据可行性、目标值、约束满足情况、异常类型等返回 reward。

这类 reward 的优点是信号更贴近真实 OR 任务结果；缺点是执行成本高、环境依赖重，并且必须处理超时、异常、不安全代码和求解器许可证问题。

常见失败来源包括：

- 模型输出不是合法 Python 代码。
- 代码没有按约定暴露函数或变量。
- Gurobi 未安装或许可证不可用。
- 求解超时。
- 生成模型违反约束但仍返回了结果。
- 数据样本字段和 reward function 期望字段不一致。

## 8. 沙箱执行与 Runtime

关键文件：

- `src/orarla/runtime/executor.py`
- `src/orarla/sandbox/utils.py`

这部分负责把模型生成内容变成可执行对象，并限制执行边界。主要职责包括：

- 创建临时执行环境或临时文件。
- 提取 markdown/code block 中的 Python 代码。
- 设置超时和进程隔离。
- 捕获 stdout、stderr、异常和返回值。
- 对执行结果做结构化封装，供 reward manager 使用。

对于 RL 训练来说，这层非常重要，因为 rollout 会产生大量不稳定输出。没有稳定 runtime，训练会被随机异常、卡死进程或污染全局状态拖垮。

## 9. 数据与任务格式

README 和示例显示，训练数据通常通过 parquet 文件提供。PPO 训练一般需要区分：

- train files：训练集。
- val files：验证集。
- prompt/input 字段：给模型的问题描述。
- ground truth / metadata：reward function 可能需要的参考答案、约束、实例数据或目标值。

OR 数据可能来自 `skills/or-dataset` 相关目录，里面包括任务说明、失败模式、领域参考资料等。该目录更像是数据构建和任务知识库，而不是训练主循环本身。

如果要新增任务，建议先明确四件事：

1. prompt 中给模型什么信息。
2. 模型输出必须遵守什么格式。
3. reward function 需要哪些样本字段。
4. 如何判断可行解、最优性或部分得分。

## 10. 测试与验证

已读测试文件：

- `tests/test_SIRL.py`

该测试用于验证 SIRL 相关流程或配置能否正常工作。由于项目依赖 Ray、GPU、大模型和 Gurobi，本地完整测试门槛较高。实践中可以分层验证：

- 纯 Python 工具函数：用 pytest 快速验证。
- reward function：用小样本和短 timeout 验证。
- sandbox executor：用简单生成代码验证成功、失败、超时路径。
- PPO 训练：先用极小数据集、极小 batch、少量 step 做 smoke test。
- 完整训练：确认数据、模型、GPU、Gurobi license 和输出目录都可用后再运行。

## 11. 推荐阅读顺序

如果你想快速读懂项目，建议按这个顺序：

1. `README.zh.md`：先理解项目目标和官方推荐命令。
2. `pyproject.toml`：确认依赖、包结构和 Python 版本约束。
3. `examples/SIRL/run_withoutKL.sh`：理解实际训练命令如何拼出来。
4. `src/verl/trainer/main_ppo.py`：看训练从哪里启动。
5. `src/verl/trainer/ppo/ray_trainer.py`：看 PPO 主循环如何组织。
6. `src/orarla/reward_manager/gurobi.py`：看 OR reward 如何接入训练。
7. `examples/SIRL/reward_func/batch_score_gurobi.py`：看具体 reward function 输入输出约定。
8. `src/orarla/runtime/executor.py` 和 `src/orarla/sandbox/utils.py`：看模型代码如何被执行。
9. `tests/test_SIRL.py`：看项目作者期望怎样验证 SIRL 流程。

## 12. 一次训练的大致调用链

可以把一次 SIRL/PPO 训练理解成下面这条链路：

```text
examples/SIRL/run_withoutKL.sh
    -> python -m verl.trainer.main_ppo + Hydra overrides
        -> main_ppo.py 初始化配置、Ray、tokenizer、worker、reward manager
            -> RayPPOTrainer.fit()
                -> 读取 parquet batch
                -> actor rollout 生成模型回答/代码
                -> Orarla reward manager 调用 reward function
                    -> runtime/sandbox 执行生成代码
                    -> Gurobi 求解或校验 OR 问题
                    -> 返回 reward tensor / metrics
                -> PPO advantage 与 loss 计算
                -> actor/critic 参数更新
                -> validate / checkpoint / logging
```

## 13. 上手建议

在本地跑通项目前，建议先准备：

- Python 环境和项目依赖。
- 可用 GPU 与 CUDA/PyTorch 版本。
- Ray 可正常启动。
- 训练和验证 parquet 数据路径。
- Hugging Face 或本地模型路径。
- Gurobi 安装和许可证。
- 输出目录、checkpoint 目录、日志目录写权限。

最小可行验证路径：

1. 先运行纯 reward function 的小样本测试，确认 Gurobi 和 sandbox 正常。
2. 再用极小 parquet 数据运行 1-2 个 PPO step。
3. 最后再扩大 batch、rollout 数和训练步数。

## 14. 排错重点

排查 Orarla 问题时优先看这些位置：

- 训练启动失败：检查 `examples/SIRL/run_withoutKL.sh` 的路径、模型名、Hydra override。
- Ray worker 失败：检查 GPU 数量、资源池配置、CUDA 可见设备。
- reward 全是 0 或异常：检查 `batch_score_gurobi.py` 输入字段、代码提取逻辑、Gurobi 状态。
- 进程卡死：检查 sandbox timeout、Gurobi time limit、生成代码是否进入死循环。
- checkpoint 不保存：检查 trainer 保存间隔、输出目录权限和分布式 rank 条件。
- 验证指标异常：检查 train/val 数据字段是否一致，验证 reward 和训练 reward 是否同源。

## 15. 总结

Orarla 的主线并不复杂：它不是从零实现一个 RL 框架，而是在 `verl` 的 PPO/Ray 训练能力上，增加面向运筹优化任务的 reward、runtime、sandbox 和数据体系。读懂项目的关键，是把通用训练框架和 OR-specific 业务逻辑分开看。

最重要的三个入口是：

- `examples/SIRL/run_withoutKL.sh`：实际怎么启动训练。
- `src/verl/trainer/main_ppo.py` 与 `src/verl/trainer/ppo/ray_trainer.py`：训练怎么跑。
- `src/orarla/reward_manager/gurobi.py` 与 `examples/SIRL/reward_func/batch_score_gurobi.py`：OR 结果如何变成强化学习奖励。
