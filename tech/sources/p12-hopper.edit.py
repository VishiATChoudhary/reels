# Writes edit.json for p12-hopper from srcmap.json (voice timing) on FOR YOU's beat grid (166.7 bpm, build-up cut on
# 4-beat units), and prints the source times the lip-synced Hopper shots must start at (p12-hopper.sh uses them).
import json
m=json.load(open('srcmap.json')); S=m["segments"]
D=m["drop"]; B=60/166.66
b=lambda n: round(D+n*B,3)
def src_at(reel):  # source time under the voice at a reel time
    s=max((x for x in S if x["reel"]<=reel), key=lambda x:x["reel"]); return round(s["src"]+reel-s["reel"],3)
shots=[
 # hook: Hopper's face on frame 1 under the headline
 {"name":"hopper_hook","from":0,"zoom":1.4,"origin":"50% 20%"},
 # build-up: slow (4 beats), cold, muted; back to Hopper once
 {"name":"glasses","from":b(-50)},{"name":"pool","from":S[1]["reel"]},{"name":"switch1","from":b(-40)},
 {"name":"hopper_a","from":S[2]["reel"]},{"name":"clock1","from":b(-28)},{"name":"clock2","from":b(-24)},
 {"name":"desk","from":S[3]["reel"]},{"name":"typist","from":b(-16)},{"name":"calendar1","from":S[4]["reel"]},
 # riser: 2 beats, into the drop
 {"name":"grab","from":b(-8)},{"name":"hang1","from":b(-6)},{"name":"clock3","from":b(-4)},{"name":"hang2","from":b(-2)},
 # drop and payoff: 2 to 4 beat cuts, vivid
 {"name":"swing","from":b(0),"flash":True},{"name":"clock4","from":b(2)},{"name":"hang3","from":b(4)},
 {"name":"hopper_b","from":S[6]["reel"]},{"name":"markone","from":b(12)},{"name":"calendar2","from":S[7]["reel"]},
 {"name":"univac","from":b(21)},{"name":"pool2","from":b(26)},{"name":"switch2","from":b(30)},{"name":"beam","from":b(33)},
 {"name":"hopper_c","from":b(39)},{"name":"hopper_end","from":b(45)}]
groups=[([0,1],"glass"),([2,4],"stack"),([5,7],None),([8,10],"stack"),([11,11],None),([12,14],"stack"),([15,18],"italic"),
 ([19,22],"stack"),([23,26],"stack"),([27,29],"stack"),([30,30],"glass"),([31,34],"stack"),([35,37],None),([38,38],None),
 ([39,41],"glass"),([42,44],None),([45,48],"stack"),([49,51],"stack"),([52,54],None),([55,55],"italic"),([56,57],"stack"),
 ([58,59],"stack"),([60,62],"stack"),([63,66],"stack"),([67,68],"italic"),([69,71],None),([72,73],"stack"),([74,77],"stack"),
 ([78,79],None),([80,82],None),([83,85],"stack"),([86,89],"italic"),([90,92],"stack"),([93,93],None),([94,95],"stack"),
 ([96,98],None),([99,99],"italic"),([100,103],"glass")]
C=[]
for r,k in groups:
    c={"w":r}
    if k=="stack": c["layout"]="stack"
    if k=="italic": c["italic"]=True
    if k=="glass": c["glass"]=True
    C.append(c)
edit={"frame":"card","end":round(b(49),2),"voFrom":0,
 "music":[{"src":"shared/music/for-you.mp3","start":m["musicStart"],"at":0,"volume":0.32}],
 "headline":{"text":"grace hopper banned one phrase from her *office*","to":b(-45)},
 "shots":shots,"captions":C}
json.dump(edit,open('edit.json','w'),indent=1)
print("sync src: hopper_hook",src_at(0),"hopper_a",src_at(S[2]["reel"]),"hopper_b",src_at(S[6]["reel"]),"hopper_c",src_at(b(39)),"end",edit["end"])
print("shot lengths:",' '.join(f"{s['name']}:{(shots[i+1]['from'] if i+1<len(shots) else edit['end'])-s['from']:.2f}" for i,s in enumerate(shots)))
