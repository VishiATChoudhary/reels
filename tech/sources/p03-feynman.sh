HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/../../tools/lib.sh"
ep tech p03-feynman
for f in feynman chalk cray tape chipfilm h100 nnviz; do ln -sf ../../ep03/raw/$f.mp4 raw/$f.mp4; done
get cheetah  LMcb-I7os8o              # cheetah running, super slow motion (OryxR5)
get cheetah2 hTCqkw21osA              # cheetah running, front view
get indy     T4nMNjOIRbA 0:00-3:52    # 1950s Indy cars, start-up and race
get birds    yk30eXL7954              # slow motion birds flapping wings (HansNature)

get plane50  kvogIK-fjc8              # 1950 airplane takeoff close-up
get convair  g1wUBKFRs4s              # 1960s Swissair Convair take-off and in flight, 35mm
get jetfan   uDQUSyWMqqg              # jet engine fan blades spinning
get calcs    XIR4tK5ZOL8              # 1960s UK office, women at mechanical calculators, 16mm
get reels    A5r40BvnEEE              # 1960s computer tape reels spinning
get ibm      jtyOR8L4yH0              # 1960s early IBM computers, 35mm
get dragster SXV3E8Tj_oE              # NHRA top fuel launch, super slow motion (wheels)
get f1tire   iG90mjvR0J4              # F1 tyre over a kerb, slow motion
get wright   _xjKCDedaOs              # 1909 Wilbur Wright onboard flight, public domain
get f15      1Be9hIV2JsM              # F-15 afterburner take-off, slow motion
get concorde MvACffFXxrk              # Concorde take-off with reheat
get eniac    r2SCpzXqmP8              # ENIAC at the Moore School, 1946 (Hagley)
get honeywell aGzScvOXoRg             # Honeywell 200 computer, 1964 (AP)
[ -f vo.wav ] || python3 "$HERE/p03-feynman.vo.py"
python3 "$HERE/p03-feynman.edit.py"

FEY="crop=624:480:118:0"                        # strip the pillarbox
KINO="crop=560:560:180:10"                      # Kinolibrary 4:3: under the K logo, above the burnt-in timecode
INDY="crop=330:330:90:0"; CONC="crop=300:300:170:0"; HONEY="crop=900:900:300:180"   # clear of watermarks
shot fey_hook  feynman  95.70  1.6 "$WARM"  square "$FEY"
shot cheetah   cheetah  19.5   2.1 "$COLD"  square
shot indy      indy     46.5   1.7 "$BLEAK" square "$INDY"
shot burnout   dragster 12.5   1.4 "$TEAL"  square
shot wright    wright   1.0    1.5 "$BLEAK" square
shot gull      birds    0.5    1.2 "$COLD"  square
shot concorde1 concorde 29.0   1.2 "$TEAL"  square "$CONC"
shot gull2     birds    50.0   1.9 "$COLD"  square
shot fey_a     feynman  134.00 1.4 "$WARM"  square "$FEY"
shot eniac1    eniac    200.0  2.1 "$COLD"  square
shot chalk     chalk    247.0  2.4 "$BLEAK" square
shot calcs1    calcs    1.0    0.9 "$COLD"  square "$KINO"
shot calcs2    calcs    38.0   1.2 "$BLEAK" square "$KINO"
shot calcs3    calcs    76.0   1.2 "$TEAL"  square "$KINO"
shot ibm1      ibm      9.0    0.8 "$COLD"  square "$KINO"
shot eniac2    eniac    215.0  0.8 "$TEAL"  square
shot craylit   cray     82.6   0.8 "$COLD"  square
shot honey1    honeywell 14.0  0.6 "$BLEAK" square "$HONEY"
shot tapes     ibm      70.0   0.6 "$TEAL"  square "$KINO"
shot dragster  dragster 4.2    1.2 "$VIVID" square
shot ibm2      ibm      20.0   1.2 "$RED"   square "$KINO"
shot concorde2 concorde 33.0   1.2 "$AMBER" square "$CONC"
shot f15       f15      48.5   1.2 "$VIVID" square
shot jetfan    jetfan   3.0    1.2 "$TEAL"  square
shot nnviz     nnviz    21.7   1.7 "$VIVID" square
shot fey_c     feynman  246.30 1.7 "$WARM"  square "$FEY"
shot h100      h100     47.5   1.2 "$AMBER" square
shot chalk2    chalk    157.0  1.2 "$WARM"  square
shot eniac3    eniac    22.5   1.7 "$AMBER" square
shot honey2    honeywell 30.0  1.2 "$TEAL"  square "$HONEY"
shot calcs4    calcs    80.0   0.8 "$AMBER" square "$KINO"
shot fey_end   feynman  139.50 1.7 "$WARM"  square "$FEY"   # the pause after "in that sense": not talking
