"""Every live page probe in scripts/growthos/health.py must match the committed docs/ page, so a redesign that
drops a marker fails Tests here instead of opening a false SEV-2 incident on the live site."""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts", "growthos"))
import health  # noqa: E402


def test_page_markers_exist_in_committed_pages():
    missing = []
    for name, url, marker in health.PAGES:
        path = url.split("autopilotoi.app/", 1)[1]
        f = os.path.join(ROOT, "docs", path, "index.html")
        assert os.path.exists(f), f"{name}: {f} missing"
        if marker not in open(f, encoding="utf-8").read():
            missing.append(f"{name}: '{marker}' not in docs/{path}index.html")
    assert not missing, missing
