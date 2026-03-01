#!/usr/bin/env python3
"""
Position, order, and history tools for the MetaTrader 5 MCP server.
"""

from __future__ import annotations

from typing import Any

import MetaTrader5 as mt5

from .logger import logger
from .schemas import (
    HistoryDealsGetParams,
    HistoryDealsTotalParams,
    HistoryOrdersGetParams,
    HistoryOrdersTotalParams,
    OrdersGetParams,
    PositionsGetParams,
)
from .utils import filter_none, mcp, mt5_to_python, parse_datetime


@mcp.tool
def mt5_positions_total() -> int:
    """Get the total number of open positions."""
    logger.info("mt5_positions_total called")
    return mt5.positions_total()


@mcp.tool
def mt5_positions_get(params: PositionsGetParams) -> Any:
    """
    Get open positions, optionally filtered by symbol, group pattern, or ticket.

    Only one filter is used at a time; if `symbol` is provided it takes precedence
    over `ticket`. If `group` is provided, only positions whose symbol names match
    the pattern are returned.

    The `group` filter supports wildcards ('*'), comma-separated conditions, and
    negation ('!'). Conditions are applied left-to-right (inclusions before exclusions).
    Examples:
        group='*EUR*'           → positions on EUR pairs
        group='*,!*USD*'        → all positions except USD pairs
    """
    kwargs = filter_none(params.model_dump())
    logger.info("mt5_positions_get called with %s", kwargs)
    if kwargs:
        result = mt5.positions_get(**kwargs)
    else:
        result = mt5.positions_get()
    return mt5_to_python(result)


@mcp.tool
def mt5_orders_total() -> int:
    """Get the total number of active pending orders."""
    logger.info("mt5_orders_total called")
    return mt5.orders_total()


@mcp.tool
def mt5_orders_get(params: OrdersGetParams) -> Any:
    """
    Get active pending orders, optionally filtered by symbol, group pattern, or ticket.

    Parameter precedence (only one filter is applied by MT5):
      - If `symbol` is provided, only orders on that symbol are returned and
        `ticket` is ignored.
      - If `group` is provided, orders are filtered by symbol name pattern.
      - If `ticket` is provided, the specific order is returned.
      - If none are provided, all active orders are returned.

    The `group` filter supports wildcards ('*'), comma-separated conditions, and
    negation ('!'). Conditions are applied left-to-right (inclusions before exclusions).
    Examples:
        group='*GBP*'           → orders on GBP pairs
        group='*, !*EUR*'       → all orders except EUR pairs
    """
    kwargs = filter_none(params.model_dump())
    logger.info("mt5_orders_get called with %s", kwargs)
    if kwargs:
        result = mt5.orders_get(**kwargs)
    else:
        result = mt5.orders_get()
    return mt5_to_python(result)


@mcp.tool
def mt5_history_orders_total(params: HistoryOrdersTotalParams) -> int:
    """Get the total number of orders in history for a date range."""
    logger.info(
        "mt5_history_orders_total called date_from=%s date_to=%s",
        params.date_from,
        params.date_to,
    )
    date_from = parse_datetime(params.date_from)
    date_to = parse_datetime(params.date_to)
    return mt5.history_orders_total(date_from, date_to)


@mcp.tool
def mt5_history_orders_get(params: HistoryOrdersGetParams) -> Any:
    """
    Get orders from history, filtered by date range and/or symbol group, order ticket, or position ticket.

    `date_from` and `date_to` (UTC, 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS') are required
    when filtering by date range; they can be combined with `group`.
    Use `ticket` to retrieve a single order by ticket number, or `position` to retrieve
    all orders linked to a specific position.

    The `group` filter supports wildcards ('*'), comma-separated conditions, and
    negation ('!'). Conditions are applied left-to-right (inclusions before exclusions).
    Examples:
        group='*EUR*'           → history orders on EUR pairs
        group='*, !*USD*'       → all history orders except USD pairs
    """
    raw = params.model_dump()
    kwargs: dict[str, Any] = {}

    if raw.get("date_from") and raw.get("date_to"):
        kwargs["date_from"] = parse_datetime(raw["date_from"])
        kwargs["date_to"] = parse_datetime(raw["date_to"])

    for key in ("group", "ticket", "position"):
        value = raw.get(key)
        if value is not None:
            kwargs[key] = value

    logger.info("mt5_history_orders_get called with %s", kwargs)

    if kwargs:
        result = mt5.history_orders_get(**kwargs)
    else:
        result = mt5.history_orders_get()
    return mt5_to_python(result)


@mcp.tool
def mt5_history_deals_total(params: HistoryDealsTotalParams) -> int:
    """Get the total number of deals in history for a date range."""
    logger.info(
        "mt5_history_deals_total called date_from=%s date_to=%s",
        params.date_from,
        params.date_to,
    )
    date_from = parse_datetime(params.date_from)
    date_to = parse_datetime(params.date_to)
    return mt5.history_deals_total(date_from, date_to)


@mcp.tool
def mt5_history_deals_get(params: HistoryDealsGetParams) -> Any:
    """
    Get deals from history, filtered by date range and/or symbol group, deal ticket, or position ticket.

    `date_from` and `date_to` (UTC, 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS') are required
    when filtering by date range; they can be combined with `group`.
    Use `ticket` to retrieve a single deal by ticket number, or `position` to retrieve
    all deals linked to a specific position.

    The `group` filter supports wildcards ('*'), comma-separated conditions, and
    negation ('!'). Conditions are applied left-to-right (inclusions before exclusions).
    Examples:
        group='*EUR*'           → history deals on EUR pairs
        group='*, !*USD*'       → all history deals except USD pairs
    """
    raw = params.model_dump()
    kwargs: dict[str, Any] = {}

    if raw.get("date_from") and raw.get("date_to"):
        kwargs["date_from"] = parse_datetime(raw["date_from"])
        kwargs["date_to"] = parse_datetime(raw["date_to"])

    for key in ("group", "ticket", "position"):
        value = raw.get(key)
        if value is not None:
            kwargs[key] = value

    logger.info("mt5_history_deals_get called with %s", kwargs)

    if kwargs:
        result = mt5.history_deals_get(**kwargs)
    else:
        result = mt5.history_deals_get()
    return mt5_to_python(result)
