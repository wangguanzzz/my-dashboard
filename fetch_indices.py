#!/usr/bin/env python3
"""Fetch US stock market indices data via Yahoo Finance API."""
import requests
import json
from datetime import datetime

INDICES = {
    "^GSPC": "S&P 500",
    "^DJI": "Dow Jones",
    "^IXIC": "NASDAQ",
    "^RUT": "Russell 2000",
    "^VIX": "VIX",
}

def fetch():
    result = {}
    
    for symbol, name in INDICES.items():
        try:
            # Use Yahoo Finance quote API
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {"interval": "1d", "range": "2d"}
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json",
            }
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            data = resp.json()
            
            chart = data.get("chart", {}).get("result", [{}])[0]
            timestamps = chart.get("timestamp", [])
            closes = chart.get("indicators", {}).get("quote", [{}])[0].get("close", [])
            
            if not timestamps or not closes:
                continue
                
            current = closes[-1]
            prev = closes[-2] if len(closes) > 1 and closes[-2] is not None else current
            
            change = current - prev
            change_pct = (change / prev * 100) if prev != 0 else 0
            
            result[symbol] = {
                "name": name,
                "symbol": symbol,
                "price": round(current, 2),
                "change": round(change, 2),
                "change_pct": round(change_pct, 2),
            }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
    
    result["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("/home/ubuntu/.openclaw/workspace/dashboard/data/indices.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"Updated at {result['updated']}")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    fetch()
