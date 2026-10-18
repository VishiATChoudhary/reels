# Voice + caption timing for p02-jobs-arc. Splices jobs.mp4 into vo.wav, writes srcmap.json and words.json.
# Structure: teaser (the payoff line, flash-forward hook) > silence > story, with "blew" landing on WILD's drop.
import csv, json, subprocess
DROP_TRACK=20.40; BLEW_SRC=44.34  # measured onset of "blew" (waveform)
# one continuous take on the music: the voice starts on frame 1, the track starts wherever puts its drop on "blew"
segs=[(17.00,25.25,0.12),   # The condor used the least energy to move a kilometer, and humans came in with a rather unimpressive showing.
      (26.88,31.55,0.30),   # It was not too proud a showing for the crown of creation.
      (33.62,34.84,0.04),   # but then somebody
      (36.37,41.19,0.35),   # had the insight to test the efficiency of locomotion for a man on a bicycle.
      (44.15,50.35,0.40),   # blew the condor away, completely off the top of the charts. And that's what a computer is to me.
      (51.50,58.70,0)]      # it's the most remarkable tool that we've ever come up with. And it's the equivalent of a bicycle for our minds.
allsegs=segs
t=0; mp=[]
for a,b,g in allsegs:
    mp.append({"reel":round(t,3),"src":a,"dur":round(b-a,3)}); t+=b-a+g
drop=mp[4]["reel"]+(BLEW_SRC-segs[4][0])
musicStart=round(DROP_TRACK-drop,3)  # s into the track at frame 1
assert musicStart>=0, "story is longer than the build-up"
json.dump({"drop":round(drop,3),"musicStart":musicStart,"segments":mp},open('srcmap.json','w'),indent=1)
f=';'.join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,areverse,afade=t=in:d=0.05,areverse,apad=pad_dur={g}[p{i}]" for i,(a,b,g) in enumerate(allsegs))
f+=';'+''.join(f'[p{i}]' for i in range(len(allsegs)))+f'concat=n={len(allsegs)}:v=0:a=1,aformat=channel_layouts=stereo,aresample=48000,highpass=f=80,loudnorm=I=-15:TP=-1.5[o]'
subprocess.run(['ffmpeg','-v','error','-y','-i','raw/jobs.mp4','-filter_complex',f,'-map','[o]','-ar','48000','vo.wav'],check=True)
# captions: one whisper pass over the source clip (consistent timing), mapped through the splices
subprocess.run(['ffmpeg','-v','error','-y','-ss','16','-i','raw/jobs.mp4','-vn','-ar','16000','-ac','1','raw/src16.wav'],check=True)
subprocess.run(['whisper-cli','-m','../../../tools/models/ggml-base.en.bin','-f','raw/src16.wav','-ml','1','-sow','-ocsv','-of','raw/src16','-np'],check=True,capture_output=True)
src=[(16+int(r['start'])/1000, r['text'].strip()) for r in csv.DictReader(open('raw/src16.csv')) if r['text'].strip()]
out=[]
for s in mp:
    for tt,w in src:
        if s["src"]-0.06 <= tt < s["src"]+s["dur"]-0.08 and w!="about":
            out.append({"w":w,"s":round(s["reel"]+max(0,tt-s["src"]),3)})
for i,x in enumerate(out): x["e"]=min(out[i+1]["s"],x["s"]+0.5) if i+1<len(out) else x["s"]+0.5
out[0]["s"]=0.0  # the first word is on screen from frame 1
for x in out:
    if x["w"].lower().startswith("blew"): x["s"]=round(drop,3)
json.dump(out,open('words.json','w'),indent=0)
print("drop at",round(drop,3),"track starts at",musicStart,"vo ends",round(t,2))
print(' '.join(f"{i}:{x['w']}@{x['s']:.2f}" for i,x in enumerate(out)))
