// TikTok Content Posting API + Display API. Until TikTok audits the app it can only send drafts to the
// creator's inbox (mode "draft", default) or post SELF_ONLY ("private"). "public" needs an audited app;
// the logged-in browser fallback (browser.mjs) posts publicly without one.
import { execFileSync } from "node:child_process";
import { randomBytes } from "node:crypto";
import { openSync, readSync, statSync } from "node:fs";
import { createInterface } from "node:readline/promises";
import { fail, request, sleep, vault } from "./lib.mjs";

const API = "https://open.tiktokapis.com/v2";
const SCOPES = "user.info.basic,user.info.stats,video.upload,video.publish,video.list";

const app = () => ({
  client_key: vault.need("TIKTOK_CLIENT_KEY", "developers.tiktok.com > your app > Credentials"),
  client_secret: vault.need("TIKTOK_CLIENT_SECRET", "developers.tiktok.com > your app > Credentials"),
});

async function saveTokens(res) {
  if (!res.access_token) fail(`TikTok token error: ${JSON.stringify(res)}`);
  vault.set("TIKTOK_ACCESS_TOKEN", res.access_token);
  vault.set("TIKTOK_REFRESH_TOKEN", res.refresh_token);
  vault.set("TIKTOK_TOKEN_EXPIRES", Date.now() + res.expires_in * 1000);
}

const oauth = (params) => request(`${API}/oauth/token/`, {
  method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ ...app(), ...params }),
});

// Redirect URIs must be static https, so no localhost listener: log in, then paste the URL you land on.
export async function login() {
  const redirect_uri = vault.need("TIKTOK_REDIRECT_URI", "any https URL registered under Login Kit, e.g. https://<you>.github.io/callback/");
  const state = randomBytes(8).toString("hex");
  const url = `https://www.tiktok.com/v2/auth/authorize/?${new URLSearchParams({ client_key: app().client_key, scope: SCOPES, response_type: "code", redirect_uri, state })}`;
  execFileSync("open", [url]);
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  const back = new URL((await rl.question("Approve in the browser, then paste the URL it redirects to:\n> ")).trim());
  rl.close();
  if (back.searchParams.get("state") !== state) fail("state mismatch, start again");
  await saveTokens(await oauth({ code: back.searchParams.get("code"), grant_type: "authorization_code", redirect_uri }));
}

// Access tokens last 24 h, refresh tokens a year.
async function token() {
  if (Number(vault.get("TIKTOK_TOKEN_EXPIRES") ?? 0) - Date.now() < 300e3) {
    await saveTokens(await oauth({ grant_type: "refresh_token", refresh_token: vault.need("TIKTOK_REFRESH_TOKEN", "npm run social -- login tiktok") }));
  }
  return vault.get("TIKTOK_ACCESS_TOKEN");
}

const tt = async (path, body = {}) => {
  const res = await request(`${API}${path}`, {
    method: "POST", body: JSON.stringify(body),
    headers: { Authorization: `Bearer ${await token()}`, "Content-Type": "application/json; charset=UTF-8" },
  });
  if (res.error?.code && res.error.code !== "ok") fail(`TikTok ${path}: ${res.error.code} ${res.error.message}`);
  return res.data;
};

export const ready = () => !!vault.get("TIKTOK_REFRESH_TOKEN");
export const whoami = async () => {
  const res = await request(`${API}/user/info/?fields=open_id,display_name,username,follower_count,likes_count,video_count`, { headers: { Authorization: `Bearer ${await token()}` } });
  return res.data.user;
};

// Under 64 MB goes up as one chunk; larger files in 10 MB chunks with the last one taking the remainder.
function chunks(size) {
  const chunk = size <= 64 * 1024 * 1024 ? size : 10 * 1024 * 1024;
  return { video_size: size, chunk_size: chunk, total_chunk_count: Math.floor(size / chunk) };
}

async function upload(url, file, { video_size, chunk_size, total_chunk_count }) {
  const fd = openSync(file, "r");
  for (let i = 0; i < total_chunk_count; i++) {
    const start = i * chunk_size, end = i === total_chunk_count - 1 ? video_size : start + chunk_size;
    const buf = Buffer.alloc(end - start);
    readSync(fd, buf, 0, buf.length, start);
    const res = await fetch(url, { method: "PUT", body: buf, headers: { "Content-Type": "video/mp4", "Content-Range": `bytes ${start}-${end - 1}/${video_size}` } });
    if (!res.ok) fail(`TikTok chunk ${i}: ${res.status} ${await res.text()}`);
  }
}

export async function post(file, caption, mode = "draft") {
  const source_info = { source: "FILE_UPLOAD", ...chunks(statSync(file).size) };
  let init;
  if (mode === "draft") {
    init = await tt("/post/publish/inbox/video/init/", { source_info });
  } else {
    const { privacy_level_options } = await tt("/post/publish/creator_info/query/");
    const privacy_level = mode === "public" ? "PUBLIC_TO_EVERYONE" : "SELF_ONLY";
    if (!privacy_level_options.includes(privacy_level)) fail(`TikTok allows only ${privacy_level_options} for this app`);
    init = await tt("/post/publish/video/init/", {
      post_info: { title: caption.slice(0, 2200), privacy_level, disable_duet: false, disable_stitch: false, disable_comment: false, is_aigc: false },
      source_info,
    });
  }
  await upload(init.upload_url, file, source_info);
  for (;;) {
    const s = await tt("/post/publish/status/fetch/", { publish_id: init.publish_id });
    if (s.status === "FAILED") fail(`TikTok publish failed: ${s.fail_reason}`);
    if (s.status === "SEND_TO_USER_INBOX") return { remote: init.publish_id, url: null, note: "draft in TikTok inbox: open the app and post it (expires in 24 h)" };
    if (s.status === "PUBLISH_COMPLETE") {
      const id = s.publicaly_available_post_id?.[0];
      return { remote: id ? String(id) : init.publish_id, url: id ? `https://www.tiktok.com/@${(await whoami()).username}/video/${id}` : null };
    }
    await sleep(5000);
  }
}

// Video ids from the ledger are matched against the account's recent videos (drafts get an id once posted).
export async function metrics() {
  const { videos = [] } = await tt("/video/list/?fields=id,title,create_time,share_url,view_count,like_count,comment_count,share_count", { max_count: 20 });
  return videos.map((v) => ({ remote: v.id, created: new Date(v.create_time * 1000).toISOString(), title: v.title?.slice(0, 40), views: v.view_count, likes: v.like_count, comments: v.comment_count, shares: v.share_count, url: v.share_url }));
}
