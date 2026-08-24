import pytest

from tools.execution_backend import ExecutorShutdownError, TerminalBenchSessionBackend


class FakeTerminalBenchSession:
    def __init__(self):
        self.received_command = None

    def send_command(self, command):
        # Terminal-Bench's real tmux session expects a TerminalCommand-like
        # object and accesses these attributes. Passing a raw str used to raise
        # AttributeError: 'str' object has no attribute 'append_enter'.
        assert command.append_enter is True
        assert command.command == "echo hello"
        self.received_command = command
        return {"stdout": "hello\n", "exit_code": 0}


class CapturingTerminalBenchSession:
    def __init__(self):
        self.received_command = None

    def send_command(self, command):
        self.received_command = command
        return {"stdout": "ok\n", "exit_code": 0}


class ShutdownTerminalBenchSession:
    def run(self, command):
        raise RuntimeError("cannot schedule new futures after shutdown")


class BrokenTerminalBenchSession:
    def run(self, command):
        raise ValueError("command protocol is invalid")


def test_terminal_bench_send_command_receives_terminal_command_like_object():
    session = FakeTerminalBenchSession()
    backend = TerminalBenchSessionBackend(session)

    result = backend.run_command("echo hello")

    assert session.received_command is not None
    assert "STDOUT:\nhello" in result


def test_terminal_bench_multiline_send_command_keeps_heredoc_delimiter_standalone():
    session = CapturingTerminalBenchSession()
    backend = TerminalBenchSessionBackend(session)
    heredoc_command = """python - <<'PY'
print('hello')
PY"""

    result = backend.run_command(heredoc_command)

    assert "STDOUT:\nok" in result
    assert session.received_command is not None
    sent = session.received_command.command
    assert "\nPY\n" in sent
    assert "\nPY;" not in sent
    assert sent.endswith("\ntrue")


def test_shutdown_session_raises_non_retryable_executor_error():
    backend = TerminalBenchSessionBackend(ShutdownTerminalBenchSession())

    with pytest.raises(ExecutorShutdownError, match="cannot schedule new futures after shutdown"):
        backend.run_command("echo hello")


def test_non_shutdown_session_errors_are_still_raised():
    backend = TerminalBenchSessionBackend(BrokenTerminalBenchSession())

    try:
        backend.run_command("echo hello")
    except ValueError as error:
        assert str(error) == "command protocol is invalid"
    else:
        raise AssertionError("non-shutdown session errors must not be swallowed")
