import React from "react";
import { AbsoluteFill, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Audio, Video } from "@remotion/media";
import { FPS, H, HANDLE, INK, SANS, W, WIDE, clamp } from "./style";

// One short in the reference style (tech/STYLE.md): footage in a single frame on black, a real voice,
// lowercase Helvetica captions that fade in word by word, glass caps for the key words, music under the
// voice at a constant level. Nothing else on screen. Everything comes from public/<theme>/<ep>/edit.json.
export type Word = { w: string; s: number; e: number };
export type Caption = { w: [number, number]; layout?: "line" | "stack"; italic?: boolean; glass?: boolean };
export type EditData = {
  frame: "card" | "wide";
  end: number; // s, where the edit stops
  voFrom: number; // s, where the voice starts
  // music clips: start = s into the track, at = s into the edit, dur = how long (default: to the end)
  music: { src: string; start: number; volume: number; at?: number; dur?: number }[];
  headline?: { text: string; to: number }; // the hook line above the frame, readable on mute
  hook?: { text: string; to: number }; // glass word over the first shot, before the voice
  shots: { name: string; from: number; zoom?: number; origin?: string; flash?: boolean }[]; // s, each runs until the next one
  captions: Caption[];
};
// handle and font come from the theme (themes/<theme>.json: "handle", "look.font")
export type EditProps = { theme: string; ep: string; handle?: string; font?: string; edit?: EditData; words?: Word[] };
const Font = React.createContext(SANS);

// the frame the footage sits in (measured from the references)
const CARD = { left: 14, top: 434, width: 1052, height: 1052, radius: 100 };
const WIDEF = { left: 0, top: 482, width: 1080, height: 955, radius: 0 };
const frameOf = (e: EditData) => (e.frame === "card" ? CARD : WIDEF);
const sec = (s: number) => Math.round(s * FPS);
const clean = (w: string) => w.toLowerCase().replace(/[^a-z0-9'.%$-]/g, "").replace(/\.$/, "");

// zoom: a tighter crop that punches in on the cut (hook jump cuts); flash: two white frames on the cut
const Shot: React.FC<{ src: string; dur: number; zoom?: number; origin?: string; flash?: boolean }> = ({ src, dur, zoom = 1, origin, flash }) => {
  const f = useCurrentFrame();
  const punch = zoom > 1 ? interpolate(f, [0, 5], [1.12, 1], clamp) : 1;
  const k = zoom * punch * interpolate(f, [0, dur], [1, 1.04], clamp);
  return (
    <>
      <Video src={src} muted style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${k})`, transformOrigin: origin ?? "50% 50%" }} />
      {flash && <AbsoluteFill style={{ background: "#fff", opacity: interpolate(f, [0, 3], [0.85, 0], clamp) }} />}
    </>
  );
};

// a word arrives over 0.1 s, faint and soft first (ref: ~6 frames at 60 fps), no scale, no slide
const useIn = (at: number) => {
  const f = useCurrentFrame();
  if (at <= 1) return { opacity: 1, filter: "none" };
  return {
    opacity: interpolate(f, [at, at + 3], [0, 1], clamp),
    filter: `blur(${interpolate(f, [at, at + 3], [6, 0], clamp)}px)`,
  };
};

const W_ = ({ text, at, style }: { text: string; at: number; style?: React.CSSProperties }) => (
  <span style={{ display: "inline-block", ...useIn(at), ...style }}>{text}</span>
);

const fit = (chars: number, base: number, perChar: number) => Math.min(base, Math.floor(960 / (chars * perChar)));
const shadow = "0 2px 14px rgba(0,0,0,.45)";

// lowercase line or stack: a small lead above the big last word ("on / everything")
const Words: React.FC<{ c: Caption; words: Word[]; off: number }> = ({ c, words, off }) => {
  const font = React.useContext(Font);
  const ws = words.slice(c.w[0], c.w[1] + 1).map((x) => ({ t: clean(x.w), at: sec(off + x.s) }));
  const base: React.CSSProperties = {
    fontFamily: font, fontWeight: 700, fontStyle: c.italic ? "italic" : "normal", color: INK,
    letterSpacing: "-0.055em", textShadow: shadow, lineHeight: 0.82,
  };
  if (c.layout === "stack" && ws.length > 1) {
    const lead = ws.slice(0, -1), last = ws[ws.length - 1];
    const big = fit(last.t.length, 150, 0.54);
    return (
      <div style={{ display: "inline-block", textAlign: "left", ...base }}>
        <div style={{ fontSize: Math.round(big * 0.5), marginLeft: big * 0.04 }}>
          {lead.map((x, i) => <W_ key={i} text={x.t + (i < lead.length - 1 ? " " : "")} at={x.at} style={{ whiteSpace: "pre" }} />)}
        </div>
        <div style={{ fontSize: big, marginTop: -big * 0.06 }}><W_ text={last.t} at={last.at} /></div>
      </div>
    );
  }
  const size = fit(ws.reduce((a, x) => a + x.t.length + 0.4, 0), ws.length === 1 ? 150 : 120, 0.52);
  return (
    <div style={{ ...base, fontSize: size, whiteSpace: "nowrap" }}>
      {ws.map((x, i) => <W_ key={i} text={x.t + (i < ws.length - 1 ? " " : "")} at={x.at} style={{ whiteSpace: "pre", marginRight: i < ws.length - 1 ? "-0.12em" : 0 }} />)}
    </div>
  );
};

// glass caps in quotes (ref A: ”PRESSURE”): the footage shows through the letters, brightened
const Glass: React.FC<{ text: string; at: number }> = ({ text, at }) => {
  const t = `”${text.toUpperCase()}”`;
  const size = fit(t.length, 172, 0.66);
  const s: React.CSSProperties = { fontFamily: React.useContext(Font), fontWeight: 800, fontSize: size, letterSpacing: "-0.045em", lineHeight: 1, whiteSpace: "nowrap" };
  // fade each layer on its own: opacity or a filter on a parent would isolate the blend from the footage
  const o = useIn(at).opacity;
  return (
    <div style={{ position: "relative" }}>
      <div style={{ ...s, color: "transparent", textShadow: "0 4px 30px rgba(0,0,0,.55)", opacity: o }}>{t}</div>
      <div style={{ ...s, position: "absolute", inset: 0, color: "#fff", mixBlendMode: "overlay", opacity: o }}>{t}</div>
      <div style={{ ...s, position: "absolute", inset: 0, color: "#fff", mixBlendMode: "overlay", opacity: o }}>{t}</div>
      <div style={{ ...s, position: "absolute", inset: 0, color: "rgba(255,255,255,.22)", opacity: o }}>{t}</div>
    </div>
  );
};

const Captions: React.FC<{ edit: EditData; words: Word[] }> = ({ edit, words }) => {
  const f = useCurrentFrame();
  const off = edit.voFrom;
  // the black gap is a hard cut to nothing: no words on it either
  const cur = edit.shots.findLast((s) => f >= sec(s.from));
  if (cur?.name === "black") return null;
  const starts = edit.captions.map((c) => sec(off + words[c.w[0]].s));
  const i = starts.findLastIndex((s) => f >= s);
  if (i < 0) return null;
  const c = edit.captions[i];
  const lastWord = sec(off + words[c.w[1]].e + 0.35);
  const until = Math.min(i + 1 < starts.length ? starts[i + 1] : sec(edit.end) - 10, lastWord);
  if (f >= until) return null;
  const fr = frameOf(edit);
  return (
    <div style={{ position: "absolute", left: 0, width: W, top: fr.top, height: fr.height, display: "flex", alignItems: "center", justifyContent: "center" }}>
      {c.glass ? (
        <Glass text={words.slice(c.w[0], c.w[1] + 1).map((x) => clean(x.w)).join(" ")} at={starts[i]} />
      ) : (
        <Words c={c} words={words} off={off} />
      )}
    </div>
  );
};

const Hook: React.FC<{ edit: EditData }> = ({ edit }) => {
  const f = useCurrentFrame();
  if (!edit.hook || f >= sec(edit.hook.to)) return null;
  const fr = frameOf(edit);
  return (
    <div style={{ position: "absolute", left: 0, width: W, top: fr.top, height: fr.height, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <Glass text={edit.hook.text} at={0} />
    </div>
  );
};

// the hook line: above the frame, two lines max, there from the first frame (no fade: it must read instantly)
const Headline: React.FC<{ edit: EditData }> = ({ edit }) => {
  const f = useCurrentFrame();
  if (!edit.headline || f >= sec(edit.headline.to)) return null;
  const fr = frameOf(edit);
  return (
    <div style={{ position: "absolute", left: 70, right: 70, bottom: H - fr.top + 34, textAlign: "center", fontFamily: React.useContext(Font), fontWeight: 700, fontSize: 66, lineHeight: 1.02, letterSpacing: "-0.04em", color: INK }}>
      {edit.headline.text.split(/(\*[^*]+\*)/).map((p, i) => (p.startsWith("*") ? <i key={i}>{p.slice(1, -1)}</i> : p))}
    </div>
  );
};

export const Edit: React.FC<EditProps> = ({ theme, ep, handle = HANDLE, font = SANS, edit, words }) => {
  const f = useCurrentFrame();
  const { durationInFrames: end } = useVideoConfig();
  if (!edit || !words) return null;
  const base = `${theme}/${ep}`;
  const fr = frameOf(edit);
  const shots = edit.shots.map((s, i) => ({ ...s, a: sec(s.from), b: i + 1 < edit.shots.length ? sec(edit.shots[i + 1].from) : end }));
  return (
    <Font.Provider value={font}>
    <AbsoluteFill style={{ background: "#000" }}>
      {/* everything that sits on the picture shares its stacking context, so the glass blends with the footage */}
      <AbsoluteFill>
        <div style={{ position: "absolute", left: fr.left, top: fr.top, width: fr.width, height: fr.height, borderRadius: fr.radius, overflow: "hidden", background: "#000" }}>
          {shots.filter((s) => s.name !== "black").map((s) => (
            <Sequence key={s.name + s.a} from={s.a} durationInFrames={s.b - s.a} layout="none">
              <Shot src={staticFile(`${base}/cuts/${s.name}.mp4`)} dur={s.b - s.a} zoom={s.zoom} origin={s.origin} flash={s.flash} />
            </Sequence>
          ))}
        </div>
        <Hook edit={edit} />
        <Headline edit={edit} />
        <Captions edit={edit} words={words} />
        <div style={{ position: "absolute", left: 0, width: W, top: fr.top + fr.height - 58, textAlign: "center", fontFamily: WIDE, fontSize: 19, letterSpacing: "0.5em", color: INK, opacity: 0.85 }}>
          {handle.toUpperCase()}
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "#000", opacity: interpolate(f, [end - 10, end], [0, 1], clamp) }} />
      {edit.music.map((m, i) => {
        const at = sec(m.at ?? 0);
        const len = m.dur ? sec(m.dur) : end - at;
        return (
          <Sequence key={i} from={at} durationInFrames={len} layout="none">
            <Audio src={staticFile(m.src)} trimBefore={sec(m.start)} volume={(t) => m.volume * interpolate(t, [len - (m.dur ? 3 : 12), len], [1, 0], clamp)} />
          </Sequence>
        );
      })}
      <Sequence from={sec(edit.voFrom)} layout="none">
        <Audio src={staticFile(`${base}/vo.wav`)} />
      </Sequence>
    </AbsoluteFill>
    </Font.Provider>
  );
};

// read edit.json and words.json at render time; length comes from the edit
export const calcEdit = async ({ props }: { props: EditProps }) => {
  const base = `${props.theme}/${props.ep}`;
  const load = <T,>(f: string) => fetch(staticFile(`${base}/${f}`)).then((r) => (r.ok ? (r.json() as Promise<T>) : undefined));
  const [edit, words] = await Promise.all([load<EditData>("edit.json"), load<Word[]>("words.json")]);
  if (!edit || !words) return {};
  return { durationInFrames: sec(edit.end), props: { ...props, edit, words } };
};

