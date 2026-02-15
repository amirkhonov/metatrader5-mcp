#!/usr/bin/env python3
"""
Connection and account-related tools for the MetaTrader 5 MCP server.
"""

from __future__ import annotations

from typing import Any

import MetaTrader5 as mt5

from .logger import logger
from .schemas import InitializeParams, LoginParams
from .utils import filter_none, mcp, mt5_to_python


@mcp.tool
def mt5_initialize(params: InitializeParams) -> str:
    """
    Initialize connection to MetaTrader 5 terminal.

    All fields on `params` are optional and map directly to `mt5.initialize`.
    """
    kwargs = filter_none(params.model_dump())

    safe_kwargs: dict[str, Any] = dict(kwargs)
    if "password" in safe_kwargs:
        safe_kwargs["password"] = "***"
    logger.info("mt5_initialize called with %s", safe_kwargs)

    result = mt5.initialize(**kwargs)
    if not result:
        error = mt5.last_error()
        return f"Initialization failed: {error}"
    return "Successfully initialized MT5 connection"


@mcp.tool
def mt5_shutdown() -> str:
    """Close connection to MetaTrader 5 terminal."""
    logger.info("mt5_shutdown called")
    mt5.shutdown()
    return "MT5 connection closed"


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


@mcp.tool
def mt5_login(params: LoginParams) -> str:
    """
    Connect to a trading account using login, password, and server.
    """
    logger.info("mt5_login called for login=%s server=%s", params.login, params.server)
    result = mt5.login(
        login=params.login,
        password=params.password,
        server=params.server,
    )
    if not result:
        error = mt5.last_error()
        return f"Login failed: {error}"
    return "Successfully logged in"
