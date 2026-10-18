#!/usr/bin/env bash
# ep06: AlphaGo vs Lee Sedol, game 2, Seoul (2016): move 37.
# Voice from AlphaGo (2017, DeepMind documentary): the live commentary, then Fan Hui.
#   bash tech/sources/ep06.sh
source "$(dirname "$0")/../../tools/lib.sh"
ep tech ep06

# get always takes a section: lib.sh's empty sec array trips set -u on macOS bash 3.2
get doc     WXuK6gekU1Y 48:00-62:00  # AlphaGo - The Movie (full documentary), the move 37 sequence
get move37  JNrXgpSEEIE 0:00-2:32    # "Move 37!!" live broadcast clip, game 2
get board   pGZluQUkflo 5:00-6:30    # real board, overhead, stones placed by hand
get tpu     FsxthdQ_sL4 0:00-2:40    # inside a Google Cloud TPU data centre
[ -f raw/trailer.mp4 ] || cp ~/shennies/synapse/promo/public/broll/8tq1C8spV_g.mp4 raw/trailer.mp4   # AlphaGo trailer

# "To Be Mortal" by Fuzzeke (no copyright, epic hybrid orchestral): silence at 47 s, full drop at 48 s,
# so starting at 35 s puts the drop on Fan Hui's "What?"
music WHDHsjXr6YA 35

# doc 49:51.55 to 50:09.65: "That's a very surprising move." "I thought it was a mistake."
# Fan Hui: "When I see this move, for me, it's just a big shock. What? ..."
vo doc 111.55 129.65
words
# words.json by hand: whisper base drifts on this clip (and drops the stutters), so the timings were
# placed from per-phrase whisper runs and the loudness envelope
python3 -c '
import json, sys
json.dump([{"w": w, "s": float(s), "e": float(e)} for w, s, e in (l.split() for l in sys.stdin if l.strip())],
          open("words.json", "w"), indent=0)' <<'WORDS'
That's 0.05 0.60
a 0.60 0.95
very, 0.95 1.45
that's 1.85 2.20
a 2.20 2.30
very 2.30 2.60
surprising 2.70 3.40
move. 3.45 4.10
I 4.28 4.45
thought 4.50 4.85
it 4.85 4.98
was, 4.98 5.35
I 5.42 5.60
thought 5.62 5.95
it 5.95 6.05
was 6.05 6.35
a 6.40 6.80
mistake. 6.85 7.80
When 9.19 9.45
I 9.45 9.49
see 9.49 9.79
this 9.79 10.12
move, 10.12 10.65
for 10.65 10.75
me, 10.75 11.07
it's 11.07 11.27
just 11.27 11.63
a 11.63 11.79
big 11.79 12.00
shock. 12.00 12.60
What? 12.73 13.20
Normally, 14.43 14.87
human, 14.87 15.13
we 15.13 15.34
never 15.34 15.61
play 15.61 15.81
this 15.81 16.01
one, 16.01 16.34
because 16.34 16.76
it's 16.76 17.43
bad. 17.43 17.95
WORDS

COOL="$NOW,colorbalance=bs=0.04:rs=-0.02"
# vertical crop centred on x = $1 (fraction of the 16:9 frame)
at() { echo "crop=ih*9/16:ih:iw*$1-ih*9/32:0"; }
# documentary frames carry burnt-in subtitles: drop the bottom 18 % first
sub() { echo "crop=iw:ih*0.82:0:0,$(at "$1")"; }

shot stone     trailer 7.2    1.0 "$COOL" fill "$(at 0.55)"
shot leeclose  doc     248.0  0.8 "$COOL" fill "$(sub 0.58)"
shot overhead  board   24.0   0.8 "$COOL" fill "$(at 0.40)"
shot team      doc     184.0  0.8 "$COOL" fill "$(sub 0.50)"
shot leehand   doc     288.0  0.8 "$COOL" fill "$(sub 0.40)"
shot netgraph  trailer 25.0   0.8 "$COOL" fill "$(at 0.40)"
shot comms     doc     114.3  1.8 "$COOL" fill "$(at 0.45)"    # commentators, in sync with the vo
shot bcast     doc     328.0  1.6 "$COOL" fill "$(sub 0.40)"
shot leethink  doc     56.0   1.8 "$COOL" fill "$(sub 0.50)"
shot copper    tpu     112.0  1.2 "$COOL"
shot overhead2 board   72.0   1.8 "$COOL" fill "$(at 0.45)"
shot gamecut   doc     121.0  1.4 "$COOL" fill "$(sub 0.45)"   # the doc's own cut, in sync
shot fanhui    doc     122.4  1.9 "$COOL" fill "$(sub 0.55)"   # Fan Hui, "a big shock"
shot aui       doc     514.0  1.5 "$COOL" fill "$(sub 0.30)"   # AlphaGo's own board UI
shot fanhui2   doc     125.8  2.5 "$COOL" fill "$(sub 0.62)"   # Fan Hui, "Normally, human..."
shot leefinal  doc     264.0  3.8 "$COOL" fill "$(sub 0.50)"
