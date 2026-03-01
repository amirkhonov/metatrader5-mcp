#!/usr/bin/env python3
"""
Connection and account-related tools for the MetaTrader 5 MCP server.
"""

from __future__ import annotations

from typing import Any

import MetaTrader5 as mt5

from .logger import logger
from .utils import mcp, mt5_to_python


@mcp.tool
def mt5_version() -> Any:
    """Get MetaTrader 5 terminal version information."""
    logger.info("mt5_version called")
    return mt5_to_python(mt5.version())


@mcp.tool
def mt5_terminal_info() -> Any:
    """Get information about the MetaTrader 5 terminal (status, settings, paths)."""
    logger.info("mt5_terminal_info called")
    return mt5_to_python(mt5.terminal_info())


@mcp.tool
def mt5_last_error() -> Any:
    """Get information about the last error that occurred."""
    logger.info("mt5_last_error called")
    return mt5_to_python(mt5.last_error())


@mcp.tool
def mt5_account_info() -> Any:
    """Get current trading account information including balance, equity, margin, profit, etc."""
    logger.info("mt5_account_info called")
    return mt5_to_python(mt5.account_info())
