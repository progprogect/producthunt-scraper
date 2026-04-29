# Excel Export Design — All-Inclusive with Visual Marking

## Philosophy
Every discovered hunter stays in the export. Scoring signals who's worth contacting first.

## Visual marking
| Color | Segment | Score threshold |
|-------|---------|-----------------|
| 🟩 Green (#C6EFCE) | ⭐ Priority | ≥ 50 |
| 🟨 Yellow (#FFEB9C) | ✅ Secondary | ≥ 25 |
| ⬜ Light gray (#F5F5F5) | — Below | < 25 |

## Columns
| # | Column | Description |
|---|--------|-------------|
| 1 | Status | ⭐ Priority / ✅ Secondary / — |
| 2 | Name | Display name |
| 3 | PH Profile URL | Clickable link |
| 4 | LinkedIn URL | Clickable link (empty if none) |
| 5 | LinkedIn? | ✅ or ❌ quick indicator |
| 6 | Score | 0-100 |
| 7 | Segment | Text segment label |
| 8 | PH Followers | Integer |
| 9 | X Followers | Integer (0 if not collected) |
| 10 | Twitter Handle | @handle |
| 11 | Categories | Comma-separated, max 5 |
| 12 | Geo | Country + 🇪🇺 for EU |
| 13 | Last Activity | ISO date or — |
| 14 | Products Hunted | Count |
| 15 | Avg Upvotes | 0 (not currently collected) |

## Scoring limitations (April 2026)
- **avg_upvotes_last_10** = 0 for all hunters (collecting it requires visiting each product page)
- This wastes 20% of the scoring weight → max achievable score is ~68-79
- Recommended thresholds: `priority=50`, `secondary=25`
- To improve: collect avg_upvotes by visiting hunter's `/submitted` page

## Sorting
Priority first → Secondary → Below threshold, within each group sorted by Score DESC.
