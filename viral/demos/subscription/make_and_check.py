"""Labeled synthetic demo for the Subscription agent (no real person's data).
Builds a 3 month sample statement, runs the same recurring charge rules the agent prompt asks Claude to apply
(same merchant, amount within 5%, roughly monthly or yearly), and checks the numbers shown on screen.
python3 viral/demos/subscription/make_and_check.py  -> writes sample_statement.csv + expected.json, exits 1 on mismatch"""
import csv, json, os, random, statistics, datetime as dt
D = os.path.dirname(os.path.abspath(__file__)); random.seed(7)
REC = [("STREAMFLIX", 15.49, 5), ("MUSICBOX FAMILY", 16.99, 9), ("CLOUDDRIVE 2TB", 9.99, 12), ("FITCLUB GYM", 29.99, 1),
       ("PHOTOEDIT PRO", 8.99, 20), ("NEWSDAILY DIGITAL", 4.99, 3), ("MEALKIT TRIAL>PLAN", 59.94, 15)]
ONE_OFF = [("GROCERY MART", 40, 140), ("GAS STATION", 30, 65), ("COFFEE CORNER", 4, 9), ("PHARMACY", 8, 35), ("ONLINE STORE", 15, 120), ("RESTAURANT", 18, 75)]
rows = []
for m in (8, 9, 10):
    for name, amt, day in REC:
        if name.startswith("MEALKIT") and m == 8:
            rows.append((dt.date(2026, m, day), "MEALKIT FREE TRIAL", 0.00)); continue
        rows.append((dt.date(2026, m, day), name, amt))
    for _ in range(12):
        n, lo, hi = random.choice(ONE_OFF); rows.append((dt.date(2026, m, random.randint(1, 28)), n, round(random.uniform(lo, hi), 2)))
rows.sort()
with open(os.path.join(D, "sample_statement.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["date", "description", "amount", "note"])
    for d, n, a in rows: w.writerow([d.isoformat(), n, f"{a:.2f}", "SAMPLE DATA"])

# the agent's rules, applied deterministically
by = {}
for d, n, a in rows:
    if a > 0: by.setdefault(n, []).append((d, a))
found = []
for n, xs in by.items():
    if len(xs) < 2: continue
    amts = [a for _, a in xs]; gaps = [(xs[i + 1][0] - xs[i][0]).days for i in range(len(xs) - 1)]
    if max(amts) / min(amts) <= 1.05 and all(25 <= g <= 35 for g in gaps):
        found.append({"merchant": n, "monthly": round(statistics.median(amts), 2), "yearly": round(statistics.median(amts) * 12, 2)})
found.sort(key=lambda x: -x["yearly"])
total_m = round(sum(x["monthly"] for x in found), 2); total_y = round(sum(x["yearly"] for x in found), 2)
exp = {"recurring": found, "monthly_total": total_m, "yearly_total": total_y,
       "note": "SAMPLE DATA. Recurring = same merchant, amount within 5%, every 25 to 35 days. The user decides what to cancel."}
json.dump(exp, open(os.path.join(D, "expected.json"), "w"), indent=1)
want = {"STREAMFLIX", "MUSICBOX FAMILY", "CLOUDDRIVE 2TB", "FITCLUB GYM", "PHOTOEDIT PRO", "NEWSDAILY DIGITAL", "MEALKIT TRIAL>PLAN"}
got = {x["merchant"] for x in found}
assert got == want, (got ^ want)
assert abs(8.99 * 12 - 107.88) < 1e-9 and total_y == round(total_m * 12, 2)
print(f"OK: {len(found)} recurring charges, ${total_m:.2f}/month, ${total_y:.2f}/year (sample data)")
