"""Competitor / outlier research queue (Revenue Engine 2.0, Upgrade A).

Records live in research/queue.jsonl, one JSON object per candidate:
  id, platform, account, post_url, collected (UTC date), posted (date or null), topic, format, hook_type, cta,
  metric ("views" or "interactions"), post_value, creator_median, median_sample (n posts), median_window,
  provenance (where the numbers came from, e.g. "metricool competitors api 2026-11-03" or "public page, manual"),
  audience_problem_fit (0-5), offer_relevance (0-5), evidence_quality (0-5), ease (0-5),
  offer_id, original_angle (our own rewrite of the principle, never their words), status (new|briefed|tested|dropped)

python3 scripts/revenue/research.py rank      -> scored list (unbenchmarked items are listed separately, never scored)
python3 scripts/revenue/research.py check     -> validates every record"""
import json, os, sys, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUEUE = os.path.join(ROOT, "research", "queue.jsonl")
W = {"relative_outlier": .35, "audience_problem_fit": .25, "offer_relevance": .20, "evidence_quality": .10, "ease": .10}
REQUIRED = ["id", "platform", "account", "post_url", "collected", "topic", "format", "hook_type", "cta", "provenance",
            "audience_problem_fit", "offer_relevance", "evidence_quality", "ease", "offer_id", "original_angle", "status"]


def load(path=QUEUE):
    return [json.loads(l) for l in open(path) if l.strip()] if os.path.exists(path) else []


def validate(r):
    errs = [f"missing {k}" for k in REQUIRED if r.get(k) in (None, "")]
    for k in ("audience_problem_fit", "offer_relevance", "evidence_quality", "ease"):
        if isinstance(r.get(k), (int, float)) and not 0 <= r[k] <= 5:
            errs.append(f"{k} must be 0..5")
    if r.get("post_value") is not None and r.get("creator_median") is not None:
        if not r.get("median_sample") or r["median_sample"] < 5:
            errs.append("creator_median needs median_sample >= 5 posts")
        if r.get("metric") not in ("views", "interactions"):
            errs.append("metric must be views or interactions")
    return errs


def benchmarked(r):
    return bool(r.get("post_value") is not None and r.get("creator_median") and (r.get("median_sample") or 0) >= 5)


def score_all(records):
    """opportunity_score = .35 outlier + .25 fit + .20 offer + .10 evidence + .10 ease, each normalised 0..1.
    The outlier ratio is log-normalised across the benchmarked set. Weights are test assumptions."""
    import math
    bench = [r for r in records if benchmarked(r)]
    ratios = [r["post_value"] / r["creator_median"] for r in bench]
    lo, hi = (min(map(math.log1p, ratios)), max(map(math.log1p, ratios))) if ratios else (0, 1)
    out = []
    for r, ratio in zip(bench, ratios):
        rel = (math.log1p(ratio) - lo) / (hi - lo) if hi > lo else 1.0
        sc = (W["relative_outlier"] * rel + W["audience_problem_fit"] * r["audience_problem_fit"] / 5 + W["offer_relevance"] * r["offer_relevance"] / 5
              + W["evidence_quality"] * r["evidence_quality"] / 5 + W["ease"] * r["ease"] / 5)
        out.append({**r, "outlier_ratio": round(ratio, 2), "opportunity_score": round(sc, 3)})
    out.sort(key=lambda x: -x["opportunity_score"])
    unbench = [{**r, "opportunity_score": None, "label": "unbenchmarked"} for r in records if not benchmarked(r)]
    return out, unbench


if __name__ == "__main__":
    recs = load()
    if (sys.argv[1:] or ["rank"])[0] == "check":
        bad = {r.get("id", "?"): validate(r) for r in recs}
        bad = {k: v for k, v in bad.items() if v}
        print(json.dumps(bad, indent=1) if bad else f"{len(recs)} records valid"); sys.exit(1 if bad else 0)
    ranked, unb = score_all(recs)
    for r in ranked[:10]:
        print(f"{r['opportunity_score']:.3f}  x{r['outlier_ratio']:<5} {r['platform']:<9} {r['topic'][:40]:<40} -> {r['offer_id']}")
    print(f"\n{len(unb)} unbenchmarked (not scored): " + ", ".join(r["id"] for r in unb[:20]))
