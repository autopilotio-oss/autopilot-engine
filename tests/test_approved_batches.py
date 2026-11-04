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
