import json
m=json.load(open('srcmap.json')); S=m["segments"]
D=m["drop"]; B=60/75.0
b=lambda n: round(D+n*B,3)
def src_at(reel):  # source time under the voice at a reel time
    s=max((x for x in S if x["reel"]<=reel), key=lambda x:x["reel"]); return round(s["src"]+reel-s["reel"],3)
shots=[
 {"name":"clarke_hook","from":0,"zoom":1.6,"origin":"50% 30%"},
 {"name":"sat","from":b(-34)},{"name":"operators","from":b(-31)},{"name":"tahiti","from":b(-28)},{"name":"bus","from":b(-25)},
 {"name":"clarke_a","from":b(-22)},{"name":"surgeons","from":b(-19)},{"name":"edinburgh","from":b(-16)},{"name":"masks","from":b(-14)},{"name":"theatre","from":b(-12)},
 {"name":"beams","from":b(-10)},{"name":"earth","from":b(-8)},
 {"name":"bridge","from":b(-5)},{"name":"tube","from":b(-4)},{"name":"crowd","from":b(-3)},{"name":"waterloo","from":b(-2)},
 {"name":"train","from":b(-1.5)},{"name":"faces","from":b(-1)},{"name":"bridge2","from":b(-0.5)},
 {"name":"fibre","from":b(0),"flash":True},{"name":"call","from":b(1)},{"name":"phone","from":b(2)},{"name":"clarke_b","from":b(3)},
 {"name":"plane","from":b(4)},{"name":"bali","from":b(5)},{"name":"waves","from":b(6)},{"name":"bali2","from":b(7)},
 {"name":"clarke_end","from":b(8)}]
groups=[([0,3],"glass"),([4,6],None),([7,8],"stack"),([9,10],"stack"),([11,12],None),([13,15],"stack"),([16,17],"stack"),
 ([18,19],"stack"),([20,21],"stack"),([22,23],"stack"),([24,26],None),([27,29],"stack"),([30,30],None),([31,31],"glass"),
 ([32,35],"stack"),([36,38],None),([39,41],"stack"),([42,44],None),([45,46],"stack"),([47,48],"stack"),([49,49],None),
 ([50,51],"stack"),([52,54],"stack"),([55,57],"stack"),([58,58],None),([59,61],"stack"),([62,64],"italic"),([65,67],"stack"),
 ([68,69],None),([70,71],"stack"),([72,73],"stack"),([74,74],"glass"),([75,76],None),([77,77],"italic"),
 ([78,80],None),([81,82],"stack"),([83,85],"stack"),([86,87],"stack"),([88,88],None),([89,90],"glass")]
C=[]
for r,k in groups:
    c={"w":r}
    if k=="stack": c["layout"]="stack"
    if k=="italic": c["italic"]=True
    if k=="glass": c["glass"]=True
    C.append(c)
edit={"frame":"card","end":round(b(10),2),"voFrom":0,
 "music":[{"src":"shared/music/utopia.mp3","start":m["musicStart"],"at":0,"volume":0.32}],
 "headline":{"text":"in 1964 arthur c clarke described how you'd *work*","to":b(-33)},
 "shots":shots,"captions":C}
json.dump(edit,open('edit.json','w'),indent=1)
print("sync src: clarke_hook",src_at(0),"clarke_a",src_at(b(-22)),"clarke_b",src_at(b(3)),"end",edit["end"])
