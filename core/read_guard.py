"""Runtime read ledger and anti-spin guard for AgentEngine."""
from __future__ import annotations

import json
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
        """Backward-compatible reminder API: returns reminders list only.

        New code should call :meth:`before_read` and inspect the returned
        ``ReadDecision``; this alias keeps older call sites (and tests) working.
        """
        return self.before_read(tool_input).reminders

    def to_dict(self) -> Dict[str, Any]:
        """Serialize read coverage so duplicate detection survives reload."""
        return {
            "duplicate_threshold": self.duplicate_threshold,
            "exact_counts": [
                {"path": path, "start_line": start, "end_line": end, "count": count}
                for (path, start, end), count in self.exact_counts.items()
            ],
            "ranges": [
                {"path": read_range.path, "start_line": read_range.start_line,
                 "end_line": read_range.end_line}
                for ranges in self.ranges_by_path.values() for read_range in ranges
            ],
            "last_read": ({"path": self.last_read.path,
                           "start_line": self.last_read.start_line,
                           "end_line": self.last_read.end_line}
                          if self.last_read else None),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RuntimeReadLedger":
        ledger = cls(duplicate_threshold=int(data.get("duplicate_threshold", 2)))
        for item in data.get("exact_counts", []):
            key = (normalize_read_path(str(item.get("path", ""))),
                   ReadRange._to_optional_int(item.get("start_line")),
                   ReadRange._to_optional_int(item.get("end_line")))
            ledger.exact_counts[key] = int(item.get("count", 0))
        for item in data.get("ranges", []):
            read_range = ReadRange.from_tool_input(item)
            if read_range.path:
                ledger._record_allowed_range(read_range)
        last = data.get("last_read")
        if last:
            ledger.last_read = ReadRange.from_tool_input(last)
        return ledger

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
    """Detect consecutive non-progressing read/tool rounds."""

    checkpoint_threshold: int = 3
    stop_threshold: int = 6
    streak: int = 0
    should_stop: bool = False
    _last_signature: Optional[str] = field(default=None, repr=False)
    _same_signature_streak: int = 0
    _same_failure_streak: int = 0

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

    signature_reminder_threshold: int = 3
    signature_stop_threshold: int = 5
    failure_reminder_threshold: int = 2
    failure_stop_threshold: int = 3

    def record_round(self, round_data: Any) -> Optional[str]:
        """Record one tool round; returns a reminder / terminal message or None.

        Accepts either the legacy list of tool names (``["read_file", ...]``)
        or a list of ``(tool_name, kwargs, output)`` tuples.  Detects:
        - consecutive read-only rounds (checkpoint / stop thresholds);
        - repeated identical tool calls with no progress;
        - repeated identical tool failures.
        """
        if not round_data:
            return None
        # 兼容旧调用：List[str] → (name, {}, "")
        if isinstance(round_data[0], str):
            round_data = [(n, {}, "") for n in round_data]

        tool_names = [n for n, _, _ in round_data]
        is_read_only = all(n in self.READ_ONLY_TOOLS for n in tool_names)
        is_failure = any(self._looks_like_failure(o) for _, _, o in round_data)

        # 轮签名（工具名 + kwargs），用于重复/失败检测
        signature = tuple(sorted(
            (n, json.dumps(kw, sort_keys=True, ensure_ascii=False, default=str))
            for n, kw, _ in round_data
        ))

        # 相同失败检测（独立于只读判定：任何工具连续失败都应更快停止）
        if is_failure:
            if signature == self._last_signature and self._last_signature is not None:
                self._same_failure_streak += 1
            else:
                self._last_signature = signature
                self._same_failure_streak = 1
            self._same_signature_streak = 0
            if self._same_failure_streak >= self.failure_stop_threshold:
                self.should_stop = True
                return (
                    f"⛔ 无进展：已连续 {self._same_failure_streak} 次相同工具失败，"
                    "请改变策略或总结结论后停止本轮。"
                )
            if self._same_failure_streak >= self.failure_reminder_threshold:
                return (
                    f"⚠️ 相同工具失败：已连续 {self._same_failure_streak} 次执行相同工具且失败，"
                    "请更换方法或先分析错误原因。"
                )
            return None

        if not is_read_only:
            # 写入/其他工具成功轮：重置所有游标
            self.streak = 0
            self._same_signature_streak = 0
            self._same_failure_streak = 0
            self._last_signature = None
            self.should_stop = False
            return None

        self.streak += 1

        # 只读连续轮：checkpoint → stop（防空转优先于重复签名检测）
        if self.streak >= self.stop_threshold:
            self.should_stop = True
            return (
                f"⛔ 无进展：已连续 {self.streak} 轮只执行读取/搜索类工具，停止本轮。"
            )
        if self.streak >= self.checkpoint_threshold:
            return (
                f"⚠️ 只读工具防空转检查点：已连续 {self.streak} 轮只执行读取/搜索类工具。"
                "下一步请先用简短文字总结已读文件、关键结论和明确的下一步动作；"
                "如果信息已足够，请停止继续读取并开始修改或回答。"
            )

        # 相同签名无进展 → 提醒后停止
        if signature == self._last_signature and self._last_signature is not None:
            self._same_signature_streak += 1
        else:
            self._last_signature = signature
            self._same_signature_streak = 1
        self._same_failure_streak = 0

        if self._same_signature_streak >= self.signature_stop_threshold:
            self.should_stop = True
            return (
                f"⛔ 无进展：已连续 {self._same_signature_streak} 次相同工具调用且无进展，"
                "请基于已有信息总结结论或执行下一步。"
            )
        if self._same_signature_streak >= self.signature_reminder_threshold:
            return (
                f"⚠️ 重复工具调用：已连续 {self._same_signature_streak} 次执行相同工具，"
                "结果无变化，请停止重复调用。"
            )
        return None

    @staticmethod
    def _looks_like_failure(output: Any) -> bool:
        text = str(output or "").lower()
        return any(marker in text for marker in (
            "错误", "失败", "error", "failed", "exception", "traceback",
        ))

    def record_tool_round(self, round_data: Any) -> Optional[str]:
        """Alias of :meth:`record_round` kept for backward compatibility."""
        return self.record_round(round_data)
