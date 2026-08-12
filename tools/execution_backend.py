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
from abc import ABC, abstractmethod
from typing import Any

import chardet


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

    def run_command(self, command: str) -> str:
        for method_name in ("run", "exec", "execute", "send_command"):
            method = getattr(self.session, method_name, None)
            if callable(method):
                payload = self._coerce_command_for_method(method_name, command)
                return self._format_result(method(payload))
        raise RuntimeError(
            "Terminal-Bench session does not expose a supported command method "
            "(expected one of: run, exec, execute, send_command)"
        )

    @staticmethod
    def _coerce_command_for_method(method_name: str, command: str) -> Any:
        if method_name != "send_command":
            return command

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
    def _format_result(result: Any) -> str:
        if isinstance(result, str):
            return result or "Command executed with no output."

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
