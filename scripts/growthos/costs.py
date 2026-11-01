"""P1-13 Profit controller and budget guard (section 13).

Cost sources are recorded as spend.recorded events with kind: subscription (monthly vendor plan), usage (per job:
Claude runs, ElevenLabs, renders), fee (Gumroad, from orders) or modeled (support time, never counted as cash).
Unknown costs stay UNKNOWN: they are listed, never turned into zero. Caps come only from config/growthos/budget.json,
which the owner sets; until then the guard reports UNCAPPED instead of inventing a number.

python3 scripts/growthos/costs.py report [YYYY-MM]"""
import datetime as dt, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import Store, ROOT  # noqa: E402

CFG = os.path.join(ROOT, "config", "growthos")
# Services in use. amount_minor None = UNKNOWN (not visible from here). Only Kit's plan was stated by Seb (Oct 2026).
SERVICES = [
    {"vendor": "Kit", "plan": "Creator ($39/mo, stated by Seb)", "amount_minor": 3900, "source": "owner statement"},
    {"vendor": "ManyChat", "plan": "paid (stated by Seb)", "amount_minor": None, "source": "owner statement, amount unknown"},
    {"vendor": "Metricool", "plan": "unknown", "amount_minor": None, "source": "not visible"},
    {"vendor": "ElevenLabs", "plan": "unknown", "amount_minor": None, "source": "not visible"},
    {"vendor": "Claude", "plan": "unknown (scheduled tasks need a paid plan)", "amount_minor": None, "source": "not visible"},
    {"vendor": "Porkbun (autopilotoi.app)", "plan": "domain, yearly", "amount_minor": None, "source": "not visible"},
    {"vendor": "GitHub", "plan": "public repo Actions + Pages", "amount_minor": 0, "source": "public repos are free"},
]


def budget(cfg_dir=None):
    return json.load(open(os.path.join(cfg_dir or CFG, "budget.json")))


def record_usage(store, vendor, amount_minor, job_id, kind="usage", currency="USD", estimated=False, note=None):
    return store.append("spend.recorded", {"vendor": vendor, "amount_minor": int(amount_minor), "currency": currency, "kind": kind,
                                           "job_id": job_id, "estimated": estimated, "note": note}, "growthos.costs", f"{vendor}:{job_id}", "costs")


def ai_spend_today(store, day=None):
    day = day or dt.datetime.now(dt.timezone.utc).date().isoformat()  # same clock as occurred_at_utc
    return sum(e["payload"]["amount_minor"] for e in store.of("spend.recorded")
               if e["payload"]["kind"] == "usage" and e["occurred_at_utc"][:10] == day and e["payload"]["vendor"] in ("Claude", "Anthropic API", "ElevenLabs"))


def guard(store, cfg_dir=None, day=None):
    """Returns the budget state the policy service uses. Caps are cents; None = not set by the owner."""
    b = budget(cfg_dir); spent = ai_spend_today(store, day)
    soft = b.get("ai_daily_soft_cap"); hard = b.get("ai_daily_hard_cap")
    return {"spent_today_minor": spent, "soft_cap_minor": soft, "hard_cap_minor": hard,
            "soft_cap_hit": soft is not None and spent >= soft, "hard_cap_hit": hard is not None and spent >= hard,
            "status": "UNCAPPED (owner has not set caps)" if soft is None and hard is None else "capped"}


def report(store, money_view, month=None):
    month = month or dt.date.today().strftime("%Y-%m")
    known = sum(s["amount_minor"] for s in SERVICES if s["amount_minor"])
    unknown = [s["vendor"] for s in SERVICES if s["amount_minor"] is None]
    usage = [e["payload"] for e in store.of("spend.recorded") if e["occurred_at_utc"][:7] == month]
    cash_usage = sum(u["amount_minor"] for u in usage if u["kind"] != "modeled")
    modeled = sum(u["amount_minor"] for u in usage if u["kind"] == "modeled")
    usd = (money_view.get("by_currency") or {}).get("USD", {})
    net = usd.get("net_receipts_minor", 0)
    contribution = net - known - cash_usage
    return {"month": month, "net_receipts_usd_minor": net, "known_costs_minor": known + cash_usage, "unknown_costs": unknown,
            "modeled_costs_minor": modeled, "contribution_minor": contribution,
            "contribution_status": "INCOMPLETE (unknown costs: " + ", ".join(unknown) + ")" if unknown else "complete",
            "services": SERVICES}


if __name__ == "__main__":
    import orders
    st = Store(); print(json.dumps({"guard": guard(st), "report": report(st, orders.money(st), sys.argv[2] if len(sys.argv) > 2 else None)}, indent=1))
