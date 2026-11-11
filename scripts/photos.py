"""Stock photos and cutouts for carousels (runs in GitHub Actions: .github/workflows/photos.yml).

Requests: queue/photos/<slug>.json  {"query": "laptop on desk dark", "orientation": "portrait", "n": 3, "status": "pending"}
For each pending request: search Pexels (free license, commercial use OK), download the top results, cut the subject out
with rembg, save to docs/media/car/photos/<slug>/:
  01.jpg      the original (resized)
  01_cut.png  transparent cutout (full color; the carousel CSS makes it grayscale)
  credits.json photographer, page url, Pexels id (Pexels asks for credit when possible; we keep it with the image)
Rules: never request a named real person; generic people, hands, objects and places only. Status becomes "done" or "failed".

Keyless topic search (no Pexels key): same {"query": ...} request; searches Unsplash then Openverse, skips Unsplash+ and
  anything under 900px, writes sheet.jpg (numbered picks). "cutout": false skips rembg.

Unsplash by id (free Unsplash License, no key): {"unsplash": ["6TdCjWc16bQ"], "status": "pending"}.
Seb's own photos (sent in chat): queue/photos/<slug>.json {"files": ["queue/photos/in/<slug>/1.jpg", ...], "source": "...",
  "status": "pending"}. No Pexels call, just resize + cutout, same outputs. "source" records where the photo came from
  (his own shot, an official press kit, licensed). Posts using a real person's photo always go to Seb for approval.

    python3 scripts/photos.py            (needs PEXELS_API_KEY)"""
import glob, io, json, os, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get("PEXELS_API_KEY", "").strip()


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "autopilot-photos/1", **(headers or {})})
    return urllib.request.urlopen(req, timeout=60).read()


def run():
    from PIL import Image
    from rembg import remove, new_session
    session = new_session("isnet-general-use")
    done = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "queue", "photos", "*.json"))):
        r = json.load(open(f))
        if r.get("status") != "pending":
            continue
        slug = os.path.basename(f)[:-5]; out = os.path.join(ROOT, "docs", "media", "car", "photos", slug); os.makedirs(out, exist_ok=True)
        if r.get("files"):
            try:
                credits = []
                for i, fp in enumerate(r["files"], 1):
                    img = Image.open(os.path.join(ROOT, fp)).convert("RGB"); img.thumbnail((1600, 1600))
                    img.save(os.path.join(out, f"{i:02d}.jpg"), quality=90)
                    cut = remove(img, session=session); bbox = cut.getbbox()
                    if bbox:
                        cut = cut.crop(bbox)
                    cut.save(os.path.join(out, f"{i:02d}_cut.png"))
                    credits.append({"n": i, "file": fp, "source": r.get("source", "sent by Seb")})
                json.dump({"credits": credits}, open(os.path.join(out, "credits.json"), "w"), indent=1)
                r["status"] = "done"; r["count"] = len(credits)
            except Exception as e:
                r["status"] = "failed"; r["error"] = repr(e)[:300]
            json.dump(r, open(f, "w"), indent=1); done += 1; print(slug, r["status"]); continue
        if r.get("unsplash"):          # free Unsplash License photos picked by id (no API key needed)
            try:
                credits = []
                for i, pid in enumerate(r["unsplash"], 1):
                    src = (r.get("urls") or [None] * 99)[i - 1] or f"https://unsplash.com/photos/{pid}/download?force=true&w=1600"
                    img = Image.open(io.BytesIO(get(src))).convert("RGB")
                    img.thumbnail((1600, 1600))
                    img.save(os.path.join(out, f"{i:02d}.jpg"), quality=90)
                    cut = remove(img, session=session); bbox = cut.getbbox()
                    if bbox:
                        cut = cut.crop(bbox)
                    cut.save(os.path.join(out, f"{i:02d}_cut.png"))
                    credits.append({"n": i, "unsplash_id": pid, "url": f"https://unsplash.com/photos/{pid}", "license": "Unsplash License"})
                json.dump({"credits": credits}, open(os.path.join(out, "credits.json"), "w"), indent=1)
                r["status"] = "done"; r["count"] = len(credits)
            except Exception as e:
                r["status"] = "failed"; r["error"] = repr(e)[:300]
            json.dump(r, open(f, "w"), indent=1); done += 1; print(slug, r["status"]); continue
        if not KEY:                    # keyless topic search: Unsplash (free license, Unsplash+ skipped), then Openverse (CC, commercial OK)
            try:
                n = r.get("n", 6); credits = []; cands = []
                q = urllib.parse.urlencode({"query": r["query"], "per_page": 30, "orientation": r.get("orientation", "portrait")})
                try:
                    for ph in json.loads(get("https://unsplash.com/napi/search/photos?" + q)).get("results", []):
                        if ph.get("premium") or ph.get("plus") or "plus.unsplash.com" in ph["urls"]["raw"]:
                            continue
                        cands.append((ph["urls"]["raw"] + "&w=1800&q=88&fm=jpg", {"unsplash_id": ph["id"], "url": ph["links"]["html"],
                                      "photographer": ph["user"]["name"], "license": "Unsplash License", "alt": ph.get("alt_description")}))
                except Exception as e:
                    print(slug, "unsplash search failed", repr(e)[:120])
                if len(cands) < n:
                    q2 = urllib.parse.urlencode({"q": r["query"], "license_type": "commercial,modification", "page_size": 20})
                    try:
                        for ph in json.loads(get("https://api.openverse.org/v1/images/?" + q2)).get("results", []):
                            cands.append((ph["url"], {"openverse_id": ph["id"], "url": ph.get("foreign_landing_url"), "photographer": ph.get("creator"),
                                          "license": f"CC {ph.get('license','').upper()} {ph.get('license_version','')}".strip(), "alt": ph.get("title")}))
                    except Exception as e:
                        print(slug, "openverse search failed", repr(e)[:120])
                for src, meta in cands:
                    if len(credits) >= n:
                        break
                    try:
                        img = Image.open(io.BytesIO(get(src))).convert("RGB")
                    except Exception:
                        continue
                    if min(img.size) < 900:
                        continue
                    i = len(credits) + 1
                    img.thumbnail((1800, 1800)); img.save(os.path.join(out, f"{i:02d}.jpg"), quality=88)
                    if r.get("cutout", True):
                        cut = remove(img, session=session); bbox = cut.getbbox()
                        if bbox:
                            cut = cut.crop(bbox)
                        cut.save(os.path.join(out, f"{i:02d}_cut.png"))
                    credits.append({"n": i, **meta})
                if credits:                # numbered contact sheet so the picker can choose fast
                    th = [Image.open(os.path.join(out, f"{c['n']:02d}.jpg")) for c in credits]
                    W = 360; sheet = Image.new("RGB", (W * min(4, len(th)), 450 * ((len(th) + 3) // 4)), "#111")
                    from PIL import ImageDraw
                    d = ImageDraw.Draw(sheet)
                    for k, im in enumerate(th):
                        im = im.copy(); im.thumbnail((W - 10, 440)); x, y = (k % 4) * W + 5, (k // 4) * 450 + 5
                        sheet.paste(im, (x, y)); d.rectangle([x, y, x + 40, y + 30], fill="#D4FF3A"); d.text((x + 12, y + 8), str(k + 1), fill="#000")
                    sheet.save(os.path.join(out, "sheet.jpg"), quality=85)
                json.dump({"query": r["query"], "credits": credits}, open(os.path.join(out, "credits.json"), "w"), indent=1)
                r["status"] = "done" if credits else "failed"; r["count"] = len(credits)
                if not credits: r["error"] = "no usable results"
            except Exception as e:
                r["status"] = "failed"; r["error"] = repr(e)[:300]
            json.dump(r, open(f, "w"), indent=1); done += 1; print(slug, r["status"], r.get("count", 0)); continue
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
