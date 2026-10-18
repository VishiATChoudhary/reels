import csv, json, subprocess
DROP_TRACK=41.30; EVERY_SRC=40.15  # measured onset of "everything" (waveform)
segs=[(13.35,19.15,0.12),   # When you grow up, you tend to get told that the world is the way it is.
      (20.35,25.30,0.30),   # Your life is just to live your life inside the world. Try not to bash into the walls too much.
      (32.60,35.45,0.30),   # But life, that's a very limited life.
      (35.50,40.11,0.35),   # Life can be much broader once you discover one simple fact, and that is
      (40.12,45.70,0.35),   # everything around you that you call life was made up by people that were no smarter than you.
      (46.65,52.45,0.45),   # And you can change it, you can influence it, you can build your own things that other people can use.
      (94.40,96.65,0)]      # Once you learn that, you'll never be the same again.
CLIMAX=4
t=0; mp=[]
for a,b,g in segs:
    mp.append({"reel":round(t,3),"src":a,"dur":round(b-a,3)}); t+=b-a+g
drop=mp[CLIMAX]["reel"]+(EVERY_SRC-segs[CLIMAX][0])
musicStart=round(DROP_TRACK-drop,3)  # s into the track at frame 1
assert musicStart>=0, "story is longer than the build-up"
json.dump({"drop":round(drop,3),"musicStart":musicStart,"segments":mp},open('srcmap.json','w'),indent=1)
f=';'.join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,areverse,afade=t=in:d=0.05,areverse,apad=pad_dur={g}[p{i}]" for i,(a,b,g) in enumerate(segs))
f+=';'+''.join(f'[p{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,aformat=channel_layouts=stereo,aresample=48000,highpass=f=80,loudnorm=I=-15:TP=-1.5[o]'
subprocess.run(['ffmpeg','-v','error','-y','-i','raw/jobs.mp4','-filter_complex',f,'-map','[o]','-ar','48000','vo.wav'],check=True)
# whisper each source segment on its own (word times are source times; a pass over the whole clip drifts
# by up to 1 s on the slow opening), then place them at the segment's reel time
out=[]
for i,(s_,(a,b,g)) in enumerate(zip(mp,segs)):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i','raw/jobs.mp4','-vn','-ar','16000','-ac','1',f'raw/seg{i}.wav'],check=True)
    subprocess.run(['whisper-cli','-m','../../../tools/models/ggml-base.en.bin','-f',f'raw/seg{i}.wav','-ml','1','-sow','-ocsv','-of',f'raw/seg{i}','-np'],check=True,capture_output=True)
    for r in csv.DictReader(open(f'raw/seg{i}.csv')):
        w=r['text'].strip()
        if w and not w.startswith('['): out.append({"w":w,"s":round(s_["reel"]+int(r['start'])/1000,3)})
out[0]["s"]=0.0  # the first word is on screen from frame 1
for x in out:
    if x["w"].lower().startswith("everything"): x["s"]=round(drop,3)
for i,x in enumerate(out): x["e"]=min(out[i+1]["s"],x["s"]+0.5) if i+1<len(out) else x["s"]+0.5
json.dump(out,open('words.json','w'),indent=0)
print("drop at",round(drop,3),"track starts at",musicStart,"vo ends",round(t,2))
print(' '.join(f"{i}:{x['w']}@{x['s']:.2f}" for i,x in enumerate(out)))
