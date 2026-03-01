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
from .schemas import (
    OrderCalcMarginParams,
    OrderCalcProfitParams,
    OrderCheckParams,
    OrderSendParams,
)
from .utils import filter_none, mcp, mt5_to_python

# ---------------------------------------------------------------------------
# Retcode helpers — shared by order_send and order_check
# ---------------------------------------------------------------------------

_SUCCESS_RETCODES: frozenset[int] = frozenset(
    {
        mt5.TRADE_RETCODE_DONE,  # 10009 - market order executed
        mt5.TRADE_RETCODE_PLACED,  # 10008 - pending order placed
        mt5.TRADE_RETCODE_DONE_PARTIAL,  # 10010 - partially filled (rest cancelled)
    }
)

_RETCODE_MESSAGES: dict[int, str] = {
    mt5.TRADE_RETCODE_REQUOTE: "REQUOTE - price changed, retry with a fresh quote",
    mt5.TRADE_RETCODE_REJECT: "REJECT - request rejected by the broker",
    mt5.TRADE_RETCODE_CANCEL: "CANCEL - request cancelled by the trader",
    mt5.TRADE_RETCODE_ERROR: "ERROR - general request processing error",
    mt5.TRADE_RETCODE_TIMEOUT: "TIMEOUT - no response from the trade server",
    mt5.TRADE_RETCODE_INVALID: "INVALID - invalid request structure",
    mt5.TRADE_RETCODE_INVALID_VOLUME: "INVALID_VOLUME - check min/max/step lot size for the symbol",
    mt5.TRADE_RETCODE_INVALID_PRICE: "INVALID_PRICE - price is stale; fetch a fresh ask/bid first",
    mt5.TRADE_RETCODE_INVALID_STOPS: "INVALID_STOPS - SL or TP violates the minimum distance rules",
    mt5.TRADE_RETCODE_TRADE_DISABLED: "TRADE_DISABLED - trading is disabled for this symbol or account",
    mt5.TRADE_RETCODE_MARKET_CLOSED: "MARKET_CLOSED - the market is not open for trading right now",
    mt5.TRADE_RETCODE_NO_MONEY: "NO_MONEY - insufficient margin to place this order",
    mt5.TRADE_RETCODE_PRICE_CHANGED: "PRICE_CHANGED - price moved during execution, retry",
    mt5.TRADE_RETCODE_PRICE_OFF: "PRICE_OFF - broker is not streaming quotes for this symbol",
    mt5.TRADE_RETCODE_INVALID_EXPIRATION: "INVALID_EXPIRATION - invalid order expiration date/time",
    mt5.TRADE_RETCODE_ORDER_CHANGED: "ORDER_CHANGED - order state changed during processing",
    mt5.TRADE_RETCODE_TOO_MANY_REQUESTS: "TOO_MANY_REQUESTS - slow down; too many requests per second",
    mt5.TRADE_RETCODE_NO_CHANGES: "NO_CHANGES - modify request contains no actual changes",
    mt5.TRADE_RETCODE_SERVER_DISABLES_AT: "SERVER_DISABLES_AT - auto-trading disabled by the server",
    mt5.TRADE_RETCODE_CLIENT_DISABLES_AT: "CLIENT_DISABLES_AT - auto-trading disabled in MT5 terminal settings",
    mt5.TRADE_RETCODE_LOCKED: "LOCKED - order is locked for processing, retry shortly",
    mt5.TRADE_RETCODE_FROZEN: "FROZEN - order or position is frozen (check symbol trading hours)",
    mt5.TRADE_RETCODE_INVALID_FILL: "INVALID_FILL - filling mode not supported; try type_filling=2 (RETURN)",
    mt5.TRADE_RETCODE_CONNECTION: "CONNECTION - no connection to the trade server",
    mt5.TRADE_RETCODE_ONLY_REAL: "ONLY_REAL - operation allowed on real accounts only",
    mt5.TRADE_RETCODE_LIMIT_ORDERS: "LIMIT_ORDERS - maximum number of pending orders reached",
    mt5.TRADE_RETCODE_LIMIT_VOLUME: "LIMIT_VOLUME - maximum order/position volume for this symbol reached",
    mt5.TRADE_RETCODE_INVALID_ORDER: "INVALID_ORDER - incorrect or prohibited order type",
    mt5.TRADE_RETCODE_POSITION_CLOSED: "POSITION_CLOSED - position with this identifier is already closed",
    mt5.TRADE_RETCODE_INVALID_CLOSE_VOLUME: "INVALID_CLOSE_VOLUME - close volume exceeds the current position volume",
    mt5.TRADE_RETCODE_CLOSE_ORDER_EXIST: "CLOSE_ORDER_EXIST - a close order already exists for this position",
    mt5.TRADE_RETCODE_LIMIT_POSITIONS: "LIMIT_POSITIONS - maximum number of open positions reached (server limit)",
    mt5.TRADE_RETCODE_REJECT_CANCEL: "REJECT_CANCEL - pending order activation rejected; order cancelled",
    mt5.TRADE_RETCODE_LONG_ONLY: "LONG_ONLY - only long (buy) positions are allowed for this symbol",
    mt5.TRADE_RETCODE_SHORT_ONLY: "SHORT_ONLY - only short (sell) positions are allowed for this symbol",
    mt5.TRADE_RETCODE_CLOSE_ONLY: "CLOSE_ONLY - only position closing is allowed for this symbol",
    mt5.TRADE_RETCODE_FIFO_CLOSE: "FIFO_CLOSE - positions must be closed in FIFO order (account rule)",
}


def _describe_retcode(retcode: int) -> str:
    """Return a human-readable description for a trade retcode."""
    return _RETCODE_MESSAGES.get(retcode, f"retcode {retcode} (undocumented)")


def _get_filling_mode_error_suggestion(symbol: str) -> str:
    """Provide a broker-specific suggestion for filling mode when INVALID_FILL occurs."""
    info = mt5.symbol_info(symbol)
    if info is None:
        return ""

    modes = []
    if info.filling_mode & mt5.SYMBOL_FILLING_FOK:
        modes.append("0 (FOK)")
    if info.filling_mode & mt5.SYMBOL_FILLING_IOC:
        modes.append("1 (IOC)")

    # If the broker explicitly lists modes, suggest them.
    # Otherwise, 2 (RETURN) is often the default for netting accounts or certain symbols.
    if modes:
        return f" Supported modes for this symbol: {', '.join(modes)}."
    else:
        return " Try type_filling=2 (RETURN) if you haven't already."


def _deserialize_result(result: Any) -> dict[str, Any]:
    """
    Convert an MT5 trade result named tuple into a plain dict.

    The ``request`` field nested inside the result is itself a named tuple
    (MqlTradeRequest), so it needs a second pass of conversion.
    """
    result_dict: dict[str, Any] = mt5_to_python(result)  # type: ignore[assignment]
    # The nested MqlTradeRequest field also needs converting
    if isinstance(result_dict, dict) and hasattr(result_dict.get("request"), "_asdict"):
        result_dict["request"] = result_dict["request"]._asdict()
    return result_dict


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool
def mt5_order_send(params: OrderSendParams) -> Any:
    """
    Send a trading order to MetaTrader 5.

    action (required):
      1  = TRADE_ACTION_DEAL      - Instant market execution
      5  = TRADE_ACTION_PENDING   - Place a pending order
      6  = TRADE_ACTION_SLTP      - Modify SL/TP on an open position
      7  = TRADE_ACTION_MODIFY    - Modify an existing pending order
      8  = TRADE_ACTION_REMOVE    - Delete a pending order
      10 = TRADE_ACTION_CLOSE_BY  - Close a position using an opposite one

    type (order type):
      0=BUY, 1=SELL
      2=BUY_LIMIT, 3=SELL_LIMIT
      4=BUY_STOP,  5=SELL_STOP
      6=BUY_STOP_LIMIT, 7=SELL_STOP_LIMIT
      8=CLOSE_BY

    type_filling:
      0=FOK (Fill or Kill), 1=IOC (Immediate or Cancel), 2=RETURN

    type_time:
      0=GTC, 1=DAY, 2=SPECIFIED (requires expiration), 3=SPECIFIED_DAY

    All fields (MqlTradeRequest):
      symbol       - Symbol name, e.g. 'EURUSD'
      volume       - Trade volume in lots
      price        - Order price (ask for BUY, bid for SELL)
      stoplimit    - Limit price for BUY_STOP_LIMIT / SELL_STOP_LIMIT
      sl           - Stop Loss price
      tp           - Take Profit price
      deviation    - Maximum price deviation in points (market orders)
      magic        - Expert Advisor ID (magic number)
      comment      - Order comment (up to 31 chars)
      expiration   - Unix timestamp; only for type_time=2
      order        - Ticket of existing order (MODIFY / REMOVE)
      position     - Open position ticket (SLTP / CLOSE_BY)
      position_by  - Opposite position ticket (CLOSE_BY)

    Returns MqlTradeResult: retcode, deal, order, volume, price,
    bid, ask, comment, request_id, and the echoed request structure.
    """
    request = filter_none(params.model_dump())
    logger.info("mt5_order_send request=%s", request)

    result = mt5.order_send(request)

    # ── Stage 1: MT5 internal failure (None means the API call itself failed) ──
    if result is None:
        error_code, error_msg = mt5.last_error()
        logger.error("mt5_order_send returned None: [%s] %s", error_code, error_msg)
        raise RuntimeError(
            f"mt5.order_send() returned None.\n"
            f"MT5 error {error_code}: {error_msg}\n"
            f"Request: {request}\n"
            f"Common causes:\n"
            f"  • MT5 not initialised - call mt5_initialize first\n"
            f"  • Symbol not selected - call mt5_symbol_select first\n"
            f"  • Auto-trading disabled - enable in MT5 terminal options\n"
            f"  • Invalid account or insufficient permissions"
        )

    result_dict = _deserialize_result(result)
    retcode = result_dict.get("retcode")

    # ── Stage 2: Broker-level rejection (result returned but order not accepted) ──
    if retcode not in _SUCCESS_RETCODES:
        broker_comment = result_dict.get("comment", "")
        description = _describe_retcode(retcode)

        # Enhance INVALID_FILL with specific suggestions
        if retcode == mt5.TRADE_RETCODE_INVALID_FILL:
            symbol = request.get("symbol", "")
            if symbol:
                description += _get_filling_mode_error_suggestion(symbol)

        logger.error("mt5_order_send failed retcode=%s (%s)", retcode, description)
        raise RuntimeError(
            f"Order rejected by broker: {description}\n"
            f"Broker comment: {broker_comment!r}\n"
            f"Request: {request}\n"
            f"Result:  {result_dict}"
        )

    logger.info(
        "mt5_order_send success retcode=%s deal=%s order=%s",
        retcode,
        result_dict.get("deal"),
        result_dict.get("order"),
    )
    return result_dict


@mcp.tool
def mt5_order_check(params: OrderCheckParams) -> Any:
    """
    Check funds sufficiency for a trading operation without sending it.

    Use this BEFORE mt5_order_send to validate parameters and margin.
    Accepts the same MqlTradeRequest fields as mt5_order_send:

      action       - 1=DEAL, 5=PENDING, 6=SLTP, 7=MODIFY, 8=REMOVE, 10=CLOSE_BY
      symbol       - Symbol name (e.g. 'EURUSD')
      volume       - Trade volume in lots
      type         - 0=BUY, 1=SELL, 2=BUY_LIMIT, 3=SELL_LIMIT, 4=BUY_STOP,
                     5=SELL_STOP, 6=BUY_STOP_LIMIT, 7=SELL_STOP_LIMIT, 8=CLOSE_BY
      price        - Order price (ask for BUY, bid for SELL)
      stoplimit    - Limit price for BUY_STOP_LIMIT / SELL_STOP_LIMIT
      sl           - Stop Loss price
      tp           - Take Profit price
      deviation    - Maximum price deviation in points
      magic        - Expert Advisor ID (magic number)
      comment      - Order comment
      type_time    - 0=GTC, 1=DAY, 2=SPECIFIED (use expiration), 3=SPECIFIED_DAY
      type_filling - 0=FOK, 1=IOC, 2=RETURN
      expiration   - Unix timestamp, only for type_time=2 (ORDER_TIME_SPECIFIED)
      order        - Ticket of existing order (MODIFY / REMOVE)
      position     - Open position ticket (SLTP / CLOSE_BY)
      position_by  - Opposite position ticket (CLOSE_BY)

    Returns MqlTradeCheckResult: retcode, balance, equity, profit,
    margin, margin_free, margin_level, comment, and the echoed request.
    A retcode of 0 means the check passed.
    """
    request = filter_none(params.model_dump())
    logger.info("mt5_order_check request=%s", request)

    result = mt5.order_check(request)

    if result is None:
        error_code, error_msg = mt5.last_error()
        logger.error("mt5_order_check returned None: [%s] %s", error_code, error_msg)
        raise RuntimeError(
            f"mt5.order_check() returned None.\n"
            f"MT5 error {error_code}: {error_msg}\n"
            f"Request: {request}\n"
            f"Common causes:\n"
            f"  • MT5 not initialised - call mt5_initialize first\n"
            f"  • Invalid parameters - check symbol, volume, and price\n"
            f"  • Symbol not selected - call mt5_symbol_select first"
        )

    result_dict = _deserialize_result(result)
    retcode = result_dict.get("retcode")

    if retcode != 0:
        description = _describe_retcode(retcode)
        broker_comment = result_dict.get("comment", "")

        # Enhance INVALID_FILL with specific suggestions
        if retcode == mt5.TRADE_RETCODE_INVALID_FILL:
            symbol = request.get("symbol", "")
            if symbol:
                description += _get_filling_mode_error_suggestion(symbol)

        logger.warning("mt5_order_check failed retcode=%s (%s)", retcode, description)
        raise RuntimeError(
            f"Order check failed: {description}\n"
            f"Broker comment: {broker_comment!r}\n"
            f"Request: {request}\n"
            f"Result:  {result_dict}"
        )

    return result_dict


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
    result = mt5.order_calc_margin(
        params.action,
        params.symbol,
        params.volume,
        params.price,
    )
    if result is None:
        error_code, error_msg = mt5.last_error()
        raise RuntimeError(
            f"mt5.order_calc_margin() returned None.\n"
            f"MT5 error {error_code}: {error_msg}\n"
            f"Params: action={params.action}, symbol={params.symbol!r}, "
            f"volume={params.volume}, price={params.price}"
        )
    return float(result)


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
    result = mt5.order_calc_profit(
        params.action,
        params.symbol,
        params.volume,
        params.price_open,
        params.price_close,
    )
    if result is None:
        error_code, error_msg = mt5.last_error()
        raise RuntimeError(
            f"mt5.order_calc_profit() returned None.\n"
            f"MT5 error {error_code}: {error_msg}\n"
            f"Params: action={params.action}, symbol={params.symbol!r}, "
            f"volume={params.volume}, price_open={params.price_open}, price_close={params.price_close}"
        )
    return float(result)
