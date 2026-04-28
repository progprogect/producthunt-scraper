# ProductHunt Hunter Pipeline

Automated pipeline for discovering, scoring, and exporting top ProductHunt hunters.

## Features
- Scrapes PH by topics or keywords (Cloudflare-bypass via nodriver)
- Enriches hunter profiles: followers, LinkedIn URL, Twitter, country, avg upvotes
- Hard gates: min followers, min hunts, activity window
- Scores 0-100 on 5 signals (PH followers 25%, category fit 25%, avg upvotes 20%, products 15%, X followers 10%)
- Exports Priority/Secondary hunters with LinkedIn to Excel

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env  # Add your GETXAPI_KEY
python main.py
```

## Environment
```
GETXAPI_KEY=get-x-api-...
```

## Scoring Rubric
| Signal | Weight |
|--------|--------|
| PH followers | 25% (log-scale 1K–50K) |
| Category fit | 25% (overlap with target categories) |
| Avg upvotes (last 10) | 20% (log-scale 50–5000) |
| Products hunted | 15% (linear 10–100) |
| X followers | 10% (log-scale 100–100K) |
| Hit rate (top 5%) | 0% (skipped — rarely scrapeable) |
