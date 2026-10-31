"""Revenue Engine 2.0 acceptance tests. Run: python3 -m pytest -q tests/"""
import datetime, glob, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts", "revenue"))
import ids, ledger, research, experiments, catalog, quality, brief  # noqa: E402

TODAY = datetime.date(2026, 11, 5)


def sale(i, perm="subs-agent", price=1000, fee=129, **kw):
    return {"id": f"sale{i}", "product_permalink": perm, "price": price, "gumroad_fee": fee, "currency": "usd",
            "created_at": "2026-11-04T15:00:00Z", "email": "buyer@example.com", "full_name": "Real Person", **kw}


# ---------- IDs + UTMs ----------
def test_ids_and_utm():
    assert ids.offer_id("all-money-agents") == "all_money_agents"
    assert ids.permalink("all_money_agents") == "all-money-agents"
    assert ids.campaign_id("Subscription Leak", datetime.date(2026, 11, 3)) == "subscription_leak_2026w45"
    cid = ids.content_id("ig", "reel", "subs", 3, "b")
    assert cid == "ig_reel_subs_003_b" and ids.parse_content_id(cid)["platform"] == "instagram"
    u = ids.utm_url("https://autopilotoi.app/g/subs/?x=1", "instagram", "subscription_leak_2026w45", cid)
    assert "x=1" in u and "utm_source=instagram" in u and "utm_medium=organic_social" in u and f"utm_content={cid}" in u


def test_missing_utms_stay_unknown():
    assert ids.source_of({}) == {k: "unknown" for k in ("utm_source", "utm_medium", "utm_campaign", "utm_content")}
    assert ids.source_of({"utm_source": ["TikTok"]})["utm_source"] == "tiktok"


# ---------- Ledger: payment truth ----------
def test_ledger_strips_pii():
    evs = ledger.to_events(sale(1))
    blob = json.dumps(evs)
    assert "buyer@example.com" not in blob and "Real Person" not in blob and "sale1" not in blob
    assert evs[0]["offer_id"] == "subs_agent" and evs[0]["gross_cents"] == 1000 and evs[0]["utm_source"] == "unknown"


def test_ledger_dedupes_repeated_syncs():
    first = ledger.to_events(sale(1)) + ledger.to_events(sale(2))
    events, added = ledger.merge([], first)
    assert added == 2
    events, added = ledger.merge(events, ledger.to_events(sale(1)) + ledger.to_events(sale(2)))
    assert added == 0 and len(events) == 2


def test_refund_reconciles():
    events, _ = ledger.merge([], ledger.to_events(sale(1)) + ledger.to_events(sale(2, refunded=True)))
    s = ledger.summarize(events, TODAY)
    w = s["last_7d"]["by_currency"]["usd"]
    assert s["last_7d"]["orders"] == 2 and w["gross_cents"] == 2000 and w["refund_cents"] == 1000
    assert w["net_cents"] == 2000 - 258 - 1000 and s["refunds_all_time"] == 1


def test_zero_sales_case():
    s = ledger.summarize([], TODAY)
    assert s["verified_orders_all_time"] == 0 and s["last_7d"]["orders"] == 0 and s["attribution_coverage"] is None
    lines, n = brief.revenue_lines(s)
    assert n == 0 and "0 verified orders" in lines[0] and "$0.00" in lines[0]


def test_currencies_never_mixed_and_tests_excluded():
    evs = ledger.to_events(sale(1)) + ledger.to_events(sale(2, currency="eur")) + ledger.to_events(sale(3, test=True)) + ledger.to_events(sale(4, price=0))
    s = ledger.summarize(ledger.merge([], evs)[0], TODAY)
    assert set(s["last_7d"]["by_currency"]) == {"usd", "eur"} and s["verified_orders_all_time"] == 2


def test_attribution_from_url_params():
    s = ledger.summarize(ledger.merge([], ledger.to_events(sale(1, url_params={"utm_source": "instagram", "utm_campaign": "subs_2026w45"})) + ledger.to_events(sale(2)))[0], TODAY)
    assert s["by_source"]["instagram"]["orders"] == 1 and s["by_source"]["unknown"]["orders"] == 1 and s["attribution_coverage"] == 0.5


# ---------- Research + experiments ----------
def rec(i, post=None, med=None, n=10):
    return {"id": f"r{i}", "platform": "instagram", "account": "@x", "post_url": f"https://instagram.com/p/{i}", "collected": "2026-11-01",
            "topic": "subscriptions", "format": "reel", "hook_type": "number", "cta": "comment", "provenance": "test",
            "audience_problem_fit": 4, "offer_relevance": 5, "evidence_quality": 3, "ease": 4, "offer_id": "subs_agent",
            "original_angle": "ours", "status": "new", "metric": "views", "post_value": post, "creator_median": med, "median_sample": n}


def test_research_scoring_and_unbenchmarked():
    ranked, unb = research.score_all([rec(1, 50000, 5000), rec(2, 6000, 5000), rec(3), rec(4, 9000, 1000, n=3)])
    assert [r["id"] for r in ranked] == ["r1", "r2"] and ranked[0]["outlier_ratio"] == 10.0
    assert {r["id"] for r in unb} == {"r3", "r4"} and all(r["opportunity_score"] is None for r in unb)
    assert research.validate(rec(1, 50000, 5000)) == [] and "creator_median needs median_sample >= 5 posts" in research.validate(rec(4, 9000, 1000, n=3))


def test_experiment_rules():
    e = {"experiment_id": "subs_hook_001", "content_id": "ig_reel_subs_003_a", "hypothesis": "A number hook beats a question",
         "offer_id": "subs_agent", "platform": "instagram", "audience": "non followers (trial reel)", "variable_under_test": "hook",
         "variant_a": "$133 a month on things you forgot", "variant_b": "Do you know what you pay for?", "publish_window": "2026-11-03/2026-11-06",
         "review_date": "2026-11-07", "primary_metric": {"objective": "guide_visit", "metric": "guide visits per 1000 views"},
         "min_sample": 1000, "guardrails": ["no hype", "same CTA"], "status": "running"}
    assert experiments.validate(e) == []
    bad = dict(e, decision="a_wins", observed_sample=40, status="decided", evidence_link="x")
    assert "winner declared below the predeclared min_sample" in experiments.validate(bad)
    assert experiments.validate(dict(e, variable_under_test="everything"))


# ---------- Catalog, funnels, quality ----------
def test_catalog_live_offers_have_guides_and_known_links():
    cat = catalog.build()
    live = [o for o in cat["offers"] if o["status"] == "live"]
    assert len(live) >= 8
    for o in live:
        if o["kind"] == "kit":
            assert o["guides"], f"{o['offer_id']} has no guide"
    unknown = [m for k, m in catalog.issues(cat) if "unknown Gumroad product" in m or "retired product" in m or "has no page" in m]
    assert not unknown, unknown


def test_quality_gate_passes_catalog():
    slugs = [os.path.basename(os.path.dirname(f)) for f in glob.glob(os.path.join(ROOT, "products", "*", "product.json")) if not json.load(open(f)).get("retired")]
    errs = [e for s in slugs for e in quality.check(s)]
    assert not errs, errs


def test_sitemap_urls_have_pages():
    sm = open(os.path.join(ROOT, "docs", "sitemap.xml")).read()
    for path in re.findall(r"https://autopilotoi\.app/([^<]*)</loc>", sm):
        assert os.path.exists(os.path.join(ROOT, "docs", path, "index.html")), path


def test_guide_pages_build_reproducibly():
    """The site builder runs clean and produces no unexpected diff (production pages preserved)."""
    r = subprocess.run(["python3", "tools/guides/build.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    diff = subprocess.run(["git", "status", "--porcelain", "docs/g", "docs/sitemap.xml"], cwd=ROOT, capture_output=True, text=True).stdout
    assert diff.strip() == "", diff


# ---------- PII + credentials ----------
SECRET = re.compile(r"(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-ant-[A-Za-z0-9-]{20,}|xox[bp]-[A-Za-z0-9-]{20,}|-----BEGIN (RSA |EC )?PRIVATE KEY-----)")


def test_no_secrets_or_unsealed_kits_in_repo():
    files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    hits = []
    for f in files:
        if f.endswith((".png", ".jpg", ".mp4", ".enc", ".pdf", ".ttf", ".otf", ".woff2", ".zip", ".wav", ".mp3")):
            if f.endswith(".pdf") and f.startswith("products/"):
                hits.append(f"unsealed kit {f}")
            continue
        try:
            if SECRET.search(open(os.path.join(ROOT, f), encoding="utf-8", errors="ignore").read()):
                hits.append(f)
        except (IsADirectoryError, FileNotFoundError):
            pass
    assert not hits, hits


def test_ledger_files_have_no_pii():
    for f in glob.glob(os.path.join(ROOT, "state", "ledger", "*")):
        t = open(f).read()
        assert not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", t), f"email address in {f}"
