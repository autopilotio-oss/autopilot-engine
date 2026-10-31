"""Creates Gumroad products from products/<slug>/product.json (+ sealed file). Runs in GitHub Actions with
GUMROAD_TOKEN and KIT_PRIVATE_KEY. Records results in state/products.json."""
import os, sys, json, glob, subprocess, urllib.request, urllib.parse, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.gumroad.com/v2"; TOK = os.environ.get("GUMROAD_TOKEN", "").strip()
DBG = []
def call(method, path, data=None, raw=False):
    data = dict(data or {}); data["access_token"] = TOK
    body = urllib.parse.urlencode(data, doseq=True).encode()
    req = urllib.request.Request(API + path, data=body, method=method, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try: r = urllib.request.urlopen(req, timeout=120).read().decode(); return json.loads(r)
    except urllib.error.HTTPError as e:
        msg = e.read().decode()[:300].replace(TOK, "***"); DBG.append([method, path, e.code, msg]); print(f"::warning title=Gumroad {method} {path} {e.code}::{msg}"); raise
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
def reconcile(st):
    """Read what is actually on Gumroad: fill missing ids, record live state, and publish docs/live.json
    (the list of buyable permalinks the site uses to hide buttons for products that are not live)."""
    try: r = call_get("/products?" + urllib.parse.urlencode({"access_token": TOK}))
    except Exception as e: DBG.append(["reconcile_fail", repr(e)[:200]]); return
    live = []; by_id = {v.get("id"): k for k, v in st.items() if v.get("id")}
    for pr in r.get("products", []):
        perm = by_id.get(pr.get("id")) or pr.get("custom_permalink") or (pr.get("short_url") or "").rstrip("/").split("/")[-1]
        if not perm: continue
        if pr.get("published"): live.append(perm)
        if perm not in st and os.path.exists(os.path.join(ROOT, "products", perm, "product.json")):
            # Product exists on Gumroad (e.g. an earlier create that never got recorded): adopt it instead of
            # failing forever with "custom permalink is already used". version 0 forces a file + description update.
            st[perm] = {"id": pr.get("id"), "url": pr.get("short_url") or f"https://autopilotoi.gumroad.com/l/{perm}", "published": bool(pr.get("published")), "version": 0, "adopted": True}
            DBG.append(["adopted", perm, bool(pr.get("published"))])
        if perm in st:
            if not st[perm].get("id"): st[perm]["id"] = pr.get("id"); DBG.append(["id_filled", perm])
            st[perm]["live"] = bool(pr.get("published"))
    for k, v in st.items():
        if v.get("published") and k not in live:
            DBG.append(["not_live_on_gumroad", k]); v["live"] = False
    json.dump({"live": sorted(live), "checked": __import__("datetime").datetime.utcnow().isoformat(timespec="seconds") + "Z"},
              open(os.path.join(ROOT, "docs", "live.json"), "w"), indent=1)
def call_get(path):
    return json.loads(urllib.request.urlopen(API + path, timeout=60).read().decode())
def heal_unpublished(st):
    """A product we released (published in state, not retired or draft) that Gumroad shows as unpublished gets re-enabled."""
    for k, v in st.items():
        f = os.path.join(ROOT, "products", k, "product.json")
        if not (v.get("published") and v.get("live") is False and v.get("id") and os.path.exists(f)): continue
        p = json.load(open(f))
        if p.get("retired") or p.get("draft"): continue
        try: call("PUT", f"/products/{v['id']}/enable", {}); v["live"] = True; DBG.append(["re_enabled", k]); print(f"::notice title=Gumroad re-enabled::{k}")
        except Exception as e: DBG.append(["re_enable_fail", k, repr(e)[:200]])
def sync_offer_code(st):
    """Owner approved launch code (config/growthos/campaign.json offer_code): create it on each listed product while
    active, delete it after 'until'. List prices never change."""
    cf = os.path.join(ROOT, "config", "growthos", "campaign.json")
    if not os.path.exists(cf): return
    oc = json.load(open(cf)).get("offer_code") or {}
    if not oc.get("name"): return
    import datetime as _dt
    active = _dt.datetime.now(_dt.timezone.utc) < _dt.datetime.fromisoformat(oc["until"].replace("Z", "+00:00"))
    for slug in oc.get("products", []):
        pid = (st.get(slug) or {}).get("id")
        if not pid or not (st.get(slug) or {}).get("published"): continue
        try:
            have = [c for c in call_get(f"/products/{pid}/offer_codes?" + urllib.parse.urlencode({"access_token": TOK})).get("offer_codes", [])
                    if (c.get("name") or "").upper() == oc["name"].upper()]
            if active and not have:
                call("POST", f"/products/{pid}/offer_codes", {"name": oc["name"], "amount_off": oc["percent_off"], "offer_type": "percent",
                     "max_purchase_count": oc.get("max_purchase_count", 100)})
                DBG.append(["offer_code_created", slug, oc["name"]])
            elif not active:
                for c in have:
                    call("DELETE", f"/products/{pid}/offer_codes/{c['id']}", {}); DBG.append(["offer_code_deleted", slug, oc["name"]])
            else: DBG.append(["offer_code_ok", slug])
        except Exception as e: DBG.append(["offer_code_fail", slug, repr(e)[:200]])
def main():
    if not TOK: print("No GUMROAD_TOKEN yet"); return
    try:
        DBG.append(["token_len", len(TOK)])
        u = urllib.request.urlopen(API + "/user?" + urllib.parse.urlencode({"access_token": TOK}), timeout=60).read().decode(); DBG.append(["user", "ok"])
        print("::notice title=Gumroad user::connected")
    except urllib.error.HTTPError as e: m = e.read().decode()[:200]; DBG.append(["user", e.code, m]); print(f"::warning title=Gumroad user check {e.code}::" + m)
    sp = os.path.join(ROOT, "state", "products.json"); st = json.load(open(sp)) if os.path.exists(sp) else {}
    reconcile(st)
    # "priority": higher first, so the most important new product gets the daily create slots (Gumroad: 10 new/day)
    for f in sorted(glob.glob(os.path.join(ROOT, "products", "*", "product.json")), key=lambda x: (-json.load(open(x)).get("priority", 0), x)):
        d = os.path.dirname(f); slug = os.path.basename(d); p = json.load(open(f))
        if p.get("retired"):
            # Owner-approved retirement: unpublish on Gumroad, keep the record (reversible: set retired false + enable).
            if slug in st and st[slug].get("published") and st[slug].get("id"):
                try:
                    call("PUT", f"/products/{st[slug]['id']}/disable", {}); st[slug]["published"] = False; st[slug]["retired"] = True
                    print(f"::notice title=Gumroad retired::{slug}")
                except Exception as e: DBG.append(["retire_fail", slug, repr(e)[:300]])
            continue
        if p.get("draft"):
            continue  # not approved for release yet (agent factory QA gate)
        if slug in st and st[slug].get("adopted") and not st[slug].get("published") and st[slug].get("id"):
            # Adopted from Gumroad: push the current file, description and cover, then publish it.
            try:
                fu = ([upload(unseal(os.path.join(ROOT, "products", sub)), json.load(open(os.path.join(ROOT, "products", sub, "product.json")))["filename"]) for sub in p["bundle_of"]]
                      if p.get("bundle_of") else upload(unseal(d), p["filename"]))
                r = call("PUT", f"/products/{st[slug]['id']}", {"files[][url]": fu, "description": p["description_html"], "name": p["name"], "price": p["price_cents"]})
                DBG.append(["adopt_update", slug, str(r)[:300]])
                if p.get("cover_url"):
                    try: call("POST", f"/products/{st[slug]['id']}/covers", {"url": p["cover_url"]}); st[slug]["cover_v"] = p.get("cover_v")
                    except Exception: pass
                call("PUT", f"/products/{st[slug]['id']}/enable", {})
                st[slug].update({"published": True, "version": p.get("version", 1)}); print(f"::notice title=Gumroad live (adopted)::{slug}")
            except Exception as e: DBG.append(["adopt_fail", slug, repr(e)[:300]])
            continue
        if slug in st and st[slug].get("published"):
            # Cover refresh: bump "cover_v" in product.json to (re)upload its cover_url to Gumroad.
            if p.get("cover_v") and p.get("cover_url") and st[slug].get("id") and p["cover_v"] != st[slug].get("cover_v"):
                try:
                    r = call("POST", f"/products/{st[slug]['id']}/covers", {"url": p["cover_url"]})
                    DBG.append(["cover", slug, str(r)[:200]])
                    if r.get("success", True): st[slug]["cover_v"] = p["cover_v"]
                except Exception as e: DBG.append(["cover_fail", slug, repr(e)[:300]])
            if p.get("version", 1) != st[slug].get("version", 1) and st[slug].get("id"):
                try:
                    if p.get("bundle_of"):
                        fu = [upload(unseal(os.path.join(ROOT, "products", sub)), json.load(open(os.path.join(ROOT, "products", sub, "product.json")))["filename"]) for sub in p["bundle_of"]]
                    else:
                        fu = upload(unseal(d), p["filename"])
                    r = call("PUT", f"/products/{st[slug]['id']}", {"files[][url]": fu, "description": p["description_html"], "name": p["name"]})
                    DBG.append(["update", slug, str(r)[:300]])
                    if r.get("success"): st[slug]["version"] = p.get("version", 1); print(f"::notice title=Gumroad updated::{slug}")
                except Exception as e: DBG.append(["update_fail", slug, repr(e)[:300]])
            continue
        try:
            if p.get("bundle_of"):
                fu = []
                for sub in p["bundle_of"]:
                    sd = os.path.join(ROOT, "products", sub); sp_ = json.load(open(os.path.join(sd, "product.json")))
                    fu.append(upload(unseal(sd), sp_["filename"]))
            else:
                fu = upload(unseal(d), p["filename"])
            r = call("POST", "/products", {"name": p["name"], "price": p["price_cents"], "price_currency_type": "usd", "native_type": "digital",
                     "description": p["description_html"], "custom_permalink": p["permalink"], "tags[]": p.get("tags", []), "files[][url]": fu})
            if "product" not in r: DBG.append(["create_no_product", slug, str(r)[:400]]); print(f"::warning title=Gumroad create::{slug} {str(r)[:300]}"); continue
            pid = r["product"]["id"]
            if p.get("cover_url"):
                try: call("POST", f"/products/{pid}/covers", {"url": p["cover_url"]})
                except Exception: pass
            call("PUT", f"/products/{pid}/enable", {})
            st[slug] = {"id": pid, "url": r["product"].get("short_url") or f"https://autopilotoi.gumroad.com/l/{p['permalink']}", "published": True, "version": p.get("version", 1)}
            print(f"::notice title=Gumroad live::{p['name']} {st[slug]['url']}")
        except Exception as e:
            DBG.append(["fail", slug, repr(e)[:300]]); print(f"::warning title=Gumroad failed::{slug} {str(e)[:300]}")
    reconcile(st)
    heal_unpublished(st)
    sync_offer_code(st)
    reconcile(st)
    json.dump(st, open(sp, "w"), indent=1)
    json.dump(DBG, open(os.path.join(ROOT, "state", "gumroad_debug.json"), "w"), indent=1)
try:
    main()
except Exception as e:
    import traceback; DBG.append(["crash", traceback.format_exc()[-800:].replace(TOK, "***") if TOK else traceback.format_exc()[-800:]])
    json.dump(DBG, open(os.path.join(ROOT, "state", "gumroad_debug.json"), "w"), indent=1)
