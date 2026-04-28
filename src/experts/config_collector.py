"""Config collector — validates and returns pipeline config dict."""

def collect_config(topics, min_followers=1000, min_hunts=10, activity_days=90,
                   categories=None, priority_threshold=80, secondary_threshold=60,
                   search_mode="topics", getxapi_key_env="GETXAPI_KEY"):
    cats = categories or ["AI", "developer tools", "SaaS", "productivity"]
    assert priority_threshold > secondary_threshold, "priority_threshold must be > secondary_threshold"
    assert search_mode in ("topics", "keywords", "both"), "search_mode must be topics/keywords/both"
    return dict(topics=list(topics), min_followers=min_followers, min_hunts=min_hunts,
                activity_days=activity_days, categories=cats,
                priority_threshold=priority_threshold, secondary_threshold=secondary_threshold,
                search_mode=search_mode, batch_size=50, getxapi_key_env=getxapi_key_env)
