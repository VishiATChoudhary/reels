# reels

Short-form edits (9:16, ~30 s) for TikTok, Reels and X, in themes (tech, sports, history). One real voice tells
a story, the turning word lands on the song's drop. One Remotion project; the recipe is `RECIPE.md`.

```
themes/<theme>.json    song pool, grades + arc palette, frame, handle, registered episodes
themes/songs.json      shared song library (bpm, drop); files in public/shared/music/
themes/grades.json     shared ffmpeg grades
<theme>/THEME.md       voices, story shape, b-roll, headline voice, story bank
<theme>/episodes/      one spec per reel (<ep>.yaml)
src/shared/Edit.tsx    the renderer (card or wide frame, captions, glass caps, headline, music, voice)
src/Root.tsx           one Remotion folder per theme, from themes/*.json
tools/reel.py          new | build | words | check
tools/measure_song.py  bpm + drop of a new song
tech/sources/          older per-episode scripts (P03 to P12 still rebuild from there, with tools/lib.sh)
public/<theme>/<ep>/   vo.wav, words.json, srcmap.json, edit.json, cuts/, raw/ (media git-ignored)
```

- New reel: `python3 tools/reel.py new sports p01-jordan`, fill the spec, `python3 tools/reel.py build sports/p01-jordan`
- Preview: `npm run studio`
- Render: `npm run render` (all) or `npm run render -- Sports-P01`; check: `python3 tools/reel.py check <Id>`
- Post: write `posts/<Id>.txt`, then `npm run post -- <Id>` (X, Instagram, TikTok on their official APIs, keys in the
  Keychain vault). `npm run social -- setup` lists missing keys and where to get them; `whoami`, `metrics` (per reel, per
  platform, from `posts/ledger.jsonl`). Flags: `--only x,instagram`, `--dry`, `--tiktok draft|private|public|browser`
  (TikTok is inbox drafts until the app is audited; `browser` posts publicly through a Chrome profile you log into once
  with `npm run social -- login tiktok-browser`). Code in `tools/social/`.
- Handle: `handle` in each `themes/<theme>.json` (one account per theme, or the same everywhere).

All footage and music is third-party: never commit `public/` media. Platforms may mute or take down
copyrighted audio; swap in an in-app sound when posting if that happens.
