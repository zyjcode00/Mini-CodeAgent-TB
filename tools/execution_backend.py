"""Execution backends for command-running tools.

The default CLI runs shell commands in the local Python process.  Terminal-Bench,
however, provides a task session/container and expects agent commands to execute
through that session.  These small backends keep tool implementations stable while
allowing adapters to redirect command execution.
"""

from __future__ import annotations

from types import SimpleNamespace

import os
import platform
import subprocess
import threading
from abc import ABC, abstractmethod
from typing import Any

import chardet


class ExecutorShutdownError(RuntimeError):
    """Raised when a command cannot be submitted to a closed executor."""


class CommandCaptureError(RuntimeError):
    """Raised when a session executes a command without returning capture data."""


class ToolExecutionBackend(ABC):
    """Abstract command execution backend used by shell-like tools."""

    @abstractmethod
    def run_command(self, command: str) -> str:
        """Run *command* and return a human-readable tool result."""


class LocalExecutionBackend(ToolExecutionBackend):
    """Execute commands on the local host with the legacy BashTool behavior."""

    def run_command(self, command: str) -> str:
        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"

            if platform.system() == "Windows":
                command = f"chcp 65001 > nul && {command}"

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                env=env,
            )

            raw_output = result.stdout
            raw_error = result.stderr
            if not raw_output and not raw_error:
                return "Command executed with no output."

            output = self._decode(raw_output) if raw_output else ""
            error = self._decode(raw_error) if raw_error else ""

            sections = []
            if output:
                sections.append(f"STDOUT:\n{output}")
            if error:
                sections.append(f"STDERR:\n{error}")
            if result.returncode != 0:
                sections.append(f"EXIT_CODE: {result.returncode}")
            return "\n".join(sections)
        except Exception as e:  # noqa: BLE001 - preserve tool-facing error style.
            return f"❌ 运行出错: {str(e)}"

    @staticmethod
    def _decode(raw: bytes) -> str:
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return raw.decode("gbk")
            except UnicodeDecodeError:
                encoding = chardet.detect(raw)["encoding"] or "utf-8"
                return raw.decode(encoding, errors="replace")


class TerminalBenchSessionBackend(ToolExecutionBackend):
    """Execute commands through a Terminal-Bench session object.

    Terminal-Bench versions expose slightly different session APIs.  This backend
    intentionally supports common method names and normalizes their return values
    to the string format expected by the existing tool loop.
    """

    def __init__(self, session: Any):
        if session is None:
            raise ValueError("session is required for TerminalBenchSessionBackend")
        self.session = session
        self._state = "running"
        # Terminal-Bench drives one persistent tmux pane per session. Concurrent
        # send_command calls share its input stream and completion signal.
        self._command_lock = threading.Lock()

    @property
    def state(self) -> str:
        """Return the backend lifecycle state."""
        return self._state

    def close(self) -> None:
        """Stop accepting commands and release the session when it supports close."""
        if self._state == "closed":
            return
        self._state = "closing"
        close = getattr(self.session, "close", None)
        try:
            if callable(close):
                close_result = close()
                # A session close is allowed to be asynchronous, but the backend
                # must stop submissions immediately regardless of its return value.
                if hasattr(close_result, "__await__"):
                    raise RuntimeError("asynchronous session close must be awaited by the owner")
        finally:
            self._state = "closed"

    def run_command(self, command: str) -> str:
        if self._state != "running":
            raise ExecutorShutdownError(
                f"cannot submit command while execution backend is {self._state}"
            )

        with self._command_lock:
            for method_name in ("run", "exec", "execute", "send_command"):
                method = getattr(self.session, method_name, None)
                if callable(method):
                    payload = self._coerce_command_for_method(method_name, command)
                    try:
                        result = method(payload)
                    except RuntimeError as error:
                        if "cannot schedule new futures after shutdown" not in str(error):
                            raise
                        self._state = "closed"
                        raise ExecutorShutdownError(str(error)) from error
                    return self._format_result(result, method_name=method_name)
        raise RuntimeError(
            "Terminal-Bench session does not expose a supported command method "
            "(expected one of: run, exec, execute, send_command)"
        )

    @staticmethod
    def _coerce_command_for_method(method_name: str, command: str) -> Any:
        if method_name != "send_command":
            return command

        command = TerminalBenchSessionBackend._make_multiline_command_tmux_safe(command)

        try:
            from terminal_bench.terminal.models import TerminalCommand

            return TerminalCommand(
                command=command,
                min_timeout_sec=0.0,
                max_timeout_sec=float("inf"),
                block=True,
                append_enter=True,
            )
        except Exception:
            return SimpleNamespace(
                command=command,
                min_timeout_sec=0.0,
                max_timeout_sec=float("inf"),
                block=True,
                append_enter=True,
            )

    @staticmethod
    def _make_multiline_command_tmux_safe(command: str) -> str:
        """Keep Terminal-Bench's tmux wait suffix away from heredoc delimiters.

        Terminal-Bench's tmux-backed ``send_command`` implementation appends its
        synchronization command to the final command line.  For heredocs, the
        closing delimiter must be alone on its line, so appending ``; tmux wait``
        directly after the delimiter makes the shell keep reading stdin.  Adding
        a harmless standalone command after any multiline command ensures the
        suffix is appended to that command instead of to a heredoc delimiter.
        """

        if "\n" not in command:
            return command
        return f"{command.rstrip()}\ntrue"

    @staticmethod
    def _format_result(result: Any, *, method_name: str) -> str:
        if isinstance(result, str):
            return result or "Command executed with no output."
        if result is None:
            if method_name == "send_command":
                raise CommandCaptureError(
                    "Terminal-Bench send_command submitted the command without "
                    "returning captured output; use a synchronous session command API"
                )
            raise CommandCaptureError(
                "command execution returned no capture result"
            )

        stdout = getattr(result, "stdout", None)
        stderr = getattr(result, "stderr", None)
        exit_code = getattr(result, "returncode", getattr(result, "exit_code", None))

        if isinstance(result, dict):
            stdout = result.get("stdout", stdout)
            stderr = result.get("stderr", stderr)
            exit_code = result.get("returncode", result.get("exit_code", exit_code))

        sections = []
        if stdout:
            sections.append(f"STDOUT:\n{stdout}")
        if stderr:
            sections.append(f"STDERR:\n{stderr}")
        if exit_code not in (None, 0):
            sections.append(f"EXIT_CODE: {exit_code}")
        return "\n".join(sections) if sections else "Command executed with no output."
