"""Product Quality Gate (agent 10). Blocks release of anything that breaks the honesty or catalog rules.
python3 scripts/revenue/quality.py            -> checks every non retired product
python3 scripts/revenue/quality.py <slug>     -> checks one product (exit 1 on failure)"""
import json, os, re, sys, glob, html

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BANNED = ["guarantee", "while you sleep", "on its own", "passive income", "get rich", "risk free", "100%", "every month for you",
          "automatically cancels", "fix your credit score", "credit repair", "make money fast"]
REQUIRED = ["what you get", "how it works", "you need", "not affiliated with anthropic"]


def text_of(p):
    return html.unescape(re.sub(r"<[^>]+>", " ", p.get("description_html", ""))).lower()


def check(slug):
    f = os.path.join(ROOT, "products", slug, "product.json")
    if not os.path.exists(f):
        return [f"{slug}: no product.json"]
    p = json.load(open(f)); t = text_of(p); errs = []
    for sent in re.split(r"(?<=[.!?])\s+", t):
        if re.search(r"\b(does not|doesn't|do not|don't|nothing|never|not)\b", sent):
            continue  # negated use ("it does not guarantee a refund") is the honest wording we want
        for w in BANNED:
            if w in sent:
                errs.append(f"banned phrase: {w!r}")
    for w in REQUIRED:
        if w not in t:
            errs.append(f"missing section: {w!r}")
    if not re.search(r"does not|doesn.t|don.t|nothing (logs|sends)|never", t):
        errs.append("description must say what it does NOT do")
    if re.search(r" [-–—] ", t):
        errs.append("dash in copy")
    if p.get("price_cents") not in (1000, 2400, 3900, 4900):
        errs.append(f"price {p.get('price_cents')} is not an approved price point")
    if not p.get("bundle_of") and not (os.path.exists(os.path.join(ROOT, "products", slug, "file.enc")) and os.path.exists(os.path.join(ROOT, "products", slug, "key.enc"))):
        errs.append("sealed kit file missing (file.enc/key.enc)")
    if not (p.get("cover_url") or "").startswith("https://"):
        errs.append("cover_url missing")
    for leak in glob.glob(os.path.join(ROOT, "products", slug, "*.pdf")):
        errs.append(f"UNSEALED PDF in repo: {os.path.basename(leak)}")
    return [f"{slug}: {e}" for e in errs]


if __name__ == "__main__":
    slugs = sys.argv[1:] or [os.path.basename(os.path.dirname(f)) for f in glob.glob(os.path.join(ROOT, "products", "*", "product.json"))
                             if not json.load(open(f)).get("retired")]
    errs = [e for s in sorted(slugs) for e in check(s)]
    print("\n".join(errs) if errs else f"quality gate: {len(slugs)} product(s) pass")
    sys.exit(1 if errs else 0)
