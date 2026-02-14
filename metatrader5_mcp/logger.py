#!/usr/bin/env python3
"""
Central logging configuration for the MetaTrader 5 MCP server.

This module defines the shared `logger` instance used across the project.
"""

from __future__ import annotations

import logging

# Basic logging configuration for the whole application.
logging.basicConfig(level=logging.INFO)

# Shared logger instance for all modules.
logger = logging.getLogger("mt5-fastmcp-server")
