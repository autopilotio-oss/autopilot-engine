"""Acceptance tests for NO PROOF, NO POST (Viral Validation V2, page 9)."""
import copy, json, os, sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "viral"))
import gate  # noqa: E402

TODAY = "2026-10-31"
CID = "vv_subs_tt_reveal_001"
SAMPLE = [41000, 52000, 38000, 60000, 45000, 70000, 33000, 48000, 55000, 50000]  # median 49000


def ref(i, creator, views=650000, prov="youtube page metadata viewCount via WebFetch", sample=SAMPLE, median=49000, **kw):
    r = {"ref_id": f"r{i}", "topic": "subscription", "platform": "youtube", "url": f"https://www.youtube.com/shorts/abcdEF{i}xyz1",
         "creator": creator, "published": "2026-09-20", "captured": TODAY, "views": views, "views_provenance": prov,
         "is_paid_ad": False, "recent_views_sample": sample, "creator_median": median, "hook": "annual cost reveal"}
    r.update(kw)
    return r


def concept(**kw):
    c = {"content_id": CID, "agent": "subscription", "offer_id": "subs_agent", "platforms": ["tiktok", "instagram"],
         "problem": "forgotten subscriptions", "audience": "US adults with recurring charges", "references": ["r1", "r2", "r3"],
         "hook": "This 9 dollar charge costs you more than you think",
         "script": {"beats": [{"t": "0-2", "vo": "Nine ninety nine a month.", "on_screen": "$9.99/mo"},
                              {"t": "2-7", "vo": "That is one hundred nineteen dollars a year.", "on_screen": "$119.88/yr"}],
                    "caption": "Sample numbers. Free guide in bio."},
         "claims": [{"claim": "$9.99 x 12 = $119.88", "source_url": "https://consumer.ftc.gov/articles/getting-and-out-free-trials-auto-renewals-and-negative-option-subscriptions"}],
         "demo": {"tested": True, "artifact": "docs/media/demo/subs-agent.mp4", "synthetic": True, "labeled": True},
         "rights": {"audio": "original", "footage": "original", "voice": "licensed", "copied_footage": False, "copied_script": False},
         "cta": {"url": f"https://autopilotoi.app/g/subs/?utm_source=tiktok&utm_content={CID}", "checked": TODAY, "status": 200},
         "editorial": {"opening_hook": 14, "audience_relevance": 14, "proof_on_screen": 9, "business_fit_cta": 9, "visual_craft": 5, "reviewer": "test"},
         "state": "IDEA"}
    c.update(kw)
    return c


@pytest.fixture
def reg(tmp_path, monkeypatch):
    os.makedirs(tmp_path / "concepts")
    monkeypatch.setattr(gate, "_now", lambda: TODAY + "T12:00:00+00:00")
    def setup(refs, c):
        with open(tmp_path / "evidence.jsonl", "w") as f:
            for r in refs:
                f.write(json.dumps(r) + "\n")
        gate.save_concept(c, str(tmp_path))
        return str(tmp_path)
    return setup


GOOD = [ref(1, "Creator A"), ref(2, "Creator B"), ref(3, "Creator A", views=900000)]


def run_to(root, cid, state):
    c = gate.load_concept(cid, root)
    while c["state"] != state and c["state"] not in ("HOLD",):
        c = gate.advance(cid, "test", root, TODAY)
    return c


def test_missing_evidence_links_blocked(reg):
    root = reg(GOOD[:1], concept())
    c = run_to(root, CID, "VERIFIED")
    assert c["state"] == "HOLD" and c["hold_reason"] == "EVIDENCE"


def test_fake_view_count_blocked(reg):
    refs = [ref(1, "Creator A", prov="search_snippet_only"), GOOD[1], GOOD[2]]
    root = reg(refs, concept())
    ok, why, _ = gate.qualify(refs[0], TODAY)
    assert not ok and "VIEWS_UNVERIFIED" in why
    assert run_to(root, CID, "VERIFIED")["state"] == "HOLD"


def test_invented_median_blocked():
    ok, why, _ = gate.qualify(ref(1, "A", median=10000), TODAY)
    assert not ok and "MEDIAN_DOES_NOT_MATCH_SAMPLE" in why


def test_only_one_creator_blocked(reg):
    refs = [ref(1, "Creator A"), ref(2, "Creator A"), ref(3, "creator a")]
    root = reg(refs, concept())
    f, _, _ = gate.evidence_check(gate.load_concept(CID, root), gate.load_evidence(root), TODAY)
    assert "FEWER_THAN_2_CREATORS" in f
    assert run_to(root, CID, "VERIFIED")["state"] == "HOLD"


def test_high_views_weak_relative_performance_blocked():
    big = [900000] * 10
    ok, why, _ = gate.qualify(ref(1, "Big", views=1500000, sample=big, median=900000), TODAY)
    assert not ok and "WEAK_RELATIVE_PERFORMANCE" in why


def test_unmeasurable_median_not_certified():
    ok, why, _ = gate.qualify(ref(1, "A", sample=[], median=None), TODAY)
    assert not ok and "OUTPERFORMANCE_NOT_MEASURABLE" in why


def test_paid_ad_old_and_expired_evidence_blocked():
    assert "PAID_AD_NOT_ORGANIC_PROOF" in gate.qualify(ref(1, "A", is_paid_ad=True), TODAY)[1]
    assert "TOO_OLD" in gate.qualify(ref(1, "A", published="2025-12-01"), TODAY)[1]
    assert "EVIDENCE_EXPIRED" in gate.qualify(ref(1, "A", captured="2026-10-01"), TODAY)[1]
    assert "URL_INVALID" in gate.qualify(ref(1, "A", url="https://example.com/video"), TODAY)[1]


def test_misleading_claim_blocked(reg):
    c = concept(); c["script"]["caption"] = "Guaranteed to save you money"
    root = reg(GOOD, c)
    out = run_to(root, CID, "SCRIPTED")
    assert out["state"] == "HOLD" and out["hold_reason"] == "CLAIMS_OR_RIGHTS"


def test_dash_and_unsourced_numbers_blocked():
    c = concept(claims=[]); c["hook"] = "Cancel these — now"
    f = gate.claims_check(c)
    assert "DASH_IN_COPY" in f and "NUMBERS_WITHOUT_CLAIM_SOURCES" in f


def test_copied_footage_blocked(reg):
    c = concept(); c["rights"]["copied_footage"] = True
    root = reg(GOOD, c)
    assert run_to(root, CID, "SCRIPTED")["hold_reason"] == "CLAIMS_OR_RIGHTS"


def test_broken_or_untracked_cta_blocked():
    c = concept(); c["cta"]["url"] = f"https://autopilotoi.app/g/nope/?utm_content={CID}"
    assert "CTA_PAGE_MISSING" in gate.cta_check(c, TODAY)
    c = concept(); c["cta"]["url"] = "https://autopilotoi.app/g/subs/"
    assert "CTA_NOT_TRACKED" in gate.cta_check(c, TODAY)
    c = concept(); c["cta"]["status"] = 404
    assert "CTA_NOT_QA_TESTED" in gate.cta_check(c, TODAY)
    c = concept(); c["cta"]["product_permalink"] = "not-a-live-product"
    assert "PRODUCT_NOT_LIVE" in gate.cta_check(c, TODAY)


def test_defective_demo_blocked(reg):
    c = concept(); c["demo"]["tested"] = False
    root = reg(GOOD, c)
    assert run_to(root, CID, "DEMO_TESTED")["hold_reason"] == "DEMO"


def test_low_score_never_passes(reg):
    c = concept(); c["editorial"] = {"opening_hook": 5, "audience_relevance": 5, "proof_on_screen": 5, "business_fit_cta": 5, "visual_craft": 1}
    root = reg(GOOD, c)
    out = run_to(root, CID, "QUALITY_PASSED")
    assert out["state"] == "HOLD" and out["hold_reason"].startswith("SCORE_")


def test_scheduler_bypass_blocked(reg):
    root = reg(GOOD, concept())
    c = run_to(root, CID, "QUALITY_PASSED")
    assert c["state"] == "QUALITY_PASSED" and c["last_score"]["total"] >= 85
    with pytest.raises(gate.GateError):
        gate.advance(CID, "scheduler", root, TODAY)                     # cannot self approve
    with pytest.raises(gate.GateError):
        gate.approve(CID, "trend-scout", "chat", "yes", root, TODAY)     # not an owner
    with pytest.raises(gate.GateError):
        gate.approve(CID, "Seb", "metricool", "", root, TODAY)           # no owner channel / words
    with pytest.raises(gate.GateError):
        gate.mark_published(CID, "https://www.tiktok.com/@x/video/1", "tiktok", "scheduler", root)
    events = [json.loads(l)["event"] for l in open(os.path.join(root, "audit.jsonl"))]
    assert events.count("BYPASS_BLOCKED") >= 3
    assert gate.load_concept(CID, root)["state"] == "QUALITY_PASSED"


def test_approved_original_safe_video_can_be_queued(reg):
    root = reg(GOOD, concept())
    run_to(root, CID, "QUALITY_PASSED")
    gate.approve(CID, "Seb", "chat", "approve vv_subs_tt_reveal_001", root, TODAY)
    c = gate.advance(CID, "publisher", root, TODAY)
    assert c["state"] == "QUEUED" and c["queued"]["version"] == gate.version_hash(c)
    ok, n = gate.verify_audit(root)
    assert ok and n >= 6


def test_edit_after_approval_invalidates(reg):
    root = reg(GOOD, concept())
    run_to(root, CID, "QUALITY_PASSED")
    gate.approve(CID, "Seb", "chat", "approve", root, TODAY)
    c = gate.load_concept(CID, root); c["hook"] = "A different hook"; gate.save_concept(c, root)
    out = gate.advance(CID, "publisher", root, TODAY)
    assert out["state"] == "HOLD" and out["hold_reason"] == "APPROVAL_STALE_CONTENT_CHANGED"


def test_metrics_attach_to_correct_content_id(reg):
    root = reg(GOOD, concept())
    run_to(root, CID, "QUALITY_PASSED"); gate.approve(CID, "Seb", "chat", "approve", root, TODAY); gate.advance(CID, "p", root, TODAY)
    gate.mark_published(CID, "https://www.tiktok.com/@autopilot.oi/video/123456789", "tiktok", "publisher", root)
    ledger = [{"type": "sale", "utm_content": CID, "gross_cents": 1000}, {"type": "sale", "utm_content": "other", "gross_cents": 4900},
              {"type": "sale", "utm_content": None, "gross_cents": 1000}]
    m = gate.add_metrics(CID, "24h", {"views": 1200}, "metricool", root, ledger)
    assert m["attributed_orders"] == 1 and m["attributed_gross_cents"] == 1000
    m2 = gate.add_metrics(CID, "72h", {"views": 1500}, "metricool", root, [])
    assert m2["attribution"].startswith("none matched")


def test_audit_tamper_detected(reg):
    root = reg(GOOD, concept())
    run_to(root, CID, "VERIFIED")
    p = os.path.join(root, "audit.jsonl"); lines = open(p).read().splitlines()
    e = json.loads(lines[0]); e["actor"] = "someone else"; lines[0] = json.dumps(e)
    open(p, "w").write("\n".join(lines) + "\n")
    assert gate.verify_audit(root)[0] is False


def test_queue_guard(reg, tmp_path):
    root = reg(GOOD, concept())
    q = tmp_path / "q"; os.makedirs(q)
    json.dump([{"id": "x1", "at": "2026-11-05T13:00:00-05:00", "text": "hi"}], open(q / "a.json", "w"))
    assert any("no content_id" in p for p in gate.check_queue(root, str(q)))
    json.dump([{"id": "x1", "at": "2026-11-05T13:00:00-05:00", "content_id": CID}], open(q / "a.json", "w"))
    assert gate.check_queue(root, str(q))            # concept not queued yet
    run_to(root, CID, "QUALITY_PASSED"); gate.approve(CID, "Seb", "chat", "approve", root, TODAY); gate.advance(CID, "p", root, TODAY)
    assert gate.check_queue(root, str(q)) == []
    json.dump([{"id": "old", "at": "2026-10-30T09:00:00-05:00"}], open(q / "a.json", "w"))
    assert gate.check_queue(root, str(q)) == []       # before enforcement date
