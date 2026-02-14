#!/usr/bin/env python3
"""
Trading operation tools for the MetaTrader 5 MCP server.

Includes:
- sending and checking orders
- margin and profit calculations
"""

from __future__ import annotations

from typing import Any

import MetaTrader5 as mt5

from .logger import logger
from .utils import mcp, mt5_to_python, filter_none
from .schemas import (
    OrderCalcMarginParams,
    OrderCalcProfitParams,
    OrderCheckParams,
    OrderSendParams,
)


@mcp.tool
def mt5_order_send(params: OrderSendParams) -> Any:
    """
    Send a trading order.

    Action types:
      TRADE_ACTION_DEAL=1 (instant), TRADE_ACTION_PENDING=5
    Order types:
      BUY=0, SELL=1, BUY_LIMIT=2, SELL_LIMIT=3, BUY_STOP=4, SELL_STOP=5
    """
    request = filter_none(params.model_dump())

    safe_request: dict[str, Any] = dict(request)
    logger.info("mt5_order_send called with request=%s", safe_request)

    result = mt5.order_send(request)
    return mt5_to_python(result)


@mcp.tool
def mt5_order_check(params: OrderCheckParams) -> Any:
    """
    Check if an order can be executed without actually sending it.

    Uses the same core parameters as `mt5_order_send`.
    """
    request = filter_none(params.model_dump())
    logger.info("mt5_order_check called with request=%s", request)
    result = mt5.order_check(request)
    return mt5_to_python(result)


@mcp.tool
def mt5_order_calc_margin(params: OrderCalcMarginParams) -> float:
    """
    Calculate required margin for an order.

    Action:
      0=BUY, 1=SELL.
    """
    logger.info(
        "mt5_order_calc_margin called action=%s symbol=%s volume=%s price=%s",
        params.action,
        params.symbol,
        params.volume,
        params.price,
    )
    return float(
        mt5.order_calc_margin(
            params.action,
            params.symbol,
            params.volume,
            params.price,
        )
    )


@mcp.tool
def mt5_order_calc_profit(params: OrderCalcProfitParams) -> float:
    """
    Calculate potential profit for an order.

    Action:
      0=BUY, 1=SELL.
    """
    logger.info(
        "mt5_order_calc_profit called action=%s symbol=%s volume=%s price_open=%s price_close=%s",
        params.action,
        params.symbol,
        params.volume,
        params.price_open,
        params.price_close,
    )
    return float(
        mt5.order_calc_profit(
            params.action,
            params.symbol,
            params.volume,
            params.price_open,
            params.price_close,
        )
    )
