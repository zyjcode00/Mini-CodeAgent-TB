import subprocess

from tools import get_default_tools
from tools.execution_backend import LocalExecutionBackend, TerminalBenchSessionBackend
from tools.git_tool import GitCommitTool, GitRollbackTool, GitStatusTool


class GitSession:
    def __init__(self, cwd):
        self.cwd = str(cwd)
        self.commands = []

    def run(self, command):
        self.commands.append(command)
        result = subprocess.run(command, shell=True, cwd=self.cwd, capture_output=True, text=True)
        return {"stdout": result.stdout, "stderr": result.stderr, "exit_code": result.returncode}


def init_repo(path):
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=path, check=True)


def test_git_tools_use_terminal_bench_backend(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "README.md").write_text("initial\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "initial"], cwd=tmp_path, check=True)
    (tmp_path / "README.md").write_text("changed\n", encoding="utf-8")

    session = GitSession(tmp_path)
    backend = TerminalBenchSessionBackend(session)
    status = GitStatusTool(backend).run()
    assert "README.md" in status

    committed = GitCommitTool(backend).run("container snapshot")
    assert "快照已保存" in committed
    assert "container snapshot" in subprocess.check_output(
        ["git", "log", "-1", "--format=%s"], cwd=tmp_path, text=True
    )

    (tmp_path / "README.md").write_text("uncommitted\n", encoding="utf-8")
    rolled_back = GitRollbackTool(backend).run("HEAD")
    assert "已回滚到" in rolled_back
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == "changed\n"
    assert session.commands


def test_git_tools_default_to_local_backend():
    tools = get_default_tools()
    for name in ("get_git_status", "commit_snapshot", "git_rollback"):
        tool = next(tool for tool in tools if tool.name == name)
        assert isinstance(tool.backend, LocalExecutionBackend)


def test_git_backend_rejects_non_repository(tmp_path):
    backend = TerminalBenchSessionBackend(GitSession(tmp_path))
    assert GitStatusTool(backend).run() == "❌ 当前目录不是 Git 仓库"
