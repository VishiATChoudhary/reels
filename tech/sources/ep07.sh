#!/usr/bin/env bash
# ep07: Andrej Karpathy, "Software Is Changing (Again)", YC AI Startup School, June 2025.
# Quote: Software 3.0, prompts are programs, written in English. Fill shots (terminal / code overlay on top).
#   bash tech/sources/ep07.sh
source "$(dirname "$0")/../../tools/lib.sh"
ep tech ep07

# sources
get karpathy LCEmiRjPEtQ 0:00-12:00    # the talk, first 12 min (Software 1.0 / 2.0 / 3.0)
get pycode   _8KfAc47rRM               # scrolling Python code (Vidsplay, free stock)
get coderun  kcWr8LO6hPM               # code running on a screen (free stock)
get dc       hFbmoms5sD4               # data centre corridors (Best Free Footage)
get hgx      QGpniBJiCZw               # NVIDIA HGX H100: GPU boards, assembly
[ -f raw/nnsim.mp4 ] || cp ~/shennies/synapse/promo/public/broll/3JQ3hYko51Y.mp4 raw/nnsim.mp4   # neural net 3D simulation (MNIST)
STOCK=~/shennies/synapse/promo/public/stock
for s in 13522169 35331911 8212373; do [ -f raw/st$s.mp4 ] || cp "$STOCK/raw-$s.mp4" raw/st$s.mp4; done

# voice: 3:15.7 to 3:29.45 of the talk
vo karpathy 195.7 209.45
[ -f words.json ] || words

# music: "Chrome Pulse" (TuneLiberty), dark techno, already driving at 2:25
music Gt_8j6GrNOo 145

# grade: $NOW pushed cooler and more contrasty
G="eq=saturation=0.85:contrast=1.18:brightness=-0.02,colorbalance=bs=0.06:rs=-0.04:bm=0.03"
shot coderun   coderun   2.0  1.0 "$G"
shot gpus      hgx       47.2 1.0 "$G"
shot corridor  dc        27.0 1.0 "$G"
shot pycode    pycode    5.0  1.0 "$G"
shot stage     karpathy  49.0 1.0 "$G"
shot nnsim     nnsim     40.0 1.0 "$G"
shot silhouette st8212373 5.0 1.0 "$G"
shot karpathy1 karpathy  19.0 1.6 "$G"
shot atlas     karpathy  135.0 1.4 "$G" fill "crop=iw*0.4:ih:iw*0.6:0"
shot coder     st35331911 3.0 1.4 "$G"
shot karpathy2 karpathy  60.0 1.8 "$G"
shot racks     dc        33.0 1.6 "$G"
shot laptop    st13522169 4.0 1.8 "$G"
shot karpathy3 karpathy  361.0 2.0 "$G"
shot crowd     karpathy  4.0 2.2 "$G"
shot karpathy4 karpathy  376.0 2.3 "$G"
