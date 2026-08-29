"""Runtime read ledger and anti-spin guard for AgentEngine."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
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
            path=normalize_read_path(str(tool_input.get("path") or tool_input.get("file_path") or "")),
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

    @property
    def normalized_start(self) -> int:
        return self.start_line or 1

    @property
    def normalized_end(self) -> Optional[int]:
        return self.end_line

    def exact_key(self) -> Tuple[str, Optional[int], Optional[int]]:
        return (self.path, self.start_line, self.end_line)

    def contains(self, other: "ReadRange") -> bool:
        """Return True if this range fully contains other for the same path."""
        if self.path != other.path:
            return False
        return _contains_interval(
            self.normalized_start,
            self.normalized_end,
            other.normalized_start,
            other.normalized_end,
        )

    def is_forward_page_after(self, previous: "ReadRange") -> bool:
        """Return True for normal forward pagination in the same file."""
        if self.path != previous.path:
            return False
        if previous.end_line is None or self.start_line is None:
            return False
        return self.start_line >= previous.end_line

    def label(self) -> str:
        return f"{self.path}:{self.start_line or ''}-{self.end_line or ''}"


def normalize_read_path(path: str) -> str:
    """Normalize read_file paths so ./x, x and absolute cwd paths dedupe together."""
    if not path:
        return ""
    try:
        resolved = Path(path).expanduser().resolve(strict=False)
        cwd = Path.cwd().resolve(strict=False)
        try:
            normalized = resolved.relative_to(cwd)
        except ValueError:
            normalized = resolved
        return os.path.normcase(str(normalized).replace("\\", "/"))
    except Exception:
        return os.path.normcase(os.path.normpath(path).replace("\\", "/"))


def _contains_interval(
    outer_start: int,
    outer_end: Optional[int],
    inner_start: int,
    inner_end: Optional[int],
) -> bool:
    if outer_start > inner_start:
        return False
    if outer_end is None:
        return True
    if inner_end is None:
        return False
    return inner_end <= outer_end


def _merge_intervals(intervals: List[Tuple[int, Optional[int]]]) -> List[Tuple[int, Optional[int]]]:
    """Merge overlapping/touching intervals. None end means EOF."""
    ordered = sorted(intervals, key=lambda item: item[0])
    merged: List[Tuple[int, Optional[int]]] = []
    for start, end in ordered:
        if not merged:
            merged.append((start, end))
            continue

        prev_start, prev_end = merged[-1]
        if prev_end is None:
            continue

        if end is None:
            if start <= prev_end + 1:
                merged[-1] = (prev_start, None)
            else:
                merged.append((start, end))
            continue

        if start <= prev_end + 1:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))
    return merged


@dataclass(frozen=True)
class ReadDecision:
    """Decision made before executing read_file."""

    should_skip: bool
    reminders: List[str] = field(default_factory=list)
    tool_response: Optional[str] = None


@dataclass
class RuntimeReadLedger:
    """Tracks read_file usage during one execute_query call.

    It does not restrict legitimate reading. It only short-circuits repeated exact
    reads and ranges already covered by previous successful reads, while allowing
    forward pagination and new ranges.
    """

    duplicate_threshold: int = 2
    exact_counts: Dict[Tuple[str, Optional[int], Optional[int]], int] = field(default_factory=dict)
    ranges_by_path: Dict[str, List[ReadRange]] = field(default_factory=dict)
    merged_ranges_by_path: Dict[str, List[Tuple[int, Optional[int]]]] = field(default_factory=dict)
    last_read: Optional[ReadRange] = None

    def to_dict(self) -> dict:
        return {
            "duplicate_threshold": self.duplicate_threshold,
            "exact_counts": [list(key) + [value] for key, value in self.exact_counts.items()],
            "ranges_by_path": {
                path: [
                    {"path": item.path, "start_line": item.start_line, "end_line": item.end_line}
                    for item in ranges
                ]
                for path, ranges in self.ranges_by_path.items()
            },
            "merged_ranges_by_path": {
                path: [list(interval) for interval in intervals]
                for path, intervals in self.merged_ranges_by_path.items()
            },
            "last_read": (
                {"path": self.last_read.path, "start_line": self.last_read.start_line, "end_line": self.last_read.end_line}
                if self.last_read else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RuntimeReadLedger":
        ledger = cls(duplicate_threshold=int(data.get("duplicate_threshold", 2)))
        for item in data.get("exact_counts", []):
            if len(item) == 4:
                ledger.exact_counts[(item[0], item[1], item[2])] = int(item[3])
        for path, ranges in data.get("ranges_by_path", {}).items():
            ledger.ranges_by_path[path] = [
                ReadRange(item.get("path", path), item.get("start_line"), item.get("end_line"))
                for item in ranges
            ]
        ledger.merged_ranges_by_path = {
            path: [tuple(interval) for interval in intervals]
            for path, intervals in data.get("merged_ranges_by_path", {}).items()
        }
        last_read = data.get("last_read")
        if last_read:
            ledger.last_read = ReadRange(
                last_read.get("path", ""), last_read.get("start_line"), last_read.get("end_line")
            )
        return ledger

    def before_read(self, tool_input: Dict[str, Any]) -> ReadDecision:
        current = ReadRange.from_tool_input(tool_input or {})
        if not current.path:
            return ReadDecision(should_skip=False)

        reminders: List[str] = []
        key = current.exact_key()
        count = self.exact_counts.get(key, 0) + 1
        self.exact_counts[key] = count
        if count >= self.duplicate_threshold:
            reminders.append(
                f"⚠️ read_file 防空转提醒：已第 {count} 次读取相同范围 {current.label()}。"
                "本次不再重复返回文件内容；请基于已有信息总结结论或执行下一步。"
            )

        covered_by = self._find_covering_range(current)
        is_forward_page = bool(self.last_read and current.is_forward_page_after(self.last_read))
        if covered_by and not is_forward_page:
            reminders.append(
                f"⚠️ read_file 防空转提醒：当前范围 {current.label()} 已被先前读取的 "
                f"{covered_by.label()} 覆盖。本次不再重复返回文件内容，以减少上下文污染。"
            )

        if reminders:
            self.last_read = current
            return ReadDecision(
                should_skip=True,
                reminders=reminders,
                tool_response="\n".join(reminders),
            )

        self._record_allowed_range(current)
        return ReadDecision(should_skip=False)

    def record(self, tool_input: Dict[str, Any]) -> List[str]:
        """Backward-compatible API returning reminders for callers/tests."""
        return self.before_read(tool_input).reminders

    def _find_covering_range(self, current: ReadRange) -> Optional[ReadRange]:
        for start, end in self.merged_ranges_by_path.get(current.path, []):
            if _contains_interval(start, end, current.normalized_start, current.normalized_end):
                return ReadRange(path=current.path, start_line=start, end_line=end)
        return None

    def _record_allowed_range(self, current: ReadRange) -> None:
        self.ranges_by_path.setdefault(current.path, []).append(current)
        intervals = self.merged_ranges_by_path.setdefault(current.path, [])
        intervals.append((current.normalized_start, current.normalized_end))
        self.merged_ranges_by_path[current.path] = _merge_intervals(intervals)
        self.last_read = current


@dataclass
class ReadOnlyStreakGuard:
    """Detects consecutive read-only tool rounds and asks for a checkpoint summary."""

    checkpoint_threshold: int = 3
    streak: int = 0

    READ_ONLY_TOOLS = {
        "read_file",
        "search_code",
        "list_files_recursive",
        "list_all_symbols",
        "find_symbol_definition",
        "memory_recall",
        "memory_file_history",
        "memory_error_history",
        "memory_stats",
    }

    @classmethod
    def for_user_input(cls, user_input: str) -> "ReadOnlyStreakGuard":
        text = (user_input or "").lower()
        architecture_keywords = ("架构", "architecture", "了解", "分析项目", "阅读项目", "梳理", "调研")
        document_keywords = ("文档", "方案", "计划", "docs", "document")
        if any(keyword in text for keyword in architecture_keywords):
            return cls(checkpoint_threshold=6)
        if any(keyword in text for keyword in document_keywords):
            return cls(checkpoint_threshold=4)
        return cls(checkpoint_threshold=3)

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
