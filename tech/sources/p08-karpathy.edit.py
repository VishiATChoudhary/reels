import json
m=json.load(open('srcmap.json')); S=m["segments"]
D=m["drop"]; B=60/153.9
b=lambda n: round(D+n*B,3)
def src_at(reel):  # source time under the voice at a reel time
    s=max((x for x in S if x["reel"]<=reel), key=lambda x:x["reel"]); return round(s["src"]+reel-s["reel"],3)
# 154 bpm: the build-up cuts on 4 beats (1.56 s), the riser on 2 then 1, the payoff on 2
shots=[
 {"name":"hook","from":0,"zoom":1.6,"origin":"50% 20%"},
 {"name":"reels","from":b(-68)},{"name":"kar_a","from":b(-64),"zoom":1.6,"origin":"50% 20%"},{"name":"gpus","from":b(-60)},
 {"name":"corridor","from":b(-56)},{"name":"pycode","from":S[1]["reel"]},{"name":"coder","from":b(-50)},
 {"name":"nnviz","from":S[2]["reel"]},{"name":"nnsim","from":b(-44)},{"name":"coderun","from":b(-40)},{"name":"gpus2","from":b(-36)},
 {"name":"leds","from":b(-32)},{"name":"stage","from":S[4]["reel"]},{"name":"crowd","from":b(-24)},
 {"name":"keys","from":S[5]["reel"]},{"name":"pycode2","from":b(-18)},{"name":"term","from":b(-16)},{"name":"nnsim2","from":b(-14)},
 {"name":"gpus3","from":b(-12)},{"name":"phones","from":b(-10)},{"name":"stage2","from":b(-8)},{"name":"keys2","from":b(-6)},
 {"name":"silo","from":b(-4)},{"name":"coderun2","from":b(-3)},{"name":"reels2","from":b(-2)},{"name":"cards","from":b(-1)},
 {"name":"roar","from":b(0),"flash":True},{"name":"keys3","from":b(2)},{"name":"stage3","from":b(4)},{"name":"pycode3","from":b(8)},
 {"name":"lamp","from":b(10)},{"name":"cray","from":b(12)},{"name":"kar_end","from":b(14),"zoom":1.6,"origin":"50% 20%"}]
groups=[([0,0],"glass"),([1,3],None),([4,6],"stack"),([7,9],"stack"),([10,12],"glass"),([13,14],None),([15,16],"stack"),
 ([17,18],None),([19,20],"stack"),([21,22],"italic"),([23,25],"stack"),([26,27],None),
 ([28,29],"stack"),([30,32],"stack"),([33,34],None),([35,37],"stack"),([38,39],"stack"),([40,41],None),([42,43],"stack"),
 ([44,45],None),([46,47],"stack"),([48,49],None),([50,51],"stack"),([52,53],None),([54,55],None),([56,57],"stack"),([58,59],None),
 ([60,61],"glass"),([62,63],None),([64,65],"stack"),([66,68],"stack"),([69,70],None),([71,72],"stack"),([73,74],"stack"),
 ([75,76],None),([77,79],"stack"),([80,80],"italic"),([81,83],None),([84,86],"stack"),([87,87],"italic"),([88,89],"stack"),
 ([90,90],"italic"),([91,93],"stack"),([94,94],None),([95,96],"glass")]
C=[]
for r,k in groups:
    c={"w":r}
    if k=="stack": c["layout"]="stack"
    if k=="italic": c["italic"]=True
    if k=="glass": c["glass"]=True
    C.append(c)
edit={"frame":"card","end":round(b(20),2),"voFrom":0,
 "music":[{"src":"shared/music/mercy.mp3","start":m["musicStart"],"at":0,"volume":0.32}],
 "headline":{"text":"karpathy says the hottest new programming language isn't *python*","to":b(-66)},
 "shots":shots,"captions":C}
json.dump(edit,open('edit.json','w'),indent=1)
print("sync src: hook",src_at(0),"kar_a",src_at(b(-64)),"end",edit["end"])
