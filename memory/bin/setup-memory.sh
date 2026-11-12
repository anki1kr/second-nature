#!/usr/bin/env bash
# Wire the persistent memory vault into installed CLI coding agents.
# Single source of truth = MEMORY-PROTOCOL.md.
# Idempotent: safe to run repeatedly; pointer blocks are replaced in place.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_DIR="${AGENT_MEMORY_VAULT:-$(cd "$SCRIPT_DIR/.." && pwd)}"
PROTOCOL="$VAULT_DIR/MEMORY-PROTOCOL.md"

[ -f "$PROTOCOL" ] || { echo "ERROR: MEMORY-PROTOCOL.md not found at $PROTOCOL"; exit 1; }

BEGIN='<!-- BEGIN AGENT-MEMORY -->'
END='<!-- END AGENT-MEMORY -->'
INCLUDE_CLAUDE="${1:-}"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; GRAY='\033[0;37m'; CYAN='\033[0;36m'; NC='\033[0m'

block() {
  printf '%s\n' "$BEGIN"
  [ -n "${1:-}" ] && printf '%s\n\n' "$1"
  cat <<EOF
## Persistent memory (Agent Memory Vault)

Your persistent main memory lives in the markdown vault at \`$VAULT_DIR\`.
At the start of EVERY session, silently (do not announce):
1. Read \`wiki/hot.md\` — recent context / boot index.
2. Read \`wiki/meta/lessons-learned.md\` — standing rules; NEVER repeat a catalogued mistake.

Then follow the full protocol in \`$PROTOCOL\`. It governs auto-logging (write corrections,
new rules, and bug patterns to lessons-learned.md WITHOUT being asked), the proactive memory
flush before context runs out, session notes in \`wiki/sessions/\`, and save triggers
(remember this / save this / note karo / yaad rakh).

Memory = this vault, NEVER a tool-local memory dir. Concise mode is default. Never
auto-commit or auto-push git.
EOF
  printf '%s\n' "$END"
}

wire() {
  local name="$1" path="$2" imp="${3:-}"
  local dir; dir="$(dirname "$path")"
  [ -d "$dir" ] || { echo -e "${YELLOW}[$name] not installed (skipped): $dir${NC}"; return; }
  [ -f "$path" ] && { cp -f "$path" "$path.bak-$(date +%Y%m%d-%H%M%S)"; }
  local newblock; newblock="$(block "$imp")"
  if [ -f "$path" ] && grep -qF "$BEGIN" "$path" && grep -qF "$END" "$path"; then
    awk -v b="$BEGIN" -v e="$END" -v repl="$newblock" '
      $0 ~ b {print repl; skip=1; next}
      $0 ~ e {skip=0; next}
      skip!=1 {print}
    ' "$path" > "$path.tmp" && mv "$path.tmp" "$path"
  else
    { [ -f "$path" ] && cat "$path" && echo; echo "$newblock"; } > "$path.tmp" && mv "$path.tmp" "$path"
  fi
  echo -e "${GREEN}[$name] wired: $path${NC}"
}

echo -e "${CYAN}Persistent memory -> CLI agents installer${NC}"
echo "Protocol (source of truth): $PROTOCOL"; echo

wire 'Codex CLI'  "$HOME/.codex/AGENTS.md"
wire 'Gemini CLI' "$HOME/.gemini/GEMINI.md" "@$PROTOCOL"
wire 'OpenCode'   "$HOME/.config/opencode/AGENTS.md"

if [ "$INCLUDE_CLAUDE" = "--include-claude" ]; then
  wire 'Claude Code' "$HOME/.claude/CLAUDE.md"
else
  echo -e "${GRAY}[Claude Code] skipped (pass --include-claude to add the pointer)${NC}"
fi

echo
echo -e "${CYAN}Done. Re-run any time — edits are idempotent and backed up.${NC}"
