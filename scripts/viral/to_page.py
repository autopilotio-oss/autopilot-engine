"""Builds the Approval Queue page records (one per concept) from the register.
python3 scripts/viral/to_page.py            -> prints JSON {content_id: record} for db_write (collection "concepts")"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate  # noqa: E402


def record(c, ev, today=None):
    s = gate.score(c, ev, today)
    refs = []
    for rid in c.get("references", []):
        r = ev.get(rid)
        if not r:
            refs.append({"url": "", "creator": rid, "qualified": False, "reasons": ["NOT_IN_REGISTER"]}); continue
        ok, why, flags = gate.qualify(r, today)
        med = r.get("creator_median")
        refs.append({"url": r["url"], "creator": r["creator"], "platform": r["platform"], "published": r.get("published"),
                     "views": r.get("views"), "median": med, "n": len(r.get("recent_views_sample") or []),
                     "multiple": round(r["views"] / med, 1) if isinstance(med, int) and med and isinstance(r.get("views"), int) else None,
                     "qualified": ok, "reasons": why + flags, "hook": r.get("hook")})
    return {"content_id": c["content_id"], "agent": c.get("agent"), "title": c.get("title"), "hook": c.get("hook"),
            "state": c["state"], "hold_reason": c.get("hold_reason"), "version": gate.version_hash(c), "why": c.get("why"),
            "script": c.get("script"), "cta": {"url": (c.get("cta") or {}).get("url")}, "preview": c.get("preview"),
            "refs": refs, "score": {"total": s["total"], "points": s["points"], "hard_fails": s["hard_fails"], "decision": s["decision"]}}


if __name__ == "__main__":
    ev = gate.load_evidence()
    print(json.dumps({c["content_id"]: record(c, ev) for c in gate.all_concepts()}, indent=1, ensure_ascii=False))
