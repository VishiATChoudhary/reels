# Writes edit.json for p04-selfridge from srcmap.json (voice timing) on MEDUSA's beat grid, and prints the
# source times the lip-synced Selfridge and Shannon shots must start at (p04-selfridge.sh uses them).
# One continuous take: music and voice from frame 1, the story rides the build-up, "think" lands on the drop.
# MEDUSA is fast (130.4 bpm): the build-up cuts on 2 and 4 beat units, the riser on 1 and 1/2.
import json
m=json.load(open('srcmap.json')); S=m["segments"]
D=m["drop"]; B=60/130.43
b=lambda n: round(D+n*B,3)
def src_at(reel):  # source time under the voice at a reel time
    s=max((x for x in S if x["reel"]<=reel), key=lambda x:x["reel"]); return round(s["src"]+reel-s["reel"],3)
shots=[
 # hook: Selfridge's face on frame 1, lip-synced, under the headline
 {"name":"sel_hook","from":0,"zoom":1.6,"origin":"50% 15%"},
 # build-up: slow, cold, muted; robots, a wedding, a computer
 {"name":"elektro","from":b(-31)},{"name":"sel_a","from":b(-27)},{"name":"robby","from":b(-23)},
 {"name":"wedding","from":b(-19)},{"name":"bride","from":b(-17)},{"name":"tapes","from":b(-15)},
 # turn: the computers doing what men do
 {"name":"sel_b","from":S[3]["reel"]},{"name":"checkers","from":b(-9)},{"name":"thinker","from":b(-7)},
 # riser: cuts tighten to the drop
 {"name":"sel_c","from":S[5]["reel"]},{"name":"mouse","from":b(-3)},{"name":"printer","from":b(-2)},{"name":"relays","from":b(-1)},{"name":"console","from":b(-0.5)},
 # drop and payoff: vivid, on the beat; Shannon's prophecy
 {"name":"atlas","from":b(0),"flash":True},{"name":"h100","from":b(2)},{"name":"shannon","from":S[7]["reel"]},
 {"name":"figure","from":b(8)},{"name":"maze","from":b(10)},{"name":"lab","from":b(12)},{"name":"robby2","from":b(16)},
 {"name":"figure2","from":b(19)},{"name":"atlas2","from":b(21)},{"name":"sel_end","from":b(23)}]
groups=[([5,6],"stack"),([7,8],"italic"),
 ([9,11],None),([12,14],"stack"),([15,16],"stack"),([17,20],"stack"),([21,23],"stack"),([24,24],None),([25,26],"stack"),([27,29],"glass"),
 ([30,33],"stack"),([34,35],"stack"),([36,38],"stack"),([39,40],"italic"),
 ([41,43],"stack"),([44,45],"stack"),([46,48],"stack"),([49,50],"stack"),([51,53],"stack"),([54,56],"stack"),([57,58],"italic"),
 ([59,60],"stack"),([61,62],"stack"),([63,65],None),
 ([66,66],"italic"),([67,69],"glass"),
 ([70,71],"stack"),([72,74],"stack"),([75,77],"stack"),([78,81],None),([82,84],"stack"),([85,87],"stack"),
 ([88,90],None),([91,93],"stack"),([94,95],"glass"),([96,99],"stack")]
C=[]
for r,k in groups:
    c={"w":r}
    if k=="stack": c["layout"]="stack"
    if k=="italic": c["italic"]=True
    if k=="glass": c["glass"]=True
    C.append(c)
edit={"frame":"card","end":round(b(26),2),"voFrom":0,
 "music":[{"src":"shared/music/medusa.mp3","start":m["musicStart"],"at":0,"volume":0.32}],
 "headline":{"text":"in 1961 an mit scientist made a promise about *machines*","to":b(-27)},
 "hook":{"text":"the machines","to":1.08},
 "shots":shots,"captions":C}
json.dump(edit,open('edit.json','w'),indent=1)
print("sync src: sel_hook",src_at(0),"sel_a",src_at(b(-27)),"sel_b",src_at(S[3]["reel"]),"sel_c",src_at(S[5]["reel"]),
      "shannon",src_at(S[7]["reel"]),"end",edit["end"])
sh=edit["shots"]
for i,x in enumerate(sh): print(x["name"],x["from"],round((sh[i+1]["from"] if i+1<len(sh) else edit["end"])-x["from"],2))
