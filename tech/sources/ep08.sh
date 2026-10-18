#!/usr/bin/env bash
# ep08: Demis Hassabis to Scott Pelley, 60 Minutes (CBS, April 2025): AI could cure all disease.
# Fill shots (neural-network node graph drawn over them).
#   bash tech/sources/ep08.sh
source "$(dirname "$0")/../../tools/lib.sh"
ep tech ep08

# sources
get sixty    1XF-NG_35NE               # 60 Minutes: "What's next for AI at DeepMind" (2025)
get cells    5RAyvhOunxA 0:00-3:00     # Journey to the Microcosmos, uncut microscope footage
get micro2   cXOua0bzQxM               # scientist at a microscope (free stock)
get lab      xKSlP4rkXsY               # science laboratory, microscopes (free stock)
get dna      3WApsfiy8dE               # DNA helix particle simulation
get dna2     vb-IY-zpRDw               # DNA sequence animation (free stock)
get fold     2dV5s6v2v8Q               # protein synthesis / folding MD simulation (Spronk Studio)
BROLL=~/shennies/synapse/promo/public/broll
[ -f raw/alphafold.mp4 ] || cp "$BROLL/gg7WjuFs8F4.mp4" raw/alphafold.mp4   # AlphaFold: the making of
[ -f raw/nobel.mp4 ]     || cp "$BROLL/nobel.mp4" raw/nobel.mp4                 # Nobel ceremony 2024

# voice: 11:03.1 to 11:16.5 of the segment (Pelley asks "The end of disease?" in the middle)
vo sixty 663.1 676.5
[ -f words.json ] || words

# music: Scott Buckley, "Effervescence" (CC-BY 4.0), piano and strings building from 0:55
music pBrR83IjSUA 55

# the sync shots (hassabis1, pelley, hassabis2) start at 662.5 + their edit time, so lips match the voice
shot cells     cells     30.0  0.8 "$NOW"
shot dna       dna       4.0   0.8 "$NOW"
shot afscreen  alphafold 10.0  0.8 "$NOW"
shot tpu       sixty     260.5 0.8 "$NOW"
shot microscope micro2   2.0   0.9 "$NOW"
shot hassabis1 sixty     664.5 1.5 "$NOW"
shot fold      fold      24.0  1.4 "$NOW"
shot afprotein alphafold 165.0 1.6 "$NOW"
shot ribbon    sixty     632.0 1.6 "$NOW"
shot pelley    sixty     669.4 1.5 "$NOW"
shot hassabis2 sixty     670.9 2.0 "$NOW" fill "crop=iw*0.8:ih:iw*0.2:0"
shot nobel     nobel     165.5 2.0 "$NOW" fill "crop=iw*0.84:ih:0:0"
shot lab       lab       60.0  1.8 "$NOW"
shot seated    nobel     10.0  2.2 "$NOW" fill "crop=iw*0.5:ih*0.9:0:0"
