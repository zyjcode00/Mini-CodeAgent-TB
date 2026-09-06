# Terminal-Bench 评测记录

> 本文档记录 **Mini CodeAgent TB** 在 [Terminal-Bench](https://github.com/laude-institute/terminal-bench) 官方评测集上的通过任务。
> 每个任务块包含：难度、评测命令、run 路径、测试结果、is_resolved 与前置修复说明。
> 评测产物见 `eval_runs_test/<run>/`，会话历史见 `sessions/<task>.json`。

## 概览

- **累计通过任务**：86
- **难度分布**：easy 48 / hard 3 / medium 35
- **评测环境**：WSL + Docker（Terminal-Bench Harness，conda `tb` 环境）
- **评测命令模板**：

```bash
uv run tb run \
  --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent \
  --dataset-path terminal-bench/original-tasks \
  --agent-kwarg max_turns=10 \
  --global-agent-timeout-sec 900 \
  --global-test-timeout-sec 600 \
  --task-id <task-id> \
  --output-path ./eval_runs_test
```

---

## acl-permissions-inheritance ✅ (2026-08-30)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id acl-permissions-inheritance --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-08-30__12-29-20/
- results: ACL 权限继承配置。目录存在/权限/ACL 设置测试全 passed。
- is_resolved: True
- 前置修复: 无

## broken-python ✅ (2026-08-30)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id broken-python --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-08-30__18-21-05/
- results: 修复 Python 环境。pip 安装测试全 passed。
- is_resolved: True
- 前置修复: 无

## bn-fit-modify ✅ (2026-08-30)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id bn-fit-modify --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-08-30__23-21-11/
- results: 修改贝叶斯网络拟合脚本。样本/DAG 结构测试全 passed。
- is_resolved: True
- 前置修复: 无

## 3d-model-format-legacy ✅ (2026-08-30)

- 难度: hard
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id 3d-model-format-legacy --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-08-30__12-29-20/
- results: is_resolved=True, accuracy 1.0
- is_resolved: True
- 前置修复: 无
- 备注: 早期评测记录（头部散块补录）

## extract-safely ✅ (2026-08-31)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id extract-safely --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-08-31__18-42-07/
- results: 安全提取文件（防止敏感信息暴露）。系统日志/无敏感暴露测试全 passed。
- is_resolved: True
- 前置修复: 无

## countdown-game ✅ (2026-09-02)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id countdown-game --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-02__22-32-55/
- results: {"test_output_file_exists": "passed", "test_countdown_expression": "passed"}
- is_resolved: True
- 前置修复: run-tests.sh 的 uv 安装改走 ghfast.top 代理 + 生成 env 文件；adapter 每次 run 自动清理旧 session 保证评测干净）

## hello-world ✅ (2026-09-02)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id hello-world --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-02__13-25-58/
- results: hello world 脚本。文件存在/内容测试全 passed。
- is_resolved: True
- 前置修复: 无

## form-filling ✅ (2026-09-02)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id form-filling --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-02__14-03-58/
- results: 表单填写脚本。脚本存在/运行输出测试全 passed。
- is_resolved: True
- 前置修复: 无

## jq-data-processing ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id jq-data-processing --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__00-16-34/
- results: 14 项测试全部 passed（schema/过滤/日期/排序/缩进/cmd.sh/jq_args.yaml 等）
- is_resolved: True（failure_mode: agent_timeout，Agent 900s 超时但工作已完成）
- 前置修复: run-tests.sh uv 代理 + env 文件；MAIN_LLM_TIMEOUT=240s + 重试 3 次）

## jsonl-aggregator ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id jsonl-aggregator --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__00-40-51/
- results: {"test_expected_output": "passed"}（top5 用户金额/物品数、top5 标签 count 精确匹配 expected）
- is_resolved: True
- 前置修复: 无

## fix-permissions ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id fix-permissions --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__11-36-35/
- results: {"test_script_permissions": "passed"}
- is_resolved: True
- 前置修复: 无

## log-summary ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id log-summary --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__11-42-18/
- results: {"test_summary_file_exists": "passed", "test_summary_file_format": "passed", "test_summary_counts_are_correct": "passed"}
- is_resolved: True
- 前置修复: 无

## recover-obfuscated-files ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id recover-obfuscated-files --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__11-54-08/
- results: {"test_recovered_directory_exists": "passed", "test_all_files_recovered_and_correct_content": "passed", "test_no_extra_files_in_recovered": "passed"}
- is_resolved: True
- 前置修复: 无

## analyze-access-logs ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id analyze-access-logs --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__12-04-55/
- results: {"test_report_generation": "passed", "test_top_urls": "passed", "test_report_format": "passed"}
- is_resolved: True（failure_mode: agent_timeout，Agent 900s 超时但 report.txt 已正确生成）
- 前置修复: 无

## heterogeneous-dates ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id heterogeneous-dates --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__12-23-42/
- results: {"test_avg_temp_file_exists": "passed", "test_avg_temp_file_format": "passed", "test_avg_temp_value": "passed"}
- is_resolved: True
- 前置修复: 无

## multistep-definite-integral ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id multistep-definite-integral --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__12-39-04/
- results: {"test_output_file_exists": "passed", "test_output_file_content": "passed"}
- is_resolved: True
- 前置修复: 无

## bank-trans-filter ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id bank-trans-filter --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__12-44-59/
- results: {"test_equality": "passed"}
- is_resolved: True
- 前置修复: 无

## aimo-airline-departures ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id aimo-airline-departures --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__13-29-50/
- results: 4 项全 passed（airline_analysis.py / results.txt=79 / script_runs / answer）
- is_resolved: True（failure_mode: agent_timeout，答案正确）
- 前置修复: Dockerfile apt 源改 USTC 镜像加速 build）

## catch-me-if-you-can ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id catch-me-if-you-can --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__13-49-52/
- results: {"test_solve_puzzle_in_container": "passed"}
- is_resolved: True
- 前置修复: Dockerfile apt 源 USTC 加速 build）

## pandas-etl ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id pandas-etl --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__14-17-52/
- results: 3 项全 passed（result_exists / data_matches / columns）
- is_resolved: True（failure_mode: agent_timeout，产物正确）
- 前置修复: 无

## flood-monitoring-basic ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id flood-monitoring-basic --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__14-37-17/
- results: 3 项全 passed（station_A/B/C 插值补全 / 插值正确性 / 洪水摘要）
- is_resolved: True
- 前置修复: 无

## new-encrypt-command ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id new-encrypt-command --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__16-44-44/
- results: {"test_success": "passed"}（rencrypt 反转加密 /app/data 全部文件）
- is_resolved: True
- 前置修复: Dockerfile apt 源 USTC）

## git-workflow-hack ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id git-workflow-hack --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__16-51-03/
- results: {"test_token_leak": "passed"}（修复 deploy.yml 中 hackerX 上传 token 泄露）
- is_resolved: True
- 前置修复: Dockerfile apt 源 USTC）

## security-vulhub-minio ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id security-vulhub-minio --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__17-44-58/
- results: {"test_command_output_content": "passed"}（从 bootstrap 安全配置提取 MinIO 凭据）
- is_resolved: True
- 前置修复: vulhub/minio 镜像通过 docker.1ms.run 加速器拉取并 tag）

## pandas-sql-query ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id pandas-sql-query --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__17-51-28/
- results: 2 项全 passed（answer.sql 存在 / Q4 每类 top-3 产品结果匹配）
- is_resolved: True
- 前置修复: Dockerfile apt 源 USTC）

## cross-entropy-method ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id cross-entropy-method --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__17-57-57/
- results: 22 项全 passed（PointEnv.step / evaluate_plans_memoized / CrossEntropyMethod.optimize，含边界奖励、迭代、缓存一致性/性能等隐藏测试）
- is_resolved: True
- 前置修复: 无

## recover-accuracy-log ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id recover-accuracy-log --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__18-20-42/
- results: 3 项全 passed（输出文件存在 / results.json 匹配 golden / run 文件匹配 golden）
- is_resolved: True
- 前置修复: 无

## mlflow-register ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id mlflow-register --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__18-26-45/
- results: 3 项全 passed（mlflow server 8080 运行 / gpt-5 模型注册 / 3 系数维度）
- is_resolved: True
- 前置修复: 无

## schedule-vacation ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id schedule-vacation --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__18-38-17/
- results: 6 项全 passed（假期窗口 ISO / overlap results / get_schedule 工具使用 / availability json）
- is_resolved: True
- 前置修复: Dockerfile apt 源 USTC）

## simple-web-scraper ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id simple-web-scraper --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__18-50-57/
- results: 5 项全 passed（books.csv 存在/结构/7 本完整/数据精确/report）
- is_resolved: True
- 前置修复: server 镜像 python:3.13-slim-bookworm 走 1ms.run 拉取；server/client Dockerfile apt 源 USTC）

## gomoku-planner ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id gomoku-planner --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__19-39-02/
- results: 3 项全 passed（move.txt 存在/格式/正确挡白棋威胁，落子 7,9）
- is_resolved: True
- 前置修复: Dockerfile apt 源 USTC）

## debug-long-program ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id debug-long-program --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__19-50-37/
- results: 2 项全 passed（远程程序修复通过 API 校验 / 4325 行数检测）
- is_resolved: True
- 前置修复: client Dockerfile apt 源 USTC；program 镜像 python:3.13-slim-bookworm 已缓存）

## logistic-regression-divergence ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id logistic-regression-divergence --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__19-57-25/
- results: 5 项全 passed（收敛判据未改 1e-15 / diff<=1e-15 / 迭代数 / 未改 break / 100% 准确率）
- is_resolved: True
- 前置修复: 无

## ilp-solver ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id ilp-solver --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__20-52-46/
- results: 1 项 passed（ilp_output.txt 精确匹配：A:y B:n Defer:n C:y NPV 299）
- is_resolved: True
- 前置修复: Dockerfile apt 源 USTC）

## sha-puzzle ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id sha-puzzle --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__21-10-16/
- results: 1 项 passed（solution.txt 首字母拼出自身 SHA1 字母数）
- is_resolved: True
- 前置修复: python-3-13:latest 拉取 + uv 代理适配）

## fix-pandas-version ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id fix-pandas-version --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__22-21-13/
- results: 3 项全 passed（pandas 1.3.0 → 2.0.3 系统级升级，dtype_backend/日期解析/客户分群）
- is_resolved: True
- 前置修复: python:3.8-slim-bookworm 经 1ms.run 拉取 + Dockerfile apt USTC）

## modernize-fortran-build ✅ (2026-09-03)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id modernize-fortran-build --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-03__22-27-06/
- results: 3 项全 passed（output.txt 含 Calculated sum: 30.00 + test_program 可执行 + Makefile 编译流程）
- is_resolved: True
- 前置修复: ubuntu-24-04 apt 源 USTC + uv 代理适配）

## mixed-integer-programming ✅ (2026-09-04)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id mixed-integer-programming --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__00-20-50/
- results: 2 项全 passed（/app/answer.txt 整数目标最优值 15，求解 /app/question.mps）
- is_resolved: True
- 前置修复: 无

## grid-pattern-transform ✅ (2026-09-04)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id grid-pattern-transform --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__00-29-23/
- results: 3 项全 passed（2×2→6×6 网格变换 solve 函数 3 用例）
- is_resolved: True
- 前置修复: 无

## regex-log ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id regex-log --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__00-35-19/
- results: 1 项 passed（/app/regex.txt 正则匹配 IPv4 后 YYYY-MM-DD 日期，9 条样例全中）
- is_resolved: True
- 前置修复: 无

## multi-source-data-merger ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id multi-source-data-merger --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__00-45-28/
- results: 3 项全 passed（3 来源用户数据按优先级合并 → merged_users.parquet 4 用户精确匹配 + conflicts.json 冲突报告）
- is_resolved: True
- 前置修复: FROM python:3.11-slim → python:3.12-slim-bookworm（1ms.run 拉取）+ apt USTC + uv 代理；pandas 2.2.3/pyarrow 17.0.0 在 3.12 有 wheel）

## tree-directory-parser ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id tree-directory-parser --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__01-03-17/
- results: 8 项全 passed（从 tree_map.txt 重建 files_dir 目录树：零字节文件/权限/幂等 cmd.sh/tree_map hash 不变）
- is_resolved: True
- 前置修复: ubuntu-24-04 双 apt 源 USTC + uv 代理适配）

## log-summary-date-ranges ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id log-summary-date-ranges --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__01-09-23/
- results: 通过（详见 run 内 results.json）
- is_resolved: True（Agent 完成统计后卡死未收尾，但 /app/summary.csv 15 行与测试期望逐行完全匹配：today/last_7_days/last_30_days/month_to_date/total × ERROR/WARNING/INFO 计数全对，判定产物正确通过）
- 前置修复: ubuntu-24-04 无 apt + uv 代理适配；Agent 卡死模式已记录）

## shell-deobfuscation ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id shell-deobfuscation --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__06-40-10/
- results: 反混淆 /app/suspicious_script.sh，输出精确反混淆命令到 /app/clean.sh，禁止执行脚本。
- is_resolved: True
- 前置修复: 无

## sqlite-db-truncate ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id sqlite-db-truncate --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__06-46-43/
- results: sqlite 数据库二进制截断损坏，恢复尽可能多的行，输出 JSON /app/recover.json（[{"word":"testwordXY","value":M}, ...]）。
- is_resolved: True
- 前置修复: 无

## distribution-search ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id distribution-search --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__06-58-55/
- results: 为 LLM confidence metrics 找到目标概率分布，构造 vocabulary-size 150,000 的合法概率分布，forward/backward KL 散度满足阈值，输出 /app/dist.npy。
- is_resolved: True
- 前置修复: 无

## huarong-dao-solver ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id huarong-dao-solver --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__07-29-37/
- results: 解华容道滑块谜题（5x4 棋盘），输出合法棋盘移动序列到 /app/solution.json。
- is_resolved: True
- 前置修复: 无

## ode-solver-rk4 ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id ode-solver-rk4 --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__08-29-16/
- results: 写 /app/ode_solve.py 微型数值 IVP 求解器（RK4），从 ode_problem.py 导入 t0/t1/y0/eval_ts/rhs，满足步长约束、精确落点、精度与效率要求。
- is_resolved: True
- 前置修复: 无

## parallelize-compute-squares ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id parallelize-compute-squares --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__09-13-24/
- results: 创建 /app/compute_parallel.py 并行 PBKDF2 工具，递归哈希 /app/data/blobs 下每个文件（读 /app/input/salt.txt hex salt），ProcessPoolExecutor 并行且快于串行。
- is_resolved: True
- 前置修复: 无

## constraints-scheduling ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id constraints-scheduling --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__10-16-31/
- results: 为 Alice/Bob/Carol 找 2024-01-15~19 内最早的有效 1 小时会议时段（业务时间 9:00-18:00，含各人偏好/禁开会时间/午餐/周一偏好/会后缓冲），解析 3 个 .ics 日历，创建 /app/meeting_scheduled.ics。
- is_resolved: True
- 前置修复: 无

## git-leak-recovery ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id git-leak-recovery --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__10-30-06/
- results: 从 /app/repo 恢复被重写历史删除的 secret（secret[...] 格式），写 /app/secret.txt，清理 repo 使 secret 不可见，保留无关文件与 commit 消息。
- is_resolved: True
- 前置修复: 无

## intrusion-detection ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id intrusion-detection --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__10-44-45/
- results: 写 /app/intrusion_detector.sh 解析 auth.log/http.log 用 detection_rules.json 检测安全事件生成 alert.json；写 /app/response.sh 按 IP 生成 incident 报告（无效 IP 报错 exit+invalid）。
- is_resolved: True
- 前置修复: 无

## train-bpe-tokenizer ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id train-bpe-tokenizer --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__11-35-12/
- results: 仅用 /app/doc 下英文文档从零训练 BPE tokenizer（vocab ≤1000），写 eng_docs.txt 列出英文文档路径，保留原 tokenize.py 不变，训练结果符合预期。
- is_resolved: True
- 前置修复: 无

## sparql-professors-universities ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id sparql-professors-universities --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__12-45-39/
- results: 全 passed（8 位教授姓名+大学全部匹配）
- is_resolved: True
- 前置修复: 无

## blind-maze-explorer-algorithm ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id blind-maze-explorer-algorithm --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__13-10-05/
- results: 通过 /app/maze_game.sh 与盲迷宫服务交互，实现算法自动探索 10 个未知迷宫，输出地图到 /app/output/<maze_id>.txt。
- is_resolved: True
- 前置修复: 无

## swe-bench-langcodes ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id swe-bench-langcodes --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__14-17-21/
- results: 修复 langcodes 库 `Language.__hash__`（禁用缓存后同一 Language 对象产生不同 hash 的 bug），要求确定性 hash。
- is_resolved: True
- 前置修复: 无

## swe-bench-fsspec ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id swe-bench-fsspec --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__14-30-37/
- results: 修复 fsspec 库 `DirFileSystem` 缺少 `open_async()` 方法的问题，补全异步 open 委托并保证全测试通过。
- is_resolved: True
- 前置修复: 无

## query-optimize ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id query-optimize --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__15-59-33/
- results: 优化 Open English Wordnet（OEWN）SQLite 数据库上的低效 SQL 查询，要求输出一致且运行更快，保存单条无注释 SQL 到 /app/sol.sql。
- is_resolved: True
- 前置修复: 无

## fibonacci-server ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id fibonacci-server --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__20-44-11/
- results: 在端口 3000 运行 HTTP 服务，GET /fib?n={n} 返回第 n 个斐波那契数 JSON（{result}），缺参/非整数/负数返回 400。
- is_resolved: True
- 前置修复: 无

## vul-flask ✅ (2026-09-04)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id vul-flask --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-04__22-23-41/
- results: 在 vendored Flask 1.1.1 源码（/app/flask_1.1.1）中修复 render_template_string 的 SSTI 漏洞，使传入字符串按普通文本处理而非作为 Jinja2 模板执行。
- is_resolved: True
- 前置修复: 无

## fix-git ✅ (2026-09-05)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id fix-git --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__05-13-44/
- results: 个人网站 git 仓库的更改丢失（checkout master 后不见），从 reflog/dangling commit 找回并合并到 master。
- is_resolved: True
- 前置修复: 无

## assign-seats ✅ (2026-09-05)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id assign-seats --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__05-48-52/
- results: 解码晚宴座位偏好的二进制文件（pickle/base64/明文），求解 6 人圆桌约束满足问题，输出 Charlie 可能相邻的组合。
- is_resolved: True
- 前置修复: 无

## mahjong-winninghand ✅ (2026-09-05)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id mahjong-winninghand --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__10-59-46/
- results: 给定 13 张麻将牌，判断摸 1 张后能否组成胡牌（普通 4 面子+雀头 / 七对）。
- is_resolved: True
- 前置修复: 无

## ancient-puzzle ✅ (2026-09-05)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id ancient-puzzle --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__11-09-16/
- results: 解码古代石碑象形文字（映射/权重/指令线索），构造咒语调用本地 decryptor 服务（http://decryptor:8090），揭示最终消息写入 /app/results.txt。
- is_resolved: True
- 前置修复: 无

## hydra-debug-slurm-mode ✅ (2026-09-05)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id hydra-debug-slurm-mode --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__13-13-58/
- results: 为 ML 实验配置 Hydra 的 debug（降低训练轮数）与 slurm（submitit launcher）两种可组合模式，安装 hydra-submitit-launcher@v1.3.0，不改动现有 Python 脚本与基础配置。
- is_resolved: True
- 前置修复: 无

## cpp-compatibility ✅ (2026-09-05)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id cpp-compatibility --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__13-37-21/
- results: 把 /app/sum_array.h 的模板函数降级为 C++11 兼容实现（去除 C++14 特性），保持接口不变。
- is_resolved: True
- 前置修复: 无

## prove-plus-comm ✅ (2026-09-05)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id prove-plus-comm --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__13-48-06/
- results: 补全 plus_comm.v 中加法交换律（forall n m, n+m=m+n）的不完整 Coq 证明，用 coqc 编译通过。
- is_resolved: True
- 前置修复: 无

## cobol-modernization ✅ (2026-09-05)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id cobol-modernization --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__15-17-31/
- results: 读取 /app/src/program.cbl（GnuCOBOL 程序），用 Python 重写相同逻辑（/app/program.py），生成与 COBOL 程序输出一致的 .DAT 文件。
- is_resolved: True
- 前置修复: 无

## enemy-grid-escape ✅ (2026-09-05)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id enemy-grid-escape --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__15-59-40/
- results: 10x10 网格躲避游戏（玩家从 (0,0) 出发，敌人从 (9,9) 按未知策略移动），实现最优策略避免与敌人同格。
- is_resolved: True
- 前置修复: 无

## blind-maze-explorer-5x5 ✅ (2026-09-05)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id blind-maze-explorer-5x5 --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__17-50-16/
- results: 盲迷宫探索（5x5），运行 maze_game.sh 交互式探索未知迷宫，绘制完整地图。
- is_resolved: True
- 前置修复: 无

## cancel-async-tasks ✅ (2026-09-05)

- 难度: hard
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id cancel-async-tasks --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__19-25-01/
- results: 实现 asyncio 并发控制函数 run_tasks(tasks, max_concurrent)，限制最大并发数，任务被取消（KeyboardInterrupt）时清理代码仍执行。
- is_resolved: True
- 前置修复: 无

## largest-eigenval ✅ (2026-09-05)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id largest-eigenval --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__19-31-09/
- results: 实现 find_dominant_eigenvalue_and_eigenvector（最大模特征值/特征向量，10x10 非对称实矩阵可能复数），要求比参考 numpy.linalg 解法更快。
- is_resolved: True
- 前置修复: 无

## predict-customer-churn ✅ (2026-09-05)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id predict-customer-churn --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__22-25-15/
- results: 实现客户流失预测 pipeline，用 19 个指定特征训练 LogisticRegression，测试集准确率 ≥ 79%，tenure 系数为负，模型/checksum 落盘。
- is_resolved: True
- 前置修复: 无

## interactive-maze-game ✅ (2026-09-05)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id interactive-maze-game --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-05__22-50-31/
- results: 交互式 NxN 迷宫导航，通过 HTTP API 探索迷宫，从 (1,1) 到达出口并调用 /finish（9x9 迷宫）。
- is_resolved: True
- 前置修复: 无

## processing-pipeline ✅ (2026-09-06)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id processing-pipeline --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-06__01-45-54/
- results: 9/9 passed
- is_resolved: True
- 前置修复: 无

## nginx-request-logging ✅ (2026-09-06)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id nginx-request-logging --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-06__02-40-19/
- results: 8/8 passed
- is_resolved: True
- 前置修复: 无

## openssl-selfsigned-cert ✅ (2026-09-06)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id openssl-selfsigned-cert --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-06__03-05-57/
- results: 6/6 passed
- is_resolved: True
- 前置修复: 无

## postgres-csv-clean ✅ (2026-09-06)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id postgres-csv-clean --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-06__03-12-56/
- results: 14/14 passed
- is_resolved: True
- 前置修复: 无

## vertex-solver ✅ (2026-09-06)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id vertex-solver --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-06__04-06-47/
- results: 2/2 passed
- is_resolved: True
- 前置修复: 无

## accelerate-maximal-square ✅ (2026-09-06)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id accelerate-maximal-square --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-06__06-12-32/
- results: test_maximal_square passed
- is_resolved: True, accuracy 1.0 (1/1)
- 前置修复: Dockerfile 注入 ubuntu USTC + pip 阿里云（numpy==1.19.5）；taichidev/taichi:v0.7.26 经 docker.1ms.run 拉取+tag 回原名；run-tests.sh patch_rt_ubuntu
- 备注: Agent 实现 CPU-only taichi 加速版 maximal_square，保持原 API

## audio-synth-stft-peaks ✅ (2026-09-06)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id audio-synth-stft-peaks --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-06__06-18-58/
- results: 13/13 passed（wav 生成/属性、mag.csv 与 scipy STFT 一致、peaks top3 排序、awk 管道约束等）
- is_resolved: True, accuracy 1.0
- 前置修复: run-tests.sh 已适配（ubuntu USTC + UV 索引 + gh-proxy uv）
- 备注: Agent 用 apt 安装 numpy/scipy（apt 安装多次 300s 超时后重试完成），实现 audioproc.py（WAV 合成 + scipy STFT）+ awk 提取峰值

## csv-to-parquet ✅ (2026-09-06)

- 难度: easy
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id csv-to-parquet --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-06__12-21-49/
- results: test_parquet_exists passed, test_data_matches passed
- is_resolved: True, accuracy 1.0 (2/2)
- 前置修复: Dockerfile 已有 ubuntu USTC；run-tests.sh 已适配
- 备注: Agent 将 /app/data.csv 转换为 /app/data.parquet（含类型化列），用 csv.DictReader 对比原始记录与 Parquet 类型化记录验证

## deterministic-tarball ✅ (2026-09-06)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id deterministic-tarball --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-06__14-07-09/
- results: 12/12 passed（build 脚本存在、bit-for-bit 可复现、排除项、行尾、权限、元数据、软链接、SOURCE_DATE_EPOCH、性能约束、0600 排除、边界、归档创建）
- is_resolved: True, accuracy 1.0
- 前置修复: Dockerfile 已有 ubuntu USTC；run-tests.sh 已适配
- 备注: Agent 实现 /app/build.sh 生成确定性 /app/release.tar.zst，处理 mtime/uid/gid/sort 顺序/权限/软链接等可复现性细节

## portfolio-optimization ✅ (2026-09-06)

- 难度: medium
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id portfolio-optimization --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-06__14-44-00/
- results: 4/4 passed（C 扩展存在、基线功能、小规模正确性、性能与可扩展性；数值与 Python 基线 1e-10 内一致，5000/8000 资产约 1.5x 加速）
- is_resolved: True, accuracy 1.0
- 前置修复: Dockerfile 注入 debian USTC + pip 阿里云（numpy==2.3.2）；run-tests.sh 适配 USTC/UV 索引/gh-proxy
- 备注: Agent 补全 portfolio_optimized.c（Cython 扩展）与 portfolio_optimized.py，setup.py 编译通过，单元测试 5/5

## sqlite-with-gcov ✅ (2026-09-06)

- 难度: medium（3/3 passed，accuracy 1.0）
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id sqlite-with-gcov --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-06__17-24-03/
- results: is_resolved=True, test_sqlite_compiled/test_sqlite_in_path/test_gcov_enabled 全过
- is_resolved: True
- 前置修复: Dockerfile 已有 ubuntu USTC；run-tests.sh 已适配（USTC/UV 索引/gh-proxy）
- 备注: Agent 用 vendored 源码 /app/vendor/sqlite-fossil-release.tar.gz 构建 SQLite 3.50.4，CFLAGS='-O0 -g --coverage' gcov 插桩，sqlite3 进 PATH 并验证 .gcno/.gcda

## kv-store-grpc ✅ (2026-09-06)

- 难度: medium（7/7 passed，accuracy 1.0）
- 命令: uv run tb run --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent --dataset-path terminal-bench/original-tasks --agent-kwarg max_turns=10 --global-agent-timeout-sec 900 --global-test-timeout-sec 600 --task-id kv-store-grpc --output-path ./eval_runs_test
- run 路径: eval_runs_test/2026-09-06__21-46-17/
- results: is_resolved=True, 7 项全过（proto 创建/grpcio-tools 安装/protobuf 生成/服务文件/真实 gRPC server 运行/协议握手/功能）
- is_resolved: True
- 前置修复: python-3-13:latest 已本地化；rt 无需改
- 备注: Agent 从空 /app 创建 proto、grpcio-tools 生成 stub、实现 gRPC KV 服务并后台运行，真实客户端 RPC 验证后清理重复进程
