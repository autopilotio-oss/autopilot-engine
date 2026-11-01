"""Stock photos and cutouts for carousels (runs in GitHub Actions: .github/workflows/photos.yml).

Requests: queue/photos/<slug>.json  {"query": "laptop on desk dark", "orientation": "portrait", "n": 3, "status": "pending"}
For each pending request: search Pexels (free license, commercial use OK), download the top results, cut the subject out
with rembg, save to docs/media/car/photos/<slug>/:
  01.jpg      the original (resized)
  01_cut.png  transparent cutout (full color; the carousel CSS makes it grayscale)
  credits.json photographer, page url, Pexels id (Pexels asks for credit when possible; we keep it with the image)
Rules: never request a named real person; generic people, hands, objects and places only. Status becomes "done" or "failed".

    python3 scripts/photos.py            (needs PEXELS_API_KEY)"""
import glob, io, json, os, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get("PEXELS_API_KEY", "").strip()


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "autopilot-photos/1", **(headers or {})})
    return urllib.request.urlopen(req, timeout=60).read()


def run():
    if not KEY:
        print("No PEXELS_API_KEY yet"); return 0
    from PIL import Image
    from rembg import remove, new_session
    session = new_session("isnet-general-use")
    done = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "queue", "photos", "*.json"))):
        r = json.load(open(f))
        if r.get("status") != "pending":
            continue
        slug = os.path.basename(f)[:-5]; out = os.path.join(ROOT, "docs", "media", "car", "photos", slug); os.makedirs(out, exist_ok=True)
        try:
            q = urllib.parse.urlencode({"query": r["query"], "orientation": r.get("orientation", "portrait"), "per_page": r.get("n", 3), "size": "large"})
            res = json.loads(get("https://api.pexels.com/v1/search?" + q, {"Authorization": KEY}))
            credits = []
            for i, ph in enumerate(res.get("photos", [])[: r.get("n", 3)], 1):
                img = Image.open(io.BytesIO(get(ph["src"]["large2x"]))).convert("RGB")
                img.thumbnail((1600, 1600))
                img.save(os.path.join(out, f"{i:02d}.jpg"), quality=88)
                cut = remove(img, session=session)
                bbox = cut.getbbox()
                if bbox:
                    cut = cut.crop(bbox)
                cut.save(os.path.join(out, f"{i:02d}_cut.png"))
                credits.append({"n": i, "pexels_id": ph["id"], "photographer": ph.get("photographer"), "url": ph.get("url"), "alt": ph.get("alt")})
            json.dump({"query": r["query"], "credits": credits}, open(os.path.join(out, "credits.json"), "w"), indent=1)
            r["status"] = "done" if credits else "failed"; r["count"] = len(credits)
            if not credits: r["error"] = "no results"
        except Exception as e:
            r["status"] = "failed"; r["error"] = repr(e)[:300].replace(KEY, "***")
        json.dump(r, open(f, "w"), indent=1); done += 1
        print(slug, r["status"], r.get("count", 0))
    return done


if __name__ == "__main__":
    run()
