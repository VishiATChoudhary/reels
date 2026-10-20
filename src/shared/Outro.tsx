import React from "react";
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { INK, SANS, W, clamp } from "./style";

// End card. The footage card collapses into the open node (Edit.tsx, the last COLLAPSE frames of the edit),
// then the link grows out of its corner, the signal node lands with one ring, and the handle arrives in the
// caption type. Geometry from the synapse-site mark (viewBox 22: nodes 6.4 at (1.8,12.8) and (13.8,2.8),
// link 8.2,12.8 to 13.8,9.2); colours --paper / --sig.
export const OUTRO = 84; // frames after the edit's end
export const COLLAPSE = 18; // frames before the edit's end

const PAPER = "#F1EFE9";
const SIG = "#FF4400";
const U = 25; // px per mark unit: nodes 160 px
const STROKE = 22;
const OX = W / 2 - 11 * U;
const OY = 860 - 11 * U;
const at = (x: number, y: number) => ({ x: OX + x * U, y: OY + y * U });

// where the footage card lands: the open node, outer edge
export const NODE = { left: OX + 1.8 * U, top: OY + 12.8 * U, width: 6.4 * U, height: 6.4 * U, radius: 18, stroke: STROKE };

const A = at(8.2 - 0.3, 12.8 + 0.2); // tucked into the node corner so the joint reads as one shape
const B = at(13.8 + 0.3, 9.2 - 0.2);
const LEN = Math.hypot(B.x - A.x, B.y - A.y);
const ANGLE = (Math.atan2(B.y - A.y, B.x - A.x) * 180) / Math.PI;
const SIGN = at(13.8, 2.8);

const ease = Easing.bezier(0.16, 1, 0.3, 1);

export const Outro: React.FC<{ handle: string; font?: string }> = ({ handle, font = SANS }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const link = interpolate(f, [0, 12], [0, 1], { ...clamp, easing: ease });
  const land = spring({ frame: f - 9, fps, config: { damping: 16, stiffness: 190, mass: 0.7 } });
  const ring = interpolate(f, [12, 34], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const drift = interpolate(f, [0, OUTRO], [1, 1.035], clamp);
  const words = handle.toLowerCase().replace(/^@/, "").split("_");
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ transform: `scale(${drift})`, transformOrigin: `${W / 2}px 860px` }}>
        <div style={{ position: "absolute", ...pos(NODE), border: `${STROKE}px solid ${PAPER}`, borderRadius: NODE.radius, boxSizing: "border-box" }} />
        <div style={{ position: "absolute", left: A.x, top: A.y - STROKE / 2, width: LEN, height: STROKE, background: PAPER, borderRadius: STROKE / 2,
          transformOrigin: `0 ${STROKE / 2}px`, transform: `rotate(${ANGLE}deg) scaleX(${link})` }} />
        <div style={{ position: "absolute", left: SIGN.x, top: SIGN.y, width: NODE.width, height: NODE.height, borderRadius: NODE.radius, background: SIG,
          transformOrigin: "0% 100%", transform: `scale(${land})`, boxShadow: `0 0 ${60 * land}px rgba(255,68,0,${0.35 * land})` }} />
        <div style={{ position: "absolute", left: SIGN.x, top: SIGN.y, width: NODE.width, height: NODE.height, borderRadius: NODE.radius,
          border: `4px solid ${SIG}`, transform: `scale(${1 + ring * 0.9})`, opacity: ring > 0 ? 0.8 * (1 - ring) : 0 }} />
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 0, width: W, top: 1230, textAlign: "center", fontFamily: font, fontWeight: 700, fontSize: 96,
        letterSpacing: "-0.055em", color: INK, lineHeight: 1, whiteSpace: "pre" }}>
        {["@" + words[0], ...words.slice(1).map((w) => "_" + w)].map((w, i) => {
          const s = 22 + i * 5;
          return (
            <span key={i} style={{ display: "inline-block", opacity: interpolate(f, [s, s + 5], [0, 1], clamp),
              filter: `blur(${interpolate(f, [s, s + 5], [8, 0], clamp)}px)` }}>{w}</span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const pos = (r: { left: number; top: number; width: number; height: number }) => ({ left: r.left, top: r.top, width: r.width, height: r.height });
