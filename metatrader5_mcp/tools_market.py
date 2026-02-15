#!/usr/bin/env python3
"""
Market data tools for the MetaTrader 5 MCP server.

Includes:
- symbol information
- historical bars and ticks
"""

from __future__ import annotations

from typing import Any

import MetaTrader5 as mt5

from .logger import logger
from .schemas import (
    CopyRatesFromParams,
    CopyRatesFromPosParams,
    CopyRatesRangeParams,
    CopyTicksFromParams,
    CopyTicksRangeParams,
    SymbolParams,
    SymbolSelectParams,
    SymbolsGetParams,
)
from .utils import filter_none, mcp, mt5_to_python, parse_datetime


@mcp.tool
def mt5_symbols_total() -> int:
    """Get the total number of available symbols."""
    logger.info("mt5_symbols_total called")
    return mt5.symbols_total()


@mcp.tool
def mt5_symbols_get(params: SymbolsGetParams) -> Any:
    """
    Get all available symbols or filter by group pattern (e.g., '*EUR*', 'FOREX\\\\*').
    """
    logger.info("mt5_symbols_get called with group=%s", params.group)
    if params.group is not None:
        result = mt5.symbols_get(group=params.group)
    else:
        result = mt5.symbols_get()
    return mt5_to_python(result)


@mcp.tool
def mt5_symbol_info(params: SymbolParams) -> Any:
    """Get detailed information about a specific symbol."""
    logger.info("mt5_symbol_info called for symbol=%s", params.symbol)
    return mt5_to_python(mt5.symbol_info(params.symbol))


@mcp.tool
def mt5_symbol_info_tick(params: SymbolParams) -> Any:
    """Get the current tick (price quote) for a symbol."""
    logger.info("mt5_symbol_info_tick called for symbol=%s", params.symbol)
    return mt5_to_python(mt5.symbol_info_tick(params.symbol))


@mcp.tool
def mt5_symbol_select(params: SymbolSelectParams) -> bool:
    """Add or remove a symbol from the Market Watch window."""
    logger.info(
        "mt5_symbol_select called for symbol=%s enable=%s",
        params.symbol,
        params.enable,
    )
    return bool(mt5.symbol_select(params.symbol, params.enable))


@mcp.tool
def mt5_copy_rates_from(params: CopyRatesFromParams) -> Any:
    """
    Get historical bar data starting from a specific date.

    Timeframe in minutes:
    1=M1, 5=M5, 15=M15, 30=M30, 60=H1, 240=H4, 1440=D1, 10080=W1, 43200=MN1.
    """
    logger.info(
        "mt5_copy_rates_from called for symbol=%s timeframe=%s date_from=%s count=%s",
        params.symbol,
        params.timeframe,
        params.date_from,
        params.count,
    )
    date_from = parse_datetime(params.date_from)
    rates = mt5.copy_rates_from(
        params.symbol,
        params.timeframe,
        date_from,
        params.count,
    )
    return mt5_to_python(rates)


@mcp.tool
def mt5_copy_rates_range(params: CopyRatesRangeParams) -> Any:
    """Get historical bar data for a specific date range."""
    logger.info(
        "mt5_copy_rates_range called for symbol=%s timeframe=%s date_from=%s date_to=%s",
        params.symbol,
        params.timeframe,
        params.date_from,
        params.date_to,
    )
    date_from = parse_datetime(params.date_from)
    date_to = parse_datetime(params.date_to)
    rates = mt5.copy_rates_range(
        params.symbol,
        params.timeframe,
        date_from,
        date_to,
    )
    return mt5_to_python(rates)


@mcp.tool
def mt5_copy_rates_from_pos(params: CopyRatesFromPosParams) -> Any:
    """
    Get historical bar data starting from a position index.

    Timeframe in minutes:
    1=M1, 5=M5, 15=M15, 30=M30, 60=H1, 240=H4, 1440=D1, 10080=W1, 43200=MN1.
    """
    logger.info(
        "mt5_copy_rates_from_pos called for symbol=%s timeframe=%s start_pos=%s count=%s",
        params.symbol,
        params.timeframe,
        params.start_pos,
        params.count,
    )
    rates = mt5.copy_rates_from_pos(
        params.symbol,
        params.timeframe,
        params.start_pos,
        params.count,
    )
    return mt5_to_python(rates)


@mcp.tool
def mt5_copy_ticks_from(params: CopyTicksFromParams) -> Any:
    """
    Get historical tick data starting from a specific date.

    Flags:
    0=INFO, 2=TRADE, 4=BID, 8=ASK, 6=ALL.
    """
    logger.info(
        "mt5_copy_ticks_from called for symbol=%s date_from=%s count=%s flags=%s",
        params.symbol,
        params.date_from,
        params.count,
        params.flags,
    )
    date_from = parse_datetime(params.date_from)
    ticks = mt5.copy_ticks_from(
        params.symbol,
        date_from,
        params.count,
        params.flags,
    )
    return mt5_to_python(ticks)


@mcp.tool
def mt5_copy_ticks_range(params: CopyTicksRangeParams) -> Any:
    """
    Get historical tick data for a specific date range.

    Flags:
    0=INFO, 2=TRADE, 4=BID, 8=ASK, 6=ALL.
    """
    logger.info(
        "mt5_copy_ticks_range called for symbol=%s date_from=%s date_to=%s flags=%s",
        params.symbol,
        params.date_from,
        params.date_to,
        params.flags,
    )
    date_from = parse_datetime(params.date_from)
    date_to = parse_datetime(params.date_to)
    ticks = mt5.copy_ticks_range(
        params.symbol,
        date_from,
        date_to,
        params.flags,
    )
    return mt5_to_python(ticks)
