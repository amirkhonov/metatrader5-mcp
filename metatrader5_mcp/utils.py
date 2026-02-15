#!/usr/bin/env python3
"""
Core helpers for the MetaTrader 5 MCP server.

This module defines:
- datetime and MT5 result helpers

Tool implementations live in separate `tools_*.py` modules and import
from this file.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Shared FastMCP app
# ---------------------------------------------------------------------------

mcp = FastMCP("metatrader5-mcp")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def parse_datetime(date_str: str) -> datetime:
    """Parse datetime string in several common formats."""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"Unable to parse date: {date_str!r}")


def mt5_to_python(data: Any) -> Any:
    """
    Convert MetaTrader5 return types into JSON-serializable Python structures.

    - Named tuples -> dict
    - Lists/tuples of named tuples -> list[dict]
    - Other lists/tuples -> list
    - None -> None
    """
    if data is None:
        return None

    if hasattr(data, "_asdict"):
        # Convert named tuple to dict
        return data._asdict()

    if isinstance(data, (list, tuple)):
        if not data:
            return []
        first = data[0]
        if hasattr(first, "_asdict"):
            return [item._asdict() for item in data]
        return list(data)

    return data


def filter_none(d: dict[str, Any]) -> dict[str, Any]:
    """Return a shallow copy of dict without None values."""
    return {k: v for k, v in d.items() if v is not None}
