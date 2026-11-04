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

## Runway / Nano Banana prompt template (v2, Seb Nov 4: "needs to have a natural flow")
v1 problems: the nerves stopped dead in the left panel, the model drew hard divider lines, cables pierced the subject like puppet strings, curves were stiff.
v2 fixes: one seamless current of light that enters at the left edge and leaves at the right edge, a vertical spine of cables through the middle that continues into the rows above and below, nerves that grow out of the subject instead of stabbing into it.
Swap CENTER and nothing else.

```
Generate 1 image with Nano Banana. Ultra wide aspect ratio 21:9. Use the attached image only as a style reference for material, lighting, haze and color. It will be cut into 3 vertical posts later, but render ONE seamless continuous image: no panels, no borders, no dividing lines, no frames.

Restrained, elegant, cinematic 3D render, Octane realism, dark graphite void with soft haze and faint volumetric light from above, fine film grain.

THE FLOW: one continuous current of delicate nerve fibers flows across the whole image like a slow river of light. It enters at the left edge at mid height as a thin loose stream, widens as it travels, curves gently in a soft S shape, passes through the subject, then narrows and leaves the right edge at mid height. The fibers are organic like real nerves and mycelium: soft curves, different thicknesses, a few fine branches, some fibers close to camera and out of focus, some far behind and hazy. They are white porcelain colored, and acid lime (#D4FF3A) light pulses travel along some of them. Nothing is straight, nothing is stiff.

THE SPINE: a thin bundle of glowing lime fiber optic cables hangs from the top center of the image and continues below the subject out of the bottom center of the image, so the scene connects to whatever is above and below it.

CENTER (middle third): CENTER. White porcelain with fine panel seams, soft lime light glowing from inside. The nerve fibers grow out of the subject naturally and become part of it. No cables stabbing into it, no puppet strings.

RIGHT third: the current wraps loosely around a floating matte black glass tablet, portrait orientation, tilted slightly, edges glowing faint lime, screen dark and blank, centered in the right third.

LEFT third: only the thin incoming stream at mid height and the soft haze. The upper half and lower half of the left third stay clean and dark.

Lots of negative space. No text, no letters, no logos, no watermark, no people, no full bodies.
```
Attach `ch01-render.png` as the style reference every time so the world never drifts.
