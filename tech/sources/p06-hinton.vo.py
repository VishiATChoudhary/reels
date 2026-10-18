import csv, json, subprocess
DROP_TRACK=42.67; CLIMAX_SRC=708.10  # measured onset of "take" (waveform)
segs=[(54.55,63.25,0.30),   # I think we're moving into a period when, for the first time ever, we may have things more intelligent than us.
      (687.70,691.30,0.30),  # I don't know. I can't see a path that guarantees safety.
      (698.86,704.62,0.35),  # And normally the first time you deal with something totally novel, you get it wrong. And we can't afford to get it wrong with these things.
      (707.46,708.52,0.40),  # because they might | take over.
      (778.28,785.95,0)]     # These things do understand, and because they understand, we need to think harder about what's going to happen next, and we just don't know.
t=0; mp=[]
for a,b,g in segs:
    mp.append({"reel":round(t,3),"src":a,"dur":round(b-a,3)}); t+=b-a+g
drop=mp[3]["reel"]+(CLIMAX_SRC-segs[3][0])
musicStart=round(DROP_TRACK-drop,3)  # s into the track at frame 1
assert musicStart>=0, "story is longer than the build-up"
json.dump({"drop":round(drop,3),"musicStart":musicStart,"segments":mp},open('srcmap.json','w'),indent=1)
f=';'.join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,areverse,afade=t=in:d=0.05,areverse,apad=pad_dur={g}[p{i}]" for i,(a,b,g) in enumerate(segs))
f+=';'+''.join(f'[p{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,aformat=channel_layouts=stereo,aresample=48000,highpass=f=80,loudnorm=I=-15:TP=-1.5[o]'
subprocess.run(['ffmpeg','-v','error','-y','-i','raw/hinton.mp4','-filter_complex',f,'-map','[o]','-ar','48000','vo.wav'],check=True)
# word times: one whisper pass per source segment (a single long pass drifts by up to 0.5 s)
out=[]
for i,(s,(a,b,g)) in enumerate(zip(mp,segs)):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i','raw/hinton.mp4','-vn','-ar','16000','-ac','1',f'raw/seg{i}.wav'],check=True)
    subprocess.run(['whisper-cli','-m','../../../tools/models/ggml-base.en.bin','-f',f'raw/seg{i}.wav','-ml','1','-sow','-ocsv','-of',f'raw/seg{i}','-np'],check=True,capture_output=True)
    for r in csv.DictReader(open(f'raw/seg{i}.csv')):
        w=r['text'].strip()
        t0=round(s["reel"]+int(r['start'])/1000,3)
        if w=="gonna": out+=[{"w":"going","s":t0},{"w":"to","s":round(t0+0.1,3)}]  # he says "going to"
        elif w: out.append({"w":w,"s":t0})
for i,x in enumerate(out): x["e"]=min(out[i+1]["s"],x["s"]+0.5) if i+1<len(out) else x["s"]+0.5
out[0]["s"]=0.0  # the first word is on screen from frame 1
for x in out:
    if x["w"].lower().startswith("take"): x["s"]=round(drop,3)
json.dump(out,open('words.json','w'),indent=0)
print("drop at",round(drop,3),"track starts at",musicStart,"vo ends",round(t,2))
print(' '.join(f"{i}:{x['w']}@{x['s']:.2f}" for i,x in enumerate(out)))
