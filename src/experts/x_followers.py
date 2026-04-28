"""Fetches X/Twitter follower counts via GetXAPI."""
import requests, time

def fetch_x_followers_batch(usernames, api_key, delay=0.5):
    results={}
    for i,un in enumerate(usernames):
        try:
            r=requests.get("https://api.getxapi.com/twitter/user/info",
                           params={"userName":un},headers={"Authorization":f"Bearer {api_key}"},timeout=15)
            if r.status_code==200:
                d=r.json(); u=d.get("user") or d.get("data") or d
                results[un]=int(u.get("followers") or u.get("followersCount") or u.get("followers_count") or 0)
            elif r.status_code==429:
                time.sleep(60)
                r2=requests.get("https://api.getxapi.com/twitter/user/info",
                                params={"userName":un},headers={"Authorization":f"Bearer {api_key}"},timeout=15)
                if r2.status_code==200:
                    d=r2.json(); u=d.get("user") or d.get("data") or d
                    results[un]=int(u.get("followers") or u.get("followersCount") or 0)
                else: results[un]=0
            else: results[un]=0
        except: results[un]=0
        if i<len(usernames)-1: time.sleep(delay)
    return results
