# AI can sound right even when it's wrong (ink film 01)

Source: Seb's AI_Danger_Video_Production_Kit (Nov 8 2026). Made our own for @autopilot.oi: 90 seconds, vertical, the ink draws itself.

## Audit of the kit
| Kit | Problem for us | Our version |
|---|---|---|
| 2:49 runtime | Our TikToks average about 100 views and drop early; nearly 3 minutes is a YouTube length | about 85 to 90 s, still over 1 minute |
| Opens on a question ("What if the most dangerous thing...") | Slow, abstract first 3 seconds | Opens on the proof: a fluent AI answer citing a study, then "The study it cites does not exist." |
| Real hand + compositing, or AI video hands | We have no hand footage; AI hands and AI text fail the kit's own QC | Vector poster drawn by a pen held from out of frame, real path write-on. Every letter is our own single-stroke hand lettering, so nothing is misspelled or garbled |
| Red only at 1:18 | Fine as a color story, but late for a short | Red still enters at the twist ("But here's the catch"), now at about 0:38, and then calls back to the hook: it circles the fake citation and writes NOT REAL |
| Ending is a thesis line | No reason to save or share | Same thesis on the page, plus "Save this for the next time an answer sounds a little too sure." |
| Dashes in the title (kit uses "RIGHT — EVEN") | Breaks our no dashes rule | All on screen text and copy without dashes |

Accuracy fixes, kept from the kit's own QA notes:
- "doesn't automatically check every claim" became "On its own, it doesn't check its claims against reality", because tools with search or files attached do look things up (and can still be wrong).
- "Training tunes billions of numbers so the model gets very good at predicting what comes next" names the pretraining objective without claiming it is all the model can do.
- Named ChatGPT and Claude as chatbots (generative language models), not "AI" in general.
- The fake answer is labelled SAMPLE on the card; "Dr. L. Moreno" is fictional. No real people, faces, headlines or brands are drawn.
- Risk panels match the kit and NIST's generative AI profile: false answers, deepfakes, privacy, bias, scale.

## Look (Seb, Nov 8)
Black ink only, lime highlighter for emphasis (the fake citation, AI, TRAINING, TOKENS, USEFUL, the twist line, NOT REAL, the three boxes, WITH TRUTH.). Bold lettering, small captions. Ends on a hand drawn ap. logo: lime highlighter square, black letters, then the full page.

## Brand fit
Our rule for every helper is "it drafts, you send". This film argues for exactly that (VERIFY, PROTECT DATA, HUMAN REVIEW), without selling anything, so it works as a trust builder and a test of a new format. The page is signed AUTOPILOT.OI in the corner.

## Script (204 words)
1. This answer sounds perfect.
2. The study it cites does not exist.
3. Here's why AI does that, and how to use it anyway.
4. Chatbots like ChatGPT and Claude learn from huge amounts of text.
5. Training tunes billions of numbers so the model gets very good at predicting what comes next.
6. Your question is split into small pieces called tokens. The answer is built the same way, one piece at a time.
7. And that is useful. It can translate, explain, draft and write code in seconds.
8. But here's the catch. Sounding true is not the same as being true.
9. On its own, it doesn't check its claims against reality. So it can invent a number, a quote or a source, in the same confident voice.
10. Now add cloned voices and fake video. Private data pasted into the wrong tool. Unfair patterns copied from old data. And one small mistake repeated across a thousand messages.
11. So treat it like a fast assistant, not a judge. Verify what matters. Keep private data out. And let a person review it before it goes out.
12. AI isn't the danger. Confusing a confident answer with the truth is.
13. Save this for the next time an answer sounds a little too sure.

## Page (locked master, sheet units 1000 x 1414)
Title HOW AI WORKS / AND WHY IT CAN BE WRONG. Hook card (AI ANSWER, SAMPLE). Blue: DATA icons, network, TRAINING, PREDICT → COMPARE → ADJUST, tokens (WHAT IS A TOK EN ?). Green: USEFUL with TRANSLATE, EXPLAIN, DRAFT, CODE. Red: SOUNDS TRUE ≠ IS TRUE, arrow to the hook, ring + NOT REAL, five risk panels. Footer: A FAST ASSISTANT, NOT A JUDGE, three checked boxes, DON'T CONFUSE CONFIDENCE WITH TRUTH., signature. Every shot is a crop of this one page; ink only accumulates.

## Pipeline
`tools/ink/` (new): `films/<stem>.json` (beats, page elements cued on spoken words, camera boxes) → `voice.py` (ElevenLabs Brian, word timings) → `build.py` → `ink.html` (paper, pen, ink, camera, captions) → `render.js` (30 fps, 4 workers) → `mix.py` (pen scratch synced to every stroke, nib taps, room tone, twist pulse, quiet pad, -14 LUFS) → `docs/media/ink/<stem>.mp4`.
Run: GitHub Actions "Ink" workflow with the stem, or `FAKE=1 bash tools/ink/make.sh <stem>` for a silent timing preview.
Next films reuse the engine: write a new `films/<stem>.json`.

## Post package
- TikTok title: AI can sound right even when it's wrong
- Caption: This answer sounds perfect. The study it cites does not exist. How AI writes answers, and the 3 checks to run before you trust one. Save this for later. #ai #chatgpt #claudeai #aitips #learnontiktok
- Settings: isAigc true (AI voice), autoAddMusic false, PUBLIC_TO_EVERYONE.
- Instagram Reel: same caption; first frame is the hook card.
- 3 clips to cut after the first data: the hook to the twist (0:00 to 0:45), the risks (0:38 to 1:05), the rules (1:05 to end).

## QC checklist
Spelling on every label (the lettering comes from code, not from an image model); ink never disappears; pen nib on the line while drawing; no frame where captions hide the line being drawn; red first appears at the twist; hook readable at phone size in frame 1; final page held about 4 s; loudness about -14 LUFS.
