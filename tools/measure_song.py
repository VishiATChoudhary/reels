# measure_song.py <song.mp3> [--from S] [--to S]
# Prints BPM and drop candidates. The drop = where the low end (kick + 808, < 150 Hz) comes in and stays:
# biggest jump of bass level, 3 s after vs 3 s before, snapped to the nearest bass onset.
# Always sanity-check the top candidate on the printed level curve.
import subprocess, sys, numpy as np
f=sys.argv[1]; a=dict(zip(sys.argv[2::2], sys.argv[3::2]))
lo=float(a.get('--from',4)); hi=float(a.get('--to',70))
sr=4000; hop=40  # 10 ms
def pcm(filt):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-t',str(hi+5),'-af',filt,'-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout,np.int16).astype(float)
def env(x): return 20*np.log10(np.array([np.sqrt((x[i:i+hop*3]**2).mean()+1e-9) for i in range(0,len(x)-hop*3,hop)])+1e-9)
bass=env(pcm('lowpass=f=150,lowpass=f=150')); full=env(pcm('anull'))
flux=np.maximum(0,np.diff(full,prepend=full[0]))
w=300
cand=[]
for i in range(max(w,int(lo*100)),min(int(hi*100),len(bass)-w)):
    cand.append((bass[i:i+w].mean()-bass[i-w:i].mean(),i))
cand.sort(reverse=True); picked=[]
for j,i in cand:
    if all(abs(i-p)>400 for _,p in picked): picked.append((j,i))
    if len(picked)==4: break
bflux=np.maximum(0,np.diff(bass,prepend=bass[0]))
# BPM from the kick pattern after the strongest drop: autocorrelation summed over 1..8 beats (fine resolution)
d0=picked[0][1]; seg=(bflux+flux)[d0:d0+2000]; seg=seg-seg.mean()
ac=np.correlate(seg,seg,'full')[len(seg)-1:]
def score(bpm):
    lag=6000/bpm; v=0
    for k in range(1,9):
        L=k*lag; i=int(L); fr=L-i
        if i+1<len(ac): v+=ac[i]*(1-fr)+ac[i+1]*fr
    return v
bpm=max(np.arange(70,170,0.01),key=score)
print(f"bpm ~ {bpm:.2f}  (beat {60/bpm:.4f} s)  [check: half/double tempo is possible]")
for j,i in picked:
    k=i-40+int(np.argmax(bflux[i-40:i+40]))
    print(f"drop? {k/100:6.2f} s   bass jump {j:+.1f} dB")
print("bass level per 2 s:", ' '.join(f"{t}:{bass[t*100:(t+2)*100].mean():.0f}" for t in range(0,int(min(hi,len(bass)/100))-1,2)))
