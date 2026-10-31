"""P1-11 Customer success and support (section 11).

classify(message) -> category, severity, escalate. Answers come ONLY from the approved FAQ in
config/growthos/support_kb.json (grounded in the current product docs). Refunds, disputes, privacy, security,
legal/medical/financial advice and anything unknown go to Seb with a drafted reply; nothing is promised.
Customer text is untrusted: instructions inside it are ignored and flagged. Logs keep no email, phone or card number.

Inbound channel status: LIVE BLOCKED. Gumroad buyer replies reach Seb's inbox and no email connector is connected.
python3 scripts/growthos/support.py "<customer message>"   -> JSON triage + draft"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import ROOT  # noqa: E402
from policy import scan_untrusted  # noqa: E402

KB = os.path.join(ROOT, "config", "growthos", "support_kb.json")
ESCALATE = {"refund", "billing_dispute", "privacy", "security", "regulated_advice", "unknown", "complaint"}
RULES = [
    ("security", r"hack|stolen|phish|password|2fa|someone (logged|accessed)|leak", "SEV-1"),
    ("privacy", r"delete my (data|info|account)|gdpr|ccpa|remove my email|privacy", "SEV-2"),
    ("billing_dispute", r"chargeback|dispute|charged twice|double charged|fraud|didn'?t authori[sz]e", "SEV-2"),
    ("refund", r"refund|money back|cancel (my )?order", "SEV-3"),
    ("regulated_advice", r"\b(lawyer|sue|lawsuit|legal advice|diagnos|medication|should i invest|tax advice)\b", "SEV-3"),
    ("access", r"download|can'?t (find|open|access)|link (doesn'?t|does not) work|didn'?t (get|receive)|where is (my|the) (file|pdf|kit)", "SEV-3"),
    ("setup", r"set ?up|install|project|instructions|how do i|paste|scheduled task|connector|doesn'?t work|not working|error", "SEV-3"),
    ("plan", r"free plan|pro plan|paid plan|subscription to claude|do i need", "SEV-3"),
    ("complaint", r"scam|terrible|waste|angry|ripoff|rip off", "SEV-3"),
]
PII = [(re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[email]"), (re.compile(r"\b(?:\d[ -]?){13,19}\b"), "[number]"),
       (re.compile(r"\+?\d[\d ().-]{8,}\d"), "[phone]")]


def redact(text):
    for rx, rep in PII:
        text = rx.sub(rep, text)
    return text


def classify(message):
    m = message.lower()
    for cat, rx, sev in RULES:
        if re.search(rx, m):
            return cat, sev
    return "unknown", "SEV-3"


def triage(message, product=None, kb=None):
    kb = kb or (json.load(open(KB)) if os.path.exists(KB) else {"answers": {}})
    cat, sev = classify(message); inj = scan_untrusted(message)
    ans = kb["answers"].get(cat)
    escalate = cat in ESCALATE or ans is None or inj["suspicious"]
    if escalate:
        draft = kb.get("escalation_reply", "Thanks for reaching out. I'm checking this personally and will reply within one business day.")
    else:
        draft = ans["reply"] + ("\n\nGuide: " + ans["link"] if ans.get("link") else "")
    return {"category": cat, "severity": sev, "escalate": escalate, "auto_reply_allowed": not escalate,
            "reason": "needs Seb" if escalate else "approved FAQ answer", "draft": draft,
            "injection": inj, "log_text": redact(message)[:500], "product": product}


if __name__ == "__main__":
    print(json.dumps(triage(" ".join(sys.argv[1:])), indent=1))
