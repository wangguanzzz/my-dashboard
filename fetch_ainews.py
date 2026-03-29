#!/usr/bin/env python3
"""Fetch AI news from RSS feeds."""
import feedparser
import json
from datetime import datetime

FEEDS = [
    ("MIT Tech Review", "https://www.technologyreview.com/topic/artificial-intelligence/feed"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/"),
    ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
]

MAX_PER_SOURCE = 5

def fetch():
    all_items = []
    
    for name, url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:MAX_PER_SOURCE]:
                all_items.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "source": name,
                    "published": entry.get("published", ""),
                })
        except Exception as e:
            print(f"Error fetching {name}: {e}")
    
    result = {
        "items": all_items[:20],
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    with open("/home/ubuntu/.openclaw/workspace/dashboard/data/ainews.json", "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Fetched {len(all_items)} items at {result['updated']}")

if __name__ == "__main__":
    fetch()
