# PH Source Benchmark — Results (April 2026)

## Topic: "AI automation"

### Method
Two-step scraping:
1. Visit source page → extract `/products/slug` links (55s wait for React render)
2. Visit product pages in parallel (3 concurrent, 22s wait) → collect `/@username` links
3. Enrich profiles (4 concurrent browsers, shared cache across sources)
4. Score: PH followers 28% | Category fit 29% | Products hunted 17% | X followers 11% | Activity 15%

### Results

| Medal | Source | Profiles | Avg Score | Priority | % LinkedIn | Total Time |
|-------|--------|----------|-----------|----------|-----------|------------|
| 🥇 | **Topics** `/topics/artificial-intelligence` | 50 | **22.6** | 5 | **58%** | 382s |
| 🥈 | Search `/search?q=AI+automation` | 40 | 21.0 | 3 | 55% | 326s |
| 🥉 | Categories `/categories/ai-agents,llms` | **0** | 0 | 0 | 0% | 127s |

### Analysis

#### 🥇 Topics — WINNER
- **Highest profile count** (50 vs 40 Search) and **highest LinkedIn %** (58%)
- Breadth: `/topics/artificial-intelligence` covers all AI products
- Works reliably with 55s wait
- **Recommended for: broad AI/SaaS/productivity topics**

#### 🥈 Search — GOOD ALTERNATIVE
- **Faster** (326s vs 382s = 15% faster)
- **More specific** — matches exact keywords in product descriptions
- Fewer profiles found (40 vs 50) because fewer products match exact query
- **Recommended for: very specific niches** ("no-code automations", "AI copywriting tools")

#### 🥉 Categories — FAILED
- Category slugs `/categories/ai-agents` and `/categories/llms` didn't return product links
- Possible issue: category pages use different URL structure or require login
- Needs further investigation for PH category URL mapping

### Filename Formula
```
PH-Hunters — {Topic} — {Source} — {YYYY-MM-DD} — {N} people.xlsx
```
Examples:
- `PH-Hunters — AI automation — Topics — 2026-04-29 — 50 people.xlsx`
- `PH-Hunters — Developer Tools — Search — 2026-04-29 — 40 people.xlsx`
- `PH-Hunters — SaaS — SOURCE BENCHMARK — 2026-04-29.xlsx`

### Recommendation
**Default source: Topics.** For best results, map the user's topic input to the closest
PH topic slug. Use Search as fallback or supplement for keyword-specific queries.

### Known Issues
1. Categories source: PH category URL slugs differ from what's shown in UI
2. Scores are low (avg 20-23) because activity_date is often null → 50 points wasted
3. avg_upvotes intentionally excluded (would require additional page visits)
