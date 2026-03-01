"""
Prompts for the MetaTrader 5 MCP server.
"""

from fastmcp.prompts import Message

from .utils import mcp


@mcp.prompt
def expert_advisor_code(strategy_description: str) -> list[Message]:
    """Generates a request to write an Expert Advisor based on a strategy."""
    return [
        Message(
            f"Please write a MetaTrader 5 Expert Advisor (EA) in MQL5 based on the following strategy:\n\n{strategy_description}\n\n"
            "Include comments explaining the logic and ensure it compiles without errors."
        ),
        Message(
            "I will generate the MQL5 code for your Expert Advisor.", role="assistant"
        ),
    ]


@mcp.prompt
def market_analysis(symbol: str, timeframe: str) -> list[Message]:
    """Generates a request to analyze market data for a symbol."""
    return [
        Message(
            f"Please analyze the market for {symbol} on the {timeframe} timeframe. "
            "Use the available tools to fetch price data and technical indicators if needed. "
            "Provide a summary of the current trend and potential support/resistance levels."
        ),
        Message(
            f"I will analyze the {symbol} market on the {timeframe} timeframe using the available tools.",
            role="assistant",
        ),
    ]


@mcp.prompt
def diagnose_error(error_code: int) -> list[Message]:
    """Generates a request to diagnose an MT5 error code."""
    return [
        Message(
            f"I encountered MetaTrader 5 error code {error_code}. "
            "What does this error mean and how can I fix it?"
        ),
        Message(
            f"I will explain the meaning of error code {error_code} and suggest solutions.",
            role="assistant",
        ),
    ]


@mcp.prompt
def calculate_position_size(
    symbol: str, risk_amount: float, stop_loss_points: int
) -> list[Message]:
    """Generates a request to calculate position size based on risk."""
    return [
        Message(
            f"Please calculate the appropriate position size for {symbol} to risk no more than ${risk_amount} "
            f"with a stop loss of {stop_loss_points} points. "
            "Assume the account currency is USD. Explain the calculation step-by-step."
        ),
        Message(
            f"I will calculate the position size for {symbol} ensuring the risk does not exceed ${risk_amount}.",
            role="assistant",
        ),
    ]
