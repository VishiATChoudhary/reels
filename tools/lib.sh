# Shared sourcing helpers for every reel. Source it from an episode script:
#   source "$(dirname "$0")/../../tools/lib.sh"; ep tech ep01
# Writes into public/<theme>/<ep>/ (raw/ downloads, cuts/ graded 1080x1920 clips, vo.wav, music.mp3,
# words.json). Everything it writes is third-party footage or music and git-ignored: never commit it.
set -euo pipefail
REELS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
YT=(yt-dlp --cookies-from-browser chrome -q --no-warnings)
FMT="bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]/b"
MODEL="$REELS/tools/models/ggml-base.en.bin"

# ep <theme> <episode>: work inside public/<theme>/<episode>
ep() { OUT="$REELS/public/$1/$2"; mkdir -p "$OUT/raw" "$OUT/cuts"; cd "$OUT"; }

# get <name> <youtube id or url> [section like 1:20-2:05]: download once into raw/<name>.mp4
get() {
  [ -f "raw/$1.mp4" ] && return 0
  local sec=()
  [ -n "${3:-}" ] && sec=(--download-sections "*$3")
  "${YT[@]}" ${sec[@]+"${sec[@]}"} -f "$FMT" --merge-output-format mp4 -o "raw/$1.%(ext)s" -- "$2"
}

# music <youtube id or url> [start s]: soundtrack as music.mp3, trimmed to start at <start>
music() {
  [ -f music.mp3 ] && return 0
  "${YT[@]}" -x --audio-format mp3 --audio-quality 0 -o "raw/music.%(ext)s" -- "$1"
  ffmpeg -v error -y -ss "${2:-0}" -i raw/music.mp3 -t 40 -af "loudnorm=I=-16:TP=-1.5" -ar 48000 music.mp3
}

# grades: one dominant colour per shot (STYLE.md), alternate warm and cold. Defined once in themes/grades.json
# (shared with tools/reel.py); exported here as $COLD, $TEAL, ...
eval "$(python3 -c 'import json,shlex,sys; [print(f"{k}={shlex.quote(v)}") for k,v in json.load(open(sys.argv[1])).items() if k!="_doc"]' "$REELS/themes/grades.json")"

# shot <name> <raw name> <start s> <dur s> <grade> [fit] [pre filters]
#   fit = fill (default: crop to 9:16 and fill 1080x1920) | wide (16:9, 1080x608, for letterbox/cards)
#         | square (1080x1080, the rounded card)
shot() {
  local name=$1 src=$2 ss=$3 t=$4 grade=$5 fit=${6:-fill} pre=${7:-} geo
  if [ "$fit" = square ]; then
    geo="scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080"
  elif [ "$fit" = wide ]; then
    geo="scale=1080:608:force_original_aspect_ratio=increase,crop=1080:608"
  else
    geo="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
  fi
  ffmpeg -v error -y -ss "$ss" -t "$t" -i "raw/$src.mp4" -an \
    -vf "${pre:+$pre,}$geo,setsar=1,fps=30,$grade,format=yuv420p" \
    -c:v libx264 -crf 17 -preset fast "cuts/$name.mp4"
  echo "shot $name"
}

# vo <raw name> <start s> <end s>: the voice line as vo.wav, loudness matched, tiny fades
vo() {
  ffmpeg -v error -y -ss "$2" -to "$3" -i "raw/$1.mp4" -vn -ac 2 -ar 48000 \
    -af "highpass=f=80,loudnorm=I=-15:TP=-1.5,afade=t=in:d=0.02,areverse,afade=t=in:d=0.1,areverse" vo.wav
  echo "vo $(ffprobe -v error -show_entries format=duration -of csv=p=0 vo.wav)s"
}

# words: whisper word timings of vo.wav into words.raw.json ([{w,s,e}] in seconds).
# Copy to words.json and fix spellings by hand; the reel reads words.json.
words() {
  ffmpeg -v error -y -i vo.wav -ar 16000 -ac 1 raw/vo16.wav
  whisper-cli -m "$MODEL" -f raw/vo16.wav -ml 1 -sow -ocsv -of raw/vo16 -np >/dev/null 2>&1
  python3 - <<'PY'
import csv, json
out = []
for r in csv.DictReader(open("raw/vo16.csv")):
    w = r["text"].strip()
    if w and not w.startswith("["):
        out.append({"w": w, "s": int(r["start"]) / 1000, "e": int(r["end"]) / 1000})
json.dump(out, open("words.raw.json", "w"), indent=0)
print(" ".join(x["w"] for x in out))
PY
}

# transcript <raw name>: whole-file transcript with times, to find the quote inside a long clip
transcript() {
  ffmpeg -v error -y -i "raw/$1.mp4" -ar 16000 -ac 1 "raw/$1.16k.wav"
  whisper-cli -m "$MODEL" -f "raw/$1.16k.wav" -np 2>/dev/null
}
