"""THE ORGANISM row builder. One 21:9 render in, three finished IG posts out.

  python3 tools/carousel/rows/row.py tools/carousel/rows/ch01.json          build the row
  python3 tools/carousel/rows/row.py tools/carousel/rows/ch01.json --grid   gridded right panel to read screen corners

Needs the repo served on localhost:8790 (python3 -m http.server 8790 from the repo root).
Output: docs/media/rows/<id>/L.jpg M.jpg R.jpg row.jpg (+ panels used as backgrounds).
"""
import json, os, subprocess, sys, urllib.parse
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
URL = 'http://localhost:8790/'
W, H = 1080, 1350


def split(img):
    """Cut the render into three 4:5 panels. Drops any dark divider lines the model drew."""
    a = np.asarray(img).astype(int)
    col = a.mean(axis=(0, 2))
    w = img.width
    dark = [x for x in range(int(w * .2), int(w * .8)) if col[x] < 14]
    cuts = []
    for x in dark:
        if not cuts or x - cuts[-1][1] > 3:
            cuts.append([x, x])
        else:
            cuts[-1][1] = x
    if len(cuts) == 2:
        spans = [(0, cuts[0][0]), (cuts[0][1] + 1, cuts[1][0]), (cuts[1][1] + 1, w)]
    else:
        t = w // 3
        spans = [(0, t), (t, 2 * t), (2 * t, w)]
    pw = min(b - a_ for a_, b in spans)
    ph = min(img.height, int(pw * 1.25))
    pw = int(ph / 1.25)
    y0 = (img.height - ph) // 2
    out = []
    for a_, b in spans:
        x0 = a_ + ((b - a_) - pw) // 2
        out.append(img.crop((x0, y0, x0 + pw, y0 + ph)).resize((W, H), Image.LANCZOS))
    return out


def shoot(out, w, h, page, spec):
    u = URL + 'tools/carousel/rows/' + page + '#' + urllib.parse.quote(json.dumps(spec))
    r = subprocess.run(['node', os.path.join(HERE, 'shoot.js'), out, str(w), str(h), u], capture_output=True, text=True)
    if r.returncode:
        sys.exit('render failed: ' + r.stderr)
    return r.stdout.strip()


def warp(panel, screen_png, corners):
    """Place the product screen onto the tablet in the render. corners: TL TR BR BL in panel px."""
    S = Image.open(screen_png).convert('RGB')
    src = [(0, 0), (500, 0), (500, 600), (0, 600)]
    A, B = [], []
    for (x, y), (u, v) in zip(corners, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        B += [u, v]
    c = np.linalg.solve(np.array(A, float), np.array(B, float))
    Wp = S.transform(panel.size, Image.PERSPECTIVE, tuple(c), Image.BICUBIC)
    m = Image.new('L', panel.size, 0)
    ImageDraw.Draw(m).polygon([tuple(p) for p in corners], fill=235)
    out = Image.composite(Wp, panel, m.filter(ImageFilter.GaussianBlur(1.2)))
    tl, tr, br, bl = corners
    g = Image.new('L', panel.size, 0)
    mid = lambda p, q, t: (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    ImageDraw.Draw(g).polygon([tuple(tl), tuple(tr), mid(tr, br, .3), mid(tl, bl, .3)], fill=22)
    return Image.composite(Image.new('RGB', panel.size, (255, 255, 255)), out, g.filter(ImageFilter.GaussianBlur(30)))


def main():
    spec = json.load(open(sys.argv[1]))
    rid = spec['id']
    out = os.path.join(ROOT, 'docs', 'media', 'rows', rid)
    os.makedirs(out, exist_ok=True)
    L, M, R = split(Image.open(os.path.join(HERE, spec['render'])).convert('RGB'))
    if '--grid' in sys.argv:
        g = R.copy(); d = ImageDraw.Draw(g)
        for v in range(0, 1350, 50):
            d.line((0, v, W, v), fill=(255, 0, 0) if v % 100 == 0 else (90, 0, 0))
        for v in range(0, 1080, 50):
            d.line((v, 0, v, H), fill=(255, 0, 0) if v % 100 == 0 else (90, 0, 0))
        g.save(os.path.join(out, 'grid_R.png')); print('wrote', os.path.join(out, 'grid_R.png')); return
    st = spec['store']
    if st.get('screen'):
        sp = os.path.join(out, '_screen.png')
        shoot(sp, 500, 600, 'screen.html', st['screen'])
        R = warp(R, sp, st['screen']['corners'])
    rel = 'docs/media/rows/' + rid + '/'
    for n, im in (('L', L), ('M', M), ('R', R)):
        im.save(os.path.join(out, '_bg' + n + '.png'))
    le, ch = spec['learn'], spec['chapter']
    jobs = [('L', {'slot': 'L', 'bg': '/' + rel + '_bgL.png', **le}),
            ('M', {'slot': 'M', 'bg': '/' + rel + '_bgM.png', 'n': ch['n'], 'name': ch['name']}),
            ('R', {'slot': 'R', 'bg': '/' + rel + '_bgR.png', **{k: v for k, v in st.items() if k != 'screen'}})]
    for n, s in jobs:
        print(n, shoot(os.path.join(out, n + '.jpg'), W, H, 'panel.html', s))
    row = Image.new('RGB', (3 * W + 16, H), (255, 255, 255))
    for i, n in enumerate('LMR'):
        row.paste(Image.open(os.path.join(out, n + '.jpg')), (i * (W + 8), 0))
    row.resize((row.width // 2, H // 2)).save(os.path.join(out, 'row.jpg'), quality=90)
    print('ROW OK', out)


if __name__ == '__main__':
    main()
