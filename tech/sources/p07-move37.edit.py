import json
m=json.load(open('srcmap.json')); S=m["segments"]
D=m["drop"]; B=60/92.0
b=lambda n: round(D+n*B,3)
def src_at(reel):  # source time under the voice at a reel time
    s=max((x for x in S if x["reel"]<=reel), key=lambda x:x["reel"]); return round(s["src"]+reel-s["reel"],3)
shots=[
 {"name":"hook","from":0,"zoom":1.25,"origin":"50% 45%"},
 {"name":"lee_a","from":S[1]["reel"]},{"name":"redboard","from":b(-37)},{"name":"fanhui1","from":S[2]["reel"]},
 {"name":"lee_what","from":b(-30)},{"name":"stones","from":S[3]["reel"]},{"name":"lee_bad","from":b(-24)},
 {"name":"lee_more","from":S[4]["reel"]},{"name":"fanhui_m","from":b(-18)},{"name":"room","from":b(-15)},
 {"name":"aui","from":b(-11)},{"name":"aja","from":b(-9)},{"name":"girl","from":b(-7)},
 {"name":"hand","from":b(-5)},{"name":"leeprof","from":b(-4)},{"name":"audience","from":b(-3)},{"name":"ajareach","from":b(-2)},
 {"name":"leeprof2","from":b(-1.5)},{"name":"comms","from":b(-1)},{"name":"ajabowl","from":b(-0.5)},
 {"name":"place","from":b(0),"flash":True},{"name":"vineyard","from":b(1)},{"name":"m37board","from":b(2)},
 {"name":"fanhui_i","from":b(4.5)},{"name":"hl1","from":b(7)},{"name":"hl2","from":b(9)},{"name":"net","from":b(11)},
 {"name":"hl3","from":b(13)},{"name":"fanhui_end","from":b(15)}]
# word indices as printed before the first three were dropped
groups=[([3,4],"glass"),([5,6],"stack"),([7,8],None),([9,10],"stack"),([11,13],None),([14,14],"glass"),
 ([15,16],"stack"),([17,19],None),([20,21],"stack"),([22,23],None),([24,26],"stack"),([27,27],"italic"),
 ([28,28],None),([29,30],"stack"),([31,32],"stack"),([33,34],None),([35,37],"stack"),
 ([38,39],"stack"),([40,41],None),([42,43],"stack"),([44,45],"stack"),([46,47],"italic"),
 ([48,48],None),([49,50],"stack"),([51,52],None),([53,54],"stack"),([55,57],"stack"),([58,59],"italic"),
 ([60,61],None),([62,64],"stack"),([65,65],None),([66,66],None),([67,69],"stack"),([70,71],"stack"),
 ([72,72],"italic"),([73,74],"stack"),([75,77],"stack"),([78,80],"stack"),([81,82],None),([83,84],"stack"),
 ([85,86],"stack"),([87,89],"stack"),([90,91],"glass")]
C=[]
for (a,z),k in groups:
    c={"w":[a-3,z-3]}
    if k=="stack": c["layout"]="stack"
    if k=="italic": c["italic"]=True
    if k=="glass": c["glass"]=True
    C.append(c)
edit={"frame":"card","end":round(b(17),2),"voFrom":0,
 "music":[{"src":"shared/music/strike-me-down.mp3","start":m["musicStart"],"at":0,"volume":0.32}],
 "headline":{"text":"the move every go expert called a *mistake*","to":b(-38)},
 "shots":shots,"captions":C}
json.dump(edit,open('edit.json','w'),indent=1)
print("sync src: hook",src_at(0),"redboard",src_at(b(-37)),"fanhui_i",src_at(b(4.5)),"end",edit["end"])
