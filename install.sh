#!/usr/bin/env bash
# Install the reels-setup agent skill.
#   curl -fsSL https://raw.githubusercontent.com/VishiATChoudhary/reels/main/install.sh | bash
# Same skill via the skills CLI: npx skills add VishiATChoudhary/reels
set -euo pipefail

REPO="VishiATChoudhary/reels"
RAW="https://raw.githubusercontent.com/$REPO/main/skills/reels-setup/SKILL.md"

for dir in "$HOME/.claude/skills" "$HOME/.agents/skills"; do
  [[ "$dir" == "$HOME/.agents/skills" && ! -d "$HOME/.agents" ]] && continue
  mkdir -p "$dir/reels-setup"
  curl -fsSL "$RAW" -o "$dir/reels-setup/SKILL.md"
  echo "installed $dir/reels-setup"
done

if [[ -r /dev/tty ]] && { : < /dev/tty; } 2>/dev/null; then
  read -r -p "Star $REPO on GitHub? [Y/n] " a < /dev/tty || a=n
  if [[ ! "$a" =~ ^[Nn] ]]; then
    if command -v gh >/dev/null && gh auth status >/dev/null 2>&1; then
      gh api -X PUT "user/starred/$REPO" --silent && echo "starred, thank you"
    else
      echo "gh not logged in; star it at https://github.com/$REPO"
    fi
  fi
fi

echo "done. In Claude Code: /reels-setup (or ask your agent to set up the reels studio)"
