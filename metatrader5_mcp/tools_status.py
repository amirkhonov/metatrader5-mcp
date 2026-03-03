#!/usr/bin/env python3
"""
Status and health check tools for the MetaTrader 5 MCP server.
"""

from __future__ import annotations

import sys
from importlib.metadata import version as pkg_version
from typing import Any

import MetaTrader5 as mt5

from .logger import logger
from .utils import mcp, mt5_to_python


def _get_package_version() -> str:
    try:
        return pkg_version("metatrader5-mcp")
    except Exception:
        return "unknown"


@mcp.tool
def mt5_health_check() -> dict[str, Any]:
    """
    Perform a comprehensive health check of the MT5 connection.

    Returns status of:
    - MT5 terminal connection
    - Account login status
    - Terminal version
    - Account information
    - Connection quality
    """
    logger.info("mt5_health_check called")

    health_status = {"status": "unknown", "checks": {}, "warnings": [], "errors": []}

    # Check if MT5 is initialized
    terminal_info = mt5.terminal_info()
    if terminal_info is None:
        health_status["status"] = "error"
        health_status["errors"].append("MT5 terminal not initialized")
        health_status["checks"]["terminal_initialized"] = False
        return health_status

    health_status["checks"]["terminal_initialized"] = True

    # Check terminal info
    terminal_dict = terminal_info._asdict()
    health_status["checks"]["terminal_connected"] = terminal_dict.get(
        "connected", False
    )
    health_status["terminal_info"] = {
        "connected": terminal_dict.get("connected"),
        "trade_allowed": terminal_dict.get("trade_allowed"),
        "build": terminal_dict.get("build"),
        "company": terminal_dict.get("company"),
    }

    # Check account info
    account_info = mt5.account_info()
    if account_info is None:
        health_status["warnings"].append("No account logged in")
        health_status["checks"]["account_logged_in"] = False
    else:
        health_status["checks"]["account_logged_in"] = True
        account_dict = account_info._asdict()
        health_status["account_info"] = {
            "login": account_dict.get("login"),
            "server": account_dict.get("server"),
            "balance": account_dict.get("balance"),
            "trade_allowed": account_dict.get("trade_allowed"),
            "trade_expert": account_dict.get("trade_expert"),
        }

        # Check if trading is allowed
        if not account_dict.get("trade_allowed"):
            health_status["warnings"].append("Trading is not allowed on this account")

    # Check for errors
    last_error = mt5.last_error()
    if last_error and last_error[0] != 1:  # 1 is RET_OK
        health_status["warnings"].append(f"Last error: {last_error}")

    # Determine overall status
    if health_status["errors"]:
        health_status["status"] = "error"
    elif health_status["warnings"]:
        health_status["status"] = "warning"
    elif (
        health_status["checks"]["terminal_initialized"]
        and health_status["checks"]["terminal_connected"]
    ):
        health_status["status"] = "healthy"
    else:
        health_status["status"] = "degraded"

    return health_status


@mcp.tool
def mt5_server_info() -> dict[str, Any]:
    """
    Get comprehensive server and runtime information.

    Returns information about:
    - Python version
    - MT5 Python package version
    - MCP server version
    - System information
    """
    logger.info("mt5_server_info called")

    mt5_version = mt5.version()

    return {
        "mcp_server": {"version": _get_package_version(), "name": "metatrader5-mcp"},
        "python": {"version": sys.version, "executable": sys.executable},
        "mt5_package": mt5_to_python(mt5_version) if mt5_version else None,
        "runtime": {
            "platform": sys.platform,
        },
    }


@mcp.tool
def mt5_connection_status() -> dict[str, Any]:
    """
    Get current connection status with MT5 terminal.

    Returns quick status check for monitoring.
    """
    logger.info("mt5_connection_status called")

    terminal_info = mt5.terminal_info()
    account_info = mt5.account_info()

    status = {
        "initialized": terminal_info is not None,
        "connected": False,
        "logged_in": account_info is not None,
        "trade_allowed": False,
    }

    if terminal_info:
        terminal_dict = terminal_info._asdict()
        status["connected"] = terminal_dict.get("connected", False)

    if account_info:
        account_dict = account_info._asdict()
        status["trade_allowed"] = account_dict.get("trade_allowed", False)
        status["account"] = account_dict.get("login")
        status["server"] = account_dict.get("server")

    return status
