"""Utilities for safely serializing runtime data to UTF-8 JSON.

Runtime strings can contain lone surrogate code points when Python decodes
invalid OS/subprocess bytes with mechanisms such as ``surrogateescape``.  Those
strings are legal inside Python, but ``json.dump(..., ensure_ascii=False)`` will
raise ``UnicodeEncodeError`` when the underlying UTF-8 text stream tries to write
them.  All persistence boundaries should sanitize data through this module before
writing human-readable JSON.
"""

from __future__ import annotations

import json
from typing import Any, IO


def replace_lone_surrogates(value: Any) -> Any:
    """Recursively replace lone surrogate code points with U+FFFD.

    Normal Unicode text is preserved.  Only isolated surrogate code points in
    strings are converted to the replacement character so UTF-8 output cannot
    fail with ``surrogates not allowed``.
    """
    if isinstance(value, str):
        return value.encode("utf-16", "surrogatepass").decode("utf-16", "replace")
    if isinstance(value, list):
        return [replace_lone_surrogates(item) for item in value]
    if isinstance(value, tuple):
        return tuple(replace_lone_surrogates(item) for item in value)
    if isinstance(value, dict):
        return {
            replace_lone_surrogates(key): replace_lone_surrogates(item)
            for key, item in value.items()
        }
    return value


def safe_json_dumps(value: Any, **kwargs: Any) -> str:
    """json.dumps wrapper that sanitizes lone surrogates first."""
    return json.dumps(replace_lone_surrogates(value), **kwargs)


def safe_json_dump(value: Any, fp: IO[str], **kwargs: Any) -> None:
    """json.dump wrapper that sanitizes lone surrogates first."""
    json.dump(replace_lone_surrogates(value), fp, **kwargs)
