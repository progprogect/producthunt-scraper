#!/usr/bin/env python3
"""ProductHunt Hunter Pipeline — Interactive Entry Point"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def prompt(msg, default):
    val = input(f"{msg} (default: {default}): ").strip()
    return val if val else default

def main():
    print("=" * 60)
    print("🚀 ProductHunt Hunter Pipeline")
    print("=" * 60)

    topics       = prompt("Topics (comma-separated)", "Building with AI,Automation with AI")
    min_followers= int(prompt("Min PH followers", "1000"))
    min_hunts    = int(prompt("Min products hunted", "10"))
    activity_days= int(prompt("Activity window (days)", "90"))
    categories   = prompt("Fit categories", "AI,developer tools,SaaS,productivity")
    p_thr        = int(prompt("Priority score threshold", "80"))
    s_thr        = int(prompt("Secondary score threshold", "60"))
    mode         = prompt("Search mode (topics/keywords/both)", "topics")

    print("\n" + "=" * 60)

    from src.pipeline.pipeline import run_pipeline
    result = run_pipeline(
        topics=[t.strip() for t in topics.split(",") if t.strip()],
        min_followers=min_followers, min_hunts=min_hunts,
        activity_days=activity_days,
        categories=[c.strip() for c in categories.split(",") if c.strip()],
        priority_threshold=p_thr, secondary_threshold=s_thr,
        search_mode=mode
    )
    print("\n✅ Done:", json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    main()
