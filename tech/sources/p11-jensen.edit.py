# Writes edit.json for p11-jensen from srcmap.json (voice timing) on HUMBLE YOURSELF's beat grid (154.8 bpm, cut on
# 2-beat units), and prints the source times the lip-synced Jensen shots must start at (p11-jensen.sh uses them).
import json
m=json.load(open('srcmap.json')); S=m["segments"]
D=m["drop"]; B=60/154.84
b=lambda n: round(D+n*B,3)
def src_at(reel):  # source time under the voice at a reel time
    s=max((x for x in S if x["reel"]<=reel), key=lambda x:x["reel"]); return round(s["src"]+reel-s["reel"],3)
shots=[
 # hook: Jensen's face on frame 1 under the headline
 {"name":"jensen_hook","from":0,"zoom":1.25,"origin":"50% 33%"},
 # build-up: slow (4 beats), cold, muted; back to Jensen once
 {"name":"dawn","from":b(-56)},{"name":"stadium","from":S[1]["reel"]},{"name":"seated","from":b(-44)},{"name":"cheer","from":b(-40)},
 {"name":"jensen_a","from":S[2]["reel"]},{"name":"canvas","from":b(-32)},{"name":"ropes","from":S[3]["reel"]},{"name":"standup","from":b(-24)},
 {"name":"arena","from":b(-20)},{"name":"chalk","from":S[4]["reel"]},{"name":"pushup","from":S[5]["reel"]},{"name":"hall","from":S[6]["reel"]},
 # riser: 1 beat cuts into the drop
 {"name":"meat","from":b(-4)},{"name":"grimace","from":b(-3)},{"name":"situp","from":b(-2)},{"name":"steps","from":b(-1)},
 # drop and payoff: 2 beat cuts, vivid
 {"name":"punch","from":b(0),"flash":True},{"name":"down","from":b(1)},{"name":"whale","from":S[9]["reel"]},{"name":"signs","from":b(4)},{"name":"crowd","from":b(6)},
 {"name":"lei","from":b(8)},{"name":"jensen_c","from":b(10)},{"name":"battered","from":b(12)},{"name":"arms","from":b(14)},
 {"name":"walkout","from":b(16)},{"name":"jensen_end","from":b(17)}]
groups=[([0,2],"glass"),([3,4],"stack"),([5,6],None),([7,8],None),([9,11],"stack"),([12,14],None),([15,16],"stack"),([17,19],None),
 ([20,20],"glass"),([21,22],"stack"),([23,25],"stack"),([26,28],None),([29,29],"glass"),([30,31],"stack"),([32,33],"stack"),
 ([34,35],"stack"),([36,37],"stack"),([38,40],"stack"),([41,42],"stack"),([43,44],"stack"),([45,46],"stack"),([47,48],None),
 ([49,52],"stack"),([53,54],None),([55,58],"stack"),([59,59],"italic"),([60,61],None),([62,63],None),([64,65],"stack"),
 ([66,67],None),([68,69],"italic"),([70,71],"stack"),([72,73],"stack"),([74,75],"glass")]
C=[]
for r,k in groups:
    c={"w":r}
    if k=="stack": c["layout"]="stack"
    if k=="italic": c["italic"]=True
    if k=="glass": c["glass"]=True
    C.append(c)
edit={"frame":"card","end":round(b(20),2),"voFrom":0,
 "music":[{"src":"shared/music/humble-yourself.mp3","start":m["musicStart"],"at":0,"volume":0.32}],
 "headline":{"text":"nvidia's ceo wished stanford students a *curse*","to":b(-52)},
 "shots":shots,"captions":C}
json.dump(edit,open('edit.json','w'),indent=1)
print("sync src: jensen_hook",src_at(0),"jensen_a",src_at(S[2]["reel"]),"jensen_c",src_at(b(10)),"end",edit["end"])
print("shot lengths:",' '.join(f"{s['name']}:{(shots[i+1]['from'] if i+1<len(shots) else edit['end'])-s['from']:.2f}" for i,s in enumerate(shots)))
