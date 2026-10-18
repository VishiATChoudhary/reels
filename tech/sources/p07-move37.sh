HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/../../tools/lib.sh"
ep tech p07-move37
for f in doc board trailer tpu move37; do ln -sf ../../ep06/raw/$f.mp4 raw/$f.mp4; done
get doc2 WXuK6gekU1Y 1:22:00-1:28:30   # AlphaGo (2017), the ending: Fan Hui, "maybe it's beautiful"
[ -f vo.wav ] || python3 "$HERE/p07-move37.vo.py"
python3 "$HERE/p07-move37.edit.py"

# doc frames carry burnt-in subtitles: keep the top 82 %, square, centred on x (fraction of the width)
sub() { echo "crop=ih*0.82:ih*0.82:iw*$1-ih*0.41:0"; }
at() { echo "crop=ih:ih:iw*$1-ih/2:0"; }
BOARD="crop=870:870:520:30"            # the doc's overhead board, clear of its clock boxes
RED="crop=480:480:765:170"; REDB="crop=1080:1080:260:0"; PAIR="crop=1080:1080:150:0"   # broadcast, clear of its clocks
shot hook       move37  43.45  2.7 "$WARM"  square "$RED"
shot lee_a      doc     335.6  1.8 "$BLEAK" square "$(sub 0.42)"
shot redboard   move37  47.91  2.2 "$WARM"  square "$REDB"
shot fanhui1    doc     122.2  3.0 "$WARM"  square "$(sub 0.53)"
shot lee_what   doc     245.0  1.9 "$COLD"  square "$(sub 0.50)"
shot stones     board   3.0    2.7 "$TEAL"  square
shot lee_bad    doc     337.5  1.9 "$BLEAK" square "$(sub 0.42)"
shot lee_more   doc     292.0  2.7 "$COLD"  square "$(sub 0.50)"
shot fanhui_m   doc     297.2  2.3 "$WARM"  square "$(sub 0.55)"
shot room       doc     300.5  2.9 "$TEAL"  square "$(sub 0.45)"
shot aui        doc     507.0  1.6 "$COLD"  square "$(sub 0.40)"
shot aja        doc     96.5   1.6 "$COLD"  square "$(sub 0.50)"
shot girl       trailer 3.0    1.6 "$TEAL"  square "$(at 0.50)"
shot hand       trailer 1.5    1.0 "$BLEAK" square "$(at 0.40)"
shot leeprof    doc     252.0  1.0 "$BLEAK" square "$(sub 0.55)"
shot audience   trailer 9.5    1.0 "$COLD"  square
shot ajareach   doc     101.7  0.7 "$TEAL"  square "$(sub 0.45)"
shot leeprof2   doc     258.0  0.7 "$BLEAK" square "$(sub 0.55)"
shot comms      move37  41.0   0.7 "$COLD"  square "$PAIR"
shot ajabowl    doc     102.5  0.7 "$TEAL"  square "$(sub 0.45)"
shot place      doc     103.35 1.0 "$VIVID" square "$BOARD"
shot vineyard   doc2    288.6  1.0 "$AMBER" square "$(sub 0.50)"
shot m37board   doc     319.0  2.0 "$VIVID" square "$BOARD"
shot fanhui_i   doc     322.81 1.9 "$WARM"  square "$(sub 0.55)"
shot hl1        doc     325.0  1.6 "$AMBER" square "$BOARD"
shot hl2        doc     326.3  1.6 "$RED"   square "$BOARD"
shot net        trailer 25.0   1.6 "$TEAL"  square "$(at 0.45)"
shot hl3        doc     328.4  1.6 "$VIVID" square "$BOARD"
shot fanhui_end doc     298.0  1.6 "$WARM"  square "$(sub 0.55)"
