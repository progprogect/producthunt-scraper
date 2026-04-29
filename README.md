# ProductHunt Hunter Outreach Pipeline

Automated pipeline: discover, enrich and score top ProductHunt hunters for outreach.

See **[PRESET.md](PRESET.md)** for full documentation.

## Quick Start

```bash
pip install -r requirements.txt
# Important: headless=False required (Cloudflare bypass)
```

## Scoring (0-100)

| Signal | Weight | Scale |
|--------|--------|-------|
| Topic Fit | 29% | Category overlap 0-100% |
| PH Followers | 28% | Log 1K-50K |
| Products Hunted | 17% | Linear 10-100 |
| Activity Recency | 15% | Active <=90d=100 |
| X/Twitter Followers | 11% | Log 100-100K |

## Source Benchmark

| Source | Profiles | Avg Score | LinkedIn % |
|--------|---------|-----------|------------|
| **Topics** (recommended) | 50 | **22.5** | **58%** |
| Search | 40 | 21.2 | 55% |
| Forums | 19 | 21.6 | 26% |

## Checkpoints

```
~/Downloads/ph_scraper_checkpoint.json     -- scraped usernames
~/Downloads/ph_enricher_checkpoint.json   -- enriched profiles
~/Downloads/ph_benchmark_source_map.json  -- source mapping
```

## Docs

- [PRESET.md](PRESET.md) -- Full preset doc
- [docs/BENCHMARK_RESULTS_V2.md](docs/BENCHMARK_RESULTS_V2.md) -- Benchmark
- [docs/SPEED_BENCHMARKS.md](docs/SPEED_BENCHMARKS.md) -- Performance
