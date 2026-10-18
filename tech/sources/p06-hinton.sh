HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/../../tools/lib.sh"
ep tech p06-hinton
for f in hinton nnet h100 chip redsrv leds dc code; do ln -sf ../../ep05/raw/$f.mp4 raw/$f.mp4; done
get path    0SpecvqtIDM   # forest path in fog, free stock
get flight  Sp7MHZY2ADI   # early flying machine failures, archive (The Film Gate)
[ -f vo.wav ] || python3 "$HERE/p06-hinton.vo.py"
python3 "$HERE/p06-hinton.edit.py"

H60="crop=1080:1080:290:0"        # 60 Minutes: right of the logo, Hinton's face in the left third
H60C="crop=1080:1080:420:0"       # 60 Minutes b-roll, centred, clear of the logo
PATHE="crop=720:720:260:0"        # British Pathe: inside the pillarbox, left of the logo
CAP="crop=720:720:280:0"          # Caproni film: inside the pillarbox
shot hinton_hook hinton     54.55   2.2 "$WARM"  square "$H60"
shot nnet        nnet       14.0    2.1 "$COLD"  square
shot young       hinton     121.0   2.1 "$BLEAK" square "$H60C"   # Hinton in the 1970s
shot chat        hinton     603.0   2.1 "$TEAL"  square "$H60C"   # his GPT-4 test on screen
shot robot       hinton     193.0   2.1 "$COLD"  square "$H60C"
shot hinton_a    hinton     687.70  2.5 "$WARM"  square "$H60"
shot path        path       12.0    2.1 "$BLEAK" square
shot caproni     caproni    13.0    2.1 "$BLEAK" square "$CAP"    # Caproni Ca.60, 1921: nine wings, crashed on its second flight
shot caproni2    caproni    85.0    1.6 "$COLD"  square "$CAP"
shot hindenburg  hindenburg 172.0   1.2 "$BLEAK" square "$PATHE"
shot hinton_b    hinton     702.95  0.8 "$WARM"  square "$H60"
shot wreck       hindenburg 180.0   0.8 "$COLD"  square "$PATHE"
shot redsrv      redsrv     2.0     0.8 "$TEAL"  square
shot h100        h100       49.0    0.8 "$COLD"  square
shot chip        chip       4.0     0.6 "$TEAL"  square
shot leds        leds       3.0     0.6 "$COLD"  square
shot nnet2       nnet       34.0    0.6 "$TEAL"  square
shot robot2      hinton     196.0   0.6 "$COLD"  square "$H60C"
shot goal        hinton     188.0   0.8 "$VIVID" square "$H60C"
shot walker      hinton     203.0   0.8 "$RED"   square "$H60C"
shot chat2       hinton     618.0   1.2 "$AMBER" square "$H60C"
shot hinton_c    hinton     779.24  1.2 "$WARM"  square "$H60"
shot nnet3       nnet       110.0   1.2 "$TEAL"  square
shot kick        hinton     182.0   1.2 "$AMBER" square "$H60C"
shot board       hinton     736.5   2.1 "$VIVID" square "$H60C"   # Hinton at the whiteboard
shot redsrv2     redsrv     9.0     1.2 "$RED"   square
shot hinton_end  hinton     784.57  2.4 "$WARM"  square "$H60"
