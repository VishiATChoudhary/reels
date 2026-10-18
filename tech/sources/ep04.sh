#!/usr/bin/env bash
# ep04: Steve Jobs, "a bicycle for our minds" (1990, from the documentary "Memory & Imagination").
# Two pieces of one take: "The condor used the least energy to move a kilometer," then
# "And a man on a bicycle ... it's the equivalent of a bicycle for our minds."
#   bash tech/sources/ep04.sh
source "$(cd "$(dirname "$0")" && pwd)/../../tools/lib.sh"
ep tech ep04
B=~/shennies/synapse/promo/public/broll

# sources
for s in jobs:2hXSfS1i4jU mac:2B-XwPjn9YY board:kFlqbFORpFA chips:U_OexTUIyik fab:WVLGKq9An28; do
  [ -f "raw/${s%%:*}.mp4" ] || cp "$B/${s#*:}.mp4" "raw/${s%%:*}.mp4"
done                                      # Jobs 1990, Macintosh 1984, circuit board, chip macro, Intel fab
get condor   kr4YEfmCIg8 0:00-8:00   # The Flight of the Condor (BBC, 1982)
get bikeboom n3aKVsqRXPk 0:00-1:26   # Cycling Is Booming Again! (British Pathe, 1933)
get penny    p0LK1yYNrxo 0:00-0:36   # Cyclists (c.1900), British Pathe
get apple2   N_dMQlAWWI0 0:00-8:31   # Apple II close-ups
get mbp      KaNvXcP8Rvs 0:00-0:48   # MacBook Pro b-roll
get mbp2     8nrqWrO7Ebw 0:00-0:27   # MacBook Pro M1 b-roll

# "Interplanetary" by Martijn de Bont (free, Interstellar-style strings and organ): quiet build from 24 s,
# full entry at 48.0 s; a 34.0 s offset lands it on "the most remarkable tool"
music I18_VjY4Xuk 34.0

# vo from two pieces (vo() only takes one range): same filter chain as lib.sh vo()
ffmpeg -v error -y -i raw/jobs.mp4 -filter_complex \
  "[0:a]atrim=17.33:20.05,asetpts=PTS-STARTPTS[a];[0:a]atrim=41.95:58.5,asetpts=PTS-STARTPTS[b];\
[a][b]concat=n=2:v=0:a=1,aformat=channel_layouts=stereo,aresample=48000,\
highpass=f=80,loudnorm=I=-15:TP=-1.5,afade=t=in:d=0.02,areverse,afade=t=in:d=0.1,areverse[o]" \
  -map "[o]" -ar 48000 vo.wav
echo "vo $(ffprobe -v error -show_entries format=duration -of csv=p=0 vo.wav)s"
words

PATHE="crop=iw*0.86:ih*0.92:0:0"         # keeps the Pathe rooster (top right) and the bottom bar out

# 1900s to 1990
shot jobs_think jobs     1.5   1.2 "$OLD"
shot chart      jobs     10.5  1.1 "$OLD"
shot condor     condor   50.5  2.0 "$OLD"
shot bikes      bikeboom 36.0  1.1 "$OLD" fill "$PATHE"
shot penny      penny    31.5  1.1 "$OLD" fill "$PATHE"
shot bikes2     bikeboom 53.0  1.1 "$OLD" fill "$PATHE"
shot jobs_talk  jobs     16.5  1.5 "$OLD"
shot bikechart  jobs     43.4  1.9 "$OLD"
shot mac        mac      69.8  1.8 "$OLD"
shot jobs_cu    jobs     49.0  2.3 "$OLD"
shot apple2     apple2   140.0 1.9 "$OLD"
# now
shot board      board    2.0   2.1 "$NOW"
shot chips      chips    3.0   2.1 "$NOW"
shot fab        fab      6.4   2.4 "$NOW"
shot mbp        mbp      15.2  3.4 "$NOW"
shot mbp2       mbp2     20.2  3.6 "$NOW"

# words.json: whisper words, pauses trimmed off the word before them
python3 - <<'PY2'
import json
w = json.load(open("words.raw.json"))
end = {"kilometer,": 2.5, "charts.": 8.7, "with,": 16.25}
for x in w:
    x["e"] = end.get(x["w"], x["e"])
json.dump(w, open("words.json", "w"), indent=0)
PY2

cat > meta.json <<'JSON'
{
  "speaker": "Steve Jobs", "where": "Memory & Imagination", "year": "1990",
  "hook": "BICYCLE",
  "voDelay": 0.6,
  "music": {"title": "Interplanetary by Martijn de Bont (free, Interstellar style)", "url": "https://youtube.com/watch?v=I18_VjY4Xuk", "start": 34.0},
  "fit": "fill",
  "shots": [
    {"name": "jobs_think", "dur": 0.6,  "note": "Jobs, chin on fist, 1990"},
    {"name": "chart",      "dur": 0.55, "note": "the locomotion efficiency chart: gull, rabbit, rat"},
    {"name": "condor",     "dur": 1.4,  "note": "Andean condor gliding, BBC Flight of the Condor 1982"},
    {"name": "bikes",      "dur": 0.55, "note": "massed cyclists, Birmingham 1933, Pathe"},
    {"name": "penny",      "dur": 0.5,  "note": "penny farthing rider, c.1900"},
    {"name": "bikes2",     "dur": 0.5,  "note": "cyclists coming at camera, 1933"},
    {"name": "jobs_talk",  "dur": 0.9,  "note": "Jobs at the whiteboard"},
    {"name": "bikechart",  "dur": 1.3,  "note": "Scientific American bicycle efficiency chart"},
    {"name": "mac",        "dur": 1.2,  "note": "Macintosh on stage, 1984"},
    {"name": "jobs_cu",    "dur": 1.7,  "note": "Jobs close: that's what a computer is to me"},
    {"name": "apple2",     "dur": 1.3,  "note": "Apple II logic board"},
    {"name": "board",      "dur": 1.5,  "note": "circuit board macro"},
    {"name": "chips",      "dur": 1.5,  "note": "components macro, blue light"},
    {"name": "fab",        "dur": 1.8,  "note": "Intel cleanroom: the most remarkable tool"},
    {"name": "mbp",        "dur": 2.8,  "note": "MacBook Pro Touch Bar glowing"},
    {"name": "mbp2",       "dur": 2.97, "note": "modern MacBook keyboard and dock: a bicycle for our minds"}
  ],
  "keyWords": ["condor", "bicycle", "remarkable", "minds"]
}
JSON
python3 -c "import json;m=json.load(open('meta.json'));print('shots', len(m['shots']), 'sum %.2f' % sum(s['dur'] for s in m['shots']))"
