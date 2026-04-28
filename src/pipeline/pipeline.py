"""Main pipeline — orchestrates all experts locally."""
import asyncio, json, os, random, re, sys, time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

from src.experts.config_collector import collect_config
from src.experts.hunter_filter import filter_hunters
from src.experts.hunter_scorer import score_hunters
from src.experts.excel_exporter import export_to_excel

def get_api_key(env_var="GETXAPI_KEY"):
    return os.environ.get(env_var, "")

def run_pipeline(topics, min_followers=1000, min_hunts=10, activity_days=90,
                 categories=None, priority_threshold=80, secondary_threshold=60,
                 search_mode="topics", max_scrolls=10, headless=True, output_path=""):
    print("="*60); print("🚀 PH Hunter Pipeline"); print("="*60)
    config = collect_config(topics, min_followers, min_hunts, activity_days,
                            categories, priority_threshold, secondary_threshold, search_mode)

    # Scrape
    from src.experts.topic_scraper import scrape_topics
    raw_hunters = asyncio.run(scrape_topics(topics, search_mode, max_scrolls, headless))
    print(f"[Scrape] Found {len(raw_hunters)} raw hunters")

    # Enrich in batches
    from src.experts.profile_enricher import enrich_profiles_batch
    usernames = list(dict.fromkeys(h.get("username","") for h in raw_hunters if h.get("username")))
    all_enriched = []
    for i in range(0, len(usernames), 50):
        batch = usernames[i:i+50]
        enriched = asyncio.run(enrich_profiles_batch(batch, headless=headless))
        all_enriched.extend(enriched.values())
        print(f"  Batch {i//50+1}: {len(batch)} enriched")
        if i + 50 < len(usernames): time.sleep(3)
    print(f"[Enrich] {len(all_enriched)} profiles enriched")

    # X followers
    from src.experts.x_followers import fetch_x_followers_batch
    api_key = get_api_key(config["getxapi_key_env"])
    twitter_handles = [h.get("twitter_username","") for h in all_enriched if h.get("twitter_username")]
    x_data = fetch_x_followers_batch(list(set(twitter_handles)), api_key) if twitter_handles and api_key else {}
    print(f"[X] {len(x_data)} follower counts fetched")

    # Filter
    filtered, killed = filter_hunters(all_enriched, min_followers, min_hunts, activity_days)
    print(f"[Filter] {len(filtered)}/{len(all_enriched)} passed | {killed}")

    # Score
    scored = score_hunters(filtered, config["categories"], priority_threshold, secondary_threshold, x_data)
    p = sum(1 for h in scored if h.get("segment")=="Priority")
    s = sum(1 for h in scored if h.get("segment")=="Secondary")
    print(f"[Score] Priority: {p}, Secondary: {s}")

    # Export
    out = export_to_excel(scored, output_path)
    print(f"[Export] Saved: {out}")

    return {"raw": len(raw_hunters), "enriched": len(all_enriched), "filtered": len(filtered),
            "priority": p, "secondary": s, "excel": out}
