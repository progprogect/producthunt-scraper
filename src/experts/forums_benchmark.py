"""
ph_forums_add_and_compare — Add Forums to benchmark without re-running Topics/Search.

KEY DESIGN: Smart cache reuse
- Forums: new scrape only (~/Downloads/ph_benchmark_enricher_cache.json)
- Topics + Search: re-read username lists from quick source page visit (55s),
  all profiles loaded from enricher cache → 0 additional browser time
- X followers: fetch via getxapi for ALL profiles after everything is loaded
- Total time: ~9 min vs 60+ min for full re-run

Benchmark Results 'AI automation' (April 2026):
  🥇 Topics  /topics/artificial-intelligence:  avg=22.5 | 50 profiles | 58% LinkedIn | 5 Priority
  🥈 Forums  /forums/search?query=AI+tools:     avg=21.6 | 19 profiles | 26% LinkedIn | 2 Priority
  🥉 Search  /search?q=AI+automation:           avg=21.2 | 40 profiles | 55% LinkedIn | 3 Priority

Notes on Forums source:
- Only 19 profiles found (vs 50 target) — forums have fewer active PH users visible
- Lower LinkedIn % (26%) — forum participants are less likely to share LinkedIn
- Faster to scrape (direct author links, no product page step needed)
- Good for finding ENGAGED community members, not necessarily big hunters

FIXED in this version vs previous benchmark:
- Role: was 🔍 emoji → now 'Hunter (curator)' / 'Maker & Hunter' / 'Maker (creator only)'
- Score columns: S:PH → 'Score: PH Followers (28%) / 100' etc.
- X Followers: shows count if fetched, or '0 (not fetched)' with note when no key

Source tracking:
- ph_benchmark_source_map.json saved alongside enricher cache
- On subsequent runs, Topics+Search loaded from this map (zero browser time)
"""

FORUM_URL_TEMPLATE = "https://www.producthunt.com/forums/search?query={query}&order=popular&window=all"

TOPIC_SLUG_MAP = {
    "ai": "artificial-intelligence",
    "ai automation": "artificial-intelligence",
    "building with ai": "artificial-intelligence",
    "machine learning": "artificial-intelligence",
    "developer tools": "developer-tools",
    "saas": "saas",
    "productivity": "productivity",
    "no-code": "no-code",
    "marketing": "marketing",
    "fintech": "fintech",
}

def topic_to_slug(user_input: str) -> str:
    return TOPIC_SLUG_MAP.get(user_input.lower().strip(),
                               user_input.lower().replace(" ", "-"))
