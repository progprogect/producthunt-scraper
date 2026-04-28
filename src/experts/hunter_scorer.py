"""Scorer — 0-100 weighted signal scoring."""
import math

def _log(v, lo, hi):
    if v <= 0 or lo <= 0 or hi <= lo: return 0.0
    return max(0.0, min(100.0, (math.log10(max(v,1)) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * 100))

def _lin(v, lo, hi):
    if hi <= lo: return 0.0
    return max(0.0, min(100.0, (v - lo) / (hi - lo) * 100))

def score_hunters(hunters, categories, priority_threshold=80, secondary_threshold=60, x_followers=None):
    xf = x_followers or {}
    target_cats = [c.lower() for c in categories]
    priority, secondary, below = [], [], []
    for h in hunters:
        handle = (h.get("twitter_username") or "").strip()
        xc = int(h.get("x_followers", 0) or xf.get(handle, 0) or 0)
        hcats = [c.lower() for c in (h.get("categories") or [])]
        cat_match = sum(1 for tc in target_cats if any(tc in hc or hc in tc for hc in hcats))
        cat_s = min(100.0, cat_match / max(len(target_cats), 1) * 100)
        raw = (_log(h.get("ph_followers",0), 1000, 50000) * 25 +
               _lin(h.get("products_hunted",0), 10, 100) * 15 +
               cat_s * 25 +
               _log(h.get("avg_upvotes_last_10",0), 50, 5000) * 20 +
               _log(xc, 100, 100000) * 10)
        score = round(raw / 95)
        h.update({"score": score, "x_followers": xc})
        if score >= priority_threshold: h["segment"] = "Priority"; priority.append(h)
        elif score >= secondary_threshold: h["segment"] = "Secondary"; secondary.append(h)
        else: h["segment"] = "Below Threshold"; below.append(h)
    for lst in [priority, secondary]: lst.sort(key=lambda x: x["score"], reverse=True)
    return priority + secondary + below
