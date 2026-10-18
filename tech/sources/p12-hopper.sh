#!/usr/bin/env bash
# Grace Hopper, NSA lecture 1982: "we've always done it that way" is the most dangerous phrase. One continuous take: the
# counterclockwise clock, by the third day they recognize there was "never" (on FOR YOU's drop) any reason clocks run
# clockwise; payoff: she will materialize beside you and haunt you. Voice: p12-hopper.vo.py. Run with bash.
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/../../tools/lib.sh"
ep tech p12-hopper
vget() {  # video only (b-roll is muted), best <=1080 stream
  [ -f "raw/$1.mp4" ] && return 0
  local sec=(); [ -n "${3:-}" ] && sec=(--download-sections "*$3")
  "${YT[@]}" ${sec[@]+"${sec[@]}"} -f "bv*[height<=1080][vcodec^=avc1]/bv*[height<=1080]" --remux-video mp4 -o "raw/$1.%(ext)s" -- "$2"
}
# the lecture (NSA upload, part one, from 23:30; 480p is the best there is)
[ -f raw/hopper.mp4 ] || "${YT[@]}" --download-sections "*23:30-25:40" -f "bv*[height<=1080]+bestaudio" --merge-output-format mp4 -o "raw/hopper.%(ext)s" -- si9iqF5uTFk
vget bank     B-Vbqs-b4s0              # 1950s bank typing pool (Kinolibrary)
vget office   5x_t-lKXX6w              # 1950s office (Huntley)
vget clock    H4khmJ_ZxA8              # clock hands close-up, reversed below
vget calendar 80yeR0W7G6E              # calendar pages flipping
vget safety   M3mYnke7YYA 63:10-65:10  # Safety Last! (1923), Harold Lloyd hanging from the clock
vget markone  bN7AdQmd8So              # Harvard Mark I, 1944 (CHAP)
vget univac   j2fURxbdIZs 0:00-6:00    # Remington Rand presents the Univac
vget trek     fxVKmMSpTIE              # Star Trek TOS transporter, beam in
ln -sf ../../ep02/raw/switchboard.mp4 raw/switchboard.mp4
# the clock runs counterclockwise: reverse the footage
[ -f raw/clockrev.mp4 ] || ffmpeg -v error -y -ss 4 -t 30 -i raw/clock.mp4 -an -vf "reverse" -c:v libx264 -crf 16 -preset fast raw/clockrev.mp4
[ -f vo.wav ] || python3 "$HERE/p12-hopper.vo.py"
python3 "$HERE/p12-hopper.edit.py"

GH="crop=480:480:55:0"; BANK="crop=380:380:130:45"; OFF="crop=345:345:200:65"; SL="crop=1300:1000:310:40"
TREK="crop=480:400:187:0"; MK="crop=1440:1080:240:0"
# hook: Hopper's face on frame 1 (lip-synced), zoomed in the edit
shot hopper_hook hopper   11.45 1.5 "$WARM"  square "$GH"
# build-up: slow, cold, muted
shot glasses     bank     44.0  2.3 "$BLEAK" square "$BANK"
shot pool        bank     56.0  2.0 "$COLD"  square "$BANK"
shot switch1     switchboard 10.0 2.9 "$BLEAK" square
shot hopper_a    hopper   23.55 2.0 "$WARM"  square "$GH"
shot clock1      clockrev 2.0   1.8 "$TEAL"  square
shot clock2      clockrev 14.0  2.0 "$COLD"  square
shot desk        office   2.0   1.6 "$BLEAK" square "$OFF"
shot typist      bank     64.0  1.9 "$COLD"  square "$BANK"
shot calendar1   calendar 3.0   1.5 "$TEAL"  square
# riser: cuts tighten to the drop
shot grab        safety   54.0  0.8 "$COLD"  square "$SL"
shot hang1       safety   59.5  0.8 "$BLEAK" square "$SL"
shot clock3      clockrev 24.0  0.7 "$TEAL"  square
shot hang2       safety   61.2  0.7 "$COLD"  square "$SL"
# drop and payoff: vivid, on the beat
shot swing       safety   62.9  1.1 "$RED"   square "$SL"
shot clock4      clockrev 8.0   1.1 "$VIVID" square
shot hang3       safety   81.0  1.0 "$AMBER" square "$SL"
shot hopper_b    hopper   92.60 1.8 "$WARM"  square "$GH"
shot markone     markone  14.0  2.4 "$TEAL"  square "$MK"
shot calendar2   calendar 12.0  1.5 "$VIVID" square
shot univac      univac   153.0 1.5 "$AMBER" square
shot pool2       bank     4.0   1.5 "$AMBER" square "$BANK"
shot switch2     switchboard 13.0 1.6 "$VIVID" square
shot beam        trek     81.0  2.6 "$TEAL"  square "$TREK"
shot hopper_c    hopper   113.13 2.4 "$WARM" square "$GH"
shot hopper_end  hopper   20.20 1.8 "$WARM"  square "$GH"
