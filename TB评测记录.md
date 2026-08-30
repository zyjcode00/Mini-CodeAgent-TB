uv run tb run   --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent   --dataset-path /home/zyjcode/LLM/terminal-bench/original-tasks   --agent-kwarg max_turns=10   --task-id assign-seats   --output-path ./eval_runs_test
Results written to /home/zyjcode/LLM/mini-claude-code-cli/eval_runs_test/2026-08-30__00-17-48/results.json

uv run tb run \
  --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent \
  --dataset-path /home/zyjcode/LLM/terminal-bench/original-tasks \
  --agent-kwarg max_turns=10 \
  --task-id fix-git \
  --output-path ./eval_runs_test
Results written to /home/zyjcode/LLM/mini-claude-code-cli/eval_runs_test/2026-08-30__00-36-44/results.json


uv run tb run   --agent-import-path terminal_bench_adapter:MiniClaudeCodeAgent   --dataset-path /home/zyjcode/LLM/terminal-bench/original-tasks   --agent-kwarg max_turns=10   --task-id 3d-model-format-legacy  --output-path ./eval_runs_test

