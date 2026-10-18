# Voice + caption timing for p11-jensen. Splices jensen.mp4 (SIEPR 2024, from 35:50) into vo.wav, writes srcmap.json and words.json.
# One continuous take: high expectations, low resilience, greatness comes from character, formed out of people who
# "suffered" (lands on HUMBLE YOURSELF's drop), payoff: "I wish upon you ample doses of pain and suffering".
import csv, json, os, subprocess, numpy as np
DROP_TRACK=49.63
segs=[(25.84,28.98,0.30),   # One of my great advantages is that I have very low expectations.
      (37.82,42.85,0.30),   # Most of the Stanford graduates have very high expectations.
      (69.90,73.20,0.30),   # People with very high expectations have very low resilience.
      (77.95,81.66,0.35),   # And unfortunately resilience matters in success.
      (128.82,130.14,0.20), # And greatness is not intelligence.
      (131.36,132.97,0.04), # Greatness comes from character, and character
      (133.84,135.50,0.12), # isn't formed out of smart people.
      (135.52,136.76,0.35), # It's formed out of people who
      (136.76,137.30,0.40), # suffered.
      (145.78,149.46,0.12), # For all of you Stanford students, I wish upon you
      (150.16,151.95,0)]    # ample doses of pain and suffering.
CLIMAX=8
# climax onset from the waveform: first 10 ms frame above 15% of the word's peak
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','raw/jensen.mp4','-vn','-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout,np.int16).astype(float)
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
subprocess.run(['ffmpeg','-v','error','-y','-i','raw/jensen.mp4','-filter_complex',f,'-map','[o]','-ar','48000','vo.wav'],check=True)
# captions: the single whisper pass over this clip drifts by up to 2 s (long pauses, applause), so each segment's
# source window is transcribed once on its own (source times, not the spliced voice) and mapped through the splices
def seg_words(a,b):
    o=f'raw/seg{a:.2f}'
    if not os.path.exists(o+'.csv'):
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i','raw/jensen.mp4','-vn','-ar','16000','-ac','1',o+'.wav'],check=True)
        subprocess.run(['whisper-cli','-m','../../../tools/models/ggml-base.en.bin','-f',o+'.wav','-ml','1','-sow','-ocsv','-of',o,'-np'],check=True,capture_output=True)
    return [(int(r['start'])/1000, r['text'].strip()) for r in csv.DictReader(open(o+'.csv')) if r['text'].strip()]
out=[]
for s,(a,b,_) in zip(mp,segs):
    for tt,w in seg_words(a,b):
        if tt<s["dur"]-0.05: out.append({"w":w,"s":round(s["reel"]+tt,3)})
# whisper mishears: "isn't formed" as "is informed", "it's" as "was"
FIX={"informed":"formed","who...":"who","intelligent.":"intelligence.","was":"it's","saw":None,"it.":None}
for i,x in enumerate(out):
    if x["w"]=="is" and i+1<len(out) and out[i+1]["w"]=="informed": x["w"]="isn't"
out=[dict(x,w=FIX.get(x["w"],x["w"])) for x in out if FIX.get(x["w"],1) is not None]
for i,x in enumerate(out): x["e"]=min(out[i+1]["s"],x["s"]+0.5) if i+1<len(out) else x["s"]+0.5
out[0]["s"]=0.0  # the first word is on screen from frame 1
json.dump(out,open('words.json','w'),indent=0)
print("onset",round(ONSET,3),"drop at",round(drop,3),"track starts at",musicStart,"vo ends",round(t,2))
print(' '.join(f"{i}:{x['w']}@{x['s']:.2f}" for i,x in enumerate(out)))
