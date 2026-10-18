#!/usr/bin/env bash
# Jobs, "a bicycle for our minds", with a story arc: one continuous take, the setup rides WILD's build-up and
# "blew the condor away" lands on the drop. Voice: p02-jobs-arc.vo.py (splices jobs.mp4, writes vo.wav + srcmap.json). Run with bash.
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/../../tools/lib.sh"
ep tech p02-jobs-arc
for f in jobs condor bikeboom penny mac; do ln -sf ../../ep04/raw/$f.mp4 raw/$f.mp4; done
for f in bone apes cycle; do ln -sf ../../p01-jobs/raw/$f.mp4 raw/$f.mp4; done
[ -f vo.wav ] || python3 "$HERE/p02-jobs-arc.vo.py"
python3 "$HERE/p02-jobs-arc.edit.py"

JOBS="crop=940:716:163:2"; CONDOR="crop=960:720:280:0"; APES="crop=1920:864:0:108"
# hook: Jobs' face on frame 1, the whiteboard take (lip-synced), zoomed tight in the edit
shot jobs_hook jobs    17.15 1.5 "$WARM"  square "$JOBS"
# build-up: slow, cold, muted
shot condor1  condor   51.0  3.2 "$COLD"  square "$CONDOR"
shot condor2  condor   44.0  2.2 "$COLD"  square "$CONDOR"
shot apes1    apes     10.0  2.2 "$BLEAK" square "$APES"
shot chart    jobs     11.0  2.2 "$COLD"  square "$JOBS"
shot jobs_a   jobs     27.20 2.2 "$WARM"  square "$JOBS"
shot apes2    apes     30.0  2.8 "$BLEAK" square "$APES"
shot jobs_b   jobs     33.62 1.5 "$WARM"  square "$JOBS"
# riser: cuts tighten to the drop
shot pathe    bikeboom 36.0  1.2 "$AMBER" square
shot penny    penny    31.5  1.5 "$AMBER" square
shot helmet   cycle    12.0  0.9 "$COLD"  square
shot wheel1   cycle    15.0  0.9 "$TEAL"  square
shot pair     cycle    14.0  0.9 "$AMBER" square
shot glasses  cycle    17.0  0.6 "$COLD"  square
shot flare    cycle    1.0   0.6 "$AMBER" square
shot rider    cycle    16.0  0.6 "$TEAL"  square
shot lens     cycle    13.0  0.6 "$COLD"  square
# drop and payoff: vivid, on the beat
shot sprint   cycle    22.0  0.9 "$VIVID" square
shot hairpin  cycle    25.0  0.9 "$AMBER" square
shot bchart   jobs     43.0  1.5 "$WARM"  square "$JOBS"
shot sprint2  cycle    26.0  1.5 "$TEAL"  square
shot jobs_c   jobs     48.10 1.5 "$WARM"  square "$JOBS"
shot mac      mac      69.8  1.5 "$COLD"  square
shot ape_bone apes     76.0  1.5 "$AMBER" square "$APES"
shot smash    apes     85.0  0.9 "$RED"   square "$APES"
shot match    bone     10.2  2.1 "$TEAL"  square
shot desk     jobs     55.60 1.5 "$AMBER" square "$JOBS"
shot wheel2   cycle    15.2  1.5 "$COLD"  square
shot jobs_end jobs     4.0   2.6 "$WARM"  square "$JOBS"
