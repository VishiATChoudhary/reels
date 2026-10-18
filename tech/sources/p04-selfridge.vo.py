# Voice + caption timing for p04-selfridge. Splices tm.mp4 (The Thinking Machine, 1961) into vo.wav, writes
# srcmap.json and words.json. One continuous take: the voice starts on frame 1, the track starts wherever puts
# MEDUSA's second drop (40.42 s, after the breakdown) on "think".
import csv, json, subprocess
import numpy as np
DROP_TRACK=40.42
segs=[(92.74,94.75,0.30),   # I don't mean the machines will behave like men.
      (95.84,100.20,0.30),  # I don't think for a very long time we're going to have a difficult problem distinguishing a man from a robot.
      (101.12,103.22,0.35), # And I don't think my daughter will ever marry a computer.
      (104.45,105.74,0.12), # But I think the computers will
      (106.40,108.65,0.35), # be doing the things that men do when we say they're thinking.
      (109.15,110.86,0.35), # I'm convinced that machines can and will
      (110.86,112.18,0.40), # think in our lifetime.
      (112.93,121.73,0)]    # Shannon: I confidently expect that within a matter of 10 or 15 years, something will emerge from the
                            # laboratories, which is not too far from the robot of science fiction fame.
CLIMAX=6
# caption passes: whisper hears short clips badly, so it runs on contiguous source windows
WIN=[(92.74,94.75),(95.84,100.20),(101.12,103.22),(104.45,108.65),(109.15,112.18),(112.93,121.73)]
def pcm(a,b,sr=16000):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-ss',str(a),'-to',str(b),'-i','raw/tm.mp4','-vn','-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout,np.int16).astype(float)
# climax onset from the waveform: first 10 ms frame above 15% of the word's peak
x=pcm(*segs[CLIMAX][:2]); r=np.array([np.sqrt((x[i:i+160]**2).mean()) for i in range(0,len(x)-160,160)])
onset=segs[CLIMAX][0]+int(np.argmax(r>0.15*r.max()))/100
t=0; mp=[]
for a,b,g in segs:
    mp.append({"reel":round(t,3),"src":a,"dur":round(b-a,3)}); t+=b-a+g
drop=mp[CLIMAX]["reel"]+(onset-segs[CLIMAX][0])
musicStart=round(DROP_TRACK-drop,3)  # s into the track at frame 1
assert musicStart>=0, "story is longer than the build-up"
json.dump({"drop":round(drop,3),"musicStart":musicStart,"segments":mp},open('srcmap.json','w'),indent=1)
f=';'.join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,areverse,afade=t=in:d=0.05,areverse,apad=pad_dur={g}[p{i}]" for i,(a,b,g) in enumerate(segs))
f+=';'+''.join(f'[p{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,aformat=channel_layouts=stereo,aresample=48000,highpass=f=80,loudnorm=I=-15:TP=-1.5[o]'
subprocess.run(['ffmpeg','-v','error','-y','-i','raw/tm.mp4','-filter_complex',f,'-map','[o]','-ar','48000','vo.wav'],check=True)
out=[]
for i,(a,b) in enumerate(WIN):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i','raw/tm.mp4','-vn','-ar','16000','-ac','1',f'raw/win{i}.wav'],check=True)
    subprocess.run(['whisper-cli','-m','../../../tools/models/ggml-base.en.bin','-f',f'raw/win{i}.wav','-ml','1','-sow','-ocsv','-of',f'raw/win{i}','-np'],check=True,capture_output=True)
    for row in csv.DictReader(open(f'raw/win{i}.csv')):
        w=row['text'].strip(); st=a+int(row['start'])/1000
        if not w or w.startswith('['): continue
        s=max((x for x in mp if x["src"]-0.06<=st), key=lambda x:x["src"])
        out.append({"w":w,"s":round(s["reel"]+max(0,min(st-s["src"],s["dur"]-0.05)),3)})
for x in out:
    if x["w"]=="their": x["w"]="they're"
for i,x in enumerate(out): x["e"]=min(out[i+1]["s"],x["s"]+0.5) if i+1<len(out) else x["s"]+0.5
out[0]["s"]=0.0  # the first word is on screen from frame 1
for x in out:
    if x["w"].lower().startswith("think") and abs(x["s"]-drop)<0.5: x["s"]=round(drop,3)
json.dump(out,open('words.json','w'),indent=0)
print("climax onset src",onset,"drop at",round(drop,3),"track starts at",musicStart,"vo ends",round(t,2))
print(' '.join(f"{i}:{x['w']}@{x['s']:.2f}" for i,x in enumerate(out)))
