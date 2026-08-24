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


class EmptyOutputTerminalBenchSession:
    def run(self, command):
        return {"stdout": "", "stderr": "", "exit_code": 0}


class MissingCaptureTerminalBenchSession:
    def run(self, command):
        return None


class ClosableTerminalBenchSession:
    def __init__(self):
        self.commands = []
        self.close_calls = 0

    def run(self, command):
        self.commands.append(command)
        return {"stdout": "ok", "exit_code": 0}

    def close(self):
        self.close_calls += 1


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

    assert backend.state == "closed"
    with pytest.raises(ExecutorShutdownError, match="backend is closed"):
        backend.run_command("echo retry")


def test_closed_backend_rejects_commands_without_calling_session():
    session = ClosableTerminalBenchSession()
    backend = TerminalBenchSessionBackend(session)

    backend.close()
    backend.close()

    assert backend.state == "closed"
    assert session.close_calls == 1
    with pytest.raises(ExecutorShutdownError, match="backend is closed"):
        backend.run_command("echo too-late")
    assert session.commands == []


def test_empty_command_output_is_reported_as_a_real_empty_result():
    backend = TerminalBenchSessionBackend(EmptyOutputTerminalBenchSession())

    assert backend.run_command("true") == "Command executed with no output."


def test_missing_command_capture_is_distinguished_from_real_empty_output():
    backend = TerminalBenchSessionBackend(MissingCaptureTerminalBenchSession())

    assert backend.run_command("true") == "❌ command execution returned no capture result"


def test_non_shutdown_session_errors_are_still_raised():
    backend = TerminalBenchSessionBackend(BrokenTerminalBenchSession())

    try:
        backend.run_command("echo hello")
    except ValueError as error:
        assert str(error) == "command protocol is invalid"
    else:
        raise AssertionError("non-shutdown session errors must not be swallowed")
