#!/usr/bin/env bash
# Jensen Huang, Stanford SIEPR Economic Summit 2024: "I wish upon you ample doses of pain and suffering". One continuous
# take: high expectations, low resilience, greatness comes from character, formed out of people who "suffered" (on
# HUMBLE YOURSELF's drop). Voice: p11-jensen.vo.py (splices jensen.mp4, writes vo.wav + srcmap.json + words.json). Run with bash.
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/../../tools/lib.sh"
ep tech p11-jensen
vget() {  # video only (b-roll is muted), best <=1080 stream
  [ -f "raw/$1.mp4" ] && return 0
  local sec=(); [ -n "${3:-}" ] && sec=(--download-sections "*$3")
  "${YT[@]}" ${sec[@]+"${sec[@]}"} -f "bv*[height<=1080][vcodec^=avc1]/bv*[height<=1080]" --remux-video mp4 -o "raw/$1.%(ext)s" -- "$2"
}
# the talk (SIEPR keynote, the official upload, from 35:50); the speaker shot is 1080p, the m4a-only FMT falls back to 360p
[ -f raw/jensen.mp4 ] || "${YT[@]}" --download-sections "*35:50-38:40" -f "137+bestaudio" --merge-output-format mp4 -o "raw/jensen.%(ext)s" -- cEg8cOx7UZk
vget grads      SDo7iSRLGEQ           # Stanford 2023 commencement highlights
vget wacky      QRVOCylEPZY           # Stanford 2023 Wacky Walk
vget rockytrain _YYmfM2TfUA           # Rocky (1976) training montage, Movieclips
vget round14    PNaTy5K4Pr0           # Rocky (1976) round 14: knocked down, gets up
vget will       -ViPmcdlfbQ           # Good Will Hunting chalkboard
vget gtc        Y2F8yisiS6E 0:00-12:00  # GTC 2024 keynote opening: arena, Jensen walks out
[ -f vo.wav ] || python3 "$HERE/p11-jensen.vo.py"
python3 "$HERE/p11-jensen.edit.py"

JH="crop=1080:1080:420:0"; WILL="crop=1440:860:240:0"
# hook: Jensen's face on frame 1 (lip-synced), zoomed tight in the edit
shot jensen_hook jensen     25.84 1.6 "$WARM"  square "crop=640:640:220:40"  # wide two-shot until 28.0: crop on Jensen
# build-up: slow, cold, muted
shot dawn        rockytrain 3.0   2.5 "$COLD"  square
shot stadium     grads      4.5   1.8 "$TEAL"  square
shot seated      grads      17.0  1.9 "$BLEAK" square
shot cheer       wacky      21.0  1.6 "$COLD"  square
shot jensen_a    jensen     69.90 2.1 "$WARM"  square "$JH"
shot canvas      round14    45.0  2.1 "$BLEAK" square
shot ropes       round14    66.0  1.6 "$COLD"  square
shot standup     round14    78.0  1.9 "$TEAL"  square
shot arena       gtc        224.0 1.5 "$COLD"  square
shot chalk       will       170.0 1.8 "$TEAL"  square "$WILL"
shot pushup      rockytrain 55.0  2.0 "$COLD"  square
shot hall        will       176.0 2.1 "$TEAL"  square "$WILL"
# riser: cuts tighten to the drop
shot meat        rockytrain 77.0  0.7 "$AMBER" square
shot grimace     rockytrain 67.5  0.7 "$COLD"  square
shot situp       rockytrain 72.0  0.7 "$TEAL"  square
shot steps       rockytrain 128.0 0.7 "$AMBER" square
# drop and payoff: vivid, on the beat
shot punch       round14    31.25 0.8 "$RED"   square
shot down        round14    45.5  0.9 "$RED"   square
shot whale       wacky      25.0  1.1 "$VIVID" square
shot signs       wacky      29.0  1.1 "$AMBER" square
shot crowd       grads      157.0 1.1 "$VIVID" square
shot lei         grads      61.0  1.1 "$AMBER" square
shot jensen_c    jensen     148.72 1.1 "$WARM" square "$JH"
shot battered    round14    126.0 1.1 "$RED"   square
shot arms        rockytrain 140.0 1.1 "$AMBER" square
shot walkout     gtc        228.3 1.1 "$VIVID" square
shot jensen_end  jensen     152.5 1.5 "$WARM"  square "$JH"
