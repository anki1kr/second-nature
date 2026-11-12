#!/usr/bin/env bash
# Initialize the persistent memory vault at $AGENT_MEMORY_VAULT from template/
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_DIR="${AGENT_MEMORY_VAULT:-$HOME/.agents/memory}"

echo "Memory vault setup target: $VAULT_DIR"

if [ -d "$VAULT_DIR" ] && [ -n "$(ls -A "$VAULT_DIR" 2>/dev/null)" ]; then
    echo "Refusing to overwrite existing vault at $VAULT_DIR. Found existing files:"
    ls -la "$VAULT_DIR"
    exit 1
fi

mkdir -p "$VAULT_DIR"

if [ -d "$SCRIPT_DIR/template" ]; then
    cp -R "$SCRIPT_DIR/template/." "$VAULT_DIR/"
fi

mkdir -p "$VAULT_DIR/bin"
if [ -d "$SCRIPT_DIR/bin" ]; then
    cp -R "$SCRIPT_DIR/bin/." "$VAULT_DIR/bin/"
fi

if [ -f "$SCRIPT_DIR/MEMORY-PROTOCOL.md" ]; then
    cp -f "$SCRIPT_DIR/MEMORY-PROTOCOL.md" "$VAULT_DIR/"
fi

if [ -f "$SCRIPT_DIR/README.md" ]; then
    cp -f "$SCRIPT_DIR/README.md" "$VAULT_DIR/"
fi

echo "Vault files initialized from template."

export AGENT_MEMORY_VAULT="$VAULT_DIR"
if command -v python3 >/dev/null 2>&1; then
    python3 "$VAULT_DIR/bin/mem_index.py"
else
    python "$VAULT_DIR/bin/mem_index.py"
fi

echo "Setup completed successfully."
