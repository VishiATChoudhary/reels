HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/../../tools/lib.sh"
ep tech p04-selfridge
ln -sf ../../ep01/raw/aygSMgK3BEM.mp4 raw/tm.mp4        # The Thinking Machine (CBS / MIT, 1961)
ln -sf ../../ep01/raw/_9_AEVQ_p74.mp4 raw/theseus.mp4   # Shannon demonstrates Theseus, Bell Labs (1952)
ln -sf ../../ep01/raw/h100.mp4 raw/h100.mp4             # NVIDIA HGX H100
ln -sf ../../ep01/raw/dc.mp4 raw/dc.mp4                 # data centre corridor
get elektro  6HiRz-c3vBE              # Elektro the robot and Sparko (1940s)
get wedding  Fq2SyseflFc              # 1953 wedding home movie, rice, bride and groom
get robby    AxQ9GG6hUDM              # Forbidden Planet (1956) trailer, Robby the Robot
get atlas    tF4DML7FIWk              # Boston Dynamics Atlas, Partners in Parkour
get figure   xLVm-QKEZSI              # Figure 02 humanoids at BMW Spartanburg
get thinker  82LaGCbinhg              # Rodin's The Thinker
[ -f vo.wav ] || python3 "$HERE/p04-selfridge.vo.py"
python3 "$HERE/p04-selfridge.edit.py"

TM="crop=iw-8:ih-8:4:8"                    # drop the green line at the top of the telecine
SHAN="crop=176:176:82:8"                    # Shannon's face, above the burnt-in name
KINO43="crop=600:600:340:0"; WED="crop=900:900:270:0"; ATL="crop=1000:1000:400:0"; ROB="crop=272:272:184:0"
shot sel_hook  tm       92.74  1.6 "$WARM"  square "$TM"
shot elektro   elektro  8.0    2.1 "$COLD"  square "$KINO43"
shot sel_a     tm       96.68  2.1 "$WARM"  square "$TM"
shot robby     robby    99.0   2.1 "$BLEAK" square "$ROB"
shot wedding   wedding  2.5    1.2 "$BLEAK" square "$WED"
shot bride     wedding  16.0   1.2 "$COLD"  square "$WED"
shot tapes     tm       143.0  1.1 "$TEAL"  square "$TM"
shot sel_b     tm       104.45 2.3 "$WARM"  square "$TM"
shot checkers  tm       60.0   1.2 "$COLD"  square "$TM"
shot thinker   thinker  36.0   1.4 "$BLEAK" square
shot sel_c     tm       109.15 1.1 "$WARM"  square "$TM"
shot mouse     theseus  256.0  0.8 "$COLD"  square
shot printer   tm       81.0   0.8 "$TEAL"  square "$TM"
shot relays    theseus  98.0   0.6 "$COLD"  square
shot console   tm       128.0  0.6 "$TEAL"  square "$TM"
shot atlas     atlas    11.0   1.2 "$VIVID" square "$ATL"
shot h100      h100     47.0   1.1 "$AMBER" square
shot shannon   tm       112.93 2.4 "$WARM"  square "$SHAN"
shot figure    figure   30.0   1.2 "$TEAL"  square
shot maze      theseus  172.0  1.2 "$AMBER" square
shot lab       theseus  149.0  2.1 "$VIVID" square
shot robby2    robby    110.0  1.7 "$RED"   square "$ROB"
shot figure2   figure   6.0    1.2 "$TEAL"  square
shot atlas2    atlas    40.0   1.2 "$AMBER" square "$ATL"
shot sel_end   tm       103.25 1.7 "$WARM"  square "$TM"   # the pause after "marry a computer": not talking
