# MetaTrader5-MCP Quick Reference

## Installation

```bash
# Quick install (Windows)
install.bat

# Quick install (Linux/Mac)
./install.sh

# Manual install
pip install -r requirements.txt
pip install -e .
```

## Configuration

```bash
# 1. Copy template
cp .env.example .env

# 2. Edit with your credentials
nano .env  # or notepad .env on Windows

# 3. Run validation
python validate.py
```

## Running the Server

```bash
# Using environment variables
metatrader5-mcp

# Using command line
metatrader5-mcp --login 12345 --password secret --server Demo

# With custom log level
LOG_LEVEL=DEBUG metatrader5-mcp
```

## Common Tools

### Connection & Status

| Tool | Purpose |
|------|---------|
| `mt5_health_check` | Check connection health |
| `mt5_connection_status` | Quick status check |
| `mt5_version` | Get MT5 version |
| `mt5_terminal_info` | Get terminal info |
| `mt5_account_info` | Get account details |

### Market Data

| Tool | Purpose |
|------|---------|
| `mt5_symbol_info` | Get symbol information |
| `mt5_symbol_info_tick` | Get current tick/price |
| `mt5_copy_rates_from` | Get historical bars by date |
| `mt5_copy_rates_range` | Get bars in date range |
| `mt5_copy_ticks_from` | Get tick data |

### Trading

| Tool | Purpose |
|------|---------|
| `mt5_order_check` | Validate order before sending |
| `mt5_order_send` | Execute trade |
| `mt5_order_calc_margin` | Calculate required margin |
| `mt5_order_calc_profit` | Calculate potential profit |

### Positions & History

| Tool | Purpose |
|------|---------|
| `mt5_positions_get` | Get open positions |
| `mt5_orders_get` | Get pending orders |
| `mt5_history_orders_get` | Get order history |
| `mt5_history_deals_get` | Get deal history |

## Common Timeframes

| Code | Timeframe |
|------|-----------|
| `1` | M1 (1 minute) |
| `5` | M5 (5 minutes) |
| `15` | M15 (15 minutes) |
| `30` | M30 (30 minutes) |
| `60` | H1 (1 hour) |
| `240` | H4 (4 hours) |
| `1440` | D1 (1 day) |
| `10080` | W1 (1 week) |
| `43200` | MN1 (1 month) |

## Order Types

| Code | Type |
|------|------|
| `0` | ORDER_TYPE_BUY |
| `1` | ORDER_TYPE_SELL |
| `2` | ORDER_TYPE_BUY_LIMIT |
| `3` | ORDER_TYPE_SELL_LIMIT |
| `4` | ORDER_TYPE_BUY_STOP |
| `5` | ORDER_TYPE_SELL_STOP |

## Trade Actions

| Code | Action |
|------|--------|
| `1` | TRADE_ACTION_DEAL (instant) |
| `5` | TRADE_ACTION_PENDING |

## Example Usage

### Get Account Balance

```python
# Tool: mt5_account_info
# Returns account details including balance, equity, margin
```

### Get Current Price

```python
# Tool: mt5_symbol_info_tick
# Parameters:
{
  "symbol": "EURUSD"
}
# Returns: bid, ask, last, volume
```

### Get Historical Bars

```python
# Tool: mt5_copy_rates_from
# Parameters:
{
  "symbol": "EURUSD",
  "timeframe": 60,
  "date_from": "2024-01-01",
  "count": 100
}
# Returns: OHLCV data for 100 H1 bars
```

### Check Order Before Sending

```python
# Tool: mt5_order_check
# Parameters:
{
  "action": 1,
  "symbol": "EURUSD",
  "volume": 0.1,
  "type": 0,
  "price": 1.1000
}
# Returns: validation result with margin info
```

### Execute Buy Order

```python
# Tool: mt5_order_send
# Parameters:
{
  "action": 1,
  "symbol": "EURUSD",
  "volume": 0.1,
  "type": 0,
  "price": 1.1000,
  "sl": 1.0950,
  "tp": 1.1050,
  "deviation": 10,
  "comment": "Test order"
}
# Returns: order result with ticket number
```

### Get Open Positions

```python
# Tool: mt5_positions_get
# Parameters (all optional):
{
  "symbol": "EURUSD"  # Filter by symbol
}
# Returns: List of open positions
```

## Troubleshooting Quick Tips

### Connection Issues

```bash
# Check if MT5 is running
# Verify credentials in .env
# Run health check
python -c "from metatrader5_mcp.tools_status import mt5_health_check; print(mt5_health_check())"
```

### "Initialize failed"

1. Start MT5 terminal
2. Check terminal path in .env
3. Run as administrator
4. Verify credentials

### "Trade disabled"

1. Check account type (demo vs real)
2. Verify trading hours
3. Enable AutoTrading in MT5
4. Contact broker if needed

### Logs Not Showing

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
metatrader5-mcp 2> debug.log
```

## File Locations

| File | Purpose |
|------|---------|
| `.env` | Configuration (DO NOT COMMIT) |
| `.env.example` | Configuration template |
| `requirements.txt` | Dependencies |
| `README.md` | Full documentation |
| `TROUBLESHOOTING.md` | Detailed troubleshooting |
| `SECURITY.md` | Security best practices |
| `CONTRIBUTING.md` | Contribution guide |
| `validate.py` | Prerequisite checker |

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MT5_LOGIN` | Account number | `12345678` |
| `MT5_PASSWORD` | Account password | `secret123` |
| `MT5_SERVER` | Server name | `MetaQuotes-Demo` |
| `MT5_PATH` | Terminal path | `C:\Program Files\...` |
| `LOG_LEVEL` | Logging level | `INFO`, `DEBUG` |

## Getting Help

1. **Check documentation**: README.md, TROUBLESHOOTING.md
2. **Run validation**: `python validate.py`
3. **Check logs**: `LOG_LEVEL=DEBUG metatrader5-mcp`
4. **Search issues**: https://github.com/amirkhonov/metatrader5-mcp/issues
5. **Create issue**: Use issue template with full details

## Important Reminders

- ✅ Always test with demo account first
- ✅ Never commit .env file
- ✅ Keep MT5 terminal updated
- ✅ Monitor trades and positions
- ✅ Use stop losses
- ⚠️ Trading involves financial risk
- ⚠️ This is not financial advice

## Resources

- **Full Documentation**: [README.md](README.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Security**: [SECURITY.md](SECURITY.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **MT5 Docs**: https://www.mql5.com/en/docs/python_metatrader5
- **MCP Protocol**: https://modelcontextprotocol.io/

---

*Quick Reference v0.1.0*
