import json
m=json.load(open('srcmap.json')); S=m["segments"]
D=m["drop"]; B=60/80.0
b=lambda n: round(D+n*B,3)
def src_at(reel):  # source time under the voice at a reel time
    s=max((x for x in S if x["reel"]<=reel), key=lambda x:x["reel"]); return round(s["src"]+reel-s["reel"],3)
shots=[
 {"name":"lec_hook","from":0,"zoom":1.4,"origin":"65% 30%"},
 {"name":"biologist","from":b(-31)},{"name":"student","from":b(-28)},{"name":"kendrew","from":b(-25)},{"name":"oneprot","from":b(-22)},
 {"name":"many","from":b(-19)},{"name":"lec_a","from":b(-16)},
 {"name":"afscreen","from":S[2]["reel"]},{"name":"screen60","from":b(-12)},{"name":"team","from":b(-10)},{"name":"servers","from":b(-8)},
 {"name":"chart","from":b(-6)},{"name":"spike","from":b(-5)},{"name":"cages","from":b(-4)},{"name":"sphere","from":b(-3)},
 {"name":"grid","from":b(-2)},{"name":"helix","from":b(-1.5)},{"name":"dc2","from":b(-1)},{"name":"fold2","from":b(-0.5)},
 {"name":"burst","from":b(0),"flash":True},{"name":"pipette","from":b(1)},{"name":"rainbow","from":b(2)},{"name":"afprot","from":b(3)},
 {"name":"zoomcall","from":b(4)},{"name":"hassabis60","from":b(5)},{"name":"syringe","from":b(7)},{"name":"mosquito","from":b(8)},
 {"name":"mri","from":b(9)},{"name":"rainbow2","from":b(10)},{"name":"medal","from":b(11)}]
groups=[([0,4],"glass"),([5,7],"stack"),([8,9],"stack"),([10,12],None),([16,18],"stack"),([19,21],"italic"),([22,25],"stack"),
 ([26,27],None),([28,31],"stack"),([32,35],"stack"),([37,38],"glass"),([39,39],None),([40,42],"stack"),
 ([43,46],"stack"),([47,47],None),([48,52],"stack"),([53,54],None),([55,56],"italic"),([57,60],"stack"),([61,62],"stack"),
 ([63,65],None),([66,66],None),([67,69],"stack"),([70,73],None),
 ([74,74],"italic"),([75,77],"stack"),([78,78],None),([79,82],"stack"),
 ([83,86],"stack"),([87,89],None),([90,92],"glass"),([93,95],"stack"),([96,97],"italic")]
C=[]
for r,k in groups:
    c={"w":r}
    if k=="stack": c["layout"]="stack"
    if k=="italic": c["italic"]=True
    if k=="glass": c["glass"]=True
    C.append(c)
edit={"frame":"card","end":round(b(14),2),"voFrom":0,
 "music":[{"src":"shared/music/savior.mp3","start":m["musicStart"],"at":0,"volume":0.32}],
 "headline":{"text":"one protein used to cost a scientist five *years*","to":b(-29)},
 "shots":shots,"captions":C}
json.dump(edit,open('edit.json','w'),indent=1)
print("sync src: lec_hook",src_at(0),"lec_a",src_at(b(-16)),"hassabis60",src_at(b(5)),"end",edit["end"])
print(' '.join(f"{s['name']}@{s['from']}" for s in shots))
