#!/usr/bin/env bash
# Pilot v2: Steve Jobs, "a bicycle for our minds" (1990), cut in the STYLE.md format to "WILD" (Encore).
# Reuses ep04's downloads (symlinked) plus film b-roll. Run with bash.
source "$(dirname "$0")/../../tools/lib.sh"
ep tech p01-jobs
for f in jobs condor cyclists penny mac chips fab board mbp2 bikes; do ln -sf ../../ep04/raw/$f.mp4 raw/$f.mp4; done
get bone  UZzVNLCeYKI    # 2001: A Space Odyssey (1968), bone to satellite
get apes  VABNA_an2A0    # 2001: the apes learn the tool
get cycle QuLgTeymJUI    # cinematic road cycling

# voice: four phrases of ep04's line, spliced (srcmap.json maps each piece back to jobs.mp4 for lip sync)
[ -f vo.wav ] || { echo "vo.wav missing: build it from ../ep04/vo.wav (see git history of this script)"; exit 1; }

JOBS="crop=940:716:163:2"
CONDOR="crop=960:720:280:0"
APES="crop=1920:864:0:108"
# shot <name> <raw> <start> <dur> <grade> square <pre>
shot hook      jobs   1.5   1.0  "$WARM"  square "$JOBS"
# burst on the drop: tools, half a beat each
shot b_apes    apes   85.0  0.6  "$AMBER" square "$APES"
shot b_bone    bone   6.0   0.6  "$COLD"  square
shot b_sat     bone   12.5  0.6  "$TEAL"  square
shot b_mac     mac    69.8  0.6  "$AMBER" square
shot b_wheel   cycle  15.0  0.6  "$COLD"  square
shot b_rider   cycle  26.0  0.6  "$TEAL"  square
# the line (lip-synced Jobs shots start where srcmap.json puts them)
shot jobs_wb   jobs   17.34 1.2  "$WARM"  square "$JOBS"
shot condor    condor 51.0  2.1  "$COLD"  square "$CONDOR"
shot riders    cycle  14.0  1.6  "$AMBER" square
shot sprint    cycle  22.0  1.8  "$TEAL"  square
shot jobs_cu1  jobs   48.05 1.3  "$WARM"  square "$JOBS"
shot mac       mac    71.0  1.8  "$COLD"  square
shot ape_tool  apes   76.0  2.0  "$AMBER" square "$APES"
shot match     bone   10.2  2.1  "$TEAL"  square
shot desk      jobs   55.39 1.9  "$AMBER" square "$JOBS"   # source cutaway: a man at his Macintosh
shot wheel     cycle  15.2  0.8  "$COLD"  square
shot jobs_end  jobs   4.0   2.2  "$WARM"  square "$JOBS"   # Jobs thinking, no lips to sync
