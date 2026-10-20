import { loadFont as loadWide } from "@remotion/google-fonts/Michroma";

// Default handle; each theme can set its own in themes/<theme>.json.
export const HANDLE = "@hey_synapse";

export const W = 1080;
export const H = 1920;
export const FPS = 30;

// Captions: Helvetica Neue (macOS system font), as in both reference edits (tech/STYLE.md).
export const SANS = '"Helvetica Neue", Helvetica, Arial, sans-serif';
// Watermark: extended square caps, tracked wide (the FEROX mark).
export const WIDE = loadWide("normal", { weights: ["400"], subsets: ["latin"] }).fontFamily;

export const INK = "#FFFFFF";
export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
