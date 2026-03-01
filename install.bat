@echo off
REM Quick installation script for MetaTrader5-MCP (Windows)
REM This script sets up the environment and installs the package

echo ================================================
echo MetaTrader5-MCP Installation Script (Windows)
echo ================================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.10 or higher from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo √ Python %PYTHON_VERSION% detected
echo.

REM Check if Poetry is installed
echo Checking for Poetry...
poetry --version >nul 2>&1
if %errorlevel% equ 0 (
    echo √ Poetry detected
    set USE_POETRY=true
) else (
    echo Poetry not found. Will use pip instead.
    set USE_POETRY=false
)
echo.

REM Create virtual environment if needed
if "%USE_POETRY%"=="false" (
    echo Creating virtual environment...
    if not exist "venv" (
        python -m venv venv
        echo √ Virtual environment created
    ) else (
        echo √ Virtual environment already exists
    )

    REM Activate virtual environment
    call venv\Scripts\activate.bat
    echo √ Virtual environment activated
    echo.
)

REM Install dependencies
echo Installing dependencies...
if "%USE_POETRY%"=="true" (
    poetry install
    echo √ Dependencies installed via Poetry
) else (
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install -e .
    echo √ Dependencies installed via pip
)
echo.

REM Copy example environment file if .env doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo √ .env file created
    echo ⚠️  Please edit .env with your MT5 credentials
) else (
    echo √ .env file already exists
)
echo.

REM Ask about pre-commit hooks
set /p INSTALL_HOOKS="Install pre-commit hooks for development? (y/N): "
if /i "%INSTALL_HOOKS%"=="y" (
    pip install pre-commit
    pre-commit install
    echo √ Pre-commit hooks installed
)
echo.

echo ================================================
echo Installation Complete! 🎉
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env file with your MT5 credentials:
echo    notepad .env
echo.
echo 2. Run the server:
if "%USE_POETRY%"=="true" (
    echo    poetry run metatrader5-mcp
) else (
    echo    venv\Scripts\activate  REM if not already activated
    echo    metatrader5-mcp
)
echo.
echo 3. Or with command line arguments:
if "%USE_POETRY%"=="true" (
    echo    poetry run metatrader5-mcp --login 12345 --password secret --server MetaQuotes-Demo --path "C:\Program Files\MetaTrader 5\terminal64.exe"
) else (
    echo    metatrader5-mcp --login 12345 --password secret --server MetaQuotes-Demo --path "C:\Program Files\MetaTrader 5\terminal64.exe"
)
echo.
echo For help, see README.md or run:
echo    metatrader5-mcp --help
echo.
pause
