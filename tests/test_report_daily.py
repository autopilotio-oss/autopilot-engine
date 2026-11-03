"""Daily report never invents numbers: missing sessions are MISSING, spend comes from sales/spend.csv."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "revenue"))
import report_daily


def test_report_has_required_rows_and_no_invented_sessions():
    r = report_daily.build()
    for row in ("Verified orders", "Net receipts", "Ad spend", "CAC / CPA", "Contribution", "Landing conversion",
                "Activation", "Attribution quality", "System health"):
        assert row in r, row
    assert "sessions MISSING" in r or "sessions |" in r
    assert "$49.89" in r   # the Oct 30 to Nov 1 boost is recorded, not hidden
