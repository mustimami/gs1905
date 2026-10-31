#!/usr/bin/env python3
"""Fetch official Galatasaray RSS items and publish a small, safe JSON index."""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from urllib.parse import urlsplit

FEED_URL = "https://www.galatasaray.org/xml/gs.rss"
OUT = Path("data/news.json")
MAX_ITEMS = 60

def clean(value):
    return re.sub(r"\\s+", " ", unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()

def child_text(node, local_name):
    for child in node.iter():
        if child.tag.split("}")[-1] == local_name and child.text:
            return clean(child.text)
    return ""

def safe_image(url):
    if not url:
        return ""
    try:
        parsed = urlsplit(url.strip())
        host = (parsed.hostname or "").lower()
        if parsed.scheme == "https" and (host == "galatasaray.org" or host.endswith(".galatasaray.org")):
            return url.strip()
    except ValueError:
        pass
    return ""

def image_for(item):
    # RSS 2.0 enclosure and common Media RSS fields.
    for child in item.iter():
        name = child.tag.split("}")[-1].lower()
        if name in ("content", "thumbnail") and child.attrib.get("url"):
            candidate = safe_image(child.attrib["url"])
            if candidate:
                return candidate
        if name == "enclosure" and child.attrib.get("url"):
            candidate = safe_image(child.attrib["url"])
            if candidate:
                return candidate
    # Some feeds embed the lead image in the HTML description.
    description = child_text(item, "description")
    match = re.search(r'<img[^>]+src=["\\\']([^"\\\']+)["\\\']', description, re.I)
    return safe_image(unescape(match.group(1))) if match else ""

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
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "GS1905-NewsBot/1.1"})
    with urllib.request.urlopen(req, timeout=25) as response:
        raw = response.read()
    root = ET.fromstring(raw)
    channel = next((node for node in root.iter() if node.tag.split("}")[-1] == "channel"), None)
    entries = [node for node in list(channel or []) if node.tag.split("}")[-1] == "item"]
    records, seen = [], set()
    for item in entries:
        title = child_text(item, "title")
        link = child_text(item, "link")
        description = child_text(item, "description")
        pub = child_text(item, "pubDate")
        if not title or not link or not link.startswith("https://www.galatasaray.org/") or link in seen:
            continue
        seen.add(link)
        try:
            published = parsedate_to_datetime(pub).astimezone(timezone.utc).isoformat()
        except Exception:
            published = ""
        record = {
            "title": title[:180],
            "description": description[:280],
            "url": link,
            "published": published,
            "category": category(title),
            "source": "Galatasaray.org"
        }
        image = image_for(item)
        if image:
            record["image"] = image
        records.append(record)
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
