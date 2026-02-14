# MetaTrader 5 MCP Server

A Model Context Protocol (MCP) server that provides comprehensive access to MetaTrader 5 trading platform functionality through Python.

## Features

This MCP server exposes 32 tools for interacting with MT5, organized into the following categories:

### 🔌 Connection & Initialization
- Initialize/shutdown MT5 connection
- Get terminal version and information
- Login to trading accounts
- Get last error information

### 💰 Account Information
- Retrieve account balance, equity, margin, profit
- Get account settings and leverage

### 📊 Market Data
- Access symbol information and current prices
- Retrieve historical bar data (OHLCV) by date or position
- Get tick data with various filters and date ranges
- Manage Market Watch symbols

### 📈 Trading Operations
- Send market and pending orders
- Check order validity before execution
- Calculate required margin
- Calculate potential profit/loss

### 📋 Position & Order Management
- View open positions
- Monitor pending orders
- Access trading history (orders and deals)
- Filter by symbol, date range, or ticket

## Prerequisites

- **MetaTrader 5** terminal installed and running
- **Python 3.10+**
- **MetaTrader5** Python package
- **MCP SDK** for Python

## Installation

1. Clone or download this repository:

```bash
cd c:\Users\desktop\Projects\metatrader5-mcp
```

2. Install dependencies with **Poetry**:

```bash
poetry install
```

This installs the `metatrader5-mcp` console command in the Poetry virtualenv:

```bash
poetry run metatrader5-mcp
```

This will create a virtual environment and install `mcp`, `MetaTrader5`, `pydantic`, and dev tools.

3. (Optional) If you prefer `pip`, you can still install directly:

```bash
pip install mcp MetaTrader5 pydantic
```

### Install the Console Command

If you want the `metatrader5-mcp` command on your PATH (recommended for MCP clients),
install the package itself:

```bash
pip install -e .
```

Or use `pipx` for a global, isolated install:

```bash
pipx install .
```

## Configuration

### For Claude Desktop

Add this configuration to your Claude Desktop config file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

#### With Auto-Initialization (Recommended)

```json
{
  "mcpServers": {
    "metatrader": {
      "command": "metatrader5-mcp",
      "args": [
        "--login",    "YOUR_MT5_LOGIN",
        "--password", "YOUR_MT5_PASSWORD",
        "--server",   "YOUR_MT5_SERVER",
        "--path",     "C:\\Program Files\\MetaTrader 5\\terminal64.exe"
      ]
    }
  }
}
```

#### Manual Initialization

```json
{
  "mcpServers": {
    "metatrader": {
      "command": "metatrader5-mcp"
    }
  }
}
```

Then use the `mt5_initialize` tool to connect manually.

### Command Line Arguments

The server supports the following optional arguments:

- `--login LOGIN` - Trading account number
- `--password PASSWORD` - Trading account password
- `--server SERVER` - Trading server name (e.g., "MetaQuotes-Demo")
- `--path PATH` - Path to MT5 terminal executable

### Running Locally

```bash
# With auto-initialization
metatrader5-mcp --login 12345 --password secret --server MetaQuotes-Demo

# Without initialization (manual connection via tools)
metatrader5-mcp
```

## Usage Examples

### Initialize Connection

```
Use the mt5_initialize tool to connect to MT5 terminal.
```

### Get Account Information

```
Use mt5_account_info to retrieve:
- Balance
- Equity
- Margin (used and free)
- Profit
- Leverage
```

### Get Current Price

```
Use mt5_symbol_info_tick with symbol "EURUSD" to get:
- Current bid/ask prices
- Last trade price
- Volume
```

### Retrieve Historical Data

```
Use mt5_copy_rates_from with:
- symbol: "EURUSD"
- timeframe: 60 (H1)
- date_from: "2024-01-01"
- count: 100

Returns OHLCV data for the last 100 H1 bars.
```

### Check Order Before Sending

```
Use mt5_order_check to validate an order:
- action: 1 (TRADE_ACTION_DEAL)
- symbol: "EURUSD"
- volume: 0.1
- type: 0 (BUY)
- price: <current ask price>
```

### View Open Positions

```
Use mt5_positions_get to see all open positions, or filter by:
- symbol: "EURUSD"
- group: "*EUR*"
- ticket: specific position number
```

## Constants Reference

### Timeframes (in minutes)
- `1` - M1 (1 minute)
- `5` - M5 (5 minutes)
- `15` - M15 (15 minutes)
- `30` - M30 (30 minutes)
- `60` - H1 (1 hour)
- `240` - H4 (4 hours)
- `1440` - D1 (1 day)
- `10080` - W1 (1 week)
- `43200` - MN1 (1 month)

### Trade Actions
- `1` - TRADE_ACTION_DEAL (instant execution)
- `5` - TRADE_ACTION_PENDING (pending order)

### Order Types
- `0` - ORDER_TYPE_BUY
- `1` - ORDER_TYPE_SELL
- `2` - ORDER_TYPE_BUY_LIMIT
- `3` - ORDER_TYPE_SELL_LIMIT
- `4` - ORDER_TYPE_BUY_STOP
- `5` - ORDER_TYPE_SELL_STOP

### Tick Flags
- `0` - COPY_TICKS_INFO
- `2` - COPY_TICKS_TRADE
- `4` - COPY_TICKS_BID
- `8` - COPY_TICKS_ASK
- `6` - COPY_TICKS_ALL

### Order Filling Types
- `0` - ORDER_FILLING_FOK (Fill or Kill)
- `1` - ORDER_FILLING_IOC (Immediate or Cancel)
- `2` - ORDER_FILLING_RETURN (Return)

### Order Time Types
- `0` - ORDER_TIME_GTC (Good Till Cancelled)
- `1` - ORDER_TIME_DAY (Good Till Day)
- `2` - ORDER_TIME_SPECIFIED (Good Till Specified)
- `3` - ORDER_TIME_SPECIFIED_DAY (Good Till Specified Day)

## Error Handling

The server includes comprehensive error handling:
- MT5 connection errors are reported with error codes
- Invalid parameters are caught and explained
- All MT5 API errors include the last error from MT5

## Security Considerations

⚠️ **Important Security Notes:**

1. **Real Money Trading**: This server can execute real trades. Always test with a demo account first.
2. **Credentials**: Never hardcode passwords. Use environment variables or secure credential storage.
3. **Access Control**: Limit access to this MCP server to trusted clients only.
4. **Network**: MT5 terminal must be running on the same machine as the server.

## Troubleshooting

### "initialize() failed"
- Ensure MT5 terminal is installed and running
- Check that the terminal path is correct (if specified)
- Verify you have the correct login credentials

### "No data returned"
- Symbol might not be available in Market Watch
- Use `mt5_symbol_select` to add symbols
- Check date ranges for historical data

### Connection timeout
- Increase timeout parameter in `mt5_initialize`
- Check MT5 terminal is responsive
- Verify no firewall blocking

## Development

### Running the Server Directly

```bash
python -m metatrader5_mcp
```

The server uses stdio transport and communicates via JSON-RPC over stdin/stdout.

### Testing Tools

You can test individual MT5 functions in Python:

```python
import MetaTrader5 as mt5

# Initialize
if not mt5.initialize():
    print("Failed:", mt5.last_error())
    quit()

# Get account info
account = mt5.account_info()
print(account._asdict())

# Cleanup
mt5.shutdown()
```

## Resources

- [MetaTrader 5 Python Documentation](https://www.mql5.com/en/docs/python_metatrader5)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [MetaTrader 5 Terminal](https://www.metatrader5.com/)

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
