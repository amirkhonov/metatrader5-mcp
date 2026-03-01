# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

An MCP (Model Context Protocol) server that wraps the MetaTrader 5 Python API, exposing MT5 trading operations as MCP tools for AI assistants. **MT5 only runs on Windows** — the `MetaTrader5` Python package will not work on other platforms.

## Commands

```bash
# Install (development)
pip install -r requirements-dev.txt
pip install -e .

# Run server (credentials via CLI args)
metatrader5-mcp --login 12345 --password secret --server MetaQuotes-Demo --path "C:\Program Files\MetaTrader 5\terminal64.exe"

# Run server (credentials via .env file — KEY=VALUE format required)
# MT5_LOGIN, MT5_PASSWORD, MT5_SERVER, MT5_PATH, LOG_LEVEL
metatrader5-mcp

# Format
python -m black .

# Lint/format via pre-commit (uses black, ruff, isort)
pre-commit run --all-files

# Tests
python -m pytest tests/ -v
python -m pytest tests/test_utils.py -v        # single file
python -m pytest tests/ -k "test_mt5_to_python" # single test
```

## Architecture

### Core Pattern: Side-Effect Tool Registration

`utils.py` creates a single shared `mcp = FastMCP("metatrader5-mcp")` instance. All `tools_*.py` modules register their tools by importing this instance and using `@mcp.tool` decorators. The only purpose of the imports in `main.py` is to trigger this registration:

```python
from . import tools_connection  # noqa: F401  ← side-effect import
```

Adding a new tool means: (1) add a Pydantic schema to `schemas.py`, (2) implement the tool function with `@mcp.tool` in the appropriate `tools_*.py`, (3) import `mcp` from `.utils`. The tool is automatically available — no registration list to update.

### Tool Parameter Schemas (`schemas.py`)

All tools that take parameters use Pydantic models inheriting from `ParamsBase` (which enforces `extra="forbid"`). Optional MT5 parameters default to `None` and are stripped via `filter_none()` before being passed to MT5. This lets MT5 use its own defaults rather than receiving `None` values.

### MT5 Return Type Handling (`utils.py: mt5_to_python`)

MT5 returns three distinct types that need conversion:
- **Named tuples** (`account_info()`, `symbol_info()`, etc.) → `dict` via `._asdict()`
- **Numpy structured arrays** (`copy_rates_*()`, `copy_ticks_*()`) → `list[dict]` via dtype names
- **Plain tuples/lists** → `list`

Always pipe MT5 output through `mt5_to_python()`. Raw numpy arrays are not JSON-serializable and will break MCP transport.

### Error Handling Convention

Tools follow a two-stage error check:
1. If MT5 returns `None` → call `mt5.last_error()` and raise `RuntimeError` with diagnostics
2. If the result has a non-success `retcode` → raise `RuntimeError` with a human-readable description from `_RETCODE_MESSAGES` (trading tools only)

`_RETCODE_MESSAGES` in `tools_trading.py` maps MT5 retcodes to actionable descriptions.

### Startup Flow

`main.py:main()` loads `.env`, parses CLI args, configures logging, then optionally calls `mt5.initialize()` if any credentials are provided. Without credentials, the server starts but MT5 tools will fail until `mt5_initialize` is called (via a connection tool). The server runs `mcp.run()` over stdio (MCP transport).

## Key Constraints

- **`.env` format**: Must be `KEY=VALUE` pairs, one per line. The `load_env_file()` function in `main.py` is a manual parser (not python-dotenv) that only sets variables not already in the environment.
- **Timeframes**: Historical data tools accept timeframe as integer minutes: `1=M1, 5=M5, 15=M15, 30=M30, 60=H1, 240=H4, 1440=D1, 10080=W1, 43200=MN1`.
- **Date strings**: `parse_datetime()` accepts `YYYY-MM-DD` and `YYYY-MM-DD HH:MM:SS` (and slash variants). Dates are treated as UTC by MT5.
- **Filling modes**: Brokers vary — `INVALID_FILL` errors require checking `symbol_info().filling_mode` bitmask. The `_get_filling_mode_error_suggestion()` helper does this automatically on order failure.

## Release Process

Releases are automated via semantic-release on push to `main`. Commit messages must follow **Conventional Commits** (`feat:`, `fix:`, `chore:`, etc.). The release workflow runs `poetry version` to update `pyproject.toml` and commits `CHANGELOG.md` + `pyproject.toml` back to main with `[skip ci]`.
