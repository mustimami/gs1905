#!/usr/bin/env python3
"""Fetch the official Galatasaray RSS feed and publish a small, safe JSON index."""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

FEED_URL = "https://www.galatasaray.org/xml/gs.rss"
OUT = Path("data/news.json")
MAX_ITEMS = 60

def text_of(node, name):
    child = node.find(name)
    if child is None or child.text is None:
        return ""
    return unescape(re.sub(r"<[^>]+>", " ", child.text)).strip()

def category(title):
    t = title.casefold()
    if any(w in t for w in ("basketbol", "basket", "fiba", "eurocup", "euroleague")):
        return "Basketbol"
    if any(w in t for w in ("voleybol", "voley", "cev", "sultanlar ligi")):
        return "Voleybol"
    if any(w in t for w in ("futbol", "maç", "transfer", "şampiyonlar ligi", "süper lig", "u19", "u17", "u15")):
        return "Futbol"
    if any(w in t for w in ("kulüp", "başkan", "divan", "duyuru", "kuruluş", "galatasaray spor kulübü")):
        return "Kulüp"
    return "Diğer"

def main():
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "GS1905-NewsBot/1.0"})
    with urllib.request.urlopen(req, timeout=25) as response:
        raw = response.read()
    root = ET.fromstring(raw)
    channel = root.find("channel")
    entries = channel.findall("item") if channel is not None else []
    records = []
    seen = set()
    for item in entries:
        title = text_of(item, "title")
        link = text_of(item, "link")
        description = text_of(item, "description")
        pub = text_of(item, "pubDate")
        if not title or not link or not link.startswith("https://www.galatasaray.org/"):
            continue
        if link in seen:
            continue
        seen.add(link)
        try:
            published = parsedate_to_datetime(pub).astimezone(timezone.utc).isoformat()
        except Exception:
            published = ""
        records.append({
            "title": title[:180],
            "description": re.sub(r"\s+, " ", description)[:280],
            "url": link,
            "published": published,
            "category": category(title),
            "source": "Galatasaray.org"
        })
        if len(records) >= MAX_ITEMS:
            break
    if not records:
        raise RuntimeError("RSS feed returned no usable articles; keeping the previous news index.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {"source": FEED_URL, "updatedAt": datetime.now(timezone.utc).isoformat(), "items": records}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Published {len(records)} official articles.")

if __name__ == "__main__":
    main()
