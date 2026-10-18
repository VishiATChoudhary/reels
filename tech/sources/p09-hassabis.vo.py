import csv, json, subprocess
DROP_TRACK=48.01; BILLION_SRC=181.90  # measured onset of "billion" (waveform)
# (input, src start, src end, gap after); input 0 = Cambridge lecture section (raw/lecture.mp4 = 1590 s on), 1 = 60 Minutes
segs=[(0, 35.42, 46.30,0.30),   # As a rule of thumb, my biologist friends would always tell me that, you know, it takes a PhD student their entire PhD, so four, five years, to fold, to find the structure of just one protein.
      (0, 48.60, 51.30,0.30),   # and there are 200 million proteins known to science.
      (0,144.10,146.55,0.15),   # It's able to fold proteins in a matter of seconds.
      (0,147.55,154.30,0.30),   # We realized quite quickly that we could actually fold all 200 million proteins known to science.
      (0,181.20,181.86,0.35),   # It's kind of like a
      (0,181.88,185.10,0.40),   # billion years of PhD time done in one year.
      (1,665.30,669.75,0)]      # I think one day, maybe we can cure all disease with the help of AI.
CLIMAX=5
t=0; mp=[]
for k,a,b,g in segs:
    mp.append({"reel":round(t,3),"src":a,"dur":round(b-a,3),"in":k}); t+=b-a+g
drop=mp[CLIMAX]["reel"]+(BILLION_SRC-segs[CLIMAX][1])
musicStart=round(DROP_TRACK-drop,3)  # s into the track at frame 1
assert musicStart>=0, "story is longer than the build-up"
json.dump({"drop":round(drop,3),"musicStart":musicStart,"segments":mp},open('srcmap.json','w'),indent=1)
# each source is loudness-matched on its own, then the splices are joined
f=';'.join(f"[{k}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aformat=channel_layouts=stereo,aresample=48000,highpass=f=80,loudnorm=I=-15:TP=-1.5,afade=t=in:d=0.02,areverse,afade=t=in:d=0.05,areverse,apad=pad_dur={g}[p{i}]" for i,(k,a,b,g) in enumerate(segs))
f+=';'+''.join(f'[p{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,aresample=48000,loudnorm=I=-15:TP=-1.5[o]'
subprocess.run(['ffmpeg','-v','error','-y','-i','raw/lecture.mp4','-i','raw/sixty.mp4','-filter_complex',f,'-map','[o]','-ar','48000','vo.wav'],check=True)
# one whisper pass per source (lecture: raw/src16.csv from 0; 60 Minutes: raw/s60.csv from 650)
def words(csvf,off):
    return [(off+int(r['start'])/1000, r['text'].strip()) for r in csv.DictReader(open(csvf)) if r['text'].strip()]
src={0:words('raw/src16.csv',0),1:words('raw/s60.csv',650)}
out=[]
for s in mp:
    for tt,w in src[s["in"]]:
        if s["src"]-0.15 <= tt < s["src"]+s["dur"]-0.08:
            out.append({"w":w,"s":round(s["reel"]+max(0,tt-s["src"]),3)})
for i,x in enumerate(out): x["e"]=min(out[i+1]["s"],x["s"]+0.5) if i+1<len(out) else x["s"]+0.5
out[0]["s"]=0.0  # the first word is on screen from frame 1
for i,x in enumerate(out):
    if x["w"].lower().startswith("billion"):
        x["s"]=round(drop,3)
        if out[i-1]["w"]=="a": out[i-1]["s"]=round(mp[CLIMAX-1]["reel"]+0.55,3)  # whisper puts "a" on top of "billion"
for i,x in enumerate(out): x["e"]=min(out[i+1]["s"],x["s"]+0.5) if i+1<len(out) else x["s"]+0.5
json.dump(out,open('words.json','w'),indent=0)
print("drop at",round(drop,3),"track starts at",musicStart,"vo ends",round(t,2))
print(' '.join(f"{i}:{x['w']}@{x['s']:.2f}" for i,x in enumerate(out)))
