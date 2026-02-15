#!/usr/bin/env python3
"""
Entrypoint for the MetaTrader 5 FastMCP server with CLI argument support.

Supports arguments:
  --login     Trading account number
  --password  Trading account password
  --server    Trading server name
  --path      Path to MT5 terminal executable

Environment variables:
  MT5_LOGIN    Trading account number
  MT5_PASSWORD Trading account password
  MT5_SERVER   Trading server name
  MT5_PATH     Path to MT5 terminal executable
  LOG_LEVEL    Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

# Import tool modules so their @mcp.tool decorators register with the app.
from . import tools_connection  # noqa: F401
from . import tools_market  # noqa: F401
from . import tools_positions  # noqa: F401
from . import tools_status  # noqa: F401
from . import tools_trading  # noqa: F401
from .logger import configure_logging, logger
from .utils import mcp


def load_env_file() -> None:
    """Load environment variables from .env file if it exists."""
    env_file = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_file):
        return

    try:
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    # Only set if not already in environment
                    if key not in os.environ:
                        os.environ[key] = value
        logger.debug("Loaded environment variables from .env file")
    except Exception as e:
        logger.warning("Failed to load .env file: %s", e)


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command line arguments with environment variable fallbacks."""
    parser = argparse.ArgumentParser(
        description="MetaTrader 5 MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment variables can be used as fallbacks:
  MT5_LOGIN, MT5_PASSWORD, MT5_SERVER, MT5_PATH, LOG_LEVEL

Example:
  metatrader5-mcp --login 12345 --password secret --server MetaQuotes-Demo

Or with environment variables:
  export MT5_LOGIN=12345
  export MT5_PASSWORD=secret
  export MT5_SERVER=MetaQuotes-Demo
  metatrader5-mcp
        """,
    )

    parser.add_argument(
        "--login",
        type=int,
        default=os.getenv("MT5_LOGIN"),
        help="Trading account number (or set MT5_LOGIN env var)",
    )
    parser.add_argument(
        "--password",
        type=str,
        default=os.getenv("MT5_PASSWORD"),
        help="Trading account password (or set MT5_PASSWORD env var)",
    )
    parser.add_argument(
        "--server",
        type=str,
        default=os.getenv("MT5_SERVER"),
        help="Trading server name (or set MT5_SERVER env var)",
    )
    parser.add_argument(
        "--path",
        type=str,
        default=os.getenv("MT5_PATH"),
        help="Path to MT5 terminal executable (or set MT5_PATH env var)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default=os.getenv("LOG_LEVEL", "INFO"),
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (or set LOG_LEVEL env var)",
    )

    return parser.parse_args(args)


def main(args: Optional[list[str]] = None) -> None:
    """Run the FastMCP server over stdio with optional auto-initialization."""
    # Load .env file if it exists
    load_env_file()

    # Parse arguments
    parsed = parse_args(args)

    # Configure logging
    configure_logging(parsed.log_level)

    logger.info("MetaTrader 5 MCP Server v0.1.0")
    logger.info("Starting server with log level: %s", parsed.log_level)

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

        try:
            result = mt5.initialize(**init_kwargs)
            if not result:
                error = mt5.last_error()
                logger.error("MT5 initialization failed: %s", error)
                logger.error("Please check your credentials and MT5 terminal status")
                sys.exit(1)
            logger.info("MT5 initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize MT5: %s", e)
            logger.error("Is MetaTrader 5 installed and running?")
            sys.exit(1)
    else:
        logger.info("No credentials provided - manual initialization required")
        logger.info("Use mt5_initialize tool or provide credentials via CLI/env vars")

    logger.info("Server ready - waiting for MCP client connections")
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error("Server error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
