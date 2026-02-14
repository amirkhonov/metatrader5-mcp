#!/usr/bin/env python3
"""
Entrypoint for the MetaTrader 5 FastMCP server with CLI argument support.

Supports arguments:
  --login     Trading account number
  --password  Trading account password
  --server    Trading server name
  --path      Path to MT5 terminal executable
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional

from .logger import logger
from .utils import mcp

# Import tool modules so their @mcp.tool decorators register with the app.
from . import tools_connection  # noqa: F401
from . import tools_market  # noqa: F401
from . import tools_trading  # noqa: F401
from . import tools_positions  # noqa: F401


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="MetaTrader 5 MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--login",
        type=int,
        help="Trading account number",
    )
    parser.add_argument(
        "--password",
        type=str,
        help="Trading account password",
    )
    parser.add_argument(
        "--server",
        type=str,
        help="Trading server name",
    )
    parser.add_argument(
        "--path",
        type=str,
        help="Path to MT5 terminal executable",
    )

    return parser.parse_args(args)


def main(args: Optional[list[str]] = None) -> None:
    """Run the FastMCP server over stdio with optional auto-initialization."""
    parsed = parse_args(args)

    logger.info("MetaTrader 5 FastMCP server starting...")

    # Auto-initialize if credentials are provided
    if any([parsed.login, parsed.password, parsed.server, parsed.path]):
        import MetaTrader5 as mt5

        init_kwargs = {}
        if parsed.path:
            init_kwargs["path"] = parsed.path
        if parsed.login:
            init_kwargs["login"] = parsed.login
        if parsed.password:
            init_kwargs["password"] = parsed.password
        if parsed.server:
            init_kwargs["server"] = parsed.server

        safe_kwargs = {
            k: v if k != "password" else "***" for k, v in init_kwargs.items()
        }
        logger.info("Auto-initializing MT5 with: %s", safe_kwargs)

        result = mt5.initialize(**init_kwargs)
        if not result:
            error = mt5.last_error()
            logger.error("MT5 initialization failed: %s", error)
            sys.exit(1)
        logger.info("MT5 initialized successfully")

    mcp.run()


if __name__ == "__main__":
    main()
