"""health.check_metricool takes the raw Metricool getScheduledPosts reply ({"data": [...]}) as well as a bare list,
so the Daily Pulse can pass the saved reply straight in (it crashed with AttributeError on the wrapper)."""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts", "growthos"))
import health  # noqa: E402

POSTS = [
    {"uuid": "1", "draft": False, "providers": [{"network": "instagram", "status": "PUBLISHED"}]},
    {"uuid": "2", "draft": False, "providers": [{"network": "tiktok", "status": "ERROR"}]},
]


def _by_check(out):
    return {r["check"]: r for r in out}


def test_wrapper_and_list_give_same_result():
    assert health.check_metricool({"data": POSTS}) == health.check_metricool(POSTS)
    r = _by_check(health.check_metricool({"data": POSTS}))["metricool_errors"]
    assert r["ok"] is False and r["detail"].startswith("1 post")


def test_empty_wrapper_is_ok():
    r = _by_check(health.check_metricool({"data": []}))["metricool_errors"]
    assert r["ok"] is True
    r = _by_check(health.check_metricool({}))["metricool_errors"]
    assert r["ok"] is True
