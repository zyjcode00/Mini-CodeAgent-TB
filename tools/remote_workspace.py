import base64
import json
import shlex
from typing import Any, Dict


def python_command(script: str, arguments: Dict[str, Any]) -> str:
    """Build a shell-safe Python command for a remote execution backend."""
    encoded_script = base64.b64encode(script.encode("utf-8")).decode("ascii")
    encoded_args = base64.b64encode(
        json.dumps(arguments, ensure_ascii=False).encode("utf-8")
    ).decode("ascii")
    bootstrap = (
        "import base64,json;"
        f"ARGS=json.loads(base64.b64decode({encoded_args!r}));"
        f"exec(compile(base64.b64decode({encoded_script!r}),'<workspace-tool>','exec'))"
    )
    return f"python3 -c {shlex.quote(bootstrap)}"
