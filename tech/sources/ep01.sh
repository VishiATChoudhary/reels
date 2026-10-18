#!/usr/bin/env bash
# ep01: Oliver Selfridge, MIT Lincoln Laboratory, "The Thinking Machine" (CBS / MIT, 1961)
source "$(dirname "$0")/../../tools/lib.sh"
# lib.sh get() trips on an empty array under set -u in macOS bash 3.2
get() {
  [ -f "raw/$1.mp4" ] && return 0
  local sec=()
  [ -n "${3:-}" ] && sec=(--download-sections "*$3")
  "${YT[@]}" ${sec[@]+"${sec[@]}"} -f "$FMT" --merge-output-format mp4 -o "raw/$1.%(ext)s" -- "$2"
}
ep tech ep01

BROLL=~/shennies/synapse/promo/public/broll
[ -f raw/aygSMgK3BEM.mp4 ] || cp "$BROLL/aygSMgK3BEM.mp4" raw/   # The Thinking Machine (1961)
[ -f raw/_9_AEVQ_p74.mp4 ] || cp "$BROLL/_9_AEVQ_p74.mp4" raw/   # Shannon demonstrates Theseus, Bell Labs (1952)
get dc   jqm1i_FSr8Y   # data centre corridor, "Stock Video Free To Use"
get h100 QGpniBJiCZw   # NVIDIA HGX H100 promo (GPU boards)

# Selfridge, 95.7 to 112.55 s: ends on "in our lifetime", Shannon starts at 112.95
vo aygSMgK3BEM 95.7 112.55
words

# 'The Long Dark' by Scott Buckley, CC-BY 4.0, www.scottbuckley.com.au
music 8i_6R2zr9H8 57

TM="crop=iw-8:ih-8:4:8"   # drop the green line at the top of the telecine
shot selfridge-desk aygSMgK3BEM 93.0  1.0 "$BW" fill "$TM"
shot checkers       aygSMgK3BEM 60.0  0.8 "$BW" fill "$TM"
shot relays         _9_AEVQ_p74 98.0  0.8 "$BW"
shot punch          aygSMgK3BEM 128.0 0.8 "$BW" fill "crop=iw*0.5:ih-8:0:8"
shot tapes          aygSMgK3BEM 146.0 0.8 "$BW" fill "$TM"
shot mouse          _9_AEVQ_p74 256.0 0.9 "$BW"
shot console        aygSMgK3BEM 80.0  0.9 "$BW" fill "$TM"
shot printer        aygSMgK3BEM 81.5  1.0 "$BW" fill "$TM"
shot selfridge      aygSMgK3BEM 98.8  2.4 "$BW" fill "$TM"   # lip sync: src = 95.1 + timeline
shot keypunch       aygSMgK3BEM 137.0 1.6 "$BW" fill "crop=iw*0.55:ih-8:0:8"
shot maze           _9_AEVQ_p74 172.0 1.8 "$BW"
shot racks          _9_AEVQ_p74 112.0 1.8 "$BW"
shot testpanel      _9_AEVQ_p74 149.0 2.0 "$BW"
shot selfridge2     aygSMgK3BEM 106.4 4.0 "$BW" fill "$TM"
shot dc             dc          2.0   2.0 "$BW"
shot h100           h100        47.0  2.6 "$BW"

# hand-corrected captions; word ends snapped to measured pauses (silencedetect)
cat > words.json <<'JSON'
[
{"w": "I", "s": 0.05, "e": 0.15},
{"w": "don't", "s": 0.15, "e": 0.33},
{"w": "think", "s": 0.33, "e": 0.64},
{"w": "for", "s": 0.64, "e": 0.79},
{"w": "a", "s": 0.79, "e": 0.84},
{"w": "very", "s": 0.84, "e": 1.07},
{"w": "long", "s": 1.07, "e": 1.3},
{"w": "time", "s": 1.3, "e": 1.6},
{"w": "we're", "s": 1.6, "e": 1.75},
{"w": "going", "s": 1.75, "e": 1.84},
{"w": "to", "s": 1.84, "e": 1.94},
{"w": "have", "s": 1.94, "e": 2.25},
{"w": "a", "s": 2.25, "e": 2.3},
{"w": "difficult", "s": 2.3, "e": 2.6},
{"w": "problem", "s": 2.6, "e": 2.96},
{"w": "distinguishing", "s": 2.96, "e": 3.52},
{"w": "a", "s": 3.52, "e": 3.56},
{"w": "man", "s": 3.56, "e": 3.76},
{"w": "from", "s": 3.76, "e": 3.95},
{"w": "a", "s": 3.95, "e": 4.0},
{"w": "robot.", "s": 4.0, "e": 4.47},
{"w": "And", "s": 5.46, "e": 5.56},
{"w": "I", "s": 5.56, "e": 5.64},
{"w": "don't", "s": 5.64, "e": 5.79},
{"w": "think", "s": 5.79, "e": 5.92},
{"w": "my", "s": 5.92, "e": 6.1},
{"w": "daughter", "s": 6.1, "e": 6.32},
{"w": "will", "s": 6.32, "e": 6.48},
{"w": "ever", "s": 6.48, "e": 6.71},
{"w": "marry", "s": 6.71, "e": 7.06},
{"w": "a", "s": 7.06, "e": 7.11},
{"w": "computer.", "s": 7.11, "e": 7.48},
{"w": "But", "s": 8.78, "e": 8.9},
{"w": "I", "s": 8.9, "e": 9.0},
{"w": "think", "s": 9.0, "e": 9.1},
{"w": "the", "s": 9.1, "e": 9.14},
{"w": "computers", "s": 9.14, "e": 9.73},
{"w": "will", "s": 9.73, "e": 10.02},
{"w": "be", "s": 10.76, "e": 10.9},
{"w": "doing", "s": 10.9, "e": 11.0},
{"w": "the", "s": 11.0, "e": 11.16},
{"w": "things", "s": 11.16, "e": 11.5},
{"w": "that", "s": 11.5, "e": 11.72},
{"w": "men", "s": 11.72, "e": 11.88},
{"w": "do", "s": 11.88, "e": 12.0},
{"w": "when", "s": 12.0, "e": 12.16},
{"w": "we", "s": 12.16, "e": 12.28},
{"w": "say", "s": 12.28, "e": 12.36},
{"w": "they're", "s": 12.36, "e": 12.64},
{"w": "thinking.", "s": 12.64, "e": 12.92},
{"w": "I'm", "s": 13.5, "e": 13.64},
{"w": "convinced", "s": 13.64, "e": 14.08},
{"w": "that", "s": 14.08, "e": 14.28},
{"w": "machines", "s": 14.28, "e": 14.68},
{"w": "can", "s": 14.68, "e": 14.83},
{"w": "and", "s": 14.83, "e": 14.97},
{"w": "will", "s": 14.97, "e": 15.17},
{"w": "think", "s": 15.17, "e": 15.45},
{"w": "in", "s": 15.66, "e": 15.8},
{"w": "our", "s": 15.8, "e": 15.98},
{"w": "lifetime.", "s": 15.98, "e": 16.46}
]
JSON

cat > meta.json <<'JSON'
{
  "speaker": "Oliver Selfridge", "where": "MIT Lincoln Laboratory", "year": "1961",
  "hook": "THINK",
  "voDelay": 0.6,
  "music": {"title": "The Long Dark, Scott Buckley (CC-BY 4.0, credit: 'The Long Dark' by Scott Buckley, www.scottbuckley.com.au)",
            "url": "https://youtube.com/watch?v=8i_6R2zr9H8", "start": 57.0},
  "fit": "fill",
  "shots": [
    {"name": "selfridge-desk", "dur": 0.6,  "note": "Selfridge at his desk, chalkboard behind, before he speaks"},
    {"name": "checkers",       "dur": 0.4,  "note": "hand moves a piece on the checkers-playing computer's board"},
    {"name": "relays",         "dur": 0.35, "note": "Bell Labs relay bank behind Theseus (1952, colour graded b/w)"},
    {"name": "punch",          "dur": 0.4,  "note": "engineer reading a stack of punched cards at the card reader"},
    {"name": "tapes",          "dur": 0.4,  "note": "reel-to-reel tape drives with operators"},
    {"name": "mouse",          "dur": 0.45, "note": "Theseus, Shannon's maze-solving mouse, close"},
    {"name": "console",        "dur": 0.5,  "note": "operator at the computer console, tape drives behind"},
    {"name": "printer",        "dur": 0.6,  "note": "scientist leans over the teleprinter"},
    {"name": "selfridge",      "dur": 2.0,  "note": "Selfridge to camera, lip sync ('...a man from a robot')"},
    {"name": "keypunch",       "dur": 1.2,  "note": "hand on a keypunch keyboard, cards above"},
    {"name": "maze",           "dur": 1.4,  "note": "Claude Shannon beside the Theseus maze"},
    {"name": "racks",          "dur": 1.4,  "note": "bundled cable column through the relay racks"},
    {"name": "testpanel",      "dur": 1.6,  "note": "engineer at the TEST PANEL"},
    {"name": "selfridge2",     "dur": 3.6,  "note": "Selfridge to camera, lip sync, the key line begins ('I'm convinced that machines')"},
    {"name": "dc",             "dur": 1.6,  "note": "modern data centre corridor ('can and will think in our')"},
    {"name": "h100",           "dur": 2.15, "note": "NVIDIA H100 GPU modules ('lifetime') + tail"}
  ],
  "keyWords": ["think", "convinced", "lifetime"]
}
JSON
echo "meta ok"
