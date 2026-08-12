# ---  实现 Bash 工具 (你的老朋友) ---
from pydantic import BaseModel, Field
from .base import BaseTool
from .execution_backend import LocalExecutionBackend, ToolExecutionBackend

class BashArgs(BaseModel):
    command: str = Field(..., description="要执行的 shell 命令")

class BashTool(BaseTool):
    name = "execute_bash"
    description = "在本地系统执行 bash 命令。小心使用，确保命令安全。"
    args_schema = BashArgs

    def __init__(self, backend: ToolExecutionBackend | None = None):
        self.backend = backend or LocalExecutionBackend()

    def run(self, command: str) -> str:
        return self.backend.run_command(command)
