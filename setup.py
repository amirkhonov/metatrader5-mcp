#!/usr/bin/env python3
"""Setup script for MetaTrader5 MCP Server."""

from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip()
        for line in fh
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="metatrader5-mcp",
    version="0.1.0",
    author="MetaTrader5-MCP Contributors",
    author_email="",
    description="MCP server for MetaTrader 5 integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amirkhonov/metatrader5-mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "metatrader5-mcp=metatrader5_mcp.main:main",
        ],
    },
    keywords="metatrader5 mt5 mcp trading forex model-context-protocol",
    project_urls={
        "Bug Reports": "https://github.com/amirkhonov/metatrader5-mcp/issues",
        "Source": "https://github.com/amirkhonov/metatrader5-mcp",
        "Documentation": "https://github.com/amirkhonov/metatrader5-mcp#readme",
    },
)
