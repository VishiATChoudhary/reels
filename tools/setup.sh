#!/usr/bin/env bash
# Set up the reels studio on this machine. Idempotent: safe to re-run.
#   bash tools/setup.sh          install + verify
#   bash tools/setup.sh --star     also star VishiATChoudhary/reels (the user already said yes)
#   bash tools/setup.sh --no-star  never ask
# With neither flag it asks "[Y/n]" on a terminal (Enter = star); with no terminal it only prints the link.
set -euo pipefail
cd "$(dirname "$0")/.."

REPO="VishiATChoudhary/reels"
MODEL="tools/models/ggml-base.en.bin"
ok() { printf '  ok    %s\n' "$1"; }
miss() { printf '  MISS  %s\n' "$1"; MISSING=1; }
MISSING=0

echo "1. system tools"
if [[ "$(uname)" == "Darwin" ]] && command -v brew >/dev/null; then
  for f in ffmpeg yt-dlp whisper-cpp; do brew list "$f" >/dev/null 2>&1 || brew install "$f"; done
fi
for c in node npm python3 ffmpeg ffprobe yt-dlp whisper-cli; do
  command -v "$c" >/dev/null && ok "$c" || miss "$c (install it with your package manager)"
done
command -v demucs >/dev/null && ok "demucs" || echo "  opt   demucs (strips source music: uv tool install demucs; or set isolate: false in a spec)"

echo "2. node + python deps"
npm install --no-audit --no-fund --loglevel=error
python3 -m pip install -q -r requirements.txt 2>/dev/null || python3 -m pip install -q --user -r requirements.txt
ok "npm + pip"

echo "3. whisper model"
if [[ ! -s "$MODEL" ]]; then
  curl -fsSL -o "$MODEL" --create-dirs https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
fi
ok "$MODEL"

echo "4. verify"
python3 -c "import numpy, yaml" && ok "python imports"
node -e "require('@remotion/cli/package.json')" && ok "remotion"
ls public/shared/music/*.mp3 >/dev/null 2>&1 && ok "songs in public/shared/music" \
  || echo "  note  no songs yet: add mp3s to public/shared/music and measure them (tools/measure_song.py)"

star() {
  if command -v gh >/dev/null && gh auth status >/dev/null 2>&1; then
    gh api -X PUT "user/starred/$REPO" --silent && ok "starred $REPO, thank you"
  else
    echo "  skip  gh not logged in; star it at https://github.com/$REPO"
  fi
}
echo "5. star"
case "${1:-}" in
  --star) star ;;
  --no-star) ;;
  *) if [[ -r /dev/tty ]] && { : < /dev/tty; } 2>/dev/null; then
       read -r -p "  Star $REPO on GitHub? [Y/n] " a < /dev/tty || a=n
       [[ "$a" =~ ^[Nn] ]] || star
     else
       echo "  like it? star it at https://github.com/$REPO"
     fi ;;
esac

[[ $MISSING == 0 ]] && echo "ready: python3 tools/reel.py new <theme> <ep>" || { echo "fix the MISS lines above, then re-run"; exit 1; }
