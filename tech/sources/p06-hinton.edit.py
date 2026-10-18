import json
m=json.load(open('srcmap.json')); S=m["segments"]
D=m["drop"]; B=60/135.1
b=lambda n: round(D+n*B,3)
def src_at(reel):  # source time under the voice at a reel time
    s=max((x for x in S if x["reel"]<=reel), key=lambda x:x["reel"]); return round(s["src"]+reel-s["reel"],3)
# 135 bpm: the build-up cuts on 4-beat units (~1.8 s), the payoff on 1 to 2 beats
shots=[
 {"name":"hinton_hook","from":0,"zoom":1.25,"origin":"37% 25%"},
 {"name":"nnet","from":b(-40)},{"name":"young","from":b(-36)},{"name":"chat","from":b(-32)},{"name":"robot","from":b(-28)},
 {"name":"hinton_a","from":S[1]["reel"]},{"name":"path","from":b(-19)},
 {"name":"caproni","from":b(-15)},{"name":"caproni2","from":b(-11)},{"name":"hindenburg","from":b(-8)},
 {"name":"hinton_b","from":b(-6)},{"name":"wreck","from":b(-5)},{"name":"redsrv","from":b(-4)},{"name":"h100","from":b(-3)},
 {"name":"chip","from":b(-2)},{"name":"leds","from":b(-1.5)},{"name":"nnet2","from":b(-1)},{"name":"robot2","from":b(-0.5)},
 {"name":"goal","from":b(0),"flash":True},{"name":"walker","from":b(1)},{"name":"chat2","from":b(2)},{"name":"hinton_c","from":b(4)},
 {"name":"nnet3","from":b(6)},{"name":"kick","from":b(8)},{"name":"board","from":b(10)},{"name":"redsrv2","from":b(14)},
 {"name":"hinton_end","from":b(16)}]
groups=[([0,1],"glass"),([2,4],None),([5,7],"stack"),([8,10],"stack"),([11,12],"stack"),([13,15],None),([16,18],"stack"),([19,20],"stack"),
 ([21,23],"glass"),([24,26],None),([27,28],"stack"),([29,31],"stack"),
 ([32,33],None),([34,36],"stack"),([37,39],None),([40,42],"stack"),([43,46],"italic"),([47,49],None),([50,52],"stack"),([53,54],None),
 ([55,57],"stack"),([58,60],None),([61,61],"italic"),([62,62],None),
 ([63,64],"stack"),([65,66],"stack"),([67,68],None),([69,70],"stack"),([71,73],None),([74,75],"stack"),([76,77],None),([78,80],"stack"),
 ([81,81],None),([82,84],None),([85,86],"glass")]
C=[]
for r,k in groups:
    c={"w":r}
    if k=="stack": c["layout"]="stack"
    if k=="italic": c["italic"]=True
    if k=="glass": c["glass"]=True
    C.append(c)
edit={"frame":"card","end":round(b(21),2),"voFrom":0,
 "music":[{"src":"shared/music/storms-coming.mp3","start":m["musicStart"],"at":0,"volume":0.32}],
 "headline":{"text":"the godfather of ai was asked one question he couldn't *answer*","to":b(-37)},
 "shots":shots,"captions":C}
json.dump(edit,open('edit.json','w'),indent=1)
print("sync src: hinton_hook",src_at(0),"hinton_a",src_at(S[1]["reel"]),"hinton_b",src_at(b(-6)),"hinton_c",src_at(b(4)),
      "hinton_end",src_at(b(16)),"to",src_at(edit["end"]),"end",edit["end"])
