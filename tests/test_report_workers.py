"""Daily report worker labels: a worker whose last ok detail says 'awaiting approval' is ok, not 'waiting first run'."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "growthos"))
import reports


def test_awaiting_in_detail_is_ok():
    r = {"check": "worker:tiktok_intel", "ok": True, "detail": "last ok 20.9h ago (limit 192h) 3 guide fixes awaiting approval"}
    assert reports.worker_label(r) == "ok"


def test_no_heartbeat_yet_is_waiting():
    r = {"check": "worker:x", "ok": True, "detail": "no heartbeat yet (waiting for first run)"}
    assert reports.worker_label(r) == "waiting first run"


def test_not_ok_is_late():
    r = {"check": "worker:x", "ok": False, "detail": "no heartbeat yet (overdue)"}
    assert reports.worker_label(r) == "LATE/FAILED"


def test_open_checks_dedupes_daily_reopens():
    inc = {
        "inc:worker:kit_sync:2026-11-19": {"payload": {"incident_id": "inc:worker:kit_sync:2026-11-19", "check": "worker:kit_sync"}},
        "inc:worker:kit_sync:2026-11-20": {"payload": {"incident_id": "inc:worker:kit_sync:2026-11-20", "check": "worker:kit_sync"}},
        "inc:email:metricool:1a1e1ac2": {"payload": {"incident_id": "inc:email:metricool:1a1e1ac2"}},
    }
    assert reports.open_checks(inc) == 2
    assert reports.open_checks({}) == 0


def test_leads_null_kit_counts_are_missing_not_observed():
    assert reports.leads_fact({}, "none")[0] == "MISSING DATA"
    label, text = reports.leads_fact({"subscribers": None, "new_7d": None}, "2026-11-22")
    assert label == "MISSING DATA" and "None" not in text
    label, text = reports.leads_fact({"subscribers": 12, "new_7d": None}, "2026-11-22")
    assert label == "OBSERVED" and "12" in text and "new MISSING" in text and "None" not in text
