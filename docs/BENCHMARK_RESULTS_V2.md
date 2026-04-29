# PH Source Benchmark v2 — Forums Added (April 2026)

## Topic: "AI automation" — all 3 sources compared

### Method
- **Topics** and **Search**: reloaded from enricher cache (Topics+Search usernames from source_map)
- **Forums**: new scrape of `/forums/search?query=AI+tools&order=popular&window=all`
- **X followers**: fetched via getxapi for ALL profiles after enrichment
- **Total time: 9.1 min** (vs 60+ min for full re-run — 6x faster)

### Results

| Medal | Source | Profiles | Avg Score | Priority | % LinkedIn | % Twitter | Total Time |
|-------|--------|----------|-----------|----------|-----------|-----------|------------|
| 🥇 | **Topics** `/topics/artificial-intelligence` | **50** | **22.5** | **5** | **58%** | 44% | ~0s (cache) |
| 🥈 | Forums `/forums/search?query=AI+tools` | 19 | 21.6 | 2 | 26% | 26% | ~8 min (new) |
| 🥉 | Search `/search?q=AI+automation` | 40 | 21.2 | 3 | 55% | 40% | ~0s (cache) |

### Forums Source Analysis

**What it is:** `/forums/search?query=X&order=popular&window=all`
Extracts direct post authors from PH discussion threads — no product page step needed.

**Strengths:**
- ✅ Direct author extraction (no product page step = faster)
- ✅ Finds **engaged community members** — people who actively discuss topics
- ✅ Good complement to Topics/Search for finding vocal community voices

**Weaknesses:**
- ❌ Fewer profiles (19 vs 50 target) — forums less populated than products
- ❌ Lower LinkedIn % (26% vs 55-58%) — forum participants less likely to share LinkedIn
- ❌ Lower avg followers — community commenters vs product hunters

**Recommendation:** Use Forums as a **supplementary source** alongside Topics.
Good for finding engaged community members who may not be top product hunters.

### X Followers Note
X follower count was 0 for all profiles in this run because:
1. Profiles in enricher cache (from previous benchmark) didn't have twitter_username
   extracted correctly (short wait time in previous run)
2. New forums profiles had twitter_username extracted but getxapi may have returned 0

**Fix for next run:** Use `force_reenrich=True` or re-scrape with longer wait times.

### Column Names Fixed (v2)
| Old | New |
|-----|-----|
| 🔍 (emoji only) | Hunter (curator) / Maker & Hunter / Maker (creator only) |
| S:PH | Score: PH Followers (28%) / 100 |
| S:Cat | Score: Topic Fit (29%) / 100 |
| S:Hunts | Score: Hunts Count (17%) / 100 |
| S:X | Score: X Followers (11%) / 100 ⚠️ no X data |
| S:Act | Score: Activity Recency (15%) / 100 |

### File Naming
`PH-Hunters — AI automation — SOURCE BENCHMARK — 2026-04-29.xlsx`
Formula: `PH-Hunters — {Topic} — {Source} — {Date} — {N} people.xlsx`
