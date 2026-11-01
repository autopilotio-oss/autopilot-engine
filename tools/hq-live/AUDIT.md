# BLACKSITE V4: Phase 1 audit and status (Nov 1 2026)

## Architecture (kept)
- Presentation layer only: one HTML page (three.js r170 from jsdelivr) published as a Claude artifact. It never writes to the business systems except two confirmed owner actions (Run now, Pause/Resume a scheduled task).
- Real data in: Claude scheduler (list_triggers), Metricool (getScheduledPosts), Kit (get_growth_stats), and status/hub in the page database written hourly by the ANALYST task (GitHub Actions workers, Gumroad ledger, approvals) from scripts/growthos/hq_feed.py.
- DEMO MODE only with #demo, separate dataset, red banner.
- Nothing in the backend (agents, automations, repo, ledger, Metricool queue) was changed by the visual work.

## Weaknesses found
1. Characters: procedural primitives (capsules and spheres). Fails the V4 gate. Biggest problem.
2. Materials: canvas-generated textures, no PBR maps. Fixed in phase 2.
3. Lighting: flat hemisphere fill, no image-based light, no AO. Partly fixed.
4. Furniture: box geometry. Partly fixed.
5. UI: neon outlines, floating labels over the scene, oversized lime dock. Partly fixed.
6. Hosting limit: the artifact host cannot serve .glb, .bin or .hdr. Worked around (glTF as .json with embedded geometry, HDRI as tonemapped .jpg).
7. Testing limit: headless tests run on a software GPU, so heavy passes (ambient occlusion, MSAA) cannot be verified here; they need a real-GPU check on Seb's devices.

## Phase 2 done (this commit)
- Poly Haven CC0 assets fetched by .github/workflows/hq_assets.yml, packed by tools/hq-live/pack_assets.py: brick (red_brick_03, factory_brick), concrete floor, asphalt, rusted steel, brick factory interior light, metal office desks, hanging industrial lamps, sofa, coffee table, plants, steel shelving, wall clock, arm desk lamps, street lamps, fire escape. Credits: tools/hq-live/assets/CREDITS.md.
- Progressive loading: procedural stand-ins stay until each real asset loads; mobile profile skips street models.
- Rendering: MSAA render target, image-based light from the factory interior, GTAO ambient occlusion on the High profile.
- UI: graphite surfaces, lime only as thin accents, agent labels reduced to small status dots (full card on hover or selection), slimmer dock, softer floor rings.

## Phase 3 (Nov 1): Operative v1 built in-house (Seb: "No you make it")
- MakeHuman body via MPFB2 in headless Blender on GitHub Actions (CC0): real anatomy, face, eyes, skin texture; 52 bone Mixamo-compatible skeleton with fingers.
- CC0 clothes (knit long sleeve recolored to heather black fleece, cargo pants, sneakers) plus in-house modeled hood, knit balaclava with eye slit, kangaroo pocket, drawstrings.
- Fixes found on the way: blended materials made opaque cutout; skeleton rests in T-pose while the mesh is A-pose, so the page rebinds bones to joints measured from skin weights before posing.
- Poses solved by aiming bones at target directions per real state: typing (running), slumped (failed), leaning back (completed), phone or standing (on call), walking.
- Still not AAA: no cloth simulation wrinkles, no finger or eye animation, one body for every agent, procedural rather than motion-captured animation. Next: Mixamo clips (rig is compatible), body and skin variations per agent, eye bones.

## Earlier option list for a commissioned character (kept for reference)
No free asset matches "photoreal masked hoodie operative". Options:
| Option | Cost (estimate) | Time | Notes |
|---|---|---|---|
| A. Commission one game-ready hooded masked operative from Seb's reference (rigged with fingers, under 40k triangles, 2k PBR textures, 3 LODs, Mixamo-compatible) | about $400 to $1,500 freelance | 1 to 3 weeks | Best brand match. Variations by texture and color swaps. Recommended. |
| B. MetaHuman body/face plus custom hoodie and mask (artist in Unreal + Marvelous Designer), exported and reduced for the web | MetaHuman free under $1M revenue per Epic; artist about $300 to $1,000 | 1 to 2 weeks | Needs a PC with Unreal (artist's). Heavy assets; web needs low LODs. |
| C. Reallusion Character Creator + ActorCore | software plus export license (check current pricing) plus artist time | 1 to 2 weeks | Strong pipeline, licensing terms must allow web real-time use. |
| Animations | Mixamo, free with an Adobe account | 1 day | Idle, walk, sit, typing, phone. |
| Not recommended | AI image-to-3D (about $20/month) | days | Likely fails the "no AI plastic mannequin" gate. |

The page already loads assets/agent.glb-style characters (clips Idle, Walk, Typing, Sit); delivery needs to be packed with pack_assets.py the same way as the furniture.

## Beyond the browser
True AAA lighting (global illumination, volumetrics) at the level of Unreal Engine would mean an Unreal build streamed to the browser (Pixel Streaming) with GPU hosting billed per hour. Not recommended until the business earns; three.js with real assets is the practical ceiling for now.

## Next phases
3. Character (blocked on option choice). 4. Workstation interaction and animation once the rig exists. 5. Inspector polish (workstation inspector, department dashboards). 6. Already wired: states come from real scheduler and GitHub runs. 7 to 9. Street expansion (alley, power lines, pedestrians), weather, first person, real-GPU performance pass.
