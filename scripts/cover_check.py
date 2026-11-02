"""Which covers are live on Gumroad, and do they match our current cover art? Compares each live cover with
docs/store/<slug>-cover.png (same 1280x720 render) by mean absolute pixel difference. Prints only; changes nothing."""
import os, json, io, urllib.request, urllib.parse
from PIL import Image, ImageChops, ImageStat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); TOK = os.environ["GUMROAD_TOKEN"]
st = json.load(open(os.path.join(ROOT, "state", "products.json"))); out = {}
for slug in ("autopilot", "workspace", "workspace-founding"):
    g = json.loads(urllib.request.urlopen(f"https://api.gumroad.com/v2/products/{st[slug]['id']}?" + urllib.parse.urlencode({"access_token": TOK}), timeout=60).read())["product"]
    ref = Image.open(os.path.join(ROOT, "docs", "store", f"{slug}-cover.png")).convert("RGB").resize((320, 180))
    res = []
    for c in g.get("covers") or []:
        try:
            im = Image.open(io.BytesIO(urllib.request.urlopen(c.get("original_url") or c["url"], timeout=60).read())).convert("RGB").resize((320, 180))
            diff = sum(ImageStat.Stat(ImageChops.difference(im, ref)).mean) / 3
            res.append({"id": c.get("id"), "diff_vs_current_art": round(diff, 1), "is_current": diff < 12})
        except Exception as e: res.append({"id": c.get("id"), "error": repr(e)[:120]})
    out[slug] = {"thumbnail": g.get("thumbnail_url"), "covers": res}
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(ROOT, "state", "cover_check.json"), "w"), indent=1)
