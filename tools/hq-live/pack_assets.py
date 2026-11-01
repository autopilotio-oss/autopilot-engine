"""Pack Poly Haven downloads (tools/hq-live/assets) into what the artifact host can serve.

The artifact host serves html/js/css/json/images but not .bin/.glb/.hdr, so:
- each model's .gltf + .bin becomes <id>/<id>.json with the geometry embedded as base64 (textures stay .jpg),
- the HDRI becomes a tonemapped equirect .jpg used for environment light.
Usage: python3 tools/hq-live/pack_assets.py <src assets dir> <out dir>
"""
import json, base64, pathlib, shutil, sys
import numpy as np
from PIL import Image

def read_hdr(p):
    raw = open(p, 'rb').read(); i = raw.index(b'\n\n') + 2
    j = raw.index(b'\n', i); d = raw[i:j].decode().split(); h, w = int(d[1]), int(d[3]); data = raw[j + 1:]
    img = np.zeros((h, w, 4), np.uint8); pos = 0
    for y in range(h):
        if data[pos] == 2 and data[pos + 1] == 2:
            pos += 4
            for c in range(4):
                x = 0
                while x < w:
                    n = data[pos]; pos += 1
                    if n > 128:
                        n -= 128; img[y, x:x + n, c] = data[pos]; pos += 1
                    else:
                        img[y, x:x + n, c] = np.frombuffer(data[pos:pos + n], np.uint8); pos += n
                    x += n
        else:
            img[y] = np.frombuffer(data[pos:pos + 4 * w], np.uint8).reshape(w, 4); pos += 4 * w
    e = img[..., 3].astype(np.float32); f = np.where(e > 0, np.ldexp(1.0, (e - 136).astype(int)), 0)
    return img[..., :3].astype(np.float32) * f[..., None]

def main(src, out):
    src, out = pathlib.Path(src), pathlib.Path(out)
    for gl in sorted(src.glob('*/*_1k.gltf')):
        d = gl.parent; g = json.loads(gl.read_text())
        for b in g['buffers']:
            b['uri'] = 'data:application/octet-stream;base64,' + base64.b64encode((d / b['uri']).read_bytes()).decode()
        od = out / d.name; shutil.rmtree(od, ignore_errors=True); (od / 'textures').mkdir(parents=True)
        for im in g.get('images', []):
            shutil.copy(d / im['uri'], od / im['uri'])
        (od / f'{d.name}.json').write_text(json.dumps(g, separators=(',', ':')))
    for hdr in src.glob('*/*.hdr'):
        rgb = read_hdr(hdr); rgb = rgb * 1.6 / (1 + rgb * 1.6); rgb = np.power(np.clip(rgb, 0, 1), 1 / 2.2)
        od = out / hdr.parent.name; od.mkdir(parents=True, exist_ok=True)
        Image.fromarray((rgb * 255).astype(np.uint8)).save(od / f'{hdr.parent.name}_env.jpg', quality=90)
    for tex in src.glob('*/Diffuse.jpg'):
        od = out / tex.parent.name; od.mkdir(parents=True, exist_ok=True)
        for f in tex.parent.glob('*.jpg'):
            shutil.copy(f, od / f.name)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
