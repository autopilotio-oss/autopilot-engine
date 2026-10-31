"""Turn one daily spec into a live agent. Run from the repo root:
    python3 tools/daily/new_agent.py tools/daily/specs/<slug>.json [--check]

It checks the spec (idea gate, honesty rules), then writes:
  products/<slug>/  (sealed kit PDF + product.json)  -> Gumroad sync publishes it on push
  tools/kits/covers_extra/<key>.json + docs/store/<key>-cover.png / -thumb.png
  tools/guides/extra/<key>.json + rebuilt docs/g/ pages and sitemap
  config/keywords.json reply for the keyword
  tools/demo/eps/<slug>.json  -> the demo video workflow renders it on push
  docs/daily/<date>-<slug>.json (log)
See tools/daily/DAILY.md for the spec format and the full daily routine."""
import json, os, re, subprocess, sys, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
S = json.load(open(sys.argv[1])); CHECK = "--check" in sys.argv
e = html.escape
err = []

# ---------- checks ----------
for k in ["key", "slug", "name", "kw", "cat", "headline", "what", "need", "doesnt", "kit", "guide", "cover", "demo", "reply", "gate", "posts"]:
    if k not in S: err.append(f"missing field: {k}")
g = S.get("gate", {}); sc = g.get("scores", {})
if len(sc) != 6: err.append("gate needs 6 scores")
if any(v == 0 for v in sc.values()): err.append("gate: a zero score fails")
if sum(sc.values()) < 10: err.append(f"gate: {sum(sc.values())}/12 is below 10")
if len(g.get("problem_sources", [])) < 2: err.append("gate: need 2+ sources showing the problem is real")
if os.path.exists(os.path.join(ROOT, "products", S.get("slug", "x"))): err.append("slug already exists")
rej = open(os.path.join(ROOT, "PLAYBOOK.md")).read().lower()
blob = json.dumps(S, ensure_ascii=False)
pub = json.dumps([S.get(k) for k in ("headline", "what", "posts", "reply", "demo", "cover")], ensure_ascii=False)
if re.search(r" [-–—] ", pub): err.append("dash in public copy")
BAN = ["guarantee", "guaranteed", "while you sleep", "on its own", "automatically cancels", "passive income", "make money fast",
       "credit repair", "fix your credit score", "tech support", "100%", "risk free", "get rich", "lawyer", "legal advice", "diagnos"]
for w in BAN:
    if w in pub.lower(): err.append(f"banned phrase in public copy: {w}")
for w in ["credit repair", "tech support", "installation service", "medical diagnosis", "investment advice", "gambling", "weapons"]:
    if w in (S.get("headline", "") + S.get("what", "")).lower(): err.append(f"prohibited category: {w}")
if S.get("price_cents", 1000) != 1000: err.append("daily agents are $10 (price_cents 1000)")
if err:
    print("SPEC FAILED:\n  " + "\n  ".join(err)); sys.exit(1)
print("spec ok:", S["name"], f"gate {sum(sc.values())}/12")
if CHECK: sys.exit(0)

slug, key, name = S["slug"], S["key"], S["name"]
run = lambda *a, **k: subprocess.run(*a, check=True, cwd=k.pop("cwd", ROOT), **k)

# ---------- kit PDF, sealed ----------
kit = S["kit"] | {"name": name}
tmpk = f"/tmp/kit_{slug}.json"; json.dump(kit, open(tmpk, "w"))
pdf = f"/tmp/AUTOPILOT.OI {name} Setup.pdf"
run(["python3", "build.py", tmpk, pdf], cwd=os.path.join(ROOT, "tools", "kits"))
run(["bash", "tools/kits/seal.sh", pdf, f"products/{slug}"]); os.remove(pdf)

# ---------- product.json ----------
desc = (f"<p><strong>{e(S['headline'])}</strong></p><p>{e(S['what'])}</p>"
        f"<p><strong>What you get:</strong> a Claude prompt kit (PDF): the master prompt, 5 starter prompts, a 10 minute setup guide and a tracker.</p>"
        f"<p><strong>How it works:</strong> you paste the prompt into a Claude Project and run it whenever you need it. It reads what you upload and drafts. You check it, decide and send. {e(S['doesnt'])}</p>"
        f"<p><strong>You need:</strong> {e(S['need'])}</p>"
        f"<p><em>Education only, not financial, legal or medical advice. AUTOPILOT.OI is independent and not affiliated with Anthropic.</em></p>")
prod = {"name": f"AUTOPILOT.OI {name}", "price_cents": 1000, "permalink": slug, "filename": f"AUTOPILOT.OI {name} Setup.pdf",
        "description_html": desc, "cover_url": f"https://autopilotoi.app/store/{key}-cover.png?v=1",
        "tags": S.get("tags", ["ai", "claude", "ai agent"]), "version": 1, "cover_v": 1}
json.dump(prod, open(os.path.join(ROOT, "products", slug, "product.json"), "w"), indent=2, ensure_ascii=False)

# ---------- cover + thumb ----------
json.dump(S["cover"] | {"price": "$10"}, open(os.path.join(ROOT, "tools", "kits", "covers_extra", f"{key}.json"), "w"), indent=1, ensure_ascii=False)
run(["python3", "tools/kits/covers2.py", key])

# ---------- guide ----------
gd = S["guide"] | {"kw": S["kw"], "permalink": slug, "bundle_btn": S["guide"].get("bundle_btn", "")}
json.dump(gd, open(os.path.join(ROOT, "tools", "guides", "extra", f"{key}.json"), "w"), indent=1, ensure_ascii=False)
run(["python3", "tools/guides/build.py"])

# ---------- keyword reply ----------
kp = os.path.join(ROOT, "config", "keywords.json"); kj = json.load(open(kp))
kj["replies"][S["kw"].upper()] = S["reply"]
json.dump(kj, open(kp, "w"), indent=1, ensure_ascii=False)

# ---------- demo video episode ----------
ep = S["demo"] | {"slug": slug, "name": name, "price": "$10", "kw": S["kw"], "cover": key}
json.dump(ep, open(os.path.join(ROOT, "tools", "demo", "eps", f"{slug}.json"), "w"), indent=1, ensure_ascii=False)

# ---------- log ----------
d = datetime.date.today().isoformat(); os.makedirs(os.path.join(ROOT, "docs", "daily"), exist_ok=True)
json.dump({"date": d, "slug": slug, "name": name, "kw": S["kw"], "gate": S["gate"], "posts": S["posts"],
           "links": {"guide": f"https://autopilotoi.app/g/{key}/", "gumroad": f"https://autopilotoi.gumroad.com/l/{slug}",
                     "video": f"https://autopilotoi.app/media/demo/{slug}.mp4"}},
          open(os.path.join(ROOT, "docs", "daily", f"{d}-{slug}.json"), "w"), indent=1, ensure_ascii=False)
with open(os.path.join(ROOT, "config", "approvals_queue.md"), "a") as f:
    f.write(f"\n- {d} {name} ({slug}): AUTO RELEASED, gate {sum(sc.values())}/12. Seb chose fully automatic daily agents on Oct 31 2026.\n")
print("ready:", slug, "→ commit + push, then wait for the Gumroad sync and the demo video")
