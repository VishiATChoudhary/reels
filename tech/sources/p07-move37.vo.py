import csv, json, subprocess
DROP_TRACK=41.74; BEAU_SRC=289.35  # strike-me-down drop; measured onset of "beautiful" (waveform, doc2)
# raw/move37 = the live English broadcast (Redmond, Garlock); raw/doc = AlphaGo (2017) from 48:00; raw/doc2 = from 1:22:00
segs=[("move37",43.45,45.55,0.25),  # That's a very surprising move.
      ("move37",46.45,49.45,0.35),  # I thought it was a mistake.
      ("doc",120.70,124.65,0.25),   # Fan Hui: When I see this move, for me, it's just a big shock. What?
      ("doc",125.90,129.45,0.40),   # Normally, human, we never play this one, because it's bad.
      ("doc",294.45,298.05,0.25),   # The more I see this move, I feel something changed.
      ("doc",300.00,304.75,0.35),   # Maybe for human we think it's bad, but for AlphaGo, why not?
      ("doc2",282.60,286.35,0.35),  # Maybe he just can show humans something we never discovered.
      ("doc2",288.25,289.95,0.30),  # Maybe it's beautiful.
      ("doc",318.95,320.35,0.30),   # This move is very special.
      ("doc",322.55,329.20,0)]      # All the stones played before work together. It's connect, like a network, link everywhere.
files=sorted({s[0] for s in segs})
t=0; mp=[]
for f,a,b,g in segs:
    mp.append({"reel":round(t,3),"file":f,"src":a,"dur":round(b-a,3)}); t+=b-a+g
drop=mp[7]["reel"]+(BEAU_SRC-segs[7][1])
musicStart=round(DROP_TRACK-drop,3)  # s into the track at frame 1
assert musicStart>=0, "story is longer than the build-up"
json.dump({"drop":round(drop,3),"musicStart":musicStart,"segments":mp},open('srcmap.json','w'),indent=1)
fc=';'.join(f"[{files.index(f)}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.02,areverse,afade=t=in:d=0.05,areverse,apad=pad_dur={g}[p{i}]" for i,(f,a,b,g) in enumerate(segs))
fc+=';'+''.join(f'[p{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,aformat=channel_layouts=stereo,aresample=48000,highpass=f=80,loudnorm=I=-15:TP=-1.5[o]'
inp=sum((['-i',f'raw/{f}.mp4'] for f in files),[])
subprocess.run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc,'-map','[o]','-ar','48000','vo.wav'],check=True)
# the gaps pull single-pass loudnorm low (-17): measure and lift it (lands ~-15 after the limiter) under a limiter
import re
I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',subprocess.run(['ffmpeg','-i','vo.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr)[-1])
subprocess.run(['ffmpeg','-v','error','-y','-i','vo.wav','-af',f'volume={-16.3-I:.2f}dB,alimiter=limit=0.85','-ar','48000','raw/vo_lift.wav'],check=True)
subprocess.run(['mv','raw/vo_lift.wav','vo.wav'],check=True)
# captions: one whisper pass per source piece (the long pass drifts by a second on this film), mapped to the reel
out=[]
for i,(f,a,b,g) in enumerate(segs):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',f'raw/{f}.mp4','-vn','-ar','16000','-ac','1',f'raw/seg{i}.wav'],check=True)
    subprocess.run(['whisper-cli','-m','../../../tools/models/ggml-base.en.bin','-f',f'raw/seg{i}.wav','-ml','1','-sow','-ocsv','-of',f'raw/seg{i}','-np'],check=True,capture_output=True)
    for r in csv.DictReader(open(f'raw/seg{i}.csv')):
        w=r['text'].strip()
        if w and not w.startswith(('[','(')): out.append({"w":w,"s":round(mp[i]["reel"]+int(r['start'])/1000,3)})
# whisper base mishears Fan Hui's English: fix those words by index (times kept), drop the misheard filler,
# add the two it misses ("move." merges into "surprising", "What?" is lost)
FIX={3:"surprising",26:"normally,",27:"human,",28:"we",45:"changed.",50:"think",55:"alphago,",76:"all",78:"stones",79:"played",82:"work"}
for i,w in FIX.items(): out[i]["w"]=w
out[69]["s"]=round(mp[7]["reel"]+0.80,3)  # "it's" (waveform)
out=[x for i,x in enumerate(out) if i not in (81,86,87)]
out+=[{"w":"move.","s":round(mp[0]["reel"]+45.10-43.45,3)},{"w":"What?","s":round(mp[2]["reel"]+124.27-120.70,3)}]
for x in out:
    if x["w"].lower().startswith("beautiful"): x["s"]=round(drop,3)
out.sort(key=lambda x:x["s"])
out=out[3:]  # "that's a very" stays in the voice; the hook glass reads "surprising move" from frame 1
for i,x in enumerate(out): x["e"]=min(out[i+1]["s"],x["s"]+0.5) if i+1<len(out) else x["s"]+0.5
out[0]["s"]=0.0  # the first word is on screen from frame 1
json.dump(out,open('words.json','w'),indent=0)
print("drop at",round(drop,3),"track starts at",musicStart,"vo ends",round(t,2))
print(' '.join(f"{i}:{x['w']}@{x['s']:.2f}" for i,x in enumerate(out)))
