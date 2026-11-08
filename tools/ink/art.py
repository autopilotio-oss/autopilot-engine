"""Turn a drawing (pen lines + colour on white paper) into drawable layers for the ink engine.
python3 tools/ink/art.py <in.png> <out_dir>/<name>   ->  <name>_ink.png, <name>_col.png, <name>.json
 - ink layer: dark line pixels (alpha from darkness), drawn by the pen following skeleton strokes
 - colour layer: saturated pixels, revealed afterwards by pencil hatching inside each colour region
JSON: {"w","h","ink":[[x,y,...flattened], ...] in drawing order, "col":[[...], ...]} in source pixels."""
import sys, json, numpy as np, cv2
from skimage.morphology import skeletonize

src, out = sys.argv[1], sys.argv[2]
img = cv2.imread(src, cv2.IMREAD_COLOR)
h, w = img.shape[:2]
if max(h, w) > 1400:
    s = 1400 / max(h, w); img = cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA); h, w = img.shape[:2]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
# paper white balance: normalise by a blurred background estimate so shading on the photo does not count as ink
bg = cv2.dilate(gray, np.ones((15, 15), np.uint8)); bg = cv2.GaussianBlur(bg, (0, 0), 9)
norm = np.clip(gray / np.maximum(bg, 1) * 255, 0, 255)
sat, val = hsv[..., 1] / 255, hsv[..., 2] / 255
ink = (norm < 165) & (sat < .38)
ink = cv2.morphologyEx(ink.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)) > 0
col = ((sat > .16) | (norm < 225)) & ~ink
col = cv2.morphologyEx(col.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0

# layers (BGRA)
ink_rgba = np.zeros((h, w, 4), np.uint8); a = np.clip((200 - norm) / 150, 0, 1) * ink
ink_rgba[..., :3] = (img * 0.35).astype(np.uint8); ink_rgba[..., 3] = (a * 255).astype(np.uint8)
col_rgba = np.zeros((h, w, 4), np.uint8); col_rgba[..., :3] = img; col_rgba[..., 3] = (col * 235).astype(np.uint8)
col_rgba[..., 3] = cv2.GaussianBlur(col_rgba[..., 3], (0, 0), 0.8)
cv2.imwrite(out + "_ink.png", ink_rgba); cv2.imwrite(out + "_col.png", col_rgba)

# ---- ink strokes: skeleton -> polylines -> drawing order
sk = skeletonize(ink)
ys, xs = np.nonzero(sk); pts = set(zip(xs.tolist(), ys.tolist()))
N8 = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
nb = lambda p: [(p[0] + dx, p[1] + dy) for dx, dy in N8 if (p[0] + dx, p[1] + dy) in pts]
deg = {p: len(nb(p)) for p in pts}
seen = set(); strokes = []
def walk(p):
    path = [p]; seen.add(p)
    while True:
        nxt = [q for q in nb(path[-1]) if q not in seen]
        if not nxt: break
        # prefer continuing straight
        if len(path) > 1:
            d0 = (path[-1][0] - path[-2][0], path[-1][1] - path[-2][1])
            nxt.sort(key=lambda q: -((q[0] - path[-1][0]) * d0[0] + (q[1] - path[-1][1]) * d0[1]))
        q = nxt[0]; seen.add(q); path.append(q)
        if deg.get(q, 0) > 2 and len(path) > 3: break
    return path
for p in sorted(pts, key=lambda p: deg[p]):
    if p in seen or deg[p] > 1: continue
    s = walk(p)
    if len(s) >= 4: strokes.append(s)
for p in sorted(pts, key=lambda p: (p[1], p[0])):
    if p in seen: continue
    s = walk(p)
    if len(s) >= 6: strokes.append(s)
# simplify and order: start top left, then always the nearest unfinished stroke (a hand finishes nearby lines first)
def simp(s):
    a = np.array(s, np.float32); keep = [a[0]]
    for q in a[1:]:
        if np.hypot(*(q - keep[-1])) >= 2.5: keep.append(q)
    if np.hypot(*(a[-1] - keep[-1])) > .5: keep.append(a[-1])
    return np.array(keep)
strokes = [simp(s) for s in strokes]; strokes = [s for s in strokes if len(s) >= 2]
order = []; left = list(range(len(strokes)))
cur = np.array([0, 0], np.float32)
while left:
    best, bi, rev = 1e18, None, False
    for i in left:
        s = strokes[i]; d0 = np.sum((s[0] - cur) ** 2) + s[0][1] * 6; d1 = np.sum((s[-1] - cur) ** 2) + s[-1][1] * 6
        if d0 < best: best, bi, rev = d0, i, False
        if d1 < best: best, bi, rev = d1, i, True
    s = strokes[bi][::-1] if rev else strokes[bi]; order.append(s); cur = s[-1]; left.remove(bi)
# ---- colour hatching: per colour region, diagonal back-and-forth strokes covering its box
cols = []
n, lab, stats, _ = cv2.connectedComponentsWithStats(col.astype(np.uint8), 8)
regions = sorted([i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > 30], key=lambda i: (stats[i, 1] // 60, stats[i, 0]))
for i in regions:
    x, y, ww, hh = stats[i, :4]; step = 5; path = []; flip = False
    for d in range(-hh, ww + hh, step):
        a_ = (x + d, y + hh); b_ = (x + d + hh * .6, y)
        path += [a_, b_] if flip else [b_, a_]; flip = not flip
    cols.append(np.array(path, np.float32).clip([x - 2, y - 2], [x + ww + 2, y + hh + 2]))
json.dump({"w": w, "h": h, "ink": [s.round(1).flatten().tolist() for s in order], "col": [c.round(1).flatten().tolist() for c in cols]}, open(out + ".json", "w"))
L = sum(float(np.sum(np.hypot(*np.diff(s, axis=0).T))) for s in order)
print(f"art {out}: {w}x{h}, {len(order)} ink strokes ({L:.0f}px), {len(cols)} colour regions")
