#!/usr/bin/env python3
import requests, re, os, time
from bs4 import BeautifulSoup
from datetime import datetime

REDIRECTOR = os.getenv("TAMILMV_REDIRECTOR", "https://your-redirector.example.com")
OUTPUT_FILE = "tamilmv_feed.xml"
MAX_ITEMS = 100

def fetch_page(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print("Fetch error:", e)
        return None

def scrape():
    url = f"{REDIRECTOR}/"
    html = fetch_page(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    posts = soup.select("a")[:20]  # first 20 links
    items = []
    for post in posts:
        href = post.get("href")
        if not href: continue
        page_html = fetch_page(href)
        if not page_html: continue
        magnets = re.findall(r"magnet:\?xt=urn:[^"]+", page_html)
        if magnets:
            items.append({
                "title": post.text.strip()[:200],
                "link": href,
                "magnets": magnets,
                "pubDate": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
            })
    return items

def load_existing():
    if not os.path.exists(OUTPUT_FILE): return []
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        xml = f.read()
    matches = re.findall(r"<title>(.*?)</title>", xml)
    return matches

def save_xml(items):
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>1TamilMV Scraper</title>'
    footer = "</channel></rss>"
    body = ""
    for it in items[:MAX_ITEMS]:
        for m in it["magnets"]:
            body += f"<item><title>{it['title']}</title><link>{m}</link><pubDate>{it['pubDate']}</pubDate></item>\n"
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(header + body + footer)

def main():
    new_items = scrape()
    if not new_items: return
    existing_titles = load_existing()
    combined = []
    for n in new_items:
        if n["title"] not in existing_titles:
            combined.append(n)
    if not combined: return
    print(f"Adding {len(combined)} new items")
    save_xml(combined + [])

if __name__ == "__main__":
    main()
