"""Unit tests for the PH Hunter Pipeline."""
import json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_config_collector():
    from src.experts.config_collector import collect_config
    cfg = collect_config(["AI","SaaS"], min_followers=500, search_mode="keywords")
    assert cfg["min_followers"] == 500
    assert "AI" in cfg["topics"]
    assert cfg["search_mode"] == "keywords"
    print("✅ test_config_collector passed")

def test_filter_hunters_gates():
    from src.experts.hunter_filter import filter_hunters
    hunters = [
        {"username":"a","ph_followers":5000,"products_hunted":20,"last_activity_date":"2025-12-01"},
        {"username":"b","ph_followers":100,"products_hunted":20,"last_activity_date":"2025-12-01"},   # low followers
        {"username":"c","ph_followers":5000,"products_hunted":2,"last_activity_date":"2025-12-01"},   # few hunts
        {"username":"d","ph_followers":5000,"products_hunted":20,"last_activity_date":"2020-01-01"},  # inactive
    ]
    passed, killed = filter_hunters(hunters, min_followers=1000, min_hunts=10, activity_days=90)
    assert len(passed) == 1 and passed[0]["username"] == "a"
    assert killed["followers"] == 1
    assert killed["hunts"] == 1
    assert killed["activity"] == 1
    print("✅ test_filter_hunters_gates passed")

def test_scorer():
    from src.experts.hunter_scorer import score_hunters
    hunters = [
        {"username":"top","ph_followers":25000,"products_hunted":50,"categories":["AI","SaaS"],
         "avg_upvotes_last_10":1000,"twitter_username":"topuser","x_followers":0},
        {"username":"low","ph_followers":1100,"products_hunted":11,"categories":["cooking"],
         "avg_upvotes_last_10":10,"twitter_username":"","x_followers":0},
    ]
    scored = score_hunters(hunters, ["AI","SaaS"], 80, 60)
    scores = {h["username"]: h["score"] for h in scored}
    assert scores["top"] > scores["low"], f"top={scores['top']} should > low={scores['low']}"
    print(f"✅ test_scorer passed | top={scores['top']} low={scores['low']}")

def test_excel_exporter():
    import openpyxl
    from src.experts.excel_exporter import export_to_excel
    hunters = [
        {"username":"alice","name":"Alice","ph_url":"https://producthunt.com/@alice",
         "linkedin_url":"https://linkedin.com/in/alice","score":85,"segment":"Priority",
         "ph_followers":10000,"x_followers":5000,"categories":["AI"],"is_eu":True,
         "country":"Germany","last_activity_date":"2025-11-01","products_hunted":30,
         "avg_upvotes_last_10":500,"twitter_username":"alice"},
        {"username":"bob","name":"Bob","ph_url":"https://producthunt.com/@bob",
         "linkedin_url":None,"score":70,"segment":"Secondary",  # no linkedin — should be excluded
         "ph_followers":2000,"x_followers":0,"categories":[],"is_eu":False,
         "country":"US","last_activity_date":None,"products_hunted":15,
         "avg_upvotes_last_10":100,"twitter_username":""},
    ]
    import tempfile, os
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
        path = f.name
    try:
        out = export_to_excel(hunters, output_path=path)
        wb = openpyxl.load_workbook(out)
        ws = wb.active
        assert ws.max_row == 2, f"Expected 2 rows (header+alice), got {ws.max_row}"
        print(f"✅ test_excel_exporter passed | rows={ws.max_row}")
    finally:
        os.unlink(path)

if __name__ == "__main__":
    print("\n🧪 Running PH Hunter Pipeline Tests\n" + "="*50)
    try:
        test_config_collector()
        test_filter_hunters_gates()
        test_scorer()
        test_excel_exporter()
        print("\n✅ ALL TESTS PASSED")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
