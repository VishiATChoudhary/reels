# Voice + caption timing for p03-feynman. Splices feynman.mp4 into vo.wav, writes srcmap.json and words.json.
# One continuous take: the voice starts on frame 1, the track starts wherever puts BEFORE's drop on "better".
import csv, json, subprocess
import numpy as np
DROP_TRACK=29.11
segs=[(95.70,100.93,0.30),   # We could try to make a machine that runs like a cheetah, but it's easier to make a machine with wheels.
      (108.05,112.34,0.35),  # The airplanes don't fly like a bird. They fly, but they don't fly like a bird.
      (134.00,138.64,0.40),  # So there's no question that the later machines are not going to think like people think.
      (146.82,150.69,0.35),  # For example, they're not going to do arithmetic the same way as we do arithmetic, but they'll do it
      (150.69,151.10,0.40),  # better.
      (155.05,159.78,0.40),  # They do arithmetic better than anybody, much faster and differently.
      (246.30,252.26,0)]     # So there are some things that a computer does much better than a human, and you'd better remember that if you kind of compare machines to humans.
CLIMAX=4
def pcm(a,b,sr=16000):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-ss',str(a),'-to',str(b),'-i','raw/feynman.mp4','-vn','-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout,np.int16).astype(float)
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
subprocess.run(['ffmpeg','-v','error','-y','-i','raw/feynman.mp4','-filter_complex',f,'-map','[o]','-ar','48000','vo.wav'],check=True)
# captions: whisper on each source segment alone (the long single pass drifts up to 0.7 s around the airplane
# line in this 1985 tape), source times mapped through the splices
out=[]
for i,(s,(a,b,g)) in enumerate(zip(mp,segs)):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i','raw/feynman.mp4','-vn','-ar','16000','-ac','1',f'raw/seg{i}.wav'],check=True)
    subprocess.run(['whisper-cli','-m','../../../tools/models/ggml-base.en.bin','-f',f'raw/seg{i}.wav','-ml','1','-sow','-ocsv','-of',f'raw/seg{i}','-np'],check=True,capture_output=True)
    for row in csv.DictReader(open(f'raw/seg{i}.csv')):
        w=row['text'].strip()
        if w and not w.startswith('['): out.append({"w":w,"s":round(s["reel"]+int(row['start'])/1000,3)})
# whisper hears "they do arithmetic" as "they do it with the thick"
for i in range(len(out)-3):
    if [x["w"] for x in out[i:i+4]]==["it","with","the","thick"]:
        out[i:i+4]=[{"w":"arithmetic","s":out[i]["s"]}]
        # and places "better than anybody" late: on the waveform they run 155.69 to 156.88, "much" at 157.51
        for k,src_t in zip((1,2,3),(155.69,155.96,156.20)): out[i+k]["s"]=round(mp[5]["reel"]+src_t-segs[5][0],3)
        break
for i,x in enumerate(out): x["e"]=min(out[i+1]["s"],x["s"]+0.5) if i+1<len(out) else x["s"]+0.5
out[0]["s"]=0.0  # the first word is on screen from frame 1
for x in out:
    if x["w"].lower().startswith("better") and abs(x["s"]-drop)<0.5: x["s"]=round(drop,3)
json.dump(out,open('words.json','w'),indent=0)
print("climax onset src",onset,"drop at",round(drop,3),"track starts at",musicStart,"vo ends",round(t,2))
print(' '.join(f"{i}:{x['w']}@{x['s']:.2f}" for i,x in enumerate(out)))
