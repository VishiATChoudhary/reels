// Render reels to out/<id>.mp4: `npm run render` (all), `npm run render -- Tech03` (ids matching a prefix).
import { execFileSync } from "node:child_process";

const all = execFileSync("node_modules/.bin/remotion", ["compositions", "src/index.ts", "-q"], { encoding: "utf8" })
  .split(/\s+/).filter((id) => /^[A-Z][\w-]+$/.test(id));
const want = process.argv.slice(2);
const ids = want.length ? all.filter((id) => want.some((w) => id.startsWith(w))) : all;
for (const id of ids) {
  console.log(`render ${id}`);
  execFileSync("node_modules/.bin/remotion", ["render", "src/index.ts", id, `out/${id}.mp4`, "--codec=h264", "--crf=18", "--pixel-format=yuv420p", "--audio-bitrate=320k"], { stdio: "inherit" });
}
