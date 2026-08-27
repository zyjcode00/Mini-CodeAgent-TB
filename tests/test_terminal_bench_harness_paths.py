import subprocess
from pathlib import Path


TB_PYTHON = Path("/home/zyjcode/miniconda3/envs/tb/bin/python")


def test_harness_output_path_survives_cwd_change(tmp_path):
    script = r'''
import os
import sys
from pathlib import Path
from types import SimpleNamespace

from terminal_bench.harness.harness import Harness

root = Path(sys.argv[1])
os.chdir(root)
Harness._init_dataset = lambda self: setattr(
    self, "_dataset", SimpleNamespace(sort_by_duration=lambda: None)
)
Harness._init_agent_class = lambda self: None
Harness._init_logger = lambda self: None

harness = Harness(output_path=Path("eval_runs"), run_id="cwd-regression")
expected_run_path = root / "eval_runs" / "cwd-regression"
workspace = root / "workspace"
workspace.mkdir()
os.chdir(workspace)

assert harness._run_path == expected_run_path
result_path = harness._run_path / "post-agent.txt"
result_path.write_text("ok")
assert result_path.read_text() == "ok"
'''
    completed = subprocess.run(
        [str(TB_PYTHON), "-c", script, str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
