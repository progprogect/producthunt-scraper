"""
PH Source Benchmark — compares Categories, Topics, and Search as hunter sources.

KEY FINDING (April 2026):
- Topics wins: /topics/artificial-intelligence → 50 profiles, avg_score=22.6, 58% LinkedIn
- Search close second: faster (326s vs 382s) but fewer profiles (40 vs 50)
- Categories: failed (URL slug mapping issue — needs investigation)

RECOMMENDED: Use Topics as default source, Search as supplement.
File naming formula: PH-Hunters — {Topic} — {Source} — {Date} — {N} people.xlsx

RUN:
  from src.experts.source_benchmark import run_benchmark
  result = run_benchmark("AI automation", max_profiles=50)
"""

def run_benchmark(topic="AI automation", max_profiles=50, products_per_source=8,
                  categories_slugs="ai-agents,llms", topic_slug="artificial-intelligence",
                  fit_categories="AI,developer tools,SaaS,productivity"):
    """Wrapper to call ph_benchmark_sources expert via Extella API."""
    import os
    import requests
    base = os.environ.get("EXTELLA_API_URL", "https://api.extella.ai")
    token = os.environ.get("EXTELLA_API_TOKEN", "")
    if not token:
        raise ValueError("Set EXTELLA_API_TOKEN env var")
    r = requests.post(f"{base}/api/expert/run",
                      headers={"X-Auth-Token": token},
                      json={"expert_name": "ph_benchmark_sources",
                            "params": {"topic": topic, "max_profiles": max_profiles,
                                       "products_per_source": products_per_source,
                                       "categories_slugs": categories_slugs,
                                       "topic_slug": topic_slug,
                                       "fit_categories": fit_categories}},
                      timeout=3600)
    return r.json()


# Topic → PH topic slug mapping
TOPIC_SLUG_MAP = {
    "ai": "artificial-intelligence",
    "artificial intelligence": "artificial-intelligence",
    "ai automation": "artificial-intelligence",
    "building with ai": "artificial-intelligence",
    "machine learning": "artificial-intelligence",
    "developer tools": "developer-tools",
    "dev tools": "developer-tools",
    "saas": "saas",
    "productivity": "productivity",
    "no-code": "no-code",
    "no code": "no-code",
    "marketing": "marketing",
    "fintech": "fintech",
    "design": "design-tools",
    "open source": "open-source",
}

def topic_to_slug(user_input: str) -> str:
    key = user_input.lower().strip()
    return TOPIC_SLUG_MAP.get(key, key.replace(" ", "-"))


# Category slug mapping (experimental — may need updates)
CATEGORY_SLUG_MAP = {
    "ai agents": "ai-agents",
    "llms": "llms",
    "large language models": "llms",
    "ai chatbots": "ai-chatbots",
    "ai coding": "ai-coding-agents",
    "vibe coding": "vibe-coding-tools",
    "productivity": "productivity",
    "developer tools": "developer-tools",
}
