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
    Get open positions.

    Can filter by symbol, group pattern, or ticket number.
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
    Get active pending orders.

    Can filter by symbol, group pattern, or ticket number.
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
    Get orders from history.

    Can filter by date range, symbol group, order ticket, or position ticket.
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
    Get deals from history.

    Can filter by date range, symbol group, deal ticket, or position ticket.
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
