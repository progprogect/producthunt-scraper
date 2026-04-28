"""Scrapes PH topics/keywords for hunter usernames using nodriver."""
import asyncio, json, random, re, urllib.parse
from bs4 import BeautifulSoup
from pathlib import Path

PH_SLUGS = {
    "building with ai":"artificial-intelligence","automation with ai":"artificial-intelligence",
    "ai":"artificial-intelligence","developer tools":"developer-tools","saas":"saas",
    "productivity":"productivity","no-code":"no-code","marketing":"marketing",
}

def _slug(t): return PH_SLUGS.get(t.lower().strip(), t.lower().replace(" ","-"))

def _extract_nd(data, topic, hunters):
    def walk(n, d=0):
        if d>25 or not n: return
        if isinstance(n, dict):
            if n.get("__typename")=="Post" or (n.get("votesCount") is not None and n.get("name")):
                pi={"name":n.get("name",""),"votes":n.get("votesCount",0),"date":n.get("createdAt",""),"topics":[]}
                for e in (n.get("topics",{}).get("edges",[]) if isinstance(n.get("topics"),dict) else []):
                    if isinstance(e,dict) and e.get("node",{}).get("name"): pi["topics"].append(e["node"]["name"])
                for uk in ["user","hunter"]:
                    u=n.get(uk,{})
                    if isinstance(u,dict) and u.get("username"):
                        un=u["username"]
                        if un not in hunters: hunters[un]={"username":un,"ph_url":f"https://www.producthunt.com/@{un}","name":u.get("name",un),"source_topics":[],"hunted_posts":[]}
                        if topic not in hunters[un]["source_topics"]: hunters[un]["source_topics"].append(topic)
                        hunters[un]["hunted_posts"].append(pi)
            for v in n.values():
                if isinstance(v,(dict,list)): walk(v,d+1)
        elif isinstance(n,list):
            for i in n: walk(i,d+1)
    walk(data)

async def scrape_topics(topics, mode="topics", max_scrolls=10, headless=True):
    import nodriver as uc
    hunters={}
    browser=await uc.start(headless=headless)
    try:
        for t in topics:
            urls=[]
            if mode in ("topics","both"): urls.append(f"https://www.producthunt.com/topics/{_slug(t)}")
            if mode in ("keywords","both"): urls.append(f"https://www.producthunt.com/search?q={urllib.parse.quote(t)}&type=posts")
            for url in urls:
                page=await browser.get(url); await asyncio.sleep(random.uniform(3,5))
                prev=0
                for _ in range(max_scrolls):
                    html=await page.evaluate("document.documentElement.outerHTML")
                    soup=BeautifulSoup(html,"lxml")
                    nd=soup.find("script",id="__NEXT_DATA__")
                    if nd and nd.string:
                        try: _extract_nd(json.loads(nd.string),t,hunters)
                        except: pass
                    for a in soup.find_all("a",href=re.compile(r"^/@[a-zA-Z0-9_-]+$")):
                        un=a["href"][2:]
                        if un not in hunters: hunters[un]={"username":un,"ph_url":f"https://www.producthunt.com/@{un}","name":a.get_text(strip=True) or un,"source_topics":[t],"hunted_posts":[]}
                    if len(hunters)==prev: break
                    prev=len(hunters)
                    await page.evaluate("window.scrollTo(0,document.body.scrollHeight)")
                    await asyncio.sleep(random.uniform(2,3.5))
    finally: browser.stop()
    return list(hunters.values())
