from core.memory_context_builder import MemoryContextBuilder
from core.memory_items import MemoryItem, MemoryKind, MemoryRecallResult
from core.memory_maintenance import MemoryMaintenance


def _item(title, content, *, kind=MemoryKind.TASK.value, confidence=0.8, importance=0.6, metadata=None):
    return MemoryItem(
        title=title,
        content=content,
        kind=kind,
        confidence=confidence,
        importance=importance,
        metadata=metadata or {},
    )


def _result(item, score=0.9):
    return MemoryRecallResult(item=item, score=score, reason="test", source="unit")


def test_raw_read_file_success_memory_is_classified_as_low_quality_tool_trace():
    item = _item(
        "工具执行成功: read_file",
        "[FILE] core/engine.py\n1 | import os\n2 | class AgentEngine: ...",
        metadata={"tool_name": "read_file", "event_type": "post_tool_use"},
    )

    assert item.is_low_quality_tool_trace()


def test_conclusion_bearing_read_file_memory_is_not_filtered_as_noise():
    item = _item(
        "任务完成: 修复 read_file 防空转",
        "完成结果: 已修复重复读取问题。关键决策: 使用 ledger 保留已读范围。",
        metadata={"tool_name": "read_file", "key_decisions": ["use read ledger"]},
    )

    assert not item.is_low_quality_tool_trace()


def test_prepare_for_save_downranks_noisy_read_file_tool_trace():
    maintenance = MemoryMaintenance()
    item = _item(
        "工具执行成功: read_file",
        "读取文件成功: read_file returned a long raw file blob\n" * 80,
        metadata={"tool_name": "read_file", "event_type": "post_tool_use"},
    )

    decision = maintenance.prepare_for_save(item, existing_items=[])

    assert decision.item.metadata["low_quality_tool_trace"] is True
    assert decision.item.quality_score <= 0.15
    assert decision.action in {"archive", "save"}


def test_memory_context_builder_filters_low_quality_tool_traces_but_keeps_decisions():
    noisy = _item(
        "工具执行成功: read_file",
        "[FILE] core/memory_context_builder.py\n" + "raw source line\n" * 40,
        metadata={"tool_name": "read_file", "low_quality_tool_trace": True},
    )
    decision = _item(
        "架构决策: Phase 3 记忆降噪",
        "关键决策: 召回时过滤低质量工具轨迹，保留结论型记忆。",
        kind=MemoryKind.DECISION.value,
        metadata={"key_decisions": ["filter noisy tool traces"]},
    )

    context = MemoryContextBuilder(default_token_budget=500).build(
        "继续 phase3 修复代码",
        [_result(noisy, 0.99), _result(decision, 0.5)],
        token_budget=500,
        task_type="code_edit",
    )

    assert "工具执行成功: read_file" not in context
    assert "架构决策: Phase 3 记忆降噪" in context
    assert "过滤低质量工具轨迹" in context
