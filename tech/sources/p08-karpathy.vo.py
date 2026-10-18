import csv, json, re, subprocess
DROP_TRACK=37.40; ENG_SRC=208.84  # mercy drop; measured onset of "English" (waveform)
# raw/karpathy = "Software Is Changing (Again)", YC AI Startup School, June 2025, first 12 min
segs=[(59.38,67.48,0.35),   # Software has not changed much on such a fundamental level for 70 years. And then it's changed, I think, about twice, quite rapidly in the last few years.
      (103.40,105.75,0.12), # software 1.0 is the code you write for the computer,
      (105.95,108.25,0.35), # software 2.0 are basically neural networks.
      (186.41,190.10,0.30), # neural networks became programmable with large language models.
      (197.40,200.55,0.35), # it's worth giving it a new designation of software 3.0.
      (200.85,208.62,0.25), # And basically your prompts are now programs that program the LLM. And remarkably, these prompts are written in
      (208.78,212.60,0.35), # English. So it's kind of a very interesting programming language.
      (264.45,266.95,0)]    # Remarkably, we're now programming computers in English.
t=0; mp=[]
for a,b,g in segs:
    mp.append({"reel":round(t,3),"src":a,"dur":round(b-a,3)}); t+=b-a+g
drop=mp[6]["reel"]+(ENG_SRC-segs[6][0])
musicStart=round(DROP_TRACK-drop,3)  # s into the track at frame 1
assert musicStart>=0, "story is longer than the build-up"
json.dump({"drop":round(drop,3),"musicStart":musicStart,"segments":mp},open('srcmap.json','w'),indent=1)
f=';'.join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,areverse,afade=t=in:d=0.05,areverse,apad=pad_dur={g}[p{i}]" for i,(a,b,g) in enumerate(segs))
f+=';'+''.join(f'[p{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,aformat=channel_layouts=stereo,aresample=48000,highpass=f=80,loudnorm=I=-15:TP=-1.5[o]'
subprocess.run(['ffmpeg','-v','error','-y','-i','raw/karpathy.mp4','-filter_complex',f,'-map','[o]','-ar','48000','vo.wav'],check=True)
# the gaps pull single-pass loudnorm low: measure and lift it (lands ~-15 after the limiter)
I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',subprocess.run(['ffmpeg','-i','vo.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr)[-1])
subprocess.run(['ffmpeg','-v','error','-y','-i','vo.wav','-af',f'volume={-16.3-I:.2f}dB,alimiter=limit=0.85','-ar','48000','raw/vo_lift.wav'],check=True)
subprocess.run(['mv','raw/vo_lift.wav','vo.wav'],check=True)
# captions: one whisper pass per source piece (the long pass drifts on this talk), mapped to the reel
out=[]
for i,(a,b,g) in enumerate(segs):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i','raw/karpathy.mp4','-vn','-ar','16000','-ac','1',f'raw/seg{i}.wav'],check=True)
    subprocess.run(['whisper-cli','-m','../../../tools/models/ggml-base.en.bin','-f',f'raw/seg{i}.wav','-ml','1','-sow','-ocsv','-of',f'raw/seg{i}','-np'],check=True,capture_output=True)
    for r in csv.DictReader(open(f'raw/seg{i}.csv')):
        w=r['text'].strip()
        if w and not w.startswith(('[','(')): out.append({"w":w,"s":round(mp[i]["reel"]+int(r['start'])/1000,3)})
# whisper base slips on a few words: fix by index (times kept); "in" belongs to the line before the splice
FIX={52:"models.",93:"now",97:"English."}
for i,w in FIX.items(): out[i]["w"]=w
out[80]["s"]=round(mp[5]["reel"]+208.47-segs[5][0],3)
del out[49]  # "a" (he says "with large language models")
for x in out:
    if x["w"].lower().startswith("english") and x["s"]<drop+1: x["s"]=round(drop,3)
out.sort(key=lambda x:x["s"])
for i,x in enumerate(out): x["e"]=min(out[i+1]["s"],x["s"]+0.5) if i+1<len(out) else x["s"]+0.5
out[0]["s"]=0.0  # the first word is on screen from frame 1
json.dump(out,open('words.json','w'),indent=0)
print("drop at",round(drop,3),"track starts at",musicStart,"vo ends",round(t,2))
print(' '.join(f"{i}:{x['w']}@{x['s']:.2f}" for i,x in enumerate(out)))
