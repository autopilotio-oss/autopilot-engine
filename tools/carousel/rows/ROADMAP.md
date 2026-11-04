# THE ORGANISM: the IG design system

Seb approved the direction Nov 4 2026 ("Better we are getting there"). This file keeps it alive.
Every new IG drop follows it. Nothing else goes on the grid.

## The idea in one line
An AI comes to life on our profile, one row at a time. Each row is one cinematic image cut into 3 posts:
we TEACH (left), it GROWS (middle), we SELL (right).

## The rules (never break)
1. **One row = one render = 3 posts.** A 21:9 Nano Banana image, cut by `row.py`. Never post a single tile out of a row.
2. **Publish order is R, then M, then L** (right first, left last). The newest post sits top left, so this lands as L M R on the grid.
   2 posts per day max: R + M on day one 18:00 and 20:30, L next morning 10:00.
   The grid must already be a multiple of 3 before a row drops, or every row lands shifted.
3. **Same world every row:** dark graphite void, haze, white porcelain, lime #D4FF3A light, lime cables from the top, nerves flowing sideways across all 3 panels.
4. **Left panel stays mostly empty dark space** for the LEARN headline. **Right panel always has the floating black glass tablet**, which carries the product screen. That tablet is the store signature.
5. **Middle panel gets almost no text:** CHAPTER nn + 2 word name. The image does the talking.
6. **One type system:** Anton headlines, last line lime. Chakra Petch / mono labels. No other fonts, no stickers, no emojis on the image.
7. **Restraint.** No puns in the image, no props that spell out the headline. The story is in the organism, the hook is in the words.
8. **Truth.** Real products, real prices from the store. No invented numbers or results. Label examples SAMPLE.

## How to make a row (15 minutes)
1. Pick the next chapter below. Paste its Runway prompt (template at the bottom).
2. Save the render as `tools/carousel/rows/chNN-render.png`.
3. Copy `ch01.json` to `chNN.json`, set titles from the title bank.
4. `python3 tools/carousel/rows/row.py tools/carousel/rows/chNN.json --grid` and read the tablet screen corners (TL TR BR BL) off `grid_R.png`.
5. Put the corners in the json, run without `--grid`. Check `docs/media/rows/<id>/row.jpg`.
6. Queue record with Seb's approval quote, then schedule R, M, L.

## Chapters (the story)
| # | Name | Middle (the organism) | Store (right) |
|---|------|------------------------|---------------|
| 01 | It wakes. | porcelain head, lime eyes opening | Front Desk Kit $39 |
| 02 | It reaches. | porcelain hand, palm open, reaching right | Invoice Chaser |
| 03 | It listens. | porcelain head in profile, faint lime sound rings at the ear | Front Desk Kit $39 |
| 04 | It remembers. | porcelain brain in a glass dome, lime light in the folds | Bookkeeping Sorter |
| 05 | It speaks. | porcelain lower face, lips parted, lime light behind the teeth line | Review Desk |
| 06 | It sees. | single porcelain eye orb, lime iris | Content Week |
| 07 | It breathes. | lungs, half porcelain machine, half moss | Office Autopilot $79 |
| 08 | It feels. | porcelain heart, lime seams, mid beat | All in bundle |
| 09 | It builds. | two porcelain hands assembling a small glowing lime cube | Workspace waitlist |

After 09: season 2 (it learns to work: the office, the phone, the inbox). Ask Seb before starting.

## Title bank
Formula: 2 to 5 short lines, max 4 words per line, the last line is the payoff in lime. No dashes. No fake numbers.

LEARN (left, carousel covers)
- Prompts / that / should / be illegal.
- Prompts / that feel / like cheating.
- Stop typing. / Start / delegating.
- Copy these / before / Monday.
- Steal / this / follow up.
- The texts / that get / you paid.
- Nobody / tells owners / this.
- Your competitor / already / uses this.
- Claude did / my books. / I checked.
- Reviews / answered / while you sleep.

STORE (right)
- Your front desk. / On autopilot.   (Front Desk Kit)
- Chase invoices. / Skip the awkward.   (Invoice Chaser)
- Receipts in. / Books sorted.   (Bookkeeping Sorter)
- Every review. / Answered.   (Review Desk)
- A week of posts. / By Monday.   (Content Week)
- The whole office. / One kit.   (Office Autopilot)

## One row = one poster (Seb Nov 4: "the 3 posts feel separate")
- row.py paints out any divider lines the model draws and evens the lighting at the cuts, so the nerves run straight across.
- Type is one system across the row: AUTOPILOT.OI top left of L, THE STORE top right of R, nothing on top of M.
  Both headlines sit on the same baseline, same size. One footer line across all three: L hint, M "CHAPTER nn  NAME", R "LINK IN BIO".

## Runway / Nano Banana prompt template (v3)
v1 (ch01) look is the keeper: smooth clean glowing strands, serene porcelain. v2 (roots, tentacles, a cable cross) was rejected Nov 4.
v3 keeps the ch01 look and only asks for one seamless frame. Swap CENTER and nothing else.

```
Generate 1 image with Nano Banana. Ultra wide aspect ratio 21:9. Match the attached reference image exactly in material, lighting, haze, color and the style of the glowing strands. Render ONE seamless continuous photograph: no panels, no borders, no dividing lines, no frames, even lighting and haze across the whole width.

Restrained, elegant, cinematic 3D render, Octane realism, dark graphite void with soft haze and faint volumetric light from above, fine film grain, shallow depth of field.

CENTER of the image: CENTER. White porcelain with fine panel seams, soft acid lime (#D4FF3A) light glowing from inside. It is suspended by a few thin glowing lime fiber optic strands coming down from the top of the frame.

THE FLOW: smooth, clean strands like in the reference, some white, some glowing lime, flowing out of both sides of the subject in long gentle curves. On the left they drift out of the frame through the left edge at mid height. On the right they sweep across and wrap loosely around a floating matte black glass tablet (portrait, tilted slightly, edges glowing faint lime, screen dark and blank) at about 80 percent of the width, then continue out of the right edge. Strands are smooth and graceful, not roots, not tentacles, no branching, nothing straight or stiff.

Keep the left 30 percent mostly dark and empty except the strands at mid height. Lots of negative space. No text, no letters, no logos, no watermark, no people, no full bodies.
```
Attach `ch01-render.png` as the reference every time so the world never drifts.
