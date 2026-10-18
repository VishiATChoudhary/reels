#!/usr/bin/env python3
"""reel.py: build a reel in any theme from one spec file (<theme>/episodes/<ep>.yaml). RECIPE.md has the format.

  python3 tools/reel.py new <theme> <ep>                 scaffold the spec and register the composition
  python3 tools/reel.py build <theme>/<ep> [--only S]    S = fetch | voice | edit | cuts (default: all, in order)
  python3 tools/reel.py words <theme>/<ep>               the voice transcript with reel times, to write captions
  python3 tools/reel.py check <Id>                       contact sheet, hook + drop frames, loudness of out/<Id>.mp4

The theme (themes/<theme>.json) supplies the song pool, grades, arc palette, frame and handle; the song comes
from themes/songs.json. Everything written to public/ is third-party media and git-ignored: never commit it.
"""
import csv, hashlib, json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent.parent
MODEL = ROOT / "tools/models/ggml-base.en.bin"
FMT = "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]/b"
GEO = {"card": "scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080",
       "wide": "scale=1080:955:force_original_aspect_ratio=increase,crop=1080:955"}


def die(msg):
    sys.exit(f"reel: {msg}")


def run(*cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def jload(p):
    return json.loads(Path(p).read_text())


def theme_of(name):
    p = ROOT / f"themes/{name}.json"
    if not p.exists():
        die(f"no theme {name} (themes/{name}.json)")
    t = jload(p)
    t["grades"] = {**jload(ROOT / "themes/grades.json"), **t.get("grades", {})}
    t["grades"].pop("_doc", None)
    return t


# words are compared loosely (whisper punctuation varies); Edit.tsx shows them through its own clean()
def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


class Episode:
    def __init__(self, ref, out=None):
        if "/" not in ref:
            die("episode is <theme>/<ep>, e.g. sports/p01-kobe")
        self.theme_id, self.ep = ref.split("/", 1)
        self.theme = theme_of(self.theme_id)
        self.spec_path = ROOT / self.theme_id / "episodes" / f"{self.ep}.yaml"
        if not self.spec_path.exists():
            die(f"no spec {self.spec_path.relative_to(ROOT)} (reel.py new {self.theme_id} {self.ep})")
        self.spec = yaml.safe_load(self.spec_path.read_text()) or {}
        self.dir = Path(out) if out else ROOT / "public" / self.theme_id / self.ep
        (self.dir / "raw").mkdir(parents=True, exist_ok=True)
        (self.dir / "cuts").mkdir(exist_ok=True)
        songs = jload(ROOT / "themes/songs.json")
        key = self.spec.get("song")
        if key not in songs:
            die(f"song {key!r} is not in themes/songs.json")
        if key not in self.theme["music"]["pool"]:
            print(f"note: {key} is outside the {self.theme_id} pool")
        self.song = {**songs[key], **{k: self.spec[k] for k in ("bpm", "song_drop") if k in self.spec}}
        self.song["drop"] = self.song.pop("song_drop", self.song["drop"])
        self.frame = self.spec.get("frame", self.theme["frame"])

    def raw(self, name):
        return self.dir / "raw" / f"{name}.mp4"

    # ---- fetch: every source into raw/<name>.mp4 (download once, or link another episode's download)
    def fetch(self):
        for name, s in (self.spec.get("sources") or {}).items():
            dst = self.raw(name)
            if dst.exists():
                continue
            if "link" in s:  # theme/ep/name: reuse public/<theme>/<ep>/raw/<name>.mp4
                t, e, n = s["link"].split("/")
                src = ROOT / "public" / t / e / "raw" / f"{n}.mp4"
                if not src.exists():
                    die(f"source {name}: {src} is missing")
                dst.symlink_to(src)
            elif "file" in s:
                dst.symlink_to(Path(s["file"]).expanduser().resolve())
            elif "url" in s:
                sec = ["--download-sections", f"*{s['section']}"] if s.get("section") else []
                run("yt-dlp", "--cookies-from-browser", "chrome", "-q", "--no-warnings", *sec, "-f", FMT,
                    "--merge-output-format", "mp4", "-o", self.dir / "raw" / f"{name}.%(ext)s", "--", s["url"])
            else:
                die(f"source {name} needs url, link or file")
            print(f"source {name}")

    # ---- voice: splice the story, land the climax word on the song's drop, caption times from whisper
    def segments(self):
        v = self.spec["voice"]
        segs = []
        for s in v["segments"]:
            if isinstance(s[0], str):
                f, a, b, g = s
            else:
                (a, b, g), f = s, v["src"]
            segs.append({"file": f, "a": float(a), "b": float(b), "gap": float(g)})
        t = 0.0
        for s in segs:
            s["reel"] = round(t, 3)
            s["dur"] = round(s["b"] - s["a"], 3)
            t += s["dur"] + s["gap"]
        return segs, t

    def pcm(self, f, a, b, sr=16000):
        out = run("ffmpeg", "-v", "error", "-ss", a, "-to", b, "-i", self.raw(f), "-vn", "-ac", "1", "-ar", sr,
                  "-f", "s16le", "-", capture_output=True).stdout
        return np.frombuffer(out, np.int16).astype(float)

    def onset(self, s):
        # first 10 ms frame above 15% of the peak in the word's first 1.5 s: the waveform, never whisper
        x = self.pcm(s["file"], s["a"], min(s["b"], s["a"] + 1.5))
        r = np.array([np.sqrt((x[i:i + 160] ** 2).mean()) for i in range(0, len(x) - 160, 160)])
        return s["a"] + int(np.argmax(r > 0.15 * r.max())) / 100

    def whisper(self, f, a, b):
        # cached by (file, window): re-running a build does not re-transcribe
        key = hashlib.md5(f"{self.raw(f).resolve()}|{a}|{b}".encode()).hexdigest()[:10]
        w = self.dir / "raw" / f"w_{key}"
        if not w.with_suffix(".csv").exists():
            cut = ["-ss", a] + (["-to", b] if b is not None else [])
            run("ffmpeg", "-v", "error", "-y", *cut, "-i", self.raw(f), "-vn", "-ar", "16000", "-ac", "1", w.with_suffix(".wav"))
            run("whisper-cli", "-m", MODEL, "-f", w.with_suffix(".wav"), "-ml", "1", "-sow", "-ocsv", "-of", w, "-np",
                capture_output=True)
        rows = csv.DictReader(open(w.with_suffix(".csv")))
        return [(a + int(r["start"]) / 1000, r["text"].strip()) for r in rows
                if r["text"].strip() and not r["text"].strip().startswith("[")]

    def voice(self):
        v = self.spec["voice"]
        segs, total = self.segments()
        ci = v["climax"]["seg"]
        on = float(v["climax"].get("onset") or self.onset(segs[ci]))
        drop = round(segs[ci]["reel"] + on - segs[ci]["a"], 3)
        start = round(self.song["drop"] - drop, 3)
        if start < 0:
            die(f"story is {-start:.2f} s longer than {self.song['title']}'s build-up: cut a line before the climax")
        files = sorted({s["file"] for s in segs})
        fc = ";".join(f"[{files.index(s['file'])}:a]atrim={s['a']}:{s['b']},asetpts=PTS-STARTPTS,"
                      f"aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.02,areverse,"
                      f"afade=t=in:d=0.05,areverse,apad=pad_dur={s['gap']}[p{i}]" for i, s in enumerate(segs))
        fc += ";" + "".join(f"[p{i}]" for i in range(len(segs))) + \
            f"concat=n={len(segs)}:v=0:a=1,aformat=channel_layouts=stereo,aresample=48000,highpass=f=80,loudnorm=I=-15:TP=-1.5[o]"
        ins = sum((["-i", self.raw(f)] for f in files), [])
        run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[o]", "-ar", "48000", self.dir / "vo.wav")
        if v.get("lift", True):
            # loudnorm on a voice full of gaps lands near -17 LUFS: measure and lift it under a limiter (~-15)
            err = run("ffmpeg", "-i", self.dir / "vo.wav", "-af", "ebur128", "-f", "null", "-", capture_output=True, text=True).stderr
            lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])
            tmp = self.dir / "raw" / "vo_lift.wav"
            run("ffmpeg", "-v", "error", "-y", "-i", self.dir / "vo.wav", "-af", f"volume={-16.3 - lufs:.2f}dB,alimiter=limit=0.85",
                "-ar", "48000", tmp)
            tmp.replace(self.dir / "vo.wav")
        json.dump({"drop": drop, "musicStart": start, "segments": [
            {"reel": s["reel"], "file": s["file"], "src": s["a"], "dur": s["dur"]} for s in segs]},
            open(self.dir / "srcmap.json", "w"), indent=1)
        words = self.caption_times(segs, v)
        for i, x in enumerate(words):
            x["e"] = round(min(words[i + 1]["s"], x["s"] + 0.5), 3) if i + 1 < len(words) else round(x["s"] + 0.5, 3)
        words[0]["s"] = 0.0  # the first word is on screen from frame 1
        cw = norm(v["climax"].get("word", ""))
        near = [x for x in words if cw and norm(x["w"]).startswith(cw) and abs(x["s"] - drop) < 1.0]
        if cw and not near:
            print(f"warning: no word {cw!r} within 1 s of the drop ({drop}): check voice.climax")
        for x in near[:1]:
            x["s"] = drop
            x["e"] = max(x["e"], round(drop + 0.2, 3))
        json.dump(words, open(self.dir / "words.json", "w"), indent=0)
        print(f"voice {total:.2f} s, climax onset src {on:.2f}, drop at {drop} s, {self.song['title']} starts at {start} s")
        self.print_words(words)

    def caption_times(self, segs, v):
        mode = v.get("whisper", "single")
        out = []
        if mode == "segments":  # each piece alone: old tapes drift on a long pass
            for s in segs:
                for t, w in self.whisper(s["file"], s["a"], s["b"]):
                    out.append({"w": w, "s": round(s["reel"] + min(t - s["a"], s["dur"] - 0.05), 3)})
        elif mode == "single":  # one pass per source file, mapped through the splices
            for f in sorted({s["file"] for s in segs}, key=lambda f: min(s["reel"] for s in segs if s["file"] == f)):
                mine = [s for s in segs if s["file"] == f]
                a = float(v.get("whisper_from", max(0, min(s["a"] for s in mine) - 1)))
                b = v.get("whisper_to", max(s["b"] for s in mine) + 2)
                heard = self.whisper(f, a, None if b == "eof" else float(b))
                for s in mine:
                    for t, w in heard:
                        if s["a"] - 0.06 <= t < s["b"] - 0.08:
                            out.append({"w": w, "s": round(s["reel"] + max(0, t - s["a"]), 3)})
            out.sort(key=lambda x: x["s"])
        else:  # explicit windows [[file,] a, b]: contiguous source stretches heard together
            for win in mode:
                f, a, b = win if isinstance(win[0], str) else (v["src"], *win)
                for t, w in self.whisper(f, float(a), float(b)):
                    s = max((s for s in segs if s["file"] == f and s["a"] - 0.06 <= t), key=lambda s: s["a"], default=None)
                    if s:
                        out.append({"w": w, "s": round(s["reel"] + max(0, min(t - s["a"], s["dur"] - 0.05)), 3)})
            out.sort(key=lambda x: x["s"])
        # fix: [["it with the thick", "arithmetic"], ["their", "they're"], ["about", ""]]
        for frm, to in v.get("fix") or []:
            frm = [norm(x) for x in frm.split()]
            i = 0
            while i <= len(out) - len(frm):
                if [norm(x["w"]) for x in out[i:i + len(frm)]] == frm:
                    out[i:i + len(frm)] = [{"w": to, "s": out[i]["s"]}] if to else []
                    i += 1 if to else 0
                else:
                    i += 1
        return out

    def print_words(self, words):
        print(" ".join(f"{i}:{x['w']}@{x['s']:.2f}" for i, x in enumerate(words)))

    # ---- edit: shots on the beat grid, captions by text, written to edit.json
    def grid(self):
        m = jload(self.dir / "srcmap.json")
        return m, m["drop"], 60 / float(self.song["bpm"])

    def at(self, x, m, drop, beat):
        # 12.5 | b-30 (beats from the drop) | s3 (segment 3 starts) | drop; any of them +/- seconds
        if isinstance(x, (int, float)) or re.fullmatch(r"-?[\d.]+", str(x)):
            return round(float(x), 3)
        g = re.fullmatch(r"(b|s|drop)(-?[\d.]+)?([+-][\d.]+)?", str(x).replace(" ", ""))
        if not g:
            die(f"bad time {x!r}: use seconds, bN, sN or drop")
        k, n, off = g.groups()
        base = drop + float(n) * beat if k == "b" else m["segments"][int(n)]["reel"] if k == "s" else drop
        return round(base + float(off or 0), 3)

    def src_at(self, m, reel, f):
        s = max((s for s in m["segments"] if s["reel"] <= reel + 1e-6), key=lambda s: s["reel"])
        if s.get("file", f) != f:
            die(f"lip-sync at {reel}: the voice there is {s['file']}, not {f}")
        return round(s["src"] + reel - s["reel"], 3)

    def plan(self):
        m, drop, beat = self.grid()
        T = lambda x: self.at(x, m, drop, beat)
        end = T(self.spec["end"])
        shots = []
        for line in self.spec["shots"]:
            tok = line.split()
            if len(tok) < 3:
                die(f"shot {line!r}: <time> <name> <source>@<start|sync> <GRADE> [zoom=..] [origin=x%,y%] [flash]")
            sh = {"name": tok[1], "from": T(tok[0])}
            if tok[2] != "black":
                f, _, ss = tok[2].partition("@")
                if f not in (self.spec.get("sources") or {}):
                    die(f"shot {sh['name']}: no source {f}")
                g = re.fullmatch(r"sync([+-][\d.]+)?", ss)
                sh["src"], sh["sync"] = f, bool(g)
                sh["ss"] = round(self.src_at(m, sh["from"], f) + float(g.group(1) or 0), 3) if g else float(ss)
                sh["grade"] = tok[3] if len(tok) > 3 else die(f"shot {sh['name']}: no grade")
                if sh["grade"] not in self.theme["grades"]:
                    die(f"shot {sh['name']}: unknown grade {sh['grade']} ({' '.join(self.theme['grades'])})")
            for o in tok[4:]:
                k, _, val = o.partition("=")
                if k == "flash":
                    sh["flash"] = True
                elif k == "zoom":
                    sh["zoom"] = float(val)
                elif k == "origin":
                    sh["origin"] = val.replace(",", " ")
                elif k in ("crop", "len"):
                    sh[k] = val
                else:
                    die(f"shot {sh['name']}: unknown option {o}")
            shots.append(sh)
        shots.sort(key=lambda s: s["from"])
        names = [s["name"] for s in shots if s["name"] != "black"]
        if len(set(names)) != len(names):
            die("shot names must be unique (each is cuts/<name>.mp4)")
        for i, s in enumerate(shots):
            nxt = shots[i + 1]["from"] if i + 1 < len(shots) else end
            s["dur"] = round(float(s.get("len") or nxt - s["from"] + 0.3), 3)
        return m, drop, beat, end, shots

    def captions(self, words):
        out, i = [], 0
        for line in self.spec.get("captions") or []:
            text, _, mods = str(line).partition("|")
            want = [norm(x) for x in text.split() if norm(x)]
            skip = text.strip().startswith("~")
            got = [norm(x["w"]) for x in words[i:i + len(want)]]
            if got != want:
                ctx = " ".join(f"{j}:{words[j]['w']}" for j in range(max(0, i - 3), min(len(words), i + len(want) + 4)))
                die(f"caption {text.strip()!r} does not match the words at {i}: {ctx}")
            if not skip:
                c = {"w": [i, i + len(want) - 1]}
                for k in mods.split():
                    if k == "stack":
                        c["layout"] = "stack"
                    elif k in ("italic", "glass"):
                        c[k] = True
                    else:
                        die(f"caption {text.strip()!r}: unknown style {k} (stack, italic, glass)")
                out.append(c)
            i += len(want)
        if out and i < len(words):
            print(f"warning: words {i}..{len(words) - 1} have no caption: " + " ".join(x["w"] for x in words[i:]))
        return out

    def edit(self):
        m, drop, beat, end, shots = self.plan()
        words = jload(self.dir / "words.json")
        caps = self.captions(words)
        T = lambda x: self.at(x, m, drop, beat)
        e = {"frame": self.frame, "end": round(end, 2), "voFrom": 0,
             "music": [{"src": f"shared/music/{self.song['file']}", "start": m["musicStart"], "at": 0,
                        "volume": self.spec.get("volume", self.theme["music"]["volume"])}],
             "shots": [{k: s[k] for k in ("name", "from", "zoom", "origin", "flash") if k in s} for s in shots],
             "captions": caps}
        if self.spec.get("headline"):
            e["headline"] = {"text": self.spec["headline"], "to": T(self.spec.get("headline_to", 3))}
        if self.spec.get("hook"):
            e["hook"] = {"text": self.spec["hook"]["text"], "to": T(self.spec["hook"]["to"])}
        json.dump(e, open(self.dir / "edit.json", "w"), indent=1)
        self.lint(e, shots, drop, words)
        print(f"edit {e['end']} s, {len(shots)} shots, {len(caps)} captions, drop {drop} s, beat {beat:.3f} s")
        for i, s in enumerate(shots):
            print(f"  {s['from']:6.2f}  {s['name']:<12} {s.get('src', '-'):<10} {s.get('ss', 0):8.2f}{' sync' if s.get('sync') else '     '}"
                  f"  {s['dur']:5.2f}  {s.get('grade', '')}")

    def lint(self, e, shots, drop, words):
        arc = self.theme.get("arc", {})
        pre = set(arc.get("build", [])) | set(arc.get("turn", [])) | set(arc.get("speaker", []))
        post = set(arc.get("payoff", [])) | set(arc.get("speaker", []))
        warn = lambda s: print(f"warning: {s}")
        if not shots or shots[0]["from"] > 0 or not shots[0].get("sync"):
            warn("frame 1 should be the speaker's face, lip-synced (<source>@sync)")
        if not e.get("headline"):
            warn("no headline: the hook must read on mute")
        if not any(abs(s["from"] - drop) < 0.05 and s.get("flash") for s in shots):
            warn(f"no flash cut on the drop ({drop} s)")
        for s in shots:
            g = s.get("grade")
            if g and pre and s["from"] < drop - 0.05 and g not in pre:
                warn(f"{s['name']}: {g} before the drop (theme build + turn palette: {' '.join(arc['build'] + arc.get('turn', []))})")
            if g and post and s["from"] >= drop - 0.05 and g not in post:
                warn(f"{s['name']}: {g} after the drop (theme payoff palette: {' '.join(arc['payoff'])})")
        glass = sum(1 for c in e["captions"] if c.get("glass"))
        if e["captions"] and not 2 <= glass <= 5:
            warn(f"{glass} glass captions (aim for 3 or 4)")
        if words and words[-1]["e"] > e["end"] - 0.3:
            warn("the last word runs into the fade: move end later")

    def cuts(self):
        m, drop, beat, end, shots = self.plan()
        srcs = self.spec.get("sources") or {}
        man_p = self.dir / "cuts" / ".manifest.json"
        man = jload(man_p) if man_p.exists() else {}
        lens = {}

        def one(s):
            pre = s.get("crop") or srcs[s["src"]].get("crop") or ""
            if pre and not pre.startswith("crop="):
                pre = "crop=" + pre
            vf = f"{pre + ',' if pre else ''}{GEO[self.frame]},setsar=1,fps=30,{self.theme['grades'][s['grade']]},format=yuv420p"
            key = f"{self.raw(s['src']).resolve()}|{s['ss']}|{s['dur']}|{vf}"
            dst = self.dir / "cuts" / f"{s['name']}.mp4"
            if man.get(s["name"]) == key and dst.exists():
                return
            if s["ss"] + s["dur"] > lens[s["src"]] + 0.05:
                print(f"warning: {s['name']} runs past the end of {s['src']} ({lens[s['src']]:.1f} s)")
            run("ffmpeg", "-v", "error", "-y", "-ss", s["ss"], "-t", s["dur"], "-i", self.raw(s["src"]), "-an", "-vf", vf,
                "-c:v", "libx264", "-crf", "17", "-preset", "fast", dst)
            man[s["name"]] = key
            print(f"cut {s['name']}")

        todo = [s for s in shots if s["name"] != "black"]
        for s in todo:  # durations first, serially (shared dict), then cut in parallel
            if s["src"] not in lens:
                lens[s["src"]] = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                           self.raw(s["src"]), capture_output=True, text=True).stdout)
        with ThreadPoolExecutor(4) as ex:
            list(ex.map(one, todo))
        json.dump(man, open(man_p, "w"), indent=0)


def ep_id(theme, ep):
    return "-".join([theme["prefix"]] + [p.capitalize() if not re.fullmatch(r"p\d+", p) else p.upper() for p in ep.split("-")])


TEMPLATE = """# {theme}/{ep}: one real voice, setup on the build-up, the turning word on the drop (RECIPE.md).
# Build: python3 tools/reel.py build {theme}/{ep}   Render: npm run render -- {id}
song: {song}                      # themes/songs.json ({pool})
headline: the hook line in lowercase with one *italic* word
headline_to: b-27                 # until when (seconds, bN = N beats from the drop, sN = segment N starts)
end: b20

sources:                          # each becomes raw/<name>.mp4
  speaker: {{url: "https://www.youtube.com/watch?v=...", section: "0:00-3:00", crop: ""}}
  # broll:  {{url: "...", section: "1:20-2:05"}}
  # same:   {{link: tech/p02-jobs-arc/jobs}}       reuse another episode's download

voice:
  src: speaker                    # default source of the segments
  whisper: single                 # single | segments (old tapes that drift) | [[a, b], ...] windows
  climax: {{seg: 4, word: ""}}      # the segment that starts on the climax word, and the word
  segments:                       # [src start, src end, gap after] or [source, start, end, gap]
    - [0.0, 8.0, 0.30]            # setup
    - [9.0, 13.0, 0.30]           # low point
    - [14.0, 15.2, 0.04]          # turn: "but then..."
    - [15.2, 19.0, 0.35]          # turn, rising (0.35 of tension before the climax)
    - [20.0, 26.0, 0]             # CLIMAX word, then the payoff
  fix: []                         # whisper mishearings: [["heard words", "real words"]]

shots:                            # <time> <name> <source>@<start s | sync[+-s]> <GRADE> [zoom=1.6] [origin=50%,18%] [flash]
  - 0      hook     speaker@sync  {speaker}  zoom=1.6 origin=50%,20%
  - b-27   setup1   speaker@30.0  {build}
  - b0     drop     speaker@60.0  {payoff}  flash
  - b16    last     speaker@4.0   {speaker}

captions:                         # in order, 1 to 3 words each: "words | stack italic glass"; "~ words" = no caption
  - the first words | glass
"""


def new(theme_id, ep):
    t = theme_of(theme_id)
    p = ROOT / theme_id / "episodes" / f"{ep}.yaml"
    if p.exists():
        die(f"{p.relative_to(ROOT)} exists")
    p.parent.mkdir(parents=True, exist_ok=True)
    i = ep_id(t, ep)
    arc = t["arc"]
    p.write_text(TEMPLATE.format(theme=theme_id, ep=ep, id=i, song=t["music"]["pool"][0], pool=", ".join(t["music"]["pool"]),
                                 speaker=arc["speaker"][0], build=arc["build"][0], payoff=arc["payoff"][0]))
    tp = ROOT / f"themes/{theme_id}.json"
    raw = jload(tp)
    if not any(e["ep"] == ep for e in raw["episodes"]):
        raw["episodes"].append({"id": i, "ep": ep})
        tp.write_text(json.dumps(raw, indent=2) + "\n")
    print(f"wrote {p.relative_to(ROOT)}, registered {i}")


def find_id(cid):
    for tp in sorted((ROOT / "themes").glob("*.json")):
        t = jload(tp)
        for e in t.get("episodes", []) if isinstance(t, dict) and "prefix" in t else []:
            if e["id"] == cid:
                return t["id"], e["ep"]
    die(f"no composition {cid} in themes/*.json")


def check(cid):
    th, ep = find_id(cid)
    v = ROOT / "out" / f"{cid}.mp4"
    if not v.exists():
        die(f"render it first: npm run render -- {cid}")
    m = jload(ROOT / "public" / th / ep / "srcmap.json")
    sheet, frames = v.with_suffix(".sheet.jpg"), v.with_suffix(".frames.jpg")
    dur = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v, capture_output=True, text=True).stdout)
    rows = int(np.ceil(dur * 2 / 12))
    run("ffmpeg", "-v", "error", "-y", "-i", v, "-vf", f"fps=2,scale=180:-1,tile=12x{rows}", "-frames:v", "1", sheet)
    d = m["drop"]
    ts = [0, 0.5, 1.0, d - 0.2, d + 0.05, d + 0.4]
    ins = sum((["-ss", f"{max(0, t):.2f}", "-i", v] for t in ts), [])
    run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex",
        "".join(f"[{i}:v]trim=end_frame=1,scale=360:-1[f{i}];" for i in range(len(ts))) + "".join(f"[f{i}]" for i in range(len(ts))) +
        f"hstack=inputs={len(ts)}", "-frames:v", "1", frames)
    err = run("ffmpeg", "-i", v, "-af", "ebur128", "-f", "null", "-", capture_output=True, text=True).stderr
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1]
    print(f"{cid}: {dur:.1f} s, {lufs} LUFS (aim ~-14), drop at {d} s")
    print(f"  {sheet.relative_to(ROOT)}  (2 fps)\n  {frames.relative_to(ROOT)}  (0, 0.5, 1 s | drop -0.2, +0.05, +0.4)")


def main(a):
    if len(a) >= 3 and a[0] == "new":
        return new(a[1], a[2])
    if len(a) >= 2 and a[0] == "check":
        return check(a[1])
    if len(a) >= 2 and a[0] == "words":
        e = Episode(a[1])
        m = jload(e.dir / "srcmap.json")
        print(f"drop {m['drop']} s; segments start at " + " ".join(f"s{i}={s['reel']}" for i, s in enumerate(m["segments"])))
        return e.print_words(jload(e.dir / "words.json"))
    if len(a) >= 2 and a[0] == "build":
        out = a[a.index("--out") + 1] if "--out" in a else None
        only = a[a.index("--only") + 1] if "--only" in a else None
        e = Episode(a[1], out)
        for step in ("fetch", "voice", "edit", "cuts"):
            if only in (None, step):
                getattr(e, step)()
        return
    print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
