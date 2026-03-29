#!/usr/bin/env python3
"""Fetch GitHub Trending RSS."""
import feedparser
import json
from datetime import datetime

FEED = "https://mshibanami.github.io/GitHubTrendingRSS/daily/all.xml"

def fetch():
    try:
        feed = feedparser.parse(FEED)
        items = []
        for entry in feed.entries[:20]:
            items.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "description": entry.get("description", "")[:200],
                "author": entry.get("author", ""),
                "published": entry.get("published", ""),
            })
        
        result = {
            "items": items,
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        with open("/home/ubuntu/.openclaw/workspace/dashboard/data/github.json", "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Fetched {len(items)} items at {result['updated']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch()
