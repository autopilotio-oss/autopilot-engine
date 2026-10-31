"""Offer catalog: one canonical record per sellable offer, built from the repo (products/, guides, keywords, docs/live.json).
python3 scripts/revenue/catalog.py           -> writes config/catalog.json and prints issues
python3 scripts/revenue/catalog.py --check   -> exit 1 if a revenue-breaking issue is found"""
import json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ids import offer_id

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXTERNAL = {  # offers sold on Gumroad but not managed in products/ (created by hand)
}


def load_guides():
    sys.path.insert(0, os.path.join(ROOT, "tools", "guides"))
    import importlib
    import guides  # noqa
    importlib.reload(guides)
    return guides.G


def build():
    live = set(json.load(open(os.path.join(ROOT, "docs", "live.json"))).get("live", []))
    G = load_guides()
    kw = json.load(open(os.path.join(ROOT, "config", "keywords.json")))["replies"]
    guide_by_perm = {}
    for k, g in G.items():
        if g.get("draft"):
            continue
        perm = g.get("permalink", f"{k}-agent")
        guide_by_perm.setdefault(perm, []).append({"guide": k, "path": f"g/{k}/", "keyword": g.get("kw"), "paid": g.get("paid", True)})
    offers = []
    for f in sorted(glob.glob(os.path.join(ROOT, "products", "*", "product.json"))):
        p = json.load(open(f)); perm = p["permalink"]
        status = "retired" if p.get("retired") else "draft" if p.get("draft") else "live" if perm in live else "not_live"
        offers.append({
            "offer_id": offer_id(perm), "permalink": perm, "name": p["name"].replace("AUTOPILOT.OI ", ""),
            "price_cents": p.get("price_cents"), "currency": "USD", "kind": "bundle" if p.get("bundle_of") else "kit",
            "components": [offer_id(x) for x in p.get("bundle_of", []) if "/" not in x], "status": status,
            "checkout_url": f"https://autopilotoi.gumroad.com/l/{perm}",
            "guides": guide_by_perm.get(perm, []) or ([{"guide": "landing", "path": p["landing"], "keyword": None, "paid": True}] if p.get("landing") else []), "managed_by": "products/",
        })
    for perm, e in EXTERNAL.items():
        offers.append({"offer_id": e["offer_id"], "permalink": perm, "name": e["name"], "price_cents": e["price_cents"], "currency": "USD",
                       "kind": e["kind"], "components": [], "status": "live" if perm in live else "not_live",
                       "checkout_url": f"https://autopilotoi.gumroad.com/l/{perm}", "guides": [], "page": e["page"], "managed_by": "gumroad (manual)"})
    keywords = []
    for k, reply in kw.items():
        links = re.findall(r"https?://autopilotoi\.app/([^\s?#]*)", reply)
        keywords.append({"keyword": k, "links": links})
    return {"offers": offers, "keywords": keywords, "live": sorted(live)}


def issues(cat):
    out = []
    docs = os.path.join(ROOT, "docs")
    for o in cat["offers"]:
        if o["status"] == "retired":
            continue
        if o["status"] == "not_live":
            out.append(("revenue", f"{o['offer_id']}: not purchasable on Gumroad (not in docs/live.json); buy buttons show 'Coming soon'"))
        if o["kind"] == "kit" and o["status"] in ("live", "not_live") and not o["guides"]:
            out.append(("funnel", f"{o['offer_id']}: no free guide points to it"))
        for c in o["components"]:
            st = next((x["status"] for x in cat["offers"] if x["offer_id"] == c), None)
            if st != "live" and o["status"] == "live":
                out.append(("revenue", f"{o['offer_id']}: bundle component {c} is {st}"))
    for k in cat["keywords"]:
        for path in k["links"]:
            p = os.path.join(docs, path, "index.html") if not path.endswith(".html") else os.path.join(docs, path)
            if path and not os.path.exists(p):
                out.append(("funnel", f"keyword {k['keyword']}: link /{path} has no page in docs/"))
        if not k["links"]:
            out.append(("funnel", f"keyword {k['keyword']}: reply has no autopilotoi.app link"))
    # every Gumroad link on the site points at a known offer
    known = {o["permalink"]: o["status"] for o in cat["offers"]}
    for f in glob.glob(os.path.join(docs, "**", "*.html"), recursive=True):
        for perm in set(re.findall(r"gumroad\.com/l/([a-z0-9-]+)", open(f, encoding="utf-8", errors="ignore").read())):
            rel = os.path.relpath(f, docs)
            if perm not in known:
                out.append(("revenue", f"{rel}: links unknown Gumroad product {perm}"))
            elif known[perm] in ("retired",):
                out.append(("revenue", f"{rel}: links retired product {perm}"))
    return out


if __name__ == "__main__":
    cat = build()
    json.dump(cat, open(os.path.join(ROOT, "config", "catalog.json"), "w"), indent=1, ensure_ascii=False)
    iss = issues(cat)
    for kind, msg in iss:
        print(f"[{kind}] {msg}")
    print(f"{len(cat['offers'])} offers, {sum(o['status'] == 'live' for o in cat['offers'])} live, {len(iss)} issues")
    if "--check" in sys.argv and any(k == "revenue" for k, _ in iss):
        sys.exit(1)
