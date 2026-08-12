import subprocess

from pydantic import BaseModel, Field

from .base import BaseTool
from .execution_backend import LocalExecutionBackend


class PytestArgs(BaseModel):
    path: str = Field(..., description="要运行的测试文件或目录路径")


class PytestTool(BaseTool):
    name = "run_pytest"
    description = "运行 pytest 测试。这是验证代码正确性的唯一标准。如果失败，请根据输出的 Traceback 进行修复。"
    args_schema = PytestArgs

    def run(self, path: str) -> str:
        try:
            # Capture bytes and decode explicitly.  On Windows, child processes can
            # still emit bytes in the active code page (for example GBK/CP936) even
            # when the parent process prefers UTF-8.  subprocess.run(text=True,
            # encoding="utf-8") decodes in an internal reader thread and can raise
            # UnicodeDecodeError from threading.py/subprocess.py before we can
            # format the pytest failure for the agent.
            result = subprocess.run(
                ["pytest", "-v", path],
                capture_output=True,
            )

            stdout = LocalExecutionBackend._decode(result.stdout) if result.stdout else ""
            stderr = LocalExecutionBackend._decode(result.stderr) if result.stderr else ""

            if result.returncode == 0:
                return f"✅ 测试通过！\n{stdout}"

            # 关键：把报错信息完整传回给 Agent
            return f"❌ 测试失败 (Exit Code {result.returncode}):\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
        except Exception as e:
            return f"❌ 运行测试工具出错: {str(e)}"
