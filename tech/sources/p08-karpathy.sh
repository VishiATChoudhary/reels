HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/../../tools/lib.sh"
ep tech p08-karpathy
for f in karpathy pycode coderun dc hgx nnsim keys term1 st13522169 st35331911 st7942759 st8212373; do ln -sf ../../ep07/raw/$f.mp4 raw/$f.mp4; done
for f in tape cray nnviz; do ln -sf ../../ep03/raw/$f.mp4 raw/$f.mp4; done
ln -sf ../../ep02/raw/mf1961.mp4 raw/mf1961.mp4   # 1961 IBM computer room, tape drives (Kinolibrary)
ln -sf ../../ep05/raw/leds.mp4 raw/leds.mp4       # blinking server LEDs
[ -f vo.wav ] || python3 "$HERE/p08-karpathy.vo.py"
python3 "$HERE/p08-karpathy.edit.py"

at() { echo "crop=ih:ih:iw*$1-ih/2:0"; }
KAR="crop=1080:1080:420:0"
STAGE="crop=ih*0.6:ih*0.6:iw*0.53-ih*0.3:ih*0.22"   # Karpathy on the stage, clear of the slide text
CROWD="crop=ih*0.55:ih*0.55:iw*0.3:ih*0.45"
MF="crop=iw*0.84:ih*0.80:0:0"   # clear of the Kinolibrary timecode and logo
shot hook      karpathy   59.38 2.9 "$WARM"  square "$KAR"
shot reels     mf1961     1.0   1.9 "$BLEAK" square "$MF"
shot kar_a     karpathy   63.57 1.9 "$WARM"  square "$KAR"
shot gpus      hgx        47.2  1.9 "$TEAL"  square
shot corridor  dc         27.0  1.5 "$COLD"  square
shot pycode    pycode     5.0   1.5 "$COLD"  square
shot coder     st35331911 1.0   1.6 "$TEAL"  square
shot nnviz     nnviz      20.0  1.4 "$COLD"  square
shot nnsim     nnsim      40.0  1.9 "$TEAL"  square
shot coderun   coderun    2.0   1.9 "$TEAL"  square
shot gpus2     hgx        30.0  1.9 "$BLEAK" square
shot leds      leds       2.0   1.2 "$COLD"  square
shot stage     karpathy   350.0 2.6 "$WARM"  square "$(at 0.72)"
shot crowd     karpathy   12.0  1.6 "$TEAL"  square "$CROWD"
shot keys      keys       1.0   1.4 "$TEAL"  square
shot pycode2   pycode     15.0  1.1 "$COLD"  square
shot term      term1      5.0   1.1 "$COLD"  square
shot nnsim2    nnsim      55.0  1.1 "$TEAL"  square
shot gpus3     hgx        12.0  1.1 "$BLEAK" square
shot phones    dc         50.0  1.1 "$COLD"  square
shot stage2    karpathy   373.0 1.1 "$WARM"  square "$STAGE"
shot keys2     keys       6.0   1.1 "$TEAL"  square
shot silo      st8212373  5.0   0.7 "$COLD"  square
shot coderun2  coderun    7.0   0.7 "$TEAL"  square
shot reels2    mf1961     8.0   0.7 "$BLEAK" square "$MF"
shot cards     tape       6.0   0.7 "$COLD"  square
shot roar      karpathy   0.5   1.1 "$VIVID" square "$(at 0.72)"
shot keys3     keys       9.0   1.1 "$AMBER" square
shot stage3    karpathy   393.0 1.9 "$WARM"  square "$STAGE"
shot pycode3   pycode     20.0  1.1 "$VIVID" square
shot lamp      st13522169 3.0   1.1 "$AMBER" square
shot cray      cray       60.0  1.1 "$RED"   square
shot kar_end   karpathy   20.5  2.6 "$WARM"  square "$KAR"
