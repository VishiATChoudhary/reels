#!/usr/bin/env bash
# ep02: Arthur C. Clarke, BBC Horizon (1964), filmed at the New York World's Fair
source "$(dirname "$0")/../../tools/lib.sh"
# lib.sh get() trips on an empty array under set -u in macOS bash 3.2
get() {
  [ -f "raw/$1.mp4" ] && return 0
  local sec=()
  [ -n "${3:-}" ] && sec=(--download-sections "*$3")
  "${YT[@]}" ${sec[@]+"${sec[@]}"} -f "$FMT" --merge-output-format mp4 -o "raw/$1.%(ext)s" -- "$2"
}
ep tech ep02

BROLL=~/shennies/synapse/promo/public/broll
get clarke YwELr8ir9qM   # BBC Archive: "1964: Arthur C Clarke predicts the future | Horizon"
[ -f raw/switchboard.mp4 ] || cp "$BROLL/2BzRjfOoiVQ.mp4" raw/switchboard.mp4   # Bell switchboard operators
get telex    I2azhVnqhPE   # 1950s press agency teleprinter (Kinolibrary)
get mf1961   NVtNdzzh7x8   # 1961 IBM computer room, tape drives (Kinolibrary)
get telstar  n2WGYesBOr4   # Telstar 1962, horn antenna + animation (b/w)
get telstar2 Xq7eDAlmT_k   # Telstar 1 launch 1962, NASA (colour)
get earth    _Sl8diqCAFw   # earth at night from orbit, "Free HD Videos - No Copyright"
get sat      Nb1FK3xAxkg   # satellite orbits earth, royalty free
get fibre    to1DVmLtfBo   # fibre optics macro, free stock
get call2    GKsys0pncMs   # man on a video call, copyright free
get phone    QI1WBEhSlbU   # hand scrolling a smartphone, free stock

# Voice: two lines from the same take, joined at natural pauses (0.15 s gap):
#   136.10-147.05 "It will be possible in that age ... from London."
#   184.25-188.80 "In fact, men will no longer commute, they will communicate."
ffmpeg -v error -y -i raw/clarke.mp4 -filter_complex \
  "[0:a]atrim=136.10:147.05,asetpts=N/SR/TB[a];[0:a]atrim=184.25:188.80,asetpts=N/SR/TB[b];\
aevalsrc=0:d=0.15:s=48000:c=stereo[g];[a]aresample=48000[a2];[b]aresample=48000[b2];[a2][g][b2]concat=n=3:v=0:a=1[out]" \
  -map "[out]" -c:a aac -b:a 256k raw/splice.mp4
vo splice 0 15.65
words

# "Thinking" from VANGELIST (Rusted Music Studio, free and royalty-free), track starts at 58:08
music nv2nKjUCCGA 3564

CL="crop=1440:810:240:150"          # inside the 4:3 pillarbox, below the BBC bug
KINO1="crop=760:428:200:160"        # telex: clear of the K logo and burnt-in timecode
KINO2="crop=540:304:20:102"         # mf1961: same
TS="crop=640:360:0:30"              # telstar: above the burnt-in subtitles
TS2="crop=340:192:80:44"            # telstar2: inside the frame lines
SW="crop=960:540:160:90"            # switchboard: inside the pillarbox
shot clarke      clarke      135.5 1.0 "$OLD" wide "$CL"
shot telex       telex       10.0  0.9 "$OLD" wide "$KINO1"
shot tapes       mf1961      3.0   0.8 "$OLD" wide "$KINO2"
shot horn        telstar     8.5   0.9 "$OLD" wide "$TS"
shot launch      telstar2    8.0   0.9 "$OLD" wide "$TS2"
shot telstar     telstar2    13.0  1.1 "$OLD" wide "$TS2"
shot beams       telstar     54.5  1.4 "$OLD" wide "$TS"
shot operators   switchboard 9.5   1.7 "$OLD" wide "$SW"
shot clarke2     clarke      140.8 3.0 "$OLD" wide "$CL"   # lip sync: src = 135.5 + timeline
shot overseas    switchboard 25.0  1.9 "$OLD" wide "$SW"
shot mainframe   mf1961      19.0  2.3 "$OLD" wide "$KINO2"
shot earth       earth       3.0   1.7 "$NOW" wide
shot sat         sat         5.5   1.6 "$NOW" wide
shot fibre       fibre       2.0   1.4 "$NOW" wide
shot call        call2       5.0   1.5 "$NOW" wide
shot phone       phone       3.0   2.0 "$NOW" wide

# hand-corrected captions; word ends snapped to measured pauses (silencedetect)
cat > words.json <<'JSON'
[
{"w": "It", "s": 0.08, "e": 0.13},
{"w": "will", "s": 0.13, "e": 0.44},
{"w": "be", "s": 0.44, "e": 0.53},
{"w": "possible,", "s": 0.53, "e": 1.2},
{"w": "in", "s": 1.2, "e": 1.33},
{"w": "that", "s": 1.33, "e": 1.59},
{"w": "age,", "s": 1.59, "e": 1.99},
{"w": "perhaps", "s": 1.99, "e": 2.44},
{"w": "only", "s": 2.44, "e": 2.78},
{"w": "fifty", "s": 2.78, "e": 3.16},
{"w": "years", "s": 3.16, "e": 3.55},
{"w": "from", "s": 3.55, "e": 3.75},
{"w": "now,", "s": 3.75, "e": 4.2},
{"w": "for", "s": 4.2, "e": 4.44},
{"w": "a", "s": 4.44, "e": 4.52},
{"w": "man", "s": 4.52, "e": 4.76},
{"w": "to", "s": 4.76, "e": 4.92},
{"w": "conduct", "s": 4.92, "e": 5.48},
{"w": "his", "s": 5.48, "e": 5.72},
{"w": "business", "s": 5.72, "e": 6.4},
{"w": "from", "s": 6.4, "e": 6.98},
{"w": "Tahiti", "s": 6.98, "e": 7.5},
{"w": "or", "s": 7.5, "e": 7.74},
{"w": "Bali,", "s": 7.74, "e": 8.56},
{"w": "just", "s": 8.93, "e": 9.27},
{"w": "as", "s": 9.27, "e": 9.44},
{"w": "well", "s": 9.44, "e": 9.72},
{"w": "as", "s": 9.72, "e": 9.8},
{"w": "he", "s": 9.8, "e": 9.93},
{"w": "could", "s": 9.93, "e": 10.27},
{"w": "from", "s": 10.27, "e": 10.54},
{"w": "London.", "s": 10.54, "e": 10.73},
{"w": "In", "s": 11.45, "e": 11.52},
{"w": "fact,", "s": 11.52, "e": 11.69},
{"w": "men", "s": 12.21, "e": 12.55},
{"w": "will", "s": 12.55, "e": 12.67},
{"w": "no", "s": 12.67, "e": 12.85},
{"w": "longer", "s": 12.85, "e": 13.1},
{"w": "commute,", "s": 13.42, "e": 14.17},
{"w": "they", "s": 14.17, "e": 14.57},
{"w": "will", "s": 14.57, "e": 14.81},
{"w": "communicate.", "s": 14.81, "e": 15.53}
]
JSON

cat > meta.json <<'JSON'
{
  "speaker": "Arthur C. Clarke", "where": "BBC Horizon", "year": "1964",
  "hook": "COMMUTE",
  "voDelay": 0.6,
  "music": {"title": "Thinking, from VANGELIST by Rusted Music Studio (free, royalty-free: rustedstudio.itch.io/free-music-vangelist-final-mix)",
            "url": "https://youtube.com/watch?v=nv2nKjUCCGA", "start": 3564.0},
  "fit": "wide",
  "shots": [
    {"name": "clarke",    "dur": 0.6,  "note": "Clarke close-up before he speaks (BBC 1964)"},
    {"name": "telex",     "dur": 0.45, "note": "teleprinter platen printing"},
    {"name": "tapes",     "dur": 0.4,  "note": "IBM tape reels spinning (1961)"},
    {"name": "horn",      "dur": 0.45, "note": "Telstar ground station horn antenna"},
    {"name": "launch",    "dur": 0.5,  "note": "Telstar 1 launch, Cape Canaveral, July 1962"},
    {"name": "telstar",   "dur": 0.7,  "note": "Telstar satellite on the stand"},
    {"name": "beams",     "dur": 0.9,  "note": "animation: satellite relaying across the Atlantic"},
    {"name": "operators", "dur": 1.3,  "note": "long row of switchboard operators"},
    {"name": "clarke2",   "dur": 2.6,  "note": "Clarke to camera, lip sync ('conduct his business from Tahiti')"},
    {"name": "overseas",  "dur": 1.5,  "note": "OVERSEAS switchboard sign"},
    {"name": "mainframe", "dur": 1.9,  "note": "operator loading a tape reel in the 1961 computer room ('...from London')"},
    {"name": "earth",     "dur": 1.3,  "note": "modern: earth at night from orbit ('In fact')"},
    {"name": "sat",       "dur": 1.2,  "note": "modern satellite passing over earth ('no longer commute')"},
    {"name": "fibre",     "dur": 1.0,  "note": "fibre optic strands glowing ('they will')"},
    {"name": "call",      "dur": 1.1,  "note": "man on a video call on a laptop at home ('communicate')"},
    {"name": "phone",     "dur": 1.55, "note": "hand scrolling a smartphone, tail"}
  ],
  "keyWords": ["Tahiti", "London", "commute", "communicate."]
}
JSON
echo "meta ok"
