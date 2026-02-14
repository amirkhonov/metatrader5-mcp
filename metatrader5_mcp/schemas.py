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


# Connection & Initialization -------------------------------------------------


class InitializeParams(ParamsBase):
    path: Optional[str] = Field(
        default=None, description="Path to MT5 terminal executable"
    )
    login: Optional[int] = Field(default=None, description="Trading account number")
    password: Optional[str] = Field(
        default=None, description="Trading account password"
    )
    server: Optional[str] = Field(default=None, description="Trading server name")
    timeout: Optional[int] = Field(
        default=None, description="Connection timeout in milliseconds"
    )
    portable: Optional[bool] = Field(
        default=None, description="Portable mode flag for terminal"
    )


class LoginParams(ParamsBase):
    login: int = Field(description="Trading account number")
    password: str = Field(description="Trading account password")
    server: str = Field(description="Trading server name")


# Market Data - Symbols -------------------------------------------------------


class SymbolsGetParams(ParamsBase):
    group: Optional[str] = Field(
        default=None,
        description="Symbol group filter pattern, e.g. '*EUR*' or 'FOREX\\\\*'",
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
        description="Trade action type, e.g. 1=TRADE_ACTION_DEAL, 5=TRADE_ACTION_PENDING"
    )
    symbol: str = Field(description="Symbol name")
    volume: float = Field(description="Trade volume in lots")
    type: int = Field(
        description=(
            "Order type: 0=BUY, 1=SELL, 2=BUY_LIMIT, 3=SELL_LIMIT, "
            "4=BUY_STOP, 5=SELL_STOP"
        )
    )
    price: Optional[float] = Field(
        default=None, description="Order price (required for pending orders)"
    )
    sl: Optional[float] = Field(default=None, description="Stop Loss price")
    tp: Optional[float] = Field(default=None, description="Take Profit price")
    deviation: Optional[int] = Field(
        default=None, description="Maximum price deviation in points"
    )
    magic: Optional[int] = Field(
        default=None, description="Expert Advisor ID (magic number)"
    )
    comment: Optional[str] = Field(default=None, description="Order comment")
    type_time: Optional[int] = Field(
        default=None,
        description=("Order lifetime type: 0=GTC, 1=DAY, 2=SPECIFIED, 3=SPECIFIED_DAY"),
    )
    type_filling: Optional[int] = Field(
        default=None,
        description="Order filling type: 0=FOK, 1=IOC, 2=RETURN",
    )


class OrderCheckParams(ParamsBase):
    action: int = Field(
        description="Trade action type, e.g. 1=TRADE_ACTION_DEAL, 5=TRADE_ACTION_PENDING"
    )
    symbol: str = Field(description="Symbol name")
    volume: float = Field(description="Trade volume in lots")
    type: int = Field(
        description=(
            "Order type: 0=BUY, 1=SELL, 2=BUY_LIMIT, 3=SELL_LIMIT, "
            "4=BUY_STOP, 5=SELL_STOP"
        )
    )
    price: Optional[float] = Field(
        default=None, description="Order price (required for pending orders)"
    )


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
        default=None, description="Symbol name filter for positions"
    )
    group: Optional[str] = Field(
        default=None, description="Symbol group filter pattern"
    )
    ticket: Optional[int] = Field(
        default=None, description="Specific position ticket number"
    )


class OrdersGetParams(ParamsBase):
    symbol: Optional[str] = Field(
        default=None, description="Symbol name filter for orders"
    )
    group: Optional[str] = Field(
        default=None, description="Symbol group filter pattern"
    )
    ticket: Optional[int] = Field(
        default=None, description="Specific order ticket number"
    )


class HistoryRangeParams(ParamsBase):
    date_from: str = Field(description="Start date for history range")
    date_to: str = Field(description="End date for history range")


class HistoryOrdersTotalParams(HistoryRangeParams):
    """Parameters for mt5_history_orders_total."""


class HistoryOrdersGetParams(ParamsBase):
    date_from: Optional[str] = Field(
        default=None, description="Start date for history range"
    )
    date_to: Optional[str] = Field(
        default=None, description="End date for history range"
    )
    group: Optional[str] = Field(
        default=None, description="Symbol group filter pattern"
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
        default=None, description="Start date for history range"
    )
    date_to: Optional[str] = Field(
        default=None, description="End date for history range"
    )
    group: Optional[str] = Field(
        default=None, description="Symbol group filter pattern"
    )
    ticket: Optional[int] = Field(
        default=None, description="Deal ticket number to filter by"
    )
    position: Optional[int] = Field(
        default=None, description="Position ticket number to filter by"
    )
