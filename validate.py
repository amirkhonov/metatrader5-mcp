#!/usr/bin/env python3
"""
Validation script to check prerequisites for MetaTrader5-MCP.
Run this before installing to ensure your system is ready.
"""

import platform
import subprocess
import sys
from pathlib import Path


def print_header(text: str) -> None:
    """Print a section header."""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print("=" * 60)


def print_success(text: str) -> None:
    """Print success message."""
    print(f"✓ {text}")


def print_error(text: str) -> None:
    """Print error message."""
    print(f"✗ {text}")


def print_warning(text: str) -> None:
    """Print warning message."""
    print(f"⚠ {text}")


def check_python_version() -> bool:
    """Check if Python version is 3.10+."""
    print_header("Checking Python Version")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"Python version: {version_str}")

    if version.major == 3 and version.minor >= 10:
        print_success(f"Python {version_str} is supported")
        return True
    else:
        print_error(f"Python {version_str} is not supported")
        print("  Required: Python 3.10 or higher")
        print("  Download from: https://www.python.org/downloads/")
        return False


def check_operating_system() -> bool:
    """Check if running on Windows (required for MT5)."""
    print_header("Checking Operating System")

    os_name = platform.system()
    print(f"Operating System: {os_name}")

    if os_name == "Windows":
        print_success("Windows detected - MT5 is supported")
        return True
    else:
        print_warning(f"{os_name} detected - MT5 only runs on Windows")
        print("  You can still install the MCP server, but MT5 must run on Windows")
        print("  Consider using Wine or a Windows VM")
        return True  # Don't fail, just warn


def check_pip() -> bool:
    """Check if pip is available."""
    print_header("Checking pip")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(result.stdout.strip())
        print_success("pip is available")
        return True
    except subprocess.CalledProcessError:
        print_error("pip is not available")
        print("  Install pip: python -m ensurepip --upgrade")
        return False


def check_mt5_terminal() -> bool:
    """Check if MT5 terminal is installed (Windows only)."""
    print_header("Checking MetaTrader 5 Terminal")

    if platform.system() != "Windows":
        print_warning("Skipping MT5 check (not on Windows)")
        return True

    # Common MT5 installation paths
    possible_paths = [
        Path("C:/Program Files/MetaTrader 5/terminal64.exe"),
        Path("C:/Program Files (x86)/MetaTrader 5/terminal64.exe"),
        Path.home() / "AppData/Roaming/MetaQuotes/Terminal/MetaTrader 5/terminal64.exe",
    ]

    for path in possible_paths:
        if path.exists():
            print_success(f"MT5 found at: {path}")
            return True

    print_warning("MT5 terminal not found in common locations")
    print("  If MT5 is installed elsewhere, you can specify the path with --path")
    print("  Download MT5 from: https://www.metatrader5.com/")
    return True  # Don't fail, just warn


def check_venv() -> bool:
    """Check if venv module is available."""
    print_header("Checking Virtual Environment Support")

    try:
        import venv  # noqa: F401

        print_success("venv module is available")
        return True
    except ImportError:
        print_error("venv module is not available")
        print("  Install with: apt-get install python3-venv (Ubuntu/Debian)")
        return False


def check_git() -> bool:
    """Check if git is available."""
    print_header("Checking Git")

    try:
        result = subprocess.run(
            ["git", "--version"], capture_output=True, text=True, check=True
        )
        print(result.stdout.strip())
        print_success("Git is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_warning("Git is not available")
        print("  Git is recommended for cloning the repository")
        print("  Download from: https://git-scm.com/")
        return True  # Don't fail, just warn


def check_dependencies() -> bool:
    """Check if required Python packages can be installed."""
    print_header("Checking Package Dependencies")

    required_packages = ["fastmcp", "mcp", "MetaTrader5", "pydantic"]

    print("Required packages:")
    for package in required_packages:
        print(f"  - {package}")

    print_success("Dependencies will be installed during setup")
    return True


def main() -> int:
    """Run all validation checks."""
    print("\n" + "=" * 60)
    print("  MetaTrader5-MCP Prerequisites Validation")
    print("=" * 60)

    checks = [
        ("Python Version", check_python_version, True),
        ("Operating System", check_operating_system, False),
        ("pip", check_pip, True),
        ("Virtual Environment", check_venv, True),
        ("Git", check_git, False),
        ("MT5 Terminal", check_mt5_terminal, False),
        ("Dependencies", check_dependencies, False),
    ]

    results = []
    critical_failed = False

    for name, check_func, is_critical in checks:
        try:
            result = check_func()
            results.append((name, result, is_critical))
            if is_critical and not result:
                critical_failed = True
        except Exception as e:
            print_error(f"Check failed with error: {e}")
            results.append((name, False, is_critical))
            if is_critical:
                critical_failed = True

    # Print summary
    print_header("Validation Summary")

    for name, result, is_critical in results:
        status = "✓ PASS" if result else ("✗ FAIL" if is_critical else "⚠ WARN")
        critical_marker = " (CRITICAL)" if is_critical and not result else ""
        print(f"  {status}: {name}{critical_marker}")

    print("\n" + "=" * 60)

    if critical_failed:
        print("✗ Some critical checks failed. Please resolve them before installing.")
        print("\nNext steps:")
        print("  1. Fix the critical issues listed above")
        print("  2. Run this validation script again")
        print("  3. Proceed with installation")
        return 1
    else:
        print("✓ All critical checks passed! You're ready to install.")
        print("\nNext steps:")
        print("  1. Run the installation script:")
        if platform.system() == "Windows":
            print("     install.bat")
        else:
            print("     ./install.sh")
        print("  2. Edit .env with your MT5 credentials")
        print("  3. Run: metatrader5-mcp")
        return 0


if __name__ == "__main__":
    sys.exit(main())
