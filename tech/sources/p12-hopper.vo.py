# Voice + caption timing for p12-hopper. Splices hopper.mp4 (NSA lecture, 1982, from 23:30) into vo.wav, writes srcmap.json and words.json.
# One continuous take: "we've always done it that way" is the saddest phrase, a clock that runs counterclockwise, by the
# third day they recognize there was "never" (lands on FOR YOU's drop) any reason; payoff: she will haunt you for 24 hours.
import csv, json, os, subprocess, numpy as np
DROP_TRACK=19.72
segs=[(11.45,14.45,0.04),   # I think the saddest phrase I ever hear
      (15.62,19.66,0.30),   # is that horrible one: but we've always done it that way.
      (23.55,28.00,0.30),   # To emphasize the fact, I keep a clock which operates entirely counterclockwise.
      (29.15,31.86,0.25),   # Now the first day people meet it, they can't tell time.
      (36.88,40.57,0.35),   # Normally it's not till the third day that they recognize that there was
      (40.58,42.68,0.40),   # never any reason why clocks should run clockwise.
      (92.60,95.36,0.40),   # And it's the most dangerous phrase you can use.
      (104.75,115.20,0)]    # If during the next 12 months any one of you says "but we've always done it that way", I will instantly materialize beside you and I will haunt you for 24 hours.
CLIMAX=5
# climax onset from the waveform: first 10 ms frame above 15% of the word's peak
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','raw/hopper.mp4','-vn','-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout,np.int16).astype(float)
a,b,_=segs[CLIMAX]; r=np.array([np.sqrt((x[int((a+i/100)*16000):int((a+(i+1)/100)*16000)]**2).mean()) for i in range(int((b-a)*100))])
ONSET=a+np.argmax(r>0.15*r.max())/100
t=0; mp=[]
for a,b,g in segs:
    mp.append({"reel":round(t,3),"src":a,"dur":round(b-a,3)}); t+=b-a+g
drop=mp[CLIMAX]["reel"]+(ONSET-segs[CLIMAX][0])
musicStart=round(DROP_TRACK-drop,3)  # s into the track at frame 1
assert musicStart>=0, "story is longer than the build-up"
json.dump({"drop":round(drop,3),"musicStart":musicStart,"segments":mp},open('srcmap.json','w'),indent=1)
f=';'.join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,areverse,afade=t=in:d=0.05,areverse,apad=pad_dur={g}[p{i}]" for i,(a,b,g) in enumerate(segs))
f+=';'+''.join(f'[p{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,aformat=channel_layouts=stereo,aresample=48000,highpass=f=80,loudnorm=I=-15:TP=-1.5[o]'
subprocess.run(['ffmpeg','-v','error','-y','-i','raw/hopper.mp4','-filter_complex',f,'-map','[o]','-ar','48000','vo.wav'],check=True)
# captions: the single whisper pass over this clip drifts by up to 2 s (long pauses, applause), so each segment's
# source window is transcribed once on its own (source times, not the spliced voice) and mapped through the splices
def seg_words(a,b):
    o=f'raw/seg{a:.2f}'
    if not os.path.exists(o+'.csv'):
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i','raw/hopper.mp4','-vn','-ar','16000','-ac','1',o+'.wav'],check=True)
        subprocess.run(['whisper-cli','-m','../../../tools/models/ggml-base.en.bin','-f',o+'.wav','-ml','1','-sow','-ocsv','-of',o,'-np'],check=True,capture_output=True)
    return [(int(r['start'])/1000, r['text'].strip()) for r in csv.DictReader(open(o+'.csv')) if r['text'].strip()]
out=[]
for s,(a,b,_) in zip(mp,segs):
    for tt,w in seg_words(a,b):
        if tt<s["dur"]-0.05: out.append({"w":w,"s":round(s["reel"]+tt,3)})
# whisper mishears
FIX={"praise":"phrase","made":"meet","until":"till","clock.":"clockwise.","ten.":"time."}
out=[dict(x,w=FIX.get(x["w"],x["w"])) for x in out]
for i,x in enumerate(out):
    if x["w"]=="clock" and out[i-1]["w"]=="why": x["w"]="clocks"
for i,x in enumerate(out): x["e"]=min(out[i+1]["s"],x["s"]+0.5) if i+1<len(out) else x["s"]+0.5
out[0]["s"]=0.0  # the first word is on screen from frame 1
json.dump(out,open('words.json','w'),indent=0)
print("onset",round(ONSET,3),"drop at",round(drop,3),"track starts at",musicStart,"vo ends",round(t,2))
print(' '.join(f"{i}:{x['w']}@{x['s']:.2f}" for i,x in enumerate(out)))
