// Shared bits: Keychain vault, fetch with errors, post ledger, small helpers.
import { execFileSync } from "node:child_process";
import { appendFileSync, existsSync, readFileSync } from "node:fs";

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export const vault = {
  get: (key) => { try { return execFileSync("vault", ["get", key], { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim() || undefined; } catch { return undefined; } },
  set: (key, value) => execFileSync("vault", ["set", key], { input: String(value), stdio: ["pipe", "ignore", "inherit"] }),
  need: (key, hint) => vault.get(key) ?? fail(`vault key ${key} missing (${hint ?? `vault set ${key}`}); run: npm run social -- setup`),
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
