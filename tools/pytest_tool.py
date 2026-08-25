import shlex
import subprocess

from pydantic import BaseModel, Field

from .base import BaseTool
from .execution_backend import LocalExecutionBackend, ToolExecutionBackend


class PytestArgs(BaseModel):
    path: str = Field(..., description="要运行的测试文件或目录路径")


class PytestTool(BaseTool):
    name = "run_pytest"
    description = "运行 pytest 测试。这是验证代码正确性的唯一标准。如果失败，请根据输出的 Traceback 进行修复。"
    args_schema = PytestArgs

    def __init__(self, backend: ToolExecutionBackend | None = None):
        self.backend = backend or LocalExecutionBackend()

    def run(self, path: str) -> str:
        if not isinstance(self.backend, LocalExecutionBackend):
            return self.backend.run_command(
                f"python3 -m pytest -v -- {shlex.quote(path)}"
            )

        try:
            result = subprocess.run(
                ["pytest", "-v", path],
                capture_output=True,
            )

            stdout = LocalExecutionBackend._decode(result.stdout) if result.stdout else ""
            stderr = LocalExecutionBackend._decode(result.stderr) if result.stderr else ""

            if result.returncode == 0:
                return f"✅ 测试通过！\n{stdout}"

            return f"❌ 测试失败 (Exit Code {result.returncode}):\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
        except Exception as e:
            return f"❌ 运行测试工具出错: {str(e)}"
