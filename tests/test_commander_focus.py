"""Commander's 'prove one funnel' proposal follows the owner's campaign focus, never a parked product."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "growthos"))
import commander  # noqa: E402

BASE = {"critical": [], "not_live_offers": [], "ungated_publishers": [], "viral_waiting_owner": [],
        "subscribers": 0, "site_connected": True, "orders": 0, "budget": {"status": "capped"}, "approvals_waiting": 0}


def _first(focus):
    s = dict(BASE, focus=focus)
    return [p for p in commander.proposals(s) if p["id"] == "first_funnel"][0]


def test_funnel_follows_campaign_focus():
    p = _first({"offer": "Front Desk Kit $39 (/front-desk/) with the free Front Desk Starter (/brain/) as entry"})
    assert p["title"] == "Prove one funnel: Front Desk Kit $39"
    assert "/front-desk/" in p["action"] and "Subscription" not in p["action"]


def test_funnel_falls_back_without_focus():
    p = _first({})
    assert p["title"] == "Prove one funnel: Subscription Leak"


def test_repo_campaign_focus_is_read():
    s = commander.snapshot(commander.Store())
    assert isinstance(s["focus"], dict)
