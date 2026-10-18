#!/usr/bin/env bash
# ep03: Richard Feynman, "Can machines think?" (Q&A after a lecture, 26 September 1985).
# Line: "So there's no question that the later machines are not going to think like people think ...
# they're not going to do arithmetic the same way as we do arithmetic, but they'll do it better."
#   bash tech/sources/ep03.sh
source "$(cd "$(dirname "$0")" && pwd)/../../tools/lib.sh"
ep tech ep03
B=~/shennies/synapse/promo/public/broll

# sources
get feynman  ipRvjS7q1DI 0:00-18:30   # Richard Feynman: Can Machines Think? (1985), 4:3 pillarboxed in 854x480
get chalk    s56AUKwlN9I 4:00-9:00    # Messenger Lectures, Cornell (1964): Feynman at the blackboard
get cray     Dq7TA3kogak 0:00-2:55    # NASA Ames Cray-2 (1985), CharlieDeanArchives
get tape     aGL8pdOj9Nk 0:00-0:11    # Addmaster paper tape reader
get chipfilm L5i6Sx137-0 0:00-4:03    # Microchip Production, 1980s, Huntley Archives film 95616
get h100     QGpniBJiCZw 0:00-1:00    # NVIDIA HGX H100
get nnviz    Tsvxx-GGlTg 0:00-1:07    # fully connected neural network visualisation
[ -f raw/nnsim.mp4 ] || cp "$B/3JQ3hYko51Y.mp4" raw/nnsim.mp4   # neural network 3D simulation (cybercontrols)

# "Afternoon" by Lukrembo (Free To Use Music, free with credit): piano intro, beat drops at 27.0 s,
# so a 10.2 s offset drops it on "but they'll do it better"
music C0n-iesn9BI 10.2

vo feynman 134.05 151.3
words

FEY="crop=624:480:118:0"                 # strip the pillarbox
CHIP="crop=1316:740:302:160"             # inside the 4:3 frame, under the archive banner, over the timecode
NN="crop=900:506:300:130"                # keeps the stats text and corner watermark out

# 1985 and before
shot fey_wide  feynman  58.0   1.2 "$OLD" wide "$FEY"
shot fey_hand  feynman  136.0  1.0 "$OLD" wide "$FEY"
shot tape      tape     8.6    1.0 "$OLD" wide
shot cray      cray     21.7   1.0 "$OLD" wide
shot chalk     chalk    157.0  1.0 "$OLD" wide
shot chipdes   chipfilm 78.6   1.0 "$OLD" wide "$CHIP"
shot fey_fist  feynman  133.0  1.6 "$OLD" wide "$FEY"
shot cray_lit  cray     82.6   1.3 "$OLD" wide
shot cray_tank cray     74.0   1.5 "$OLD" wide
shot fey_talk  feynman  121.0  2.4 "$OLD" wide "$FEY"
shot chalk_cu  chalk    247.0  2.6 "$OLD" wide
shot fey_eyes  feynman  139.0  2.2 "$OLD" wide "$FEY"
# now
shot nnsim     nnsim    20.6   2.4 "$NOW" wide "$NN"
shot hgx       h100     39.8   2.2 "$NOW" wide
shot nnviz     nnviz    21.7   2.4 "$NOW" wide
shot h100      h100     47.5   3.0 "$NOW" wide

# words.json: whisper words with hand fixes (the second "arithmetic" clause came out garbled)
python3 - <<'PY2'
import json
w = json.load(open("words.raw.json"))
fix = {"intelligence,": (7.99, 8.9), "they're": (13.73, 13.85), "not#2": (13.85, 14.0), "going#2": (14.0, 14.1),
       "to#3": (14.1, 14.18), "do#1": (14.18, 14.3), "arithmetic#1": (14.3, 14.78), "the#3": (14.78, 14.88), "same#2": (14.88, 15.0)}
seen = {}
for x in w:
    k = x["w"]; seen[k] = seen.get(k, 0) + 1
    for key in (k + "#" + str(seen[k]), k):
        if key in fix:
            x["s"], x["e"] = fix[key]; break
json.dump(w, open("words.json", "w"), indent=0)
PY2

cat > meta.json <<'JSON'
{
  "speaker": "Richard Feynman", "where": "Esalen Institute", "year": "1985",
  "hook": "THINK",
  "voDelay": 0.6,
  "music": {"title": "Afternoon by Lukrembo (Free To Use Music)", "url": "https://youtube.com/watch?v=C0n-iesn9BI", "start": 10.2},
  "fit": "wide",
  "shots": [
    {"name": "fey_wide",  "dur": 0.6,  "note": "Feynman at the flip chart, wide, 1985"},
    {"name": "fey_hand",  "dur": 0.45, "note": "Feynman gesturing"},
    {"name": "tape",      "dur": 0.45, "note": "punched paper tape through a reader"},
    {"name": "cray",      "dur": 0.5,  "note": "NASA Ames Cray-2, 1985"},
    {"name": "chalk",     "dur": 0.5,  "note": "Feynman at the blackboard, Cornell 1964"},
    {"name": "chipdes",   "dur": 0.5,  "note": "1980s chip layout, red and blue masks"},
    {"name": "fey_fist",  "dur": 1.0,  "note": "Feynman: not going to think like people think"},
    {"name": "cray_lit",  "dur": 0.7,  "note": "Cray panel lights"},
    {"name": "cray_tank", "dur": 0.9,  "note": "Cray-2 coolant tank close up"},
    {"name": "fey_talk",  "dur": 1.8,  "note": "Feynman explaining, hands together"},
    {"name": "chalk_cu",  "dur": 2.0,  "note": "Feynman 1964, close"},
    {"name": "fey_eyes",  "dur": 1.6,  "note": "Feynman, arm out"},
    {"name": "nnsim",     "dur": 1.8,  "note": "3D perceptron simulation, MNIST digit"},
    {"name": "hgx",       "dur": 1.6,  "note": "HGX board on the production line"},
    {"name": "nnviz",     "dur": 1.8,  "note": "neural net visualisation, digit lighting up"},
    {"name": "h100",      "dur": 1.2, "note": "NVIDIA H100 modules: but they'll do it better"},
    {"name": "hgx", "dur": 1.65, "note": "HGX line again: lands BETTER on a bright frame"}
  ],
  "keyWords": ["think", "arithmetic", "better"]
}
JSON
python3 -c "import json;m=json.load(open('meta.json'));print('shots', len(m['shots']), 'sum %.2f' % sum(s['dur'] for s in m['shots']))"
