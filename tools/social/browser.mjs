// Fallback for when an API can't do it (TikTok public posts before the app audit): a real Chrome with its own
// profile in ~/.reels/chrome. Log in once with `npm run social -- login tiktok-browser`; the session sticks.
// Drives TikTok Studio's upload page, so it breaks if TikTok changes the page: failures save a screenshot to out/.
import { homedir } from "node:os";
import { join, resolve } from "node:path";
import { chromium } from "playwright-core";

const PROFILE = join(homedir(), ".reels", "chrome");
const UPLOAD = "https://www.tiktok.com/tiktokstudio/upload";

const open = (headless) => chromium.launchPersistentContext(PROFILE, { channel: "chrome", headless, viewport: { width: 1280, height: 900 } });

export async function login() {
  const ctx = await open(false);
  const page = ctx.pages()[0] ?? await ctx.newPage();
  await page.goto("https://www.tiktok.com/login");
  console.log("Log in to TikTok in the Chrome window, then close it.");
  await new Promise((r) => ctx.on("close", r));
}

export async function post(file, caption, { headless = false } = {}) {
  const ctx = await open(headless);
  const page = ctx.pages()[0] ?? await ctx.newPage();
  try {
    await page.goto(UPLOAD, { waitUntil: "domcontentloaded" });
    if (page.url().includes("/login")) throw new Error("not logged in: npm run social -- login tiktok-browser");
    await page.locator('input[type="file"]').setInputFiles(resolve(file), { timeout: 60e3 });
    const editor = page.locator('div[contenteditable="true"]').first();
    await editor.waitFor({ timeout: 120e3 });
    await editor.click();
    await page.keyboard.press("Meta+A");
    await page.keyboard.press("Backspace");
    for (const line of caption.split("\n")) { await page.keyboard.insertText(line); await page.keyboard.press("Shift+Enter"); }
    await page.keyboard.press("Escape"); // close the hashtag suggestion popup
    const postButton = page.locator('button[data-e2e="post_video_button"]');
    await page.waitForFunction((el) => el && !el.disabled && el.getAttribute("data-disabled") !== "true", await postButton.elementHandle({ timeout: 300e3 }), { timeout: 300e3 });
    await postButton.click();
    await page.waitForURL(/tiktokstudio\/content/, { timeout: 180e3 });
    return { remote: null, url: null, note: "posted through TikTok Studio" };
  } catch (e) {
    await page.screenshot({ path: "out/tiktok-browser-fail.png" }).catch(() => {});
    throw new Error(`${e.message} (screenshot: out/tiktok-browser-fail.png)`);
  } finally { await ctx.close(); }
}
