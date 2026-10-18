// npm run social -- <command>
//   setup                              what is configured, what is missing, where to get it
//   login tiktok | tiktok-browser      TikTok OAuth (paste-back) or log the fallback Chrome profile in
//   whoami                             account + follower stats for every configured platform
//   post <Id>... [--only x,instagram,tiktok] [--tiktok draft|private|public|browser] [--dry]
//   metrics [--only ...]               stats for everything in posts/ledger.jsonl (+ recent TikToks)
// Video: out/<Id>.mp4. Caption: posts/<Id>.txt. Credentials: macOS Keychain via `vault`.
import { existsSync } from "node:fs";
import * as browser from "./browser.mjs";
import * as instagram from "./instagram.mjs";
import { caption, fail, ledger, vault } from "./lib.mjs";
import * as tiktok from "./tiktok.mjs";
import * as x from "./x.mjs";

const PLATFORMS = { x, instagram, tiktok };
const args = process.argv.slice(2);
const flag = (name) => { const i = args.indexOf(name); return i < 0 ? undefined : args.splice(i, 2)[1]; };
const bool = (name) => { const i = args.indexOf(name); return i >= 0 && !!args.splice(i, 1); };
const only = flag("--only")?.split(",") ?? Object.keys(PLATFORMS);
const tiktokMode = flag("--tiktok") ?? "draft";
const dry = bool("--dry");
const cmd = args.shift();
const targets = only.filter((p) => PLATFORMS[p] || fail(`unknown platform ${p}`));

const SETUP = {
  x: ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET",
    "developer.x.com: create a project + app, set User authentication to Read and write, then Keys and tokens:\n" +
    "    API Key and Secret -> X_API_KEY / X_API_SECRET; Access Token and Secret (generate AFTER read+write) -> X_ACCESS_TOKEN / X_ACCESS_SECRET.\n" +
    "    Buy pay-per-use credits (about $0.015 a post)."],
  instagram: ["IG_ACCESS_TOKEN",
    "Switch the Instagram account to Professional (Creator). developers.facebook.com: create app (Business), add Instagram >\n" +
    "    API setup with Instagram login, add your account as Instagram Tester (accept in Instagram > Settings > Apps), Generate token -> IG_ACCESS_TOKEN."],
  tiktok: ["TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET", "TIKTOK_REDIRECT_URI",
    "developers.tiktok.com: create app, add Login Kit + Content Posting API (Direct Post on), scopes user.info.basic, user.info.stats,\n" +
    "    video.upload, video.publish, video.list; add any https redirect URI you own; add your account as a target user in Sandbox.\n" +
    "    Client key/secret -> TIKTOK_CLIENT_KEY / TIKTOK_CLIENT_SECRET, then: npm run social -- login tiktok"],
};

if (cmd === "setup") {
  for (const [p, entry] of Object.entries(SETUP)) {
    const keys = entry.slice(0, -1), missing = keys.filter((k) => !vault.get(k));
    console.log(`${p}: ${missing.length ? `missing ${missing.join(", ")}` : "keys ok"}${p === "tiktok" && !missing.length && !tiktok.ready() ? " (not logged in)" : ""}`);
    if (missing.length) console.log(`  ${entry.at(-1)}\n  store each with: vault set <KEY>\n`);
  }
  console.log(`tiktok-browser fallback: ${existsSync(`${process.env.HOME}/.reels/chrome`) ? "profile exists" : "not logged in (npm run social -- login tiktok-browser)"}`);
} else if (cmd === "login") {
  const which = args[0];
  if (which === "tiktok") await tiktok.login();
  else if (which === "tiktok-browser") await browser.login();
  else fail("login tiktok | tiktok-browser (X and Instagram use tokens from their dashboards, see setup)");
  console.log("logged in");
} else if (cmd === "whoami") {
  for (const p of targets) {
    if (!PLATFORMS[p].ready()) { console.log(`${p}: not configured`); continue; }
    try { console.log(`${p}:`, JSON.stringify(await PLATFORMS[p].whoami())); } catch (e) { console.log(`${p}: ${e.message}`); }
  }
} else if (cmd === "post") {
  if (!args.length) fail("post <Id>...");
  for (const id of args) {
    const video = `out/${id}.mp4`;
    if (!existsSync(video)) fail(`missing ${video} (npm run render -- ${id})`);
    const text = caption(id);
    for (const p of targets) {
      const mode = p === "tiktok" ? tiktokMode : undefined;
      if (dry) { console.log(`[dry] ${id} -> ${p}${mode ? ` (${mode})` : ""}\n${text}\n`); continue; }
      if (mode !== "browser" && !PLATFORMS[p].ready()) { console.log(`${id} -> ${p}: skipped, not configured (npm run social -- setup)`); continue; }
      try {
        const res = mode === "browser" ? await browser.post(video, text) : await PLATFORMS[p].post(video, text, mode);
        ledger.add({ id, platform: p, mode, ...res });
        console.log(`${id} -> ${p}: ${res.url ?? res.note ?? res.remote}`);
      } catch (e) { console.log(`${id} -> ${p}: FAILED ${e.message}`); process.exitCode = 1; }
    }
  }
} else if (cmd === "metrics") {
  const posts = ledger.all();
  for (const p of targets) {
    if (!PLATFORMS[p].ready()) { console.log(`${p}: not configured`); continue; }
    const mine = posts.filter((e) => e.platform === p && e.remote);
    try {
      const rows = p === "tiktok" ? await tiktok.metrics() : await PLATFORMS[p].metrics(mine.map((e) => e.remote));
      const byRemote = Object.fromEntries(mine.map((e) => [e.remote, e.id]));
      console.log(`\n${p}`);
      console.table(rows.map((r) => ({ reel: byRemote[r.remote] ?? "", ...r })));
    } catch (e) { console.log(`${p}: ${e.message}`); }
  }
} else {
  fail("usage: npm run social -- setup | login tiktok|tiktok-browser | whoami | post <Id>... | metrics");
}
