// Shared bits: credentials, fetch with errors, post ledger, small helpers.
import { execFileSync } from "node:child_process";
import { appendFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Credentials: an environment variable wins, then the `vault` CLI (macOS Keychain) if it is installed, then
// ~/.reels/keys.json (mode 600). Refreshed tokens are written back to whichever store is available.
const KEYS = `${homedir()}/.reels/keys.json`;
const hasVault = (() => { try { execFileSync("vault", ["--help"], { stdio: "ignore" }); return true; } catch { return false; } })();
const file = () => (existsSync(KEYS) ? JSON.parse(readFileSync(KEYS, "utf8")) : {});

export const vault = {
  get: (key) => {
    if (process.env[key]) return process.env[key];
    if (hasVault) { try { return execFileSync("vault", ["get", key], { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim() || undefined; } catch { return undefined; } }
    return file()[key];
  },
  set: (key, value) => {
    if (hasVault) return execFileSync("vault", ["set", key], { input: String(value), stdio: ["pipe", "ignore", "inherit"] });
    mkdirSync(`${homedir()}/.reels`, { recursive: true });
    writeFileSync(KEYS, JSON.stringify({ ...file(), [key]: String(value) }, null, 2), { mode: 0o600 });
  },
  need: (key, hint) => vault.get(key) ?? fail(`credential ${key} missing (${hint ?? key}): export it, or add it to ~/.reels/keys.json; run: npm run social -- setup`),
};

export function fail(msg) { throw new Error(msg); }

export async function request(url, init = {}) {
  const res = await fetch(url, init);
  const text = await res.text();
  let body; try { body = JSON.parse(text); } catch { body = text; }
  if (!res.ok) fail(`${init.method ?? "GET"} ${url.split("?")[0]}: ${res.status} ${typeof body === "string" ? body : JSON.stringify(body)}`);
  return body;
}

// posts/ledger.jsonl: one line per published post, so metrics know what to look up.
const LEDGER = "posts/ledger.jsonl";
export const ledger = {
  add: (entry) => appendFileSync(LEDGER, JSON.stringify({ at: new Date().toISOString(), ...entry }) + "\n"),
  all: () => existsSync(LEDGER) ? readFileSync(LEDGER, "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l)) : [],
};

export function caption(id) {
  const file = `posts/${id}.txt`;
  if (!existsSync(file)) fail(`missing ${file}`);
  return readFileSync(file, "utf8").trim();
}
