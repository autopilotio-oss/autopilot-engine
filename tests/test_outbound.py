"""Outbound Intelligence V3 tests. Fictional example businesses only (example.com / example.org)."""
import csv, datetime, json, os, sys, tempfile, importlib
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts", "outbound"))
import engine

TODAY = datetime.date(2026, 11, 3)


def sample(**kw):
    r = dict.fromkeys(engine.LEAD_FIELDS, "")
    r.update(business_name="Example Detailing (fictional)", website="https://example.com", location="Demo City",
             niche="mobile detailing", source_url="https://example.com/about", public_contact_channel="contact form",
             contact_permission="owner_relationship", need_signal="quotes by text only",
             need_evidence_url="https://example.com/quote", verified_fact="you come to the customer's home or office",
             fact_source_url="https://example.com/services", business_fit="verified", checked_at=TODAY.isoformat(),
             offer="front_desk_setup")
    r.update(kw)
    return r


@pytest.fixture
def tmp(monkeypatch):
    d = tempfile.mkdtemp()
    monkeypatch.setattr(engine, "OUTREACH", os.path.join(d, "outreach.csv"))
    monkeypatch.setattr(engine, "SUPPRESSION", os.path.join(d, "suppression.csv"))
    monkeypatch.setattr(engine, "LEDGER", os.path.join(d, "events.jsonl"))
    monkeypatch.setattr(engine, "sender", lambda: {"sender_name": "Seb, AUTOPILOT.OI", "postal_address": "1 Example St, Demo City"})
    yield d
    importlib.reload(engine)


# --- ported from the V3 starter ---
def test_full_score_needs_approval(tmp):
    s, flag, action = engine.score(sample(), TODAY)
    assert s == 100 and flag == "NEEDS_APPROVAL" and "nothing is sent" in action


def test_suppression_blocks_draft(tmp):
    engine.opt_out("https://example.com", today=TODAY)
    s, flag, _ = engine.score(sample(), TODAY)
    assert (s, flag) == (0, "SUPPRESSED") and engine.draft(sample(), "x", flag) == ""


def test_missing_fact_blocks_draft(tmp):
    s, flag, _ = engine.score(sample(verified_fact=""), TODAY)
    assert flag == "NEEDS_FACT_CHECK" and engine.draft(sample(), "x", flag) == ""


def test_no_source_is_incomplete(tmp):
    assert engine.score(sample(source_url=""), TODAY)[1] == "INCOMPLETE"


def test_duplicate_company_fails(tmp):
    src = os.path.join(tmp, "in.csv")
    with open(src, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=engine.LEAD_FIELDS); w.writeheader()
        w.writerow(sample()); w.writerow(sample(business_name="Same site, other name", website="http://www.example.com/"))
    with pytest.raises(ValueError, match="duplicate"):
        engine.process(src, os.path.join(tmp, "out.csv"), TODAY)


# --- V3 gates added here ---
def test_missing_evidence_scores_zero_not_guessed(tmp):
    s, _, _ = engine.score(sample(need_evidence_url="", contact_permission="", business_fit="", checked_at="2026-01-01"), TODAY)
    assert s == 30   # only the niche is verified


def test_public_contact_page_is_partial_permission(tmp):
    s, flag, _ = engine.score(sample(contact_permission="business_contact_page"), TODAY)
    assert s == 90 and flag == "NEEDS_APPROVAL"


def test_lead_ref_is_stable_and_pseudonymous(tmp):
    a = engine.lead_ref("https://www.Example.com/about"); b = engine.lead_ref("example.com")
    assert a == b and a.startswith("det-") and "example" not in a


def test_draft_is_honest_and_uses_offer_prices(tmp):
    d = engine.draft(sample(), "det-abc", "NEEDS_APPROVAL")
    assert "$39" in d and "$299" in d and "never sends anything on its own" in d
    assert "you come to the customer's home or office" in d and "utm_content=det-abc" in d
    assert engine.claim_issues(d) == []


def test_claim_checker_blocks_bad_drafts(tmp):
    bad = "It replies automatically 24/7 and you get more bookings. Only $19. Reply no thanks"
    issues = engine.claim_issues(bad)
    assert any("automatically" in i for i in issues) and any("$19" in i for i in issues) and any("opt out" in i for i in issues)


def test_missing_postal_address_blocks(tmp, monkeypatch):
    monkeypatch.setattr(engine, "sender", lambda: {"sender_name": "Seb", "postal_address": None})
    d = engine.draft(sample(), "det-abc", "NEEDS_APPROVAL")
    assert any("CAN-SPAM" in i for i in engine.claim_issues(d))


def test_contact_requires_approval_and_is_idempotent(tmp):
    ref = engine.lead_ref("example.com")
    engine.record(ref, "DRAFTED", today=TODAY)
    with pytest.raises(PermissionError):
        engine.record(ref, "CONTACTED", today=TODAY)
    with pytest.raises(PermissionError):
        engine.record(ref, "APPROVED", today=TODAY)          # no approver
    assert engine.record(ref, "APPROVED", approved_by="Seb", note="ok", today=TODAY)
    assert engine.record(ref, "CONTACTED", today=TODAY)
    assert engine.record(ref, "CONTACTED", today=TODAY) is False   # same stage twice is not logged twice


def test_opt_out_is_final(tmp):
    engine.opt_out("example.com", today=TODAY)
    with pytest.raises(PermissionError):
        engine.record(engine.lead_ref("example.com"), "CONTACTED", today=TODAY)
    assert engine.opt_out("example.com", today=TODAY) is False


def test_paid_only_from_verified_ledger(tmp):
    ref = engine.lead_ref("example.com")
    engine.record(ref, "APPROVED", approved_by="Seb", today=TODAY)
    engine.record(ref, "INTERESTED", today=TODAY)            # a reply is not a sale
    assert engine.summary()["paid"] == 0
    with open(engine.LEDGER, "w") as f:
        for e in [{"type": "order_paid", "order": "o1", "test": True, "free": False, "utm_content": ref, "gross_cents": 29900},
                  {"type": "order_paid", "order": "o2", "test": False, "free": True, "utm_content": ref, "gross_cents": 0},
                  {"type": "order_paid", "order": "o3", "test": False, "free": False, "utm_content": "unknown", "gross_cents": 3900}]:
            f.write(json.dumps(e) + "\n")
    assert engine.reconcile(today=TODAY) == 0                # test, free and unattributed orders never count
    with open(engine.LEDGER, "a") as f:
        f.write(json.dumps({"type": "order_paid", "order": "o4", "test": False, "free": False, "utm_content": ref,
                            "gross_cents": 29900, "offer_id": "front_desk_setup"}) + "\n")
    assert engine.reconcile(today=TODAY) == 1 and engine.reconcile(today=TODAY) == 0
    assert engine.summary()["paid"] == 1


def test_refunded_order_is_not_paid(tmp):
    ref = engine.lead_ref("example.com")
    engine.record(ref, "APPROVED", approved_by="Seb", today=TODAY)
    with open(engine.LEDGER, "w") as f:
        f.write(json.dumps({"type": "order_paid", "order": "o9", "test": False, "free": False, "utm_content": ref, "gross_cents": 3900}) + "\n")
        f.write(json.dumps({"type": "refund_processed", "order": "o9", "refund_cents": 3900}) + "\n")
    assert engine.reconcile(today=TODAY) == 0


def test_batch_writes_only_pseudonymous_public_rows(tmp):
    src = os.path.join(tmp, "in.csv")
    with open(src, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=engine.LEAD_FIELDS); w.writeheader()
        w.writerow(sample()); w.writerow(sample(business_name="Second (fictional)", website="https://example.org", verified_fact=""))
    out = engine.process(src, os.path.join(tmp, "out.csv"), TODAY)
    pub = open(engine.OUTREACH).read()
    assert "Example Detailing" not in pub and "example.com" not in pub and "example.org" not in pub
    assert [o["review_flag"] for o in out] == ["NEEDS_APPROVAL", "NEEDS_FACT_CHECK"]
    assert engine.summary()["by_stage"]["DRAFTED"] == 1 and engine.summary()["by_stage"]["RESEARCHED"] == 1


def test_module_cannot_send_or_touch_network():
    src = open(os.path.join(ROOT, "scripts", "outbound", "engine.py")).read()
    for banned in ("smtplib", "urllib.request", "requests", "http.client", "socket", "sendmail", "subprocess"):
        assert banned not in src, banned


def test_public_logs_hold_no_names_or_emails():
    for f in ("sales/outreach.csv", "sales/suppression.csv"):
        t = open(os.path.join(ROOT, f)).read()
        assert "@" not in t and "http" not in t, f


def test_follow_up_due_once_after_wait(tmp):
    ref = engine.lead_ref("example.com")
    engine.record(ref, "APPROVED", approved_by="Seb", today=TODAY)
    engine.record(ref, "CONTACTED", today=TODAY)
    assert engine.followups_due(today=TODAY + datetime.timedelta(days=2)) == []
    assert engine.followups_due(today=TODAY + datetime.timedelta(days=4)) == [ref]
    engine.record(ref, "INTERESTED", today=TODAY + datetime.timedelta(days=4))
    assert engine.followups_due(today=TODAY + datetime.timedelta(days=9)) == []


def test_no_channel_means_no_draft(tmp):
    s, flag, action = engine.score(sample(contact_permission=""), TODAY)
    assert flag == "NO_AUTHORIZED_CHANNEL" and "warm intro" in action
    assert engine.draft(sample(), "x", flag) == ""


def test_rerunning_the_batch_adds_nothing(tmp):
    src = os.path.join(tmp, "in.csv")
    with open(src, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=engine.LEAD_FIELDS); w.writeheader(); w.writerow(sample())
    engine.process(src, os.path.join(tmp, "out.csv"), TODAY)
    n = len(engine.rows())
    engine.process(src, os.path.join(tmp, "out.csv"), TODAY)
    assert len(engine.rows()) == n == 3 and engine.summary()["by_stage"]["DRAFTED"] == 1
