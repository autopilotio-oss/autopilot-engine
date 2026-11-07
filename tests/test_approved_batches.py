import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "growthos"))
import health

def test_threads_and_x_batches_count_as_approved(tmp_path):
    (tmp_path / "queue" / "threads").mkdir(parents=True)
    (tmp_path / "queue" / "x").mkdir(parents=True)
    (tmp_path / "queue" / "threads" / "d.json").write_text(json.dumps({"approval": {"quote": "q"}, "posts": [{"uuid": "u1", "metricool_id": 11}]}))
    (tmp_path / "queue" / "x" / "d.json").write_text(json.dumps([{"uuid": "u2", "approval": {"quote": "q"}}, {"uuid": "u3"}]))
    ids = health.approved_post_uuids(str(tmp_path))
    assert {"u1", "11", "u2"} <= ids and "u3" not in ids


def test_carousel_metricool_uuids_list_counts_only_when_approved(tmp_path):
    (tmp_path / "queue" / "car").mkdir(parents=True)
    (tmp_path / "queue" / "car" / "a.json").write_text(json.dumps({"approval": {"quote": "q"}, "metricool_uuids": ["c1", "c2"], "metricool_ids": [21]}))
    (tmp_path / "queue" / "car" / "b.json").write_text(json.dumps({"metricool_uuids": ["c3"]}))
    ids = health.approved_post_uuids(str(tmp_path))
    assert {"c1", "c2", "21"} <= ids and "c3" not in ids


def test_metricool_networks_flags_disconnected_threads():
    brand = {"networksData": {"instagramData": "autopilot.oi", "twitterData": "AutoPilotOi", "tiktokData": "autopilot.oi"}}
    r = health.check_metricool_networks(brand, ["instagram", "tiktok", "threads", "twitter"])[0]
    assert r["ok"] is False and r["severity"] == "SEV-2" and r["detail"].endswith("threads")
    brand["networksData"]["threadsData"] = "autopilot.oi"
    assert health.check_metricool_networks(brand, ["instagram", "tiktok", "threads", "twitter"])[0]["ok"] is True


def test_metricool_networks_reads_campaign_cadence():
    r = health.check_metricool_networks({"networksData": {}})[0]
    assert not r["ok"] and "instagram" in r["detail"]
