// X API v2 with OAuth 1.0a user context: the app's consumer keys plus the access token generated for your
// own account in the developer portal. No login flow needed. Pay-per-use credits apply to every call.
import { createHmac, randomBytes } from "node:crypto";
import { readFileSync, statSync } from "node:fs";
import { fail, request, sleep, vault } from "./lib.mjs";

const API = "https://api.x.com/2";
const KEYS = ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET"];
const pct = (s) => encodeURIComponent(s).replace(/[!'()*]/g, (c) => `%${c.charCodeAt(0).toString(16).toUpperCase()}`);

// JSON and multipart bodies are not part of the signature, only the oauth params and the query string.
export function sign(method, url, creds = KEYS.map((k) => vault.need(k, "developer.x.com > your app > Keys and tokens")),
  nonce = randomBytes(16).toString("hex"), timestamp = String(Math.floor(Date.now() / 1000))) {
  const [key, secret, token, tokenSecret] = creds;
  const u = new URL(url);
  const oauth = {
    oauth_consumer_key: key, oauth_nonce: nonce, oauth_signature_method: "HMAC-SHA1",
    oauth_timestamp: timestamp, oauth_token: token, oauth_version: "1.0",
  };
  const params = [...Object.entries(oauth), ...u.searchParams].map(([k, v]) => [pct(k), pct(v)]).sort(([a, x], [b, y]) => a < b ? -1 : a > b ? 1 : x < y ? -1 : 1);
  const base = [method, pct(u.origin + u.pathname), pct(params.map(([k, v]) => `${k}=${v}`).join("&"))].join("&");
  oauth.oauth_signature = createHmac("sha1", `${pct(secret)}&${pct(tokenSecret)}`).update(base).digest("base64");
  return "OAuth " + Object.entries(oauth).map(([k, v]) => `${pct(k)}="${pct(v)}"`).join(", ");
}

const x = (method, path, body) => {
  const url = `${API}${path}`;
  const json = body && !(body instanceof FormData);
  return request(url, {
    method, body: json ? JSON.stringify(body) : body,
    headers: { Authorization: sign(method, url), ...(json && { "Content-Type": "application/json" }) },
  });
};

export const ready = () => KEYS.every((k) => vault.get(k));
export const whoami = async () => (await x("GET", "/users/me?user.fields=public_metrics")).data;

async function upload(file) {
  const size = statSync(file).size, bytes = readFileSync(file), CHUNK = 4 * 1024 * 1024;
  const { data: { id } } = await x("POST", "/media/upload/initialize", { media_type: "video/mp4", media_category: "tweet_video", total_bytes: size });
  for (let i = 0; i * CHUNK < size; i++) {
    const form = new FormData();
    form.append("segment_index", String(i));
    form.append("media", new Blob([bytes.subarray(i * CHUNK, (i + 1) * CHUNK)]), "chunk");
    await x("POST", `/media/upload/${id}/append`, form);
  }
  let info = (await x("POST", `/media/upload/${id}/finalize`)).data.processing_info;
  while (info && !["succeeded", "failed"].includes(info.state)) {
    await sleep((info.check_after_secs ?? 2) * 1000);
    info = (await x("GET", `/media/upload?command=STATUS&media_id=${id}`)).data.processing_info;
  }
  if (info?.state === "failed") fail(`X media processing failed: ${JSON.stringify(info)}`);
  return id;
}

export async function post(file, text) {
  if (text.length > 280) text = text.split(/\n\s*\n/)[0].slice(0, 280); // first paragraph fits the limit
  const media = await upload(file);
  const { data } = await x("POST", "/tweets", { text, media: { media_ids: [media] } });
  const me = await whoami();
  return { remote: data.id, url: `https://x.com/${me.username}/status/${data.id}` };
}

export async function metrics(ids) {
  if (!ids.length) return [];
  const { data = [] } = await x("GET", `/tweets?ids=${ids.join(",")}&tweet.fields=public_metrics,created_at`);
  return data.map((t) => ({ remote: t.id, created: t.created_at, ...t.public_metrics }));
}
