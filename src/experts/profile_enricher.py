"""Enriches hunter profiles from PH pages using nodriver."""
import asyncio, json, random, re
from bs4 import BeautifulSoup

EU_CODES={"at","be","bg","hr","cy","cz","dk","ee","fi","fr","de","gr","hu","ie","it","lv","lt","lu","mt","nl","pl","pt","ro","sk","si","es","se"}
EU_NAMES={"austria","belgium","bulgaria","croatia","cyprus","czech republic","czechia","denmark","estonia","finland","france","germany","greece","hungary","ireland","italy","latvia","lithuania","luxembourg","malta","netherlands","poland","portugal","romania","slovakia","slovenia","spain","sweden"}

def _is_eu(c): return (c or "").lower() in EU_CODES|EU_NAMES

def _parse(html, username):
    r={"username":username,"ph_url":f"https://www.producthunt.com/@{username}","name":username,"bio":"","ph_followers":0,"products_hunted":0,"last_activity_date":None,"linkedin_url":None,"twitter_username":None,"country":None,"is_eu":False,"categories":[],"avg_upvotes_last_10":0,"hunted_posts":[]}
    soup=BeautifulSoup(html,"lxml")
    nd=soup.find("script",id="__NEXT_DATA__")
    if nd and nd.string:
        try:
            d=json.loads(nd.string)
            u=d.get("props",{}).get("pageProps",{}).get("user",{})
            if u:
                r["name"]=u.get("name",username); r["bio"]=u.get("headline","") or u.get("tagline","")
                r["ph_followers"]=int(u.get("followersCount",0) or 0)
                r["twitter_username"]=u.get("twitterUsername","") or ""
                co=u.get("country","") or u.get("location","")
                if co: r["country"]=co; r["is_eu"]=_is_eu(co)
                ws=u.get("websiteUrl","") or ""
                if "linkedin.com" in ws: r["linkedin_url"]=ws
                for f in ["madePosts","huntingPosts","hunteringPosts"]:
                    fo=u.get(f,{})
                    if isinstance(fo,dict) and fo.get("totalCount"): r["products_hunted"]=int(fo["totalCount"]); break
                posts=[]
                for f in ["madePosts","huntingPosts","hunteringPosts","posts"]:
                    fo=u.get(f,{})
                    if isinstance(fo,dict):
                        for e in fo.get("edges",[]):
                            n=e.get("node",{}) if isinstance(e,dict) else {}
                            if n:
                                ts=[te.get("node",{}).get("name","") for te in (n.get("topics",{}).get("edges",[]) if isinstance(n.get("topics"),dict) else []) if isinstance(te,dict)]
                                posts.append({"votes":int(n.get("votesCount",0) or 0),"date":n.get("createdAt",""),"name":n.get("name",""),"topics":ts})
                if posts:
                    r["hunted_posts"]=posts[:10]
                    dates=[p["date"] for p in posts if p.get("date")]
                    if dates: r["last_activity_date"]=max(dates)
                    ups=[p["votes"] for p in posts[:10] if p.get("votes",0)>0]
                    if ups: r["avg_upvotes_last_10"]=round(sum(ups)/len(ups),1)
                    all_t=[]; [all_t.extend(p.get("topics",[])) for p in posts]
                    r["categories"]=list(dict.fromkeys(t for t in all_t if t))[:10]
        except: pass
    if not r["linkedin_url"]:
        for a in soup.find_all("a",href=True):
            if "linkedin.com/in/" in a["href"]: r["linkedin_url"]=a["href"]; break
    if not r["twitter_username"]:
        for a in soup.find_all("a",href=True):
            m=re.search(r"(?:twitter\.com|x\.com)/([a-zA-Z0-9_]+)",a["href"])
            if m and m.group(1).lower() not in {"home","intent","share","search","i","web"}: r["twitter_username"]=m.group(1); break
    return r

async def enrich_profiles_batch(usernames, headless=True, delay=2.5):
    import nodriver as uc
    results={}
    browser=await uc.start(headless=headless)
    try:
        for un in usernames:
            try:
                page=await browser.get(f"https://www.producthunt.com/@{un}")
                await asyncio.sleep(random.uniform(2.5,delay+2))
                html=await page.evaluate("document.documentElement.outerHTML")
                results[un]=_parse(html,un)
                await asyncio.sleep(random.uniform(1,2))
            except Exception as e:
                results[un]={"username":un,"ph_url":f"https://www.producthunt.com/@{un}","ph_followers":0,"products_hunted":0,"linkedin_url":None,"twitter_username":None,"categories":[],"avg_upvotes_last_10":0,"error":str(e)}
    finally: browser.stop()
    return results
