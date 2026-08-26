"""Helpers for safely executing Python snippets in a remote workspace."""

from __future__ import annotations

import base64
import json
import shlex
from typing import Any, Mapping


def python_command(script: str, arguments: Mapping[str, Any]) -> str:
    """Build a shell-safe ``python3 -c`` command for remote execution.

    The script and its JSON arguments are encoded independently so arbitrary
    Python source, paths, Unicode, quotes, and newlines cannot alter the shell
    command.  The executed script can access the decoded mapping as ``ARGS``.
    """
    if not isinstance(script, str):
        raise TypeError("script must be a string")
    if not isinstance(arguments, Mapping):
        raise TypeError("arguments must be a mapping")

    encoded_script = base64.b64encode(script.encode("utf-8")).decode("ascii")
    encoded_args = base64.b64encode(
        json.dumps(dict(arguments), ensure_ascii=False).encode("utf-8")
    ).decode("ascii")
    bootstrap = (
        "import base64,json;"
        f"ARGS=json.loads(base64.b64decode({encoded_args!r}));"
        f"exec(compile(base64.b64decode({encoded_script!r}),'<workspace-tool>','exec'))"
    )
    return f"python3 -c {shlex.quote(bootstrap)}"
