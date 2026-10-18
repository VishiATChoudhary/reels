# The reel recipe

How to make a short in the approved style, in any theme. Reference spec: `tech/episodes/p02-jobs-arc.yaml`
(Jobs, "a bicycle for our minds", 34 s, on WILD). Visual spec measured from the reference edits: `tech/STYLE.md`.

## Workflow
```
python3 tools/reel.py new <theme> <ep>            # <theme>/episodes/<ep>.yaml from the template, registered
python3 tools/reel.py build <theme>/<ep> --only fetch   # sources into raw/
python3 tools/reel.py build <theme>/<ep> --only voice   # vo.wav, srcmap.json, words.json; prints words + times
python3 tools/reel.py build <theme>/<ep>          # everything: fetch, voice, edit.json (+ lint), cuts/
npm run render -- <Id>
python3 tools/reel.py check <Id>                  # contact sheet, hook + drop frames, loudness
```
Iterate on the spec only: re-running is cheap (whisper passes and unchanged cuts are cached).
The format is the same in every theme. What changes per theme lives in two places:
- `themes/<theme>.json`: song pool, grades and the arc palette (the lint warns on off-palette shots), frame, handle.
- `<theme>/THEME.md`: voices, story shape, what the drop is, b-roll, headline voice, and a story bank.
Songs are shared: `themes/songs.json` (bpm + drop). Grades are shared: `themes/grades.json` (+ theme extras).

## 0. Pick the theme
Read `<theme>/THEME.md`. Pick a story from its bank or find one with the same shape. A new theme = a new
`themes/<theme>.json` (copy one), a `<theme>/THEME.md`, and one import line in `src/Root.tsx`.

## The idea in one line
One real voice tells a small story. The song's build-up carries the setup, **the story's turning word lands
on the drop**, the payoff rides the beat. One continuous take: music and voice from frame 1, never a stop.

## 1. Pick the story (before downloading anything)
A clip qualifies if it has all four, in order, from one speaker:
| Part | Jobs example | Length |
|---|---|---|
| Setup | "The condor used the least energy... humans came in with a rather unimpressive showing" | 8 to 10 s |
| Low point | "It was not too proud a showing for the crown of creation" | 3 to 5 s |
| Turn (rising) | "but then somebody had the insight to test... a man on a bicycle" | 5 to 7 s |
| **Climax word** → drop | "**blew** the condor away, completely off the top of the charts" | lands on the drop |
| Payoff | "that's what a computer is to me... a bicycle for our minds" | 8 to 14 s |

The payoff may come from a second voice in the same source when the first speaker runs out (Selfridge's
"in our lifetime" answered by Shannon's "something will emerge from the laboratories", both in The Thinking
Machine, 1961).

Setup + low point + turn must fit inside the song's build-up (WILD: 20.4 s). Cut lines to fit, never speed
the voice. Trim at sentence ends or before conjunctions ("but then somebody | had the insight").

## 2. Pick the song
From the theme's pool (`themes/<theme>.json`), Encore type beats (youtube.com/@Encorebeats). A new song:
`python3 tools/measure_song.py public/shared/music/<song>.mp3`, check the drop by ear, add it to
`themes/songs.json` (WILD: 95.83 BPM, drop at 20.40 s). `song: wild` in the spec; `bpm:` / `song_drop:` override.

## 3. Voice (spec `voice:`)
1. `segments`: `[src start, src end, gap after]` (or `[source, start, end, gap]` for a second voice or file).
   Gaps: 0.04 inside a sentence, 0.12 to 0.4 between, 0.35 before the climax (tension).
2. `climax: {seg: N, word: blew}`: segment N starts on the climax word (split a segment with gap 0 if needed).
   The tool measures its onset on the waveform (first 10 ms above 15% of peak); `onset:` overrides.
   `drop = reel time of the onset`; `track start = song drop - drop`. Must be ≥ 0: the tool stops if not: cut a line.
3. `whisper:` caption times come from the source, mapped through the splices (the spliced voice drifts).
   `single` = one pass per file; `segments` = each piece alone (old tapes drift on a long pass: Feynman 1985,
   0.7 s); `[[a, b], ...]` = contiguous windows (short pieces are heard badly alone). `fix:` corrects mishearings.
4. Automatic: voice from 0.0 s, first word on screen in frame 1, word ends capped at +0.5 s, the climax
   word snapped to the drop, the gappy voice lifted to ~-15 LUFS under a limiter (`lift: false` to skip).
5. Check every segment boundary by ear and in the printed words: clipped first words ("It"), tails of cut
   lines ("look so good") and stray words ("is") show up there.

## 4. Footage (spec `sources:` and `shots:`)
- `sources:` name each file: `{url, section}` (yt-dlp), `{link: theme/ep/name}` (reuse a download) or `{file}`.
  `crop:` removes pillar/letterboxes (`cropdetect`) for every cut from that source.
- A shot: `<time> <name> <source>@<start> <GRADE> [zoom=1.6] [origin=50%,18%] [flash] [crop=..] [len=..]`.
  Cut length is automatic (until the next shot + 0.3 s); cuts are graded and sized to the frame.
- **Speaker shots are lip-synced**: `<source>@sync` starts the cut at the source time under the voice there
  (`@sync+0.15` to step past a cutaway). Check the source has the speaker on screen there (sources cut away).
- **B-roll is literal**: each phrase shows what it says (condor, apes for "humans", the species chart,
  cyclists, the 2001 bone for "tool"). Film scenes and archive both fine. No HUD, no stock-looking filler.
- Grades, one dominant colour per shot, from the theme's arc palette: `build` before the drop (muted, lonely),
  `turn` for the riser, `speaker`, `payoff` after the drop (alive). Alternate warm and cold.

## 5. The edit (spec `shots:` times, written to `edit.json`)
Beat grid: `b(n) = drop + n × 60/BPM`. Cut on it: shot times are `bN` (`b-30`, `b-1.5`, `b0`), `sN` (segment N
starts, for lip-synced turns) or seconds, each `+/-` an offset. `end:` and `headline_to:` use the same.
| Section | Cuts | Notes |
|---|---|---|
| **Hook, 0 to ~1.2 s** | 1 | Speaker's face on frame 1 (zoom 1.6, origin on the face), lip-synced. |
| Setup + low point | every 3 beats | slow, muted; return to the speaker once mid-way |
| Turn | at the segment start, then 2 beats | archive of the thing that changes everything |
| Riser, last 5 beats | 1 beat, then ½ beat | tightening into the drop |
| **Drop** | on b(0), `flash: true` | the most kinetic shot you have |
| Payoff | every 1 to 2 beats | speaker once (lip-synced), literal shots, end on the speaker not talking |
| End | b(drop + 3 beats after the last word) | 0.35 s fade to black |

## 6. Words on screen
- **Headline** above the card, frame 1 to ~3 s, no fade: a curiosity gap in lowercase with one `*italic*`
  word ("steve jobs found the answer in a study about *birds*"). It must make sense on mute.
  The theme's THEME.md gives its headline voice.
- **Captions** (in the card's centre): 1 to 3 words per caption, cut at phrase boundaries. In the spec, write
  the words in order (`- the condor | glass`, `- least energy | stack`, `- ~ um` for no caption); the tool
  matches them to the transcript and stops on the first mismatch, showing the words there.
  `stack` for a small lead + big word ("the / condor"), `italic` for the felt phrase ("look so good",
  "is to me"), the climax word alone in italic.
- **Glass caps** (”WORD”, see-through): the first words (hook), the low point, the key noun, the last line.
  3 or 4 per video.

## 7. Render and check
`npm run render -- <Id>`, then `python3 tools/reel.py check <Id>`: a 2 fps contact sheet of the whole video,
frames at 0, 0.5, 1 s (face + headline + glass on frame 1), the frames around the drop (climax caption appears
on the drop cut), loudness ~ -14 LUFS. Read the build's warnings too (palette, hook, flash, glass count).
Music volume 0.32 under voice at -15 LUFS, constant, never ducked, fades only in the last 0.4 s.

## Layout constants (src/shared/Edit.tsx)
Card 1052×1052 at (14, 434), radius 100 (`frame: card`); wide 1080×955 at y 482, hard edges (`frame: wide`). Captions Helvetica Neue 700 lowercase, tracking -0.055 em, fade in
0.1 s. Glass: Helvetica 800 caps in ” ”, overlay blend (never put a transform, opacity or filter on a parent of
the glass: it isolates the blend). Watermark = the theme's `handle` (Michroma, tracked 0.5 em) inside the card
bottom; `look.font` swaps the caption font per theme.

## Mistakes we already made
| Mistake | Fix |
|---|---|
| HUD labels, circuit traces, glitch, terminal overlays | nothing on screen but footage and words |
| Inter/pop-in captions, 16:9 cards | STYLE.md: Helvetica fade-in, square card |
| Generic server-room b-roll | literal shot per phrase |
| Teaser + hard cut to black and silence | one continuous take from frame 1 |
| Story longer than the build-up | cut lines until track start ≥ 0 |
| Whisper times on the spliced voice | map the single source pass through the splices |
| One copied script per episode | one spec per episode, `tools/reel.py` builds it |
| Lip-sync shot starting on a cutaway | check the source frame; shift past the cut (Jobs: 17.12) |
| Captions lingering over a gap | word ends capped at +0.5 s; no captions on a `black` shot |
