"""Gate filter — removes hunters that fail hard gates."""
from datetime import datetime, timezone, timedelta

def filter_hunters(hunters, min_followers=1000, min_hunts=10, activity_days=90):
    cutoff = datetime.now(timezone.utc) - timedelta(days=activity_days)
    passed, killed = [], {"followers": 0, "hunts": 0, "activity": 0}
    for h in hunters:
        if int(h.get("ph_followers", 0)) < min_followers:
            killed["followers"] += 1; continue
        if int(h.get("products_hunted", 0)) < min_hunts:
            killed["hunts"] += 1; continue
        la = h.get("last_activity_date")
        if la:
            try:
                s = str(la).split(".")[0].replace("Z", "+00:00")
                dt = datetime.fromisoformat(s)
                if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
                if dt < cutoff:
                    killed["activity"] += 1; continue
            except Exception:
                pass
        passed.append(h)
    print(f"  Filter: {len(passed)}/{len(hunters)} passed | killed={killed}")
    return passed, killed
