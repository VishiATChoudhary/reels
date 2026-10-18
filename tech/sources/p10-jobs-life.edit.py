import json
m=json.load(open('srcmap.json')); S=m["segments"]
D=m["drop"]; B=60/93.02
b=lambda n: round(D+n*B,3)
def src_at(reel):  # source time under the voice at a reel time
    s=max((x for x in S if x["reel"]<=reel), key=lambda x:x["reel"]); return round(s["src"]+reel-s["reel"],3)
shots=[
 {"name":"jobs_hook","from":0,"zoom":1.6,"origin":"52% 37%"},
 {"name":"class","from":b(-28)},{"name":"earth","from":b(-25)},{"name":"rush","from":b(-22)},{"name":"cubicle","from":b(-19)},
 {"name":"rat","from":b(-16)},{"name":"goldfish","from":b(-13)},{"name":"jobs_a","from":b(-10)},
 {"name":"skyline","from":S[3]["reel"]},{"name":"pedestal","from":b(-6)},{"name":"wright","from":b(-4)},
 {"name":"beam","from":b(-3)},{"name":"apple2","from":b(-2)},{"name":"station","from":b(-1.5)},{"name":"board","from":b(-1)},{"name":"aerial","from":b(-0.5)},
 {"name":"cross","from":b(0),"flash":True},{"name":"times","from":b(1)},{"name":"crowd","from":b(2)},{"name":"beam2","from":b(3)},
 {"name":"beam3","from":b(4)},{"name":"jobs_b","from":b(6)},{"name":"apple1","from":b(8)},{"name":"insanely","from":b(10)},
 {"name":"open","from":b(12)},{"name":"paint","from":b(14)},{"name":"girl","from":b(16)},{"name":"cheer","from":b(17)},
 {"name":"jobs_end","from":b(19)},{"name":"ovation","from":b(22),"zoom":1.3,"origin":"50% 25%"}]
groups=[([0,3],"glass"),([4,8],"stack"),([9,11],"stack"),([12,16],None),([19,21],"stack"),([22,26],"stack"),
 ([27,29],None),([30,33],"stack"),([34,36],"stack"),([37,38],None),
 ([39,40],None),([41,42],None),([43,45],"glass"),
 ([46,50],"stack"),([51,53],"stack"),([54,56],"italic"),([57,59],None),
 ([60,60],"italic"),([61,62],"stack"),([63,66],"stack"),([67,69],"stack"),([70,71],None),([72,75],"stack"),([76,77],None),
 ([78,81],"stack"),([83,85],"stack"),([87,89],"stack"),([90,92],"stack"),([93,95],"stack"),([96,97],None),
 ([98,101],"stack"),([102,103],"stack"),([104,107],"glass")]
C=[]
for r,k in groups:
    c={"w":r}
    if k=="stack": c["layout"]="stack"
    if k=="italic": c["italic"]=True
    if k=="glass": c["glass"]=True
    C.append(c)
edit={"frame":"card","end":round(b(25),2),"voFrom":0,
 "music":[{"src":"shared/music/let-me-fall.mp3","start":m["musicStart"],"at":0,"volume":0.32}],
 "headline":{"text":"steve jobs on the one fact that makes your life *bigger*","to":b(-25)},
 "shots":shots,"captions":C}
json.dump(edit,open('edit.json','w'),indent=1)
print("sync src: jobs_hook",src_at(0),"jobs_a",src_at(b(-10)),"jobs_b",src_at(b(6)),"jobs_end",src_at(b(19)),"to",src_at(b(22)),"end",edit["end"])
print(' '.join(f"{s['name']}@{s['from']}" for s in shots))
