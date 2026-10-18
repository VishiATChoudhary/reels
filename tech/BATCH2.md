# Batch 2: ten tech reels (agents' brief)

Follow the making-reels skill (~/.claude/skills/making-reels/SKILL.md), ~/shennies/reels/RECIPE.md and
tech/STYLE.md exactly. Copy the reference build tech/sources/p02-jobs-arc.{sh,vo.py,edit.py} into
tech/sources/<ep>.{sh,vo.py,edit.py} and adapt it. Output: public/tech/<ep>/ (vo.wav, words.json, srcmap.json,
edit.json, cuts/) and the render out/<Id>.mp4.

Shared rules for this batch:
- Do NOT edit anything shared: src/, tools/, RECIPE.md, STYLE.md, other episodes, p01/p02. If you need a shared
  change (a new grade, a renderer feature), message the team lead instead.
- Run scripts with bash (lib.sh is bash). Never git commit. No em dashes anywhere.
- Raw downloads that already exist from batch 1 can be symlinked from public/tech/ep0N/raw/ (see the earlier
  scripts tech/sources/ep0N.sh for what each file is and where the good lines are).
- Music: the song is already in public/shared/music/<song>.mp3 and measured (tools/measure_song.py). Use the
  listed drop (track seconds) and beat. Track start offset = drop - climax onset (must be >= 0). If the song's
  beat is fast (>120 bpm), cut on 2-beat units so the build-up cuts stay ~1.5 to 2 s.
- Total length 25 to 40 s. Headline: lowercase curiosity gap, one *italic* word, unique to the reel.
- Render: ./node_modules/.bin/remotion render src/index.ts <Id> out/<Id>.mp4 --codec=h264 --crf=18
  --pixel-format=yuv420p --audio-bitrate=320k. Then do the skill's quick check (contact sheet, frame 0, drop
  frames, LUFS) and fix what's wrong before reporting.
- Report: the story lines used (setup / low / turn / climax word / payoff), headline, song + offset + drop
  time in the reel, length, what you could not get, anything you're unsure of.

| Id | ep | Speaker / story | Song (drop s, bpm) | Sources |
|---|---|---|---|---|
| Tech-P03-Feynman | p03-feynman | Feynman 1985 "Can machines think?": machines won't think like us (cheetah/wheels, birds/airplanes) but do it better | before.mp3 (29.11, 131.9) | ep03 raw (ipRvjS7q1DI) |
| Tech-P04-Selfridge | p04-selfridge | Selfridge 1961, The Thinking Machine: "machines can and will think in our lifetime" | medusa.mp3 (10.11 or 40.42, 130.4) | ep01 raw (aygSMgK3BEM) |
| Tech-P05-Clarke | p05-clarke | Arthur C. Clarke 1964 BBC Horizon: "men will no longer commute, they will communicate" | utopia.mp3 (51.20, 75.0) | ep02 raw (YwELr8ir9qM) |
| Tech-P06-Hinton | p06-hinton | Hinton, 60 Minutes 2023: can't see a path that guarantees safety | storms-coming.mp3 (42.67, 135.1) | ep05 raw (qrvK_KuIeJk) |
| Tech-P07-Move37 | p07-move37 | AlphaGo vs Lee Sedol 2016, move 37: "I thought it was a mistake" > Fan Hui "it's beautiful" | strike-me-down.mp3 (41.74, 92.0) | ep06 raw (WXuK6gekU1Y doc) |
| Tech-P08-Karpathy | p08-karpathy | Karpathy 2025: software 1.0, 2.0, 3.0: prompts are programs, written in English | mercy.mp3 (37.40, 153.9) | ep07 raw (LCEmiRjPEtQ) |
| Tech-P09-Hassabis | p09-hassabis | Hassabis: protein folding took a PhD years, AlphaFold did 200 million, end of disease | savior.mp3 (48.01, 80.0) | ep08 raw (1XF-NG_35NE) + AlphaFold doc |
| Tech-P10-Jobs-Life | p10-jobs-life | Jobs 1994 (Silicon Valley Historical Assoc.): "everything around you that you call life was made up by people that were no smarter than you" | let-me-fall.mp3 (41.30 or 20.65, 93.0) | new: find the 1994 interview |
| Tech-P11-Jensen | p11-jensen | Jensen Huang, Stanford GSB 2024: "I wish upon you ample doses of pain and suffering" (resilience, how NVIDIA almost died) | humble-yourself.mp3 (49.63, 154.8) | new |
| Tech-P12-Hopper | p12-hopper | Grace Hopper: "the most dangerous phrase is 'we've always done it this way'" or the nanosecond wire (Letterman 1986) | for-you.mp3 (19.72, 166.7) | new |
