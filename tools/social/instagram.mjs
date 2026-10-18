// Instagram API with Instagram Login (graph.instagram.com). Needs a Professional (Creator or Business) account
// and a token from the Meta app dashboard. Reels must come from a public URL, so the file is served through a
// throwaway Cloudflare quick tunnel for the few minutes Instagram needs to fetch it.
import { spawn } from "node:child_process";
import { createReadStream, statSync } from "node:fs";
import { createServer } from "node:http";
import { randomBytes } from "node:crypto";
import { Resolver } from "node:dns/promises";
import { fail, request, sleep, vault } from "./lib.mjs";

const API = "https://graph.instagram.com/v25.0";
const token = () => vault.need("IG_ACCESS_TOKEN", "Meta app > Instagram > API setup with Instagram login > Generate token");

const ig = (method, path, params = {}) => {
  const body = new URLSearchParams({ ...params, access_token: token() });
  return method === "GET" ? request(`${API}${path}${path.includes("?") ? "&" : "?"}${body}`) : request(`${API}${path}`, { method, body });
};

export const ready = () => !!vault.get("IG_ACCESS_TOKEN");
export const whoami = () => ig("GET", "/me?fields=user_id,username,followers_count,media_count");

// Long-lived tokens last 60 days; refresh once they are a day old so they never lapse.
export async function refresh() {
  const last = Number(vault.get("IG_TOKEN_REFRESHED") ?? 0);
  if (Date.now() - last < 86400e3) return;
  const res = await request(`https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=${token()}`);
  vault.set("IG_ACCESS_TOKEN", res.access_token);
  vault.set("IG_TOKEN_REFRESHED", Date.now());
}

export async function serve(file) {
  const path = `/${randomBytes(12).toString("hex")}.mp4`;
  const server = createServer((req, res) => {
    if (req.url !== path) return res.writeHead(404).end();
    res.writeHead(200, { "Content-Type": "video/mp4", "Content-Length": statSync(file).size });
    if (req.method === "HEAD") return res.end();
    createReadStream(file).pipe(res);
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  const tunnel = spawn("cloudflared", ["tunnel", "--no-autoupdate", "--protocol", "http2", "--url", `http://127.0.0.1:${server.address().port}`], { stdio: ["ignore", "ignore", "pipe"] });
  // http2, not the default QUIC: QUIC is blocked on some networks and the tunnel then never carries traffic.
  // The URL is printed before the edge connection exists, so wait for both.
  const host = await new Promise((resolve, reject) => {
    let log = "";
    const t = setTimeout(() => { tunnel.kill(); reject(new Error(`cloudflared tunnel did not start in 60 s:\n${log.slice(-500)}`)); }, 60e3);
    tunnel.stderr.on("data", (d) => {
      log += d;
      const m = log.match(/https:\/\/[\w-]+\.trycloudflare\.com/);
      if (m && log.includes("Registered tunnel connection")) { clearTimeout(t); resolve(m[0]); }
    });
  });
  // Ask a public resolver: the local one caches the "not found" from before the tunnel registered.
  const dns = new Resolver();
  dns.setServers(["1.1.1.1"]);
  for (let i = 0; ; i++) {
    try { await dns.resolve4(new URL(host).hostname); break; } catch { if (i > 30) fail(`tunnel ${host} never resolved`); await sleep(2000); }
  }
  return { url: host + path, close: () => { tunnel.kill(); server.close(); } };
}

export async function post(file, caption) {
  await refresh();
  const { user_id } = await whoami();
  const hosted = await serve(file);
  try {
    const { id: container } = await ig("POST", `/${user_id}/media`, { media_type: "REELS", video_url: hosted.url, caption, share_to_feed: "true" });
    for (let i = 0; ; i++) {
      const { status_code, status } = await ig("GET", `/${container}?fields=status_code,status`);
      if (status_code === "FINISHED") break;
      if (["ERROR", "EXPIRED"].includes(status_code)) fail(`Instagram processing ${status_code}: ${status}`);
      if (i > 40) fail("Instagram processing took over 10 minutes");
      await sleep(15e3);
    }
    const { id } = await ig("POST", `/${user_id}/media_publish`, { creation_id: container });
    const { permalink } = await ig("GET", `/${id}?fields=permalink`);
    return { remote: id, url: permalink };
  } finally { hosted.close(); }
}

const REEL_METRICS = "views,reach,likes,comments,shares,saved,total_interactions,ig_reels_avg_watch_time";
export async function metrics(ids) {
  return Promise.all(ids.map(async (id) => {
    const { data } = await ig("GET", `/${id}/insights?metric=${REEL_METRICS}`);
    return { remote: id, ...Object.fromEntries(data.map((m) => [m.name, m.values?.[0]?.value ?? m.total_value?.value])) };
  }));
}
