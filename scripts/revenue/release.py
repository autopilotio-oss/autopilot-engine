"""Release a drafted agent after Seb approves it (Agent Factory -> approval -> publish).
python3 scripts/revenue/release.py <slug> --approved-by "Seb, <date>, <where he said yes>"

Steps: quality gate must pass -> product.json draft false -> guide draft false -> rebuild guides -> mark RELEASED in
config/approvals_queue.md. Then commit + push: the Gumroad sync creates the product (10 new products per day max).
Never run this without an explicit approval from Seb."""
import json, os, sys, subprocess, datetime, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quality


def main():
    if len(sys.argv) < 4 or sys.argv[2] != "--approved-by":
        sys.exit(__doc__)
    slug, who = sys.argv[1], sys.argv[3]
    errs = quality.check(slug)
    if errs:
        sys.exit("quality gate failed:\n" + "\n".join(errs))
    pf = os.path.join(ROOT, "products", slug, "product.json"); p = json.load(open(pf))
    p.pop("draft", None); json.dump(p, open(pf, "w"), indent=2, ensure_ascii=False); open(pf, "a").write("\n")
    key = slug.replace("-agent", "")
    gf = os.path.join(ROOT, "tools", "guides", "extra", f"{key}.json")
    if os.path.exists(gf):
        g = json.load(open(gf)); g.pop("draft", None); json.dump(g, open(gf, "w"), indent=1, ensure_ascii=False)
        subprocess.run(["python3", "tools/guides/build.py"], cwd=ROOT, check=True)
    q = os.path.join(ROOT, "config", "approvals_queue.md"); txt = open(q).read()
    d = datetime.date.today().isoformat()
    txt2 = re.sub(rf"(## [^\n]*\b{re.escape(slug)}\b[\s\S]*?)Status: AWAITING APPROVAL", rf"\1Status: APPROVED ({who}), RELEASED {d}", txt, count=1)
    if txt2 == txt:
        txt2 = txt + f"\n- {d} {slug}: APPROVED ({who}), RELEASED {d}\n"
    open(q, "w").write(txt2)
    print(f"released {slug}: commit and push, the Gumroad sync publishes it")


if __name__ == "__main__":
    main()
