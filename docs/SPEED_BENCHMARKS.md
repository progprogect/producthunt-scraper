# ProductHunt Hunter Pipeline — Speed Benchmarks

## Optimization: asyncio Parallel Browser Architecture (April 2026)

### Strategy
Replace sequential browser-per-operation with N concurrent browsers using `asyncio.gather()`.

### Core insight
- **One browser per URL** (Cloudflare-safe: each browser is independent)
- **All browsers run simultaneously** via asyncio coroutines
- **Smart polling**: exit as soon as data found (avg 20s vs flat 35s wait)
- **Stagger**: 1-1.5s between browser starts (avoids resource burst)

### Benchmark Results

#### Profile Enrichment
| Config | Wall Time | Sequential Est. | Speedup |
|--------|-----------|-----------------|---------|
| 5 profiles, 5 concurrent | 10.1s | 275s | **27x** |
| 8 profiles, 8 concurrent | 30.1s | 440s | **14.6x** |
| Recommended (6 concurrent) | — | — | **~15-20x** |

#### Product Page Scraping (Phase 2 only)
| Config | Wall Time | Sequential Est. | Speedup |
|--------|-----------|-----------------|---------|
| 12 product pages, 6 concurrent | 29s | 624s | **21.5x** |

#### Full Pipeline (theoretical, 3 days, 8 products/day, 169 profiles)
| Phase | Old Time | New Time | Speedup |
|-------|----------|----------|---------|
| Scraping (Phase 1 leaderboard) | ~5 min | ~5 min | 1x (sequential, CF-safe) |
| Scraping (Phase 2 products) | ~21 min | ~2 min | **10x** |
| Enrichment (169 profiles) | ~155 min | ~15 min | **10x** |
| Total | ~180 min | ~20 min | **~9x** |

### Implementation
- **Expert**: `ph_enrich_parallel_fast` — Extella expert for parallel enrichment
- **Expert**: `ph_scrape_parallel_fast` — Extella expert for parallel scraping  
- **Expert**: `ph_fast_pipeline_v2` — Fast orchestrator
- **Source**: `src/experts/parallel_enricher.py`, `src/experts/parallel_scraper.py`

### Limitations
- max_concurrent=8 causes occasional "Failed to connect to browser" errors (~2/8)
- Recommended: max_concurrent=6 for stability (still 15x+ speedup)
- LinkedIn/Twitter require min 20s wait (8 polls × 2.5s) even if followers found early

### Future Optimization (GraphQL API)
If PH session cookies + `/graphql` endpoint works:
- Estimated speedup: 100x+ (1s API call vs 30s browser)
- Status: In testing (currently returns empty response — CSRF or header issue)
