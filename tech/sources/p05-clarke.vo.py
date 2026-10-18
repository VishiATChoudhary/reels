import csv, json, subprocess
DROP_TRACK=51.20; CLIMAX_SRC=188.05  # measured onset of "communicate" (waveform)
segs=[(136.12,146.95,0.30),  # It will be possible in that age, perhaps only 50 years from now, for a man to conduct his business from Tahiti or Bali, just as well as he could from London.
      (160.22,169.75,0.30),  # I am perfectly serious when I suggest that one day we may have brain surgeons in Edinburgh operating on patients in New Zealand.
      (171.86,175.80,0.30),  # When that time comes, the whole world will have shrunk to a point,
      (184.00,193.75,0)]     # In fact, men will no longer commute, they will | communicate, they won't have to travel for business anymore, they'll only travel for pleasure.
t=0; mp=[]
for a,b,g in segs:
    mp.append({"reel":round(t,3),"src":a,"dur":round(b-a,3)}); t+=b-a+g
drop=mp[3]["reel"]+(CLIMAX_SRC-segs[3][0])
musicStart=round(DROP_TRACK-drop,3)  # s into the track at frame 1
assert musicStart>=0, "story is longer than the build-up"
json.dump({"drop":round(drop,3),"musicStart":musicStart,"segments":mp},open('srcmap.json','w'),indent=1)
f=';'.join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,areverse,afade=t=in:d=0.05,areverse,apad=pad_dur={g}[p{i}]" for i,(a,b,g) in enumerate(segs))
f+=';'+''.join(f'[p{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,aformat=channel_layouts=stereo,aresample=48000,highpass=f=80,loudnorm=I=-15:TP=-1.5[o]'
subprocess.run(['ffmpeg','-v','error','-y','-i','raw/clarke.mp4','-filter_complex',f,'-map','[o]','-ar','48000','vo.wav'],check=True)
# word times: one whisper pass per source segment (the long single pass runs up to 0.5 s late on this film)
out=[]
for i,(s,(a,b,g)) in enumerate(zip(mp,segs)):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i','raw/clarke.mp4','-vn','-ar','16000','-ac','1',f'raw/seg{i}.wav'],check=True)
    subprocess.run(['whisper-cli','-m','../../../tools/models/ggml-base.en.bin','-f',f'raw/seg{i}.wav','-ml','1','-sow','-ocsv','-of',f'raw/seg{i}','-np'],check=True,capture_output=True)
    for r in csv.DictReader(open(f'raw/seg{i}.csv')):
        w=r['text'].strip().replace('her','for') if r['text'].strip()=='her' else r['text'].strip()
        if w: out.append({"w":w,"s":round(s["reel"]+int(r['start'])/1000,3)})
for i,x in enumerate(out): x["e"]=min(out[i+1]["s"],x["s"]+0.5) if i+1<len(out) else x["s"]+0.5
out[0]["s"]=0.0  # the first word is on screen from frame 1
for x in out:
    if x["w"].lower().startswith("communicate"): x["s"]=round(drop,3)
json.dump(out,open('words.json','w'),indent=0)
print("drop at",round(drop,3),"track starts at",musicStart,"vo ends",round(t,2))
print(' '.join(f"{i}:{x['w']}@{x['s']:.2f}" for i,x in enumerate(out)))
