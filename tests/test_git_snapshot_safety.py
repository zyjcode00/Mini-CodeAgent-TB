import subprocess

from tools.git_tool import GitCommitTool


def _git(*args):
    return subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )


def test_snapshot_does_not_commit_deleted_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _git("init")
    _git("config", "user.email", "test@example.com")
    _git("config", "user.name", "Test")

    (tmp_path / "keep.py").write_text("original\n")
    (tmp_path / "removed.py").write_text("must survive snapshot\n")
    _git("add", ".")
    _git("commit", "-m", "initial")

    (tmp_path / "keep.py").write_text("updated\n")
    (tmp_path / "removed.py").unlink()

    result = GitCommitTool().run(message="snapshot")

    assert result.startswith("✅")
    assert "removed.py" in _git("status", "--porcelain").stdout
    assert _git("show", "--format=", "--name-status", "HEAD").stdout.strip() == "M\tkeep.py"


def test_snapshot_commits_new_files_and_modifications(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _git("init")
    _git("config", "user.email", "test@example.com")
    _git("config", "user.name", "Test")

    (tmp_path / "module.py").write_text("one\n")
    _git("add", ".")
    _git("commit", "-m", "initial")
    (tmp_path / "module.py").write_text("two\n")
    (tmp_path / "new.py").write_text("new\n")

    result = GitCommitTool().run(message="snapshot")

    assert result.startswith("✅")
    assert _git("status", "--porcelain").stdout == ""
    assert "M\tmodule.py" in _git("show", "--format=", "--name-status", "HEAD").stdout
    assert "A\tnew.py" in _git("show", "--format=", "--name-status", "HEAD").stdout
