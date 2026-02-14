# MetaTrader5-MCP Dockerfile
# Note: This is primarily for development/testing as MT5 requires Windows.
# For production, MT5 must run on the same Windows machine.

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package
RUN pip install --no-cache-dir -e .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Expose port (if needed for future HTTP interface)
# EXPOSE 8000

# Run the MCP server
ENTRYPOINT ["metatrader5-mcp"]

# Default command (can be overridden)
CMD []
