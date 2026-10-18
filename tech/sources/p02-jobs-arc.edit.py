# Writes edit.json for p02-jobs-arc from srcmap.json (voice timing) on WILD's beat grid, and prints the
# source times the lip-synced Jobs shots must start at (p02-jobs-arc.sh uses them).
# One continuous take: music and voice from frame 1, the story rides the build-up, "blew" lands on the drop.
import json
m=json.load(open('srcmap.json')); S=m["segments"]
D=m["drop"]; B=60/95.83
b=lambda n: round(D+n*B,3)
def src_at(reel):  # source time under the voice at a reel time
    s=max((x for x in S if x["reel"]<=reel), key=lambda x:x["reel"]); return round(s["src"]+reel-s["reel"],3)
shots=[
 # hook: Jobs' face on frame 1 (tight on the lip-synced whiteboard take) under the headline
 {"name":"jobs_hook","from":0,"zoom":1.6,"origin":"50% 18%"},
 # build-up: slow, cold, muted
 {"name":"condor1","from":b(-30)},{"name":"condor2","from":b(-27)},{"name":"apes1","from":b(-24)},{"name":"chart","from":b(-21)},
 {"name":"jobs_a","from":b(-18)},{"name":"apes2","from":b(-15)},{"name":"jobs_b","from":S[2]["reel"]},
 # riser: cuts tighten to the drop
 {"name":"pathe","from":S[3]["reel"]},{"name":"penny","from":b(-7)},{"name":"helmet","from":b(-5)},{"name":"wheel1","from":b(-4)},
 {"name":"pair","from":b(-3)},{"name":"glasses","from":b(-2)},{"name":"flare","from":b(-1.5)},{"name":"rider","from":b(-1)},{"name":"lens","from":b(-0.5)},
 # drop and payoff: vivid, on the beat
 {"name":"sprint","from":b(0),"flash":True},{"name":"hairpin","from":b(1)},{"name":"bchart","from":b(2)},{"name":"sprint2","from":b(4)},
 {"name":"jobs_c","from":b(6)},{"name":"mac","from":b(8)},{"name":"ape_bone","from":b(10)},{"name":"smash","from":b(12)},
 {"name":"match","from":b(13)},{"name":"desk","from":b(16)},{"name":"wheel2","from":b(18)},{"name":"jobs_end","from":b(20)}]
groups=[([0,1],"glass"),([2,3],None),([4,5],"stack"),([6,7],None),([8,9],"stack"),([10,11],"stack"),([12,14],None),([15,16],None),([17,18],"stack"),
 ([19,21],None),([22,23],None),([24,26],"stack"),([27,28],None),([29,31],"glass"),
 ([32,34],"stack"),([35,37],"stack"),([38,39],None),([40,41],"stack"),([42,43],"stack"),([44,46],None),([47,49],"stack"),
 ([50,50],"italic"),([51,52],"stack"),([53,53],None),([54,54],None),([55,57],None),([58,60],"stack"),
 ([61,63],None),([64,65],"stack"),([66,68],"italic"),([69,71],"stack"),([72,72],None),([73,73],"glass"),([74,76],None),([77,79],None),
 ([80,83],"stack"),([84,86],"stack"),([87,89],"glass")]
C=[]
for r,k in groups:
    c={"w":r}
    if k=="stack": c["layout"]="stack"
    if k=="italic": c["italic"]=True
    if k=="glass": c["glass"]=True
    C.append(c)
edit={"frame":"card","end":round(b(23),2),"voFrom":0,
 "music":[{"src":"shared/music/wild.mp3","start":m["musicStart"],"at":0,"volume":0.32}],
 "headline":{"text":"steve jobs found the answer in a study about *birds*","to":b(-27)},
 "shots":shots,"captions":C}
json.dump(edit,open('edit.json','w'),indent=1)
print("sync src: jobs_hook",src_at(0),"jobs_a",src_at(b(-18)),"jobs_b",src_at(S[2]["reel"]),"jobs_c",src_at(b(6)),"end",edit["end"])
