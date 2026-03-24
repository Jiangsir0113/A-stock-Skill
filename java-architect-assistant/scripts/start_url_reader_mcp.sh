#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export JAVA_URL_MCP_HOST="${JAVA_URL_MCP_HOST:-127.0.0.1}"
export JAVA_URL_MCP_PORT="${JAVA_URL_MCP_PORT:-8765}"
export JAVA_URL_MCP_PATH="${JAVA_URL_MCP_PATH:-/mcp}"

echo "Starting java-url-reader-mcp on http://${JAVA_URL_MCP_HOST}:${JAVA_URL_MCP_PORT}${JAVA_URL_MCP_PATH}"
exec python3 "${SCRIPT_DIR}/url_reader_mcp.py"
