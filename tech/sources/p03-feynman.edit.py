# Writes edit.json for p03-feynman from srcmap.json (voice timing) on BEFORE's beat grid, and prints the
# source times the lip-synced Feynman shots must start at (p03-feynman.sh uses them).
# One continuous take: music and voice from frame 1, the story rides the build-up, "better" lands on the drop.
# BEFORE is fast (131.9 bpm): the build-up cuts on 2 and 4 beat units, the riser on 1 and 1/2.
import json
m=json.load(open('srcmap.json')); S=m["segments"]
D=m["drop"]; B=60/131.9
b=lambda n: round(D+n*B,3)
def src_at(reel):  # source time under the voice at a reel time
    s=max((x for x in S if x["reel"]<=reel), key=lambda x:x["reel"]); return round(s["src"]+reel-s["reel"],3)
shots=[
 # hook: Feynman's face on frame 1, lip-synced, under the headline
 {"name":"fey_hook","from":0,"zoom":1.6,"origin":"40% 6%"},
 # build-up: slow, cold, muted; the cheetah, the wheels, the bird, the airplane
 {"name":"cheetah","from":b(-40)},{"name":"indy","from":b(-36)},{"name":"burnout","from":b(-33)},
 {"name":"wright","from":S[1]["reel"]},{"name":"gull","from":b(-28)},{"name":"concorde1","from":b(-26)},{"name":"gull2","from":b(-24)},
 {"name":"fey_a","from":S[2]["reel"]},{"name":"eniac1","from":b(-18)},{"name":"chalk","from":b(-14)},
 # turn: people doing arithmetic by hand
 {"name":"calcs1","from":S[3]["reel"]},{"name":"calcs2","from":b(-8)},{"name":"calcs3","from":b(-6)},
 # riser: the machines, cuts tighten to the drop
 {"name":"ibm1","from":b(-4)},{"name":"eniac2","from":b(-3)},{"name":"craylit","from":b(-2)},{"name":"honey1","from":b(-1)},{"name":"tapes","from":b(-0.5)},
 # drop and payoff: vivid, on the beat
 {"name":"dragster","from":b(0),"flash":True},{"name":"ibm2","from":b(2)},{"name":"concorde2","from":b(4)},{"name":"f15","from":b(6)},
 {"name":"jetfan","from":b(8)},{"name":"nnviz","from":b(10)},{"name":"fey_c","from":S[6]["reel"]},{"name":"h100","from":b(16)},
 {"name":"chalk2","from":b(18)},{"name":"eniac3","from":b(20)},{"name":"honey2","from":b(23)},{"name":"calcs4","from":b(25)},
 {"name":"fey_end","from":b(26)}]
groups=[([7,8],"stack"),([9,11],"stack"),([12,14],"stack"),([15,18],"stack"),([19,20],"stack"),
 ([21,22],"stack"),([23,24],None),([25,27],"italic"),([28,29],None),([30,33],"stack"),([34,36],"stack"),
 ([37,38],None),([39,40],"stack"),([41,44],"stack"),([45,48],None),([49,49],"glass"),([50,52],"italic"),
 ([53,54],"stack"),([55,57],None),([58,60],"stack"),([61,63],None),([64,67],"stack"),([68,71],"stack"),
 ([72,72],"italic"),([73,75],"stack"),([76,78],"stack"),([79,80],"stack"),([81,82],"stack"),
 ([83,85],None),([86,87],"stack"),([88,90],"stack"),([91,93],"stack"),([94,96],"stack"),([97,99],"stack"),
 ([100,101],"italic"),([102,105],None),([106,107],"stack"),([108,109],"glass")]
C=[]
for r,k in groups:
    c={"w":r}
    if k=="stack": c["layout"]="stack"
    if k=="italic": c["italic"]=True
    if k=="glass": c["glass"]=True
    C.append(c)
edit={"frame":"card","end":round(b(29),2),"voFrom":0,
 "music":[{"src":"shared/music/before.mp3","start":m["musicStart"],"at":0,"volume":0.32}],
 "headline":{"text":"feynman explained ai in 1985 with a *cheetah*","to":b(-36)},
 "hook":{"text":"a machine","to":S[0]["reel"]+1.24},
 "shots":shots,"captions":C}
json.dump(edit,open('edit.json','w'),indent=1)
print("grid b(-40..29):",{n:b(n) for n in (-40,-36,-33,-28,-26,-24,-18,-14,-8,-6,-4,0,10,16,26,29)})
print("sync src: fey_hook",src_at(0),"fey_a",src_at(S[2]["reel"]),"fey_c",src_at(S[6]["reel"]),"end",edit["end"])
