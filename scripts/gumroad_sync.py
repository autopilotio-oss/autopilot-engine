"""Creates Gumroad products from products/<slug>/product.json (+ sealed file). Runs in GitHub Actions with
GUMROAD_TOKEN and KIT_PRIVATE_KEY. Records results in state/products.json."""
import os, sys, json, glob, subprocess, urllib.request, urllib.parse, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.gumroad.com/v2"; TOK = os.environ.get("GUMROAD_TOKEN", "").strip()
def call(method, path, data=None, raw=False):
    body = urllib.parse.urlencode(data or {}, doseq=True).encode() if data is not None else None
    req = urllib.request.Request(API + path, data=body, method=method, headers={"Authorization": "Bearer " + TOK})
    try: r = urllib.request.urlopen(req, timeout=120).read().decode(); return json.loads(r)
    except urllib.error.HTTPError as e:
        print(f"::error title=Gumroad {method} {path}::{e.read().decode()[:400]}"); raise
def unseal(d):
    pk = os.environ["KIT_PRIVATE_KEY"]; tmp = tempfile.mkdtemp()
    open(tmp + "/pk.pem", "w").write(pk)
    k = subprocess.run(["openssl", "pkeyutl", "-decrypt", "-inkey", tmp + "/pk.pem", "-in", d + "/key.enc"], capture_output=True, check=True).stdout.decode()
    out = tmp + "/file.pdf"
    subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-in", d + "/file.enc", "-out", out, "-pass", "pass:" + k], check=True)
    return out
def upload(path, name):
    size = os.path.getsize(path)
    pre = call("POST", "/files/presign", {"filename": name, "file_size": size})
    parts = []; data = open(path, "rb").read(); n = len(pre["parts"]); chunk = -(-size // n)
    for i, p in enumerate(pre["parts"]):
        piece = data[i * chunk:(i + 1) * chunk]
        r = urllib.request.urlopen(urllib.request.Request(p["presigned_url"], data=piece, method="PUT"), timeout=300)
        parts.append({"part_number": p.get("part_number", i + 1), "etag": r.headers["ETag"]})
    call("POST", "/files/complete", {"upload_id": pre["upload_id"], "key": pre["key"],
         "parts[][part_number]": [x["part_number"] for x in parts], "parts[][etag]": [x["etag"] for x in parts]})
    return pre["file_url"]
def main():
    if not TOK: print("No GUMROAD_TOKEN yet"); return
    sp = os.path.join(ROOT, "state", "products.json"); st = json.load(open(sp)) if os.path.exists(sp) else {}
    for f in sorted(glob.glob(os.path.join(ROOT, "products", "*", "product.json"))):
        d = os.path.dirname(f); slug = os.path.basename(d); p = json.load(open(f))
        if slug in st and st[slug].get("published"): continue
        try:
            fu = upload(unseal(d), p["filename"])
            r = call("POST", "/products", {"name": p["name"], "price": p["price_cents"], "price_currency_type": "usd", "native_type": "digital",
                     "description": p["description_html"], "custom_permalink": p["permalink"], "tags[]": p.get("tags", []), "files[][url]": fu})
            pid = r["product"]["id"]
            if p.get("cover_url"):
                try: call("POST", f"/products/{pid}/covers", {"url": p["cover_url"]})
                except Exception: pass
            call("PUT", f"/products/{pid}/enable", {})
            st[slug] = {"id": pid, "url": r["product"].get("short_url") or f"https://autopilotoi.gumroad.com/l/{p['permalink']}", "published": True}
            print(f"::notice title=Gumroad live::{p['name']} {st[slug]['url']}")
        except Exception as e:
            print(f"::warning title=Gumroad failed::{slug} {str(e)[:300]}")
    json.dump(st, open(sp, "w"), indent=1)
main()
