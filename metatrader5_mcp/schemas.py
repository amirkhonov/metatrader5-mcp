#!/usr/bin/env python3
"""
Pydantic schemas for MetaTrader 5 MCP server tool parameters.

These models provide strict validation of incoming MCP tool arguments while
mirroring the MetaTrader5 Python integration API:
https://www.mql5.com/en/docs/python_metatrader5
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ParamsBase(BaseModel):
    """Base model with strict extra field handling."""

    model_config = ConfigDict(extra="forbid")


# Market Data - Symbols -------------------------------------------------------


class SymbolsGetParams(ParamsBase):
    group: Optional[str] = Field(
        default=None,
        description=(
            "Optional symbol group filter. Supports wildcards ('*'), comma-separated "
            "conditions, and negation ('!'). Conditions are evaluated left-to-right, "
            "so inclusion patterns must come before exclusion patterns. "
            "Examples: '*EUR*' (symbols containing EUR), "
            "'*,!*USD*,!*EUR*' (all except USD/EUR), "
            "'FOREX*,!*USD*' (FOREX symbols without USD)."
        ),
    )


class SymbolParams(ParamsBase):
    symbol: str = Field(description="Symbol name, e.g. 'EURUSD'")


class SymbolSelectParams(SymbolParams):
    enable: bool = Field(
        description="True to add symbol to Market Watch, False to remove"
    )


# Market Data - Historical Data ----------------------------------------------


class CopyRatesFromParams(ParamsBase):
    symbol: str = Field(description="Symbol name")
    timeframe: int = Field(
        description=(
            "Timeframe in minutes: 1=M1, 5=M5, 15=M15, 30=M30, 60=H1, "
            "240=H4, 1440=D1, 10080=W1, 43200=MN1"
        )
    )
    date_from: str = Field(description="Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)")
    count: int = Field(description="Number of bars to retrieve")


class CopyRatesRangeParams(ParamsBase):
    symbol: str = Field(description="Symbol name")
    timeframe: int = Field(
        description=(
            "Timeframe in minutes: 1=M1, 5=M5, 15=M15, 30=M30, 60=H1, "
            "240=H4, 1440=D1, 10080=W1, 43200=MN1"
        )
    )
    date_from: str = Field(description="Start date")
    date_to: str = Field(description="End date")


class CopyRatesFromPosParams(ParamsBase):
    symbol: str = Field(description="Symbol name")
    timeframe: int = Field(
        description=(
            "Timeframe in minutes: 1=M1, 5=M5, 15=M15, 30=M30, 60=H1, "
            "240=H4, 1440=D1, 10080=W1, 43200=MN1"
        )
    )
    start_pos: int = Field(
        description="Starting position index (0 = current bar, positive to go back)"
    )
    count: int = Field(description="Number of bars to retrieve")


class CopyTicksFromParams(ParamsBase):
    symbol: str = Field(description="Symbol name")
    date_from: str = Field(description="Start date")
    count: int = Field(description="Number of ticks to retrieve")
    flags: int = Field(
        description=(
            "Tick type flags: 0=INFO, 2=TRADE, 4=BID, 8=ASK, 6=ALL "
            "(bitwise OR of COPY_TICKS_* constants)"
        )
    )


class CopyTicksRangeParams(ParamsBase):
    symbol: str = Field(description="Symbol name")
    date_from: str = Field(description="Start date")
    date_to: str = Field(description="End date")
    flags: int = Field(
        description=(
            "Tick type flags: 0=INFO, 2=TRADE, 4=BID, 8=ASK, 6=ALL "
            "(bitwise OR of COPY_TICKS_* constants)"
        )
    )


# Trading Operations ----------------------------------------------------------


class OrderSendParams(ParamsBase):
    action: int = Field(
        description=(
            "Trade action type: 1=TRADE_ACTION_DEAL (market order), "
            "5=TRADE_ACTION_PENDING (pending order), "
            "6=TRADE_ACTION_SLTP (modify SL/TP of open position), "
            "7=TRADE_ACTION_MODIFY (modify pending order), "
            "8=TRADE_ACTION_REMOVE (delete pending order), "
            "10=TRADE_ACTION_CLOSE_BY (close by opposite position)"
        )
    )
    symbol: Optional[str] = Field(
        default=None,
        description="Symbol name - not required for TRADE_ACTION_MODIFY or TRADE_ACTION_CLOSE_BY",
    )
    volume: Optional[float] = Field(default=None, description="Trade volume in lots")
    type: Optional[int] = Field(
        default=None,
        description=(
            "Order type: 0=BUY, 1=SELL, 2=BUY_LIMIT, 3=SELL_LIMIT, "
            "4=BUY_STOP, 5=SELL_STOP, 6=BUY_STOP_LIMIT, 7=SELL_STOP_LIMIT, "
            "8=CLOSE_BY"
        ),
    )
    price: Optional[float] = Field(
        default=None,
        description=(
            "Order price. Required for pending orders. For market orders on "
            "Market/Exchange execution symbols, pass the current ask (BUY) or bid (SELL)."
        ),
    )
    stoplimit: Optional[float] = Field(
        default=None,
        description=(
            "StopLimit price - only for ORDER_TYPE_BUY_STOP_LIMIT / "
            "ORDER_TYPE_SELL_STOP_LIMIT. The limit order is placed at this price "
            "once the market reaches `price`."
        ),
    )
    sl: Optional[float] = Field(default=None, description="Stop Loss price")
    tp: Optional[float] = Field(default=None, description="Take Profit price")
    deviation: Optional[int] = Field(
        default=None,
        description="Maximum price deviation in points (for market orders)",
    )
    magic: Optional[int] = Field(
        default=None, description="Expert Advisor ID (magic number)"
    )
    comment: Optional[str] = Field(default=None, description="Order comment")
    type_time: Optional[int] = Field(
        default=None,
        description="Order expiration type: 0=GTC, 1=DAY, 2=SPECIFIED (use with expiration), 3=SPECIFIED_DAY",
    )
    type_filling: Optional[int] = Field(
        default=None,
        description="Order filling policy: 0=FOK (Fill or Kill), 1=IOC (Immediate or Cancel), 2=RETURN",
    )
    expiration: Optional[int] = Field(
        default=None,
        description=(
            "Pending order expiration as a Unix timestamp. "
            "Only used when type_time=2 (ORDER_TIME_SPECIFIED)."
        ),
    )
    order: Optional[int] = Field(
        default=None,
        description=(
            "Ticket of an existing pending order. "
            "Required for TRADE_ACTION_MODIFY and TRADE_ACTION_REMOVE."
        ),
    )
    position: Optional[int] = Field(
        default=None,
        description=(
            "Ticket of an open position. "
            "Required for TRADE_ACTION_SLTP and TRADE_ACTION_CLOSE_BY."
        ),
    )
    position_by: Optional[int] = Field(
        default=None,
        description=(
            "Ticket of the opposite position used for close-by. "
            "Required for TRADE_ACTION_CLOSE_BY."
        ),
    )


class OrderCheckParams(OrderSendParams):
    """
    Parameters for mt5_order_check().

    order_check() accepts the same MqlTradeRequest structure as order_send(),
    so this class inherits all fields from OrderSendParams unchanged.
    All fields that are optional in OrderSendParams remain optional here.

    Full field reference (from MqlTradeRequest):
      action       - TRADE_ACTION_DEAL=1, PENDING=5, SLTP=6, MODIFY=7, REMOVE=8, CLOSE_BY=10
      symbol       - Symbol name
      volume       - Trade volume in lots
      type         - Order type: BUY=0, SELL=1, BUY_LIMIT=2, SELL_LIMIT=3, BUY_STOP=4,
                     SELL_STOP=5, BUY_STOP_LIMIT=6, SELL_STOP_LIMIT=7, CLOSE_BY=8
      price        - Order price
      stoplimit    - StopLimit price (BUY_STOP_LIMIT / SELL_STOP_LIMIT only)
      sl           - Stop Loss
      tp           - Take Profit
      deviation    - Max price deviation in points
      magic        - Expert Advisor ID
      comment      - Order comment
      type_time    - Expiration: 0=GTC, 1=DAY, 2=SPECIFIED, 3=SPECIFIED_DAY
      type_filling - Filling: 0=FOK, 1=IOC, 2=RETURN
      expiration   - Unix timestamp expiry (ORDER_TIME_SPECIFIED only)
      order        - Ticket of existing order (MODIFY / REMOVE)
      position     - Open position ticket (SLTP / CLOSE_BY)
      position_by  - Opposite position ticket (CLOSE_BY)
    """


class OrderCalcMarginParams(ParamsBase):
    action: int = Field(
        description="Order direction: 0=BUY, 1=SELL (ORDER_TYPE_BUY/SELL)"
    )
    symbol: str = Field(description="Symbol name")
    volume: float = Field(description="Trade volume in lots")
    price: float = Field(description="Opening price")


class OrderCalcProfitParams(ParamsBase):
    action: int = Field(
        description="Order direction: 0=BUY, 1=SELL (ORDER_TYPE_BUY/SELL)"
    )
    symbol: str = Field(description="Symbol name")
    volume: float = Field(description="Trade volume in lots")
    price_open: float = Field(description="Opening price")
    price_close: float = Field(description="Closing price")


# Position & Order Management -------------------------------------------------


class PositionsGetParams(ParamsBase):
    symbol: Optional[str] = Field(
        default=None, description="Symbol name filter; if provided, ticket is ignored"
    )
    group: Optional[str] = Field(
        default=None,
        description=(
            "Symbol group filter. Supports wildcards ('*'), comma-separated conditions, "
            "and negation ('!'). Applied left-to-right (inclusions before exclusions). "
            "Examples: '*EUR*' (EUR pairs), '*,!*USD*' (all except USD pairs)."
        ),
    )
    ticket: Optional[int] = Field(
        default=None, description="Specific position ticket number"
    )


class OrdersGetParams(ParamsBase):
    symbol: Optional[str] = Field(
        default=None,
        description="Symbol name filter; if provided, ticket is ignored",
    )
    group: Optional[str] = Field(
        default=None,
        description=(
            "Symbol group filter. Supports wildcards ('*'), comma-separated conditions, "
            "and negation ('!'). Applied left-to-right (inclusions before exclusions). "
            "Examples: '*GBP*' (GBP pairs), '*, !*EUR*' (all except EUR pairs)."
        ),
    )
    ticket: Optional[int] = Field(
        default=None,
        description="Specific order ticket number; ignored if symbol is set",
    )


class HistoryRangeParams(ParamsBase):
    date_from: str = Field(description="Start date for history range")
    date_to: str = Field(description="End date for history range")


class HistoryOrdersTotalParams(HistoryRangeParams):
    """Parameters for mt5_history_orders_total."""


class HistoryOrdersGetParams(ParamsBase):
    date_from: Optional[str] = Field(
        default=None,
        description="Start date for history range (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS, UTC)",
    )
    date_to: Optional[str] = Field(
        default=None,
        description="End date for history range (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS, UTC)",
    )
    group: Optional[str] = Field(
        default=None,
        description=(
            "Symbol group filter. Supports wildcards ('*'), comma-separated conditions, "
            "and negation ('!'). Applied left-to-right (inclusions before exclusions). "
            "Can be combined with date_from/date_to."
        ),
    )
    ticket: Optional[int] = Field(
        default=None, description="Order ticket number to filter by"
    )
    position: Optional[int] = Field(
        default=None, description="Position ticket number to filter by"
    )


class HistoryDealsTotalParams(HistoryRangeParams):
    """Parameters for mt5_history_deals_total."""


class HistoryDealsGetParams(ParamsBase):
    date_from: Optional[str] = Field(
        default=None,
        description="Start date for history range (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS, UTC)",
    )
    date_to: Optional[str] = Field(
        default=None,
        description="End date for history range (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS, UTC)",
    )
    group: Optional[str] = Field(
        default=None,
        description=(
            "Symbol group filter. Supports wildcards ('*'), comma-separated conditions, "
            "and negation ('!'). Applied left-to-right (inclusions before exclusions). "
            "Can be combined with date_from/date_to."
        ),
    )
    ticket: Optional[int] = Field(
        default=None, description="Deal ticket number to filter by"
    )
    position: Optional[int] = Field(
        default=None, description="Position ticket number to filter by"
    )
