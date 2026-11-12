#!/usr/bin/env bash
# anki1kr/second-nature installer. No Node needed for the 9 built-in skills.
#
#   bash install.sh                 # the 9 built-in skills
#   bash install.sh --recommended   # also the 21 linked skills, from their own repos (needs Node: uses `npx skills`)
#   bash install.sh --memory        # also create the memory vault (~/.agents/memory, or $AGENT_MEMORY_VAULT)
#   bash install.sh --force         # overwrite skills that already exist with the same name
#
# Skills land in ~/.agents/skills (the shared location) and are copied into ~/.claude/skills when Claude Code is
# installed. Any other agent: `npx skills@latest add anki1kr/second-nature` picks the right folder for it.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
FORCE=0; REC=0; MEM=0
for a in "$@"; do case "$a" in --force) FORCE=1;; --recommended) REC=1;; --memory) MEM=1;; *) echo "unknown option: $a"; exit 2;; esac; done

copy_into() {
  local dest="$1"; mkdir -p "$dest"
  for d in "$HERE"/skills/*/; do
    local name; name="$(basename "$d")"
    if [ -e "$dest/$name" ] && [ "$FORCE" -eq 0 ]; then echo "  keep   $dest/$name (exists; --force to replace)"; continue; fi
    rm -rf "${dest:?}/$name"; cp -R "$d" "$dest/$name"; echo "  added  $dest/$name"
  done
}

echo "Installing built-in skills"
copy_into "$HOME/.agents/skills"
[ -d "$HOME/.claude" ] && copy_into "$HOME/.claude/skills"

if [ "$MEM" -eq 1 ]; then echo "Setting up the memory vault"; bash "$HERE/memory/setup.sh" || echo "  (vault already exists: left untouched)"; fi

if [ "$REC" -eq 1 ]; then
  command -v npx >/dev/null || { echo "--recommended needs Node.js (npx). Install Node 22+ and run again."; exit 1; }
  echo "Installing linked skills from their own repositories"
  while read -r spec; do
    [ -z "$spec" ] || [ "${spec#\#}" != "$spec" ] && continue
    echo "  $spec"; npx -y skills@latest add "$spec" -g -y >/dev/null 2>&1 || echo "    FAILED: $spec (install it by hand: npx skills add $spec)"
  done < "$HERE/recommended.txt"
fi
echo "Done. Open your agent and ask: \"which skills do I have for validating an idea?\""
