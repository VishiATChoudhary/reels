# Tech shorts: sourcing brief (for each episode)

Format (copied from the reference edits in ~/shennies/synapse/promo/shorts/REFERENCES.md):
one real voice from computing / AI history, 15 to 20 s, 9:16, word-by-word captions, cinematic tech b-roll,
fast cuts (0.25 to 0.5 s) in the first third, slower (1 to 2 s) when the key line lands. Music under the voice
at a constant level, never ducked. No app plug, no end card. Watermark @HANDLE placeholder.

Taste: archival scientist vibe (Selfridge, The Thinking Machine 1961) loved. NO pop culture (no sports, films,
cartoons, celebrities, hip hop refs), no motivational-quote clichés, nothing playful or cartoonish. Tech-centred
b-roll only: labs, computers, chips, fabs, data centres, robots, code, neural nets, scientists, archive film.

## Output contract: public/tech/<ep>/
- vo.wav: the voice line (via `vo`), 12 to 18 s, starts on the first word, ends after the last word.
- words.json: [{"w","s","e"}] seconds from vo start, spelling and punctuation corrected by hand
  (copy words.raw.json from `words`). Keep one entry per spoken word.
- music.mp3: the soundtrack (via `music <id> <start>`), instrumental only, start offset picked so the
  track is already moving (or a build that lands near the key line).
- cuts/<name>.mp4: graded shots via `shot` (fill = 1080x1920 full-bleed; wide = 1080x608 for letterbox/cards).
  Make 10 to 16 shots, each a bit longer than it will be used (0.6 to 3 s).
- meta.json:
  {
    "speaker": "Oliver Selfridge", "where": "MIT", "year": "1961",
    "hook": "THINK",                     // 1 word shown big in the first 0.6 s, before the voice
    "voDelay": 0.6,                      // s before the voice starts
    "music": {"title": "...", "url": "https://youtube.com/watch?v=...", "start": 12.0},
    "fit": "fill" | "wide",
    "shots": [ {"name": "selfridge", "dur": 0.4, "note": "what it shows"}, ... ],  // the edit, in order;
                                          // durs sum to voDelay + vo length + ~1.2 s tail
    "keyWords": ["think", "lifetime"]    // 2 to 4 words to emphasise (bigger caption + motion hit)
  }
- Reproducible: write the whole thing as tech/sources/<ep>.sh (bash, `source ../../tools/lib.sh`, `ep tech <ep>`),
  run it, and check the result.

## Tools
`source ~/shennies/reels/tools/lib.sh` gives: ep, get, music, shot, vo, words, transcript, grades $BW $OLD $NOW $DARK.
yt-dlp search: `yt-dlp --cookies-from-browser chrome --flat-playlist --print "%(id)s %(duration)s %(title)s" "ytsearch8:<query>"`.
Already-downloaded archive you may reuse (cp into raw/): ~/shennies/synapse/promo/public/broll/*.mp4 (see
~/shennies/synapse/promo/broll.sh for what each id is: Thinking Machine 1961, Shannon Theseus, Macintosh 1984,
Jobs bicycle 1990, circuit boards, chips, Intel fab, Foxconn line, neural net sim, AlphaGo trailer, AlphaFold,
DevDay 2023, Nobel 2024) and ~/shennies/synapse/promo/public/stock/raw-*.mp4 (modern stock: servers, chips, code).
Check footage by making a contact sheet (ffmpeg tile) and reading the image. Check vo with `words`.
Cuts must be yuv420p. Never git commit anything under public/.
