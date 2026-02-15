# MetaTrader 5 MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A Model Context Protocol (MCP) server that provides comprehensive access to MetaTrader 5 trading platform functionality through Python.

> **📖 New to this project?** Check out the [Quick Start Guide](QUICKSTART.md) for a condensed reference!

## 🚀 Quick Start

### Prerequisites

- **MetaTrader 5** terminal installed and running on Windows
- **Python 3.10+**

### Installation (Choose One Method)

#### Method 1: Automated Installation (Recommended)

**Windows:**
```bash
# Clone the repository
git clone https://github.com/amirkhonov/metatrader5-mcp.git
cd metatrader5-mcp

# Run installation script
install.bat
```

**Linux/Mac:**
```bash
# Clone the repository
git clone https://github.com/amirkhonov/metatrader5-mcp.git
cd metatrader5-mcp

# Run installation script
chmod +x install.sh
./install.sh
```

#### Method 2: Using pip

```bash
# Install from source
git clone https://github.com/amirkhonov/metatrader5-mcp.git
cd metatrader5-mcp
pip install -r requirements.txt
pip install -e .
```

#### Method 3: Using Poetry

```bash
git clone https://github.com/amirkhonov/metatrader5-mcp.git
cd metatrader5-mcp
poetry install
```

### Configuration

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your MT5 credentials:**
   ```env
   MT5_LOGIN=12345678
   MT5_PASSWORD=your_password
   MT5_SERVER=MetaQuotes-Demo
   MT5_PATH=C:\Program Files\MetaTrader 5\terminal64.exe
   ```

3. **Run the server:**
   ```bash
   # Using environment variables from .env
   metatrader5-mcp

   # Or with command line arguments
   metatrader5-mcp --login 12345 --password secret --server MetaQuotes-Demo
   ```

### Quick Test

```bash
# Check if the server starts correctly
metatrader5-mcp --help
```

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

- **MetaTrader 5** terminal installed and running on Windows
- **Python 3.10+**

## Installation Methods

Choose the method that works best for you:

### Option 1: Quick Install Script (Easiest)

**Windows:**
```cmd
install.bat
```

**Linux/Mac:**
```bash
./install.sh
```

The script will:
- Check Python version
- Create a virtual environment
- Install all dependencies
- Create a `.env` configuration file
- Guide you through setup

### Option 2: Manual Installation with pip

```bash
# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .

# Copy environment template
cp .env.example .env
# Edit .env with your credentials
```

### Option 3: Using Poetry

```bash
poetry install
cp .env.example .env
# Edit .env with your credentials
```

### Option 4: Using pipx (Global Install)

```bash
pipx install .
```

### Option 5: Docker (Experimental)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

**Note:** Docker support is experimental as MT5 requires Windows. Best for development/testing.

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

## Troubleshooting

Having issues? Check our comprehensive [Troubleshooting Guide](TROUBLESHOOTING.md) for:
- Installation problems
- Connection issues
- Authentication errors
- Trading problems
- Configuration issues
- Common error codes and solutions

Or run the validation script:
```bash
python validate.py
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

📖 **For comprehensive security guidance, see [SECURITY.md](SECURITY.md)**

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

### Documentation

- 📖 [Quick Start Guide](QUICKSTART.md) - Quick reference for common tasks
- 🔧 [Troubleshooting Guide](TROUBLESHOOTING.md) - Solve common issues
- 🔒 [Security Best Practices](SECURITY.md) - Keep your trading secure
- 🤝 [Contributing Guide](CONTRIBUTING.md) - How to contribute

### External Links

- [MetaTrader 5 Python Documentation](https://www.mql5.com/en/docs/python_metatrader5)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [MetaTrader 5 Terminal](https://www.metatrader5.com/)
- [GitHub Repository](https://github.com/amirkhonov/metatrader5-mcp)
- [Issue Tracker](https://github.com/amirkhonov/metatrader5-mcp/issues)

## License

MIT License - feel free to use and modify as needed. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

**⚠️ Disclaimer**: This software is for educational and informational purposes. Trading involves financial risk. Always test with demo accounts first. The authors are not responsible for any financial losses incurred through use of this software.
