"""Creative experiments (Revenue Engine 2.0, Upgrade B). One JSON object per line in experiments/experiments.jsonl.

Every content test declares ONE variable and ONE primary objective. A post without an objective stays a draft.
python3 scripts/revenue/experiments.py check   -> validate
python3 scripts/revenue/experiments.py due     -> experiments whose review date has passed and still need a decision"""
import json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ids import ID_RE, parse_content_id

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILE = os.path.join(ROOT, "experiments", "experiments.jsonl")
OBJECTIVES = {"reach", "guide_visit", "optin", "quiz_complete", "purchase", "inquiry"}
VARIABLES = {"hook", "opening", "cta", "landing_headline", "cover", "post_time", "format"}
STATUS = {"draft", "approved", "running", "measured", "decided", "dropped"}
REQUIRED = ["experiment_id", "content_id", "hypothesis", "offer_id", "platform", "audience", "variable_under_test",
            "variant_a", "variant_b", "publish_window", "review_date", "primary_metric", "min_sample", "guardrails", "status"]


def validate(e):
    errs = [f"missing {k}" for k in REQUIRED if e.get(k) in (None, "", [])]
    if e.get("variable_under_test") not in VARIABLES:
        errs.append(f"variable_under_test must be one of {sorted(VARIABLES)}")
    if e.get("primary_metric", {}).get("objective") not in OBJECTIVES if isinstance(e.get("primary_metric"), dict) else True:
        errs.append(f"primary_metric.objective must be one of {sorted(OBJECTIVES)}")
    if e.get("status") not in STATUS:
        errs.append("bad status")
    for k in ("experiment_id", "offer_id"):
        if e.get(k) and not ID_RE.match(e[k]):
            errs.append(f"{k} not a canonical id")
    if e.get("content_id") and not parse_content_id(e["content_id"])["valid"]:
        errs.append("content_id not canonical (platform_format_offer_NNN)")
    if e.get("status") == "decided" and not (e.get("decision") and e.get("evidence_link")):
        errs.append("decided experiments need decision + evidence_link")
    if e.get("decision") in ("a_wins", "b_wins") and (e.get("observed_sample") or 0) < (e.get("min_sample") or 1):
        errs.append("winner declared below the predeclared min_sample")
    return errs


def load():
    return [json.loads(l) for l in open(FILE) if l.strip()] if os.path.exists(FILE) else []


if __name__ == "__main__":
    ex = load(); cmd = (sys.argv[1:] or ["check"])[0]
    if cmd == "due":
        today = datetime.date.today().isoformat()
        for e in ex:
            if e.get("status") in ("running", "measured") and e.get("review_date", "9") <= today:
                print(e["experiment_id"], e["review_date"], e["variable_under_test"])
    else:
        bad = {e.get("experiment_id", "?"): validate(e) for e in ex}
        bad = {k: v for k, v in bad.items() if v}
        print(json.dumps(bad, indent=1) if bad else f"{len(ex)} experiments valid"); sys.exit(1 if bad else 0)
