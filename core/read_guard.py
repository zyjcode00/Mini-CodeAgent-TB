"""Runtime read ledger and anti-spin guard for AgentEngine."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ReadRange:
    """Normalized read_file target range."""

    path: str
    start_line: Optional[int] = None
    end_line: Optional[int] = None

    @classmethod
    def from_tool_input(cls, tool_input: Dict[str, Any]) -> "ReadRange":
        return cls(
            path=str(tool_input.get("path") or tool_input.get("file_path") or ""),
            start_line=cls._to_optional_int(tool_input.get("start_line")),
            end_line=cls._to_optional_int(tool_input.get("end_line")),
        )

    @staticmethod
    def _to_optional_int(value: Any) -> Optional[int]:
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def exact_key(self) -> Tuple[str, Optional[int], Optional[int]]:
        return (self.path, self.start_line, self.end_line)

    def contains(self, other: "ReadRange") -> bool:
        """Return True if this range fully contains other for the same path."""
        if self.path != other.path:
            return False
        if self.start_line is None or self.end_line is None:
            return True
        if other.start_line is None or other.end_line is None:
            return False
        return self.start_line <= other.start_line and other.end_line <= self.end_line

    def is_forward_page_after(self, previous: "ReadRange") -> bool:
        """Return True for normal forward pagination in the same file."""
        if self.path != previous.path:
            return False
        if previous.end_line is None or self.start_line is None:
            return False
        return self.start_line >= previous.end_line

    def label(self) -> str:
        return f"{self.path}:{self.start_line or ''}-{self.end_line or ''}"


@dataclass
class RuntimeReadLedger:
    """Tracks read_file usage during one execute_query call without blocking reads."""

    duplicate_threshold: int = 2
    exact_counts: Dict[Tuple[str, Optional[int], Optional[int]], int] = field(default_factory=dict)
    ranges_by_path: Dict[str, List[ReadRange]] = field(default_factory=dict)
    last_read: Optional[ReadRange] = None

    def record(self, tool_input: Dict[str, Any]) -> List[str]:
        current = ReadRange.from_tool_input(tool_input or {})
        if not current.path:
            return []

        reminders: List[str] = []
        key = current.exact_key()
        count = self.exact_counts.get(key, 0) + 1
        self.exact_counts[key] = count
        if count >= self.duplicate_threshold:
            reminders.append(
                f"⚠️ read_file 防空转提醒：已第 {count} 次读取相同范围 {current.label()}。"
                "如已获得足够信息，请先总结结论或执行下一步；只有确有遗漏时才继续读取。"
            )

        if not (self.last_read and current.is_forward_page_after(self.last_read)):
            for previous in self.ranges_by_path.get(current.path, []):
                if previous == current:
                    continue
                if previous.contains(current):
                    reminders.append(
                        f"⚠️ read_file 防空转提醒：当前范围 {current.label()} 已被先前读取的 "
                        f"{previous.label()} 覆盖。请避免重复探索，优先产出阶段性总结。"
                    )
                    break

        self.ranges_by_path.setdefault(current.path, []).append(current)
        self.last_read = current
        return reminders


@dataclass
class ReadOnlyStreakGuard:
    """Detects consecutive read-only tool rounds and asks for a checkpoint summary."""

    checkpoint_threshold: int = 3
    streak: int = 0

    READ_ONLY_TOOLS = {"read_file", "search_code", "list_files_recursive", "list_all_symbols", "find_symbol_definition"}

    def record_round(self, tool_names: List[str]) -> Optional[str]:
        if not tool_names:
            return None
        if all(name in self.READ_ONLY_TOOLS for name in tool_names):
            self.streak += 1
        else:
            self.streak = 0
            return None

        if self.streak >= self.checkpoint_threshold:
            return (
                f"⚠️ 只读工具防空转检查点：已连续 {self.streak} 轮只执行读取/搜索类工具。"
                "下一步请先用简短文字总结已读文件、关键结论和明确的下一步动作；"
                "如果信息已足够，请停止继续读取并开始修改或回答。"
            )
        return None
