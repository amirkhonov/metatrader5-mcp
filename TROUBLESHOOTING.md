# Troubleshooting Guide

This guide helps resolve common issues when setting up and using MetaTrader5-MCP.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Connection Issues](#connection-issues)
- [Authentication Issues](#authentication-issues)
- [Trading Issues](#trading-issues)
- [Performance Issues](#performance-issues)
- [Configuration Issues](#configuration-issues)

---

## Installation Issues

### Python Version Error

**Problem:** Error message about Python version being too old.

**Solution:**
```bash
# Check your Python version
python --version

# Ensure it's 3.10 or higher
# If not, download from: https://www.python.org/downloads/
```

### pip Installation Fails

**Problem:** `pip install` fails with permission errors.

**Solution:**
```bash
# Use a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Or install with --user flag
pip install --user -r requirements.txt
```

### MetaTrader5 Package Not Found

**Problem:** `ModuleNotFoundError: No module named 'MetaTrader5'`

**Solution:**
```bash
# Install MetaTrader5 package
pip install MetaTrader5

# On Windows, ensure you have the MT5 terminal installed
```

### Pre-commit Hooks Failing

**Problem:** Pre-commit hooks fail after installation.

**Solution:**
```bash
# Update hooks to latest version
pre-commit autoupdate

# Run hooks manually
pre-commit run --all-files

# If still failing, temporarily skip
git commit --no-verify -m "your message"
```

---

## Connection Issues

### "initialize() failed" Error

**Problem:** MT5 initialization fails with error code.

**Possible Causes & Solutions:**

1. **MT5 Terminal Not Running**
   ```
   Solution: Start MetaTrader 5 terminal manually before running the MCP server
   ```

2. **Incorrect Path**
   ```bash
   # Specify correct path explicitly
   metatrader5-mcp --path "C:\Program Files\MetaTrader 5\terminal64.exe"
   ```

3. **Terminal Busy**
   ```
   Solution: Close any other programs using MT5, then restart the server
   ```

4. **Insufficient Permissions**
   ```
   Solution: Run terminal as administrator (right-click → Run as administrator)
   ```

### Connection Timeout

**Problem:** Server times out when trying to connect to MT5.

**Solution:**
```bash
# Increase timeout (not currently supported, but in roadmap)
# For now, ensure MT5 terminal is responsive
# Check Task Manager for MT5 processes
# Restart MT5 terminal if frozen
```

### "No connection with the trade server"

**Problem:** MT5 terminal shows no server connection.

**Solution:**
1. Check your internet connection
2. Verify server name is correct
3. Check MT5 terminal → Tools → Options → Server
4. Try reconnecting manually in MT5 terminal
5. Contact your broker if server is down

---

## Authentication Issues

### "Authorization failed" Error

**Problem:** Login credentials are rejected.

**Solution:**
```bash
# Double-check credentials in .env file
MT5_LOGIN=12345678        # Your account number
MT5_PASSWORD=YourPassword # Exact password (case-sensitive)
MT5_SERVER=YourBroker-Server  # Exact server name

# Find correct server name:
# 1. Open MT5 terminal
# 2. Go to Tools → Options → Server
# 3. Copy exact server name

# Test with CLI arguments first
metatrader5-mcp --login 12345 --password "YourPass" --server "ExactServerName"
```

### Password with Special Characters

**Problem:** Password contains special characters causing issues.

**Solution:**
```bash
# In .env file, don't use quotes
MT5_PASSWORD=My!Pass@123

# In command line, use quotes
metatrader5-mcp --password "My!Pass@123"
```

### Wrong Trading Account

**Problem:** Server connects but shows different account.

**Solution:**
```bash
# Ensure login number is correct (not username)
# Use account number, not login name

# Check in MT5: Tools → Options → Account
# Use the number shown, not the name
```

---

## Trading Issues

### "Trade is disabled" Error

**Problem:** Cannot execute trades.

**Possible Causes:**
1. **Demo Account Expired**
   - Solution: Register new demo account or use real account

2. **Trading Hours**
   - Solution: Check market hours for your symbol
   - Some symbols only trade during specific hours

3. **Account Settings**
   - Solution: Check Tools → Options → Trade
   - Ensure AutoTrading is enabled

4. **Insufficient Permissions**
   - Solution: Some accounts restrict API trading
   - Contact broker to enable API/automated trading

### "Invalid Price" Error

**Problem:** Order rejected due to price issues.

**Solution:**
```python
# Use current market prices
# For BUY: use ask price
# For SELL: use bid price

# Get current prices first
symbol_info = mt5.symbol_info_tick("EURUSD")
ask = symbol_info.ask
bid = symbol_info.bid

# Use appropriate price for order
```

### "Not enough money" Error

**Problem:** Insufficient margin for trade.

**Solution:**
```python
# Calculate required margin before trading
margin = mt5.order_calc_margin(
    action=mt5.ORDER_TYPE_BUY,
    symbol="EURUSD",
    volume=0.1,
    price=ask
)

# Check available margin
account_info = mt5.account_info()
free_margin = account_info.margin_free

if margin > free_margin:
    print("Insufficient margin")
```

### "Invalid Volume" Error

**Problem:** Trade volume is not accepted.

**Solution:**
```python
# Check symbol's volume limits
symbol_info = mt5.symbol_info("EURUSD")
min_volume = symbol_info.volume_min  # e.g., 0.01
max_volume = symbol_info.volume_max  # e.g., 100.0
volume_step = symbol_info.volume_step  # e.g., 0.01

# Use valid volume
# Must be: min_volume <= volume <= max_volume
# Must be: multiple of volume_step
```

---

## Performance Issues

### Server Response Slow

**Problem:** MCP server responds slowly.

**Solutions:**
1. **Check MT5 Terminal Performance**
   ```
   - Close unnecessary charts in MT5
   - Remove unused indicators
   - Reduce number of symbols in Market Watch
   ```

2. **Optimize Data Requests**
   ```python
   # Request smaller data sets
   # Use count parameter to limit results
   # Don't request unnecessary historical data
   ```

3. **Check System Resources**
   ```
   - Monitor CPU/RAM usage
   - Close other applications
   - Restart MT5 terminal periodically
   ```

### High Memory Usage

**Problem:** Server uses too much memory.

**Solution:**
```bash
# Restart server periodically
# Limit historical data requests
# Clear MT5 terminal cache: Tools → Options → Charts
```

---

## Configuration Issues

### .env File Not Loaded

**Problem:** Environment variables not recognized.

**Solution:**
```bash
# Ensure .env file is in the current directory
ls -la .env  # On Unix
dir .env     # On Windows

# Check file format (no BOM, Unix line endings)
# Ensure no spaces around =
MT5_LOGIN=12345  # ✓ Correct
MT5_LOGIN = 12345  # ✗ Wrong
```

### Claude Desktop Config Not Working

**Problem:** Claude Desktop doesn't connect to server.

**Solution:**

1. **Check Config File Location**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Check file exists and is valid JSON

2. **Validate JSON Syntax**
   ```json
   {
     "mcpServers": {
       "metatrader": {
         "command": "metatrader5-mcp",
         "args": ["--login", "12345", "--password", "secret", "--server", "Demo"]
       }
     }
   }
   ```

3. **Check Command Path**
   ```bash
   # Ensure metatrader5-mcp is in PATH
   which metatrader5-mcp  # Unix
   where metatrader5-mcp  # Windows

   # If not found, use full path
   "command": "C:\\Users\\YourUser\\venv\\Scripts\\metatrader5-mcp.exe"
   ```

4. **Restart Claude Desktop**
   - Close completely (check Task Manager)
   - Start again

### Logs Not Showing

**Problem:** Cannot see server logs for debugging.

**Solution:**
```bash
# Set log level to DEBUG
export LOG_LEVEL=DEBUG  # Unix
set LOG_LEVEL=DEBUG     # Windows

# Or in .env file
LOG_LEVEL=DEBUG

# Run server and check stderr
metatrader5-mcp 2> debug.log
```

---

## Getting Help

If you're still experiencing issues:

1. **Check Existing Issues**
   - Visit: https://github.com/amirkhonov/metatrader5-mcp/issues
   - Search for similar problems

2. **Create New Issue**
   - Use issue template
   - Include:
     - Python version
     - OS version
     - MT5 version
     - Full error messages
     - Steps to reproduce
     - Logs (with sensitive data removed)

3. **Enable Debug Logging**
   ```bash
   LOG_LEVEL=DEBUG metatrader5-mcp 2> debug.log
   # Share debug.log (remove passwords/account numbers)
   ```

4. **Run Validation Script**
   ```bash
   python validate.py
   # Share output
   ```

---

## Common Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 1 | Generic error | Check MT5 terminal logs |
| 2 | Common error | Retry operation |
| 3 | Invalid parameters | Check parameter values |
| 4 | Server not ready | Wait and retry |
| 5 | Old version | Update MT5 terminal |
| 64 | Account disabled | Contact broker |
| 65 | Invalid account | Check credentials |
| 128 | Trade timeout | Retry trade |
| 129 | Invalid price | Use current market price |
| 130 | Invalid stops | Check SL/TP levels |
| 131 | Invalid volume | Check volume limits |
| 134 | Not enough money | Reduce volume or deposit |

For complete error code reference:
https://www.mql5.com/en/docs/constants/errorswarnings/enum_trade_return_codes

---

## Prevention Tips

1. **Always Test with Demo Account First**
2. **Keep MT5 Terminal Updated**
3. **Monitor System Resources**
4. **Use Version Control for Config Changes**
5. **Regular Backups of Trading Data**
6. **Keep Credentials Secure (never commit .env)**
7. **Test After MT5 Updates**

---

*Last Updated: 2024-02-14*
