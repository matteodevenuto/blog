import feedparser
import os
from datetime import datetime
import html
import requests

RSS_URL = "https://matteodevenuto.substack.com/feed"
OUTPUT_DIR = "content/blog/"

# Custom feedparser with User-Agent
def fetch_feed_with_headers(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return feedparser.parse(response.content)
    else:
        print(f"Failed to fetch feed: Status {response.status_code}")
        return feedparser.parse("")

os.makedirs(OUTPUT_DIR, exist_ok=True)

feed = fetch_feed_with_headers(RSS_URL)
print(f"Feed status: {feed.status}")
print(f"Number of entries: {len(feed.entries)}")

for entry in feed.entries:
    print(f"Processing entry: {entry.title}")
    try:
        title = html.unescape(entry.title)
        slug = entry.link.split('/')[-1]
        date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S GMT")
        content = entry.content[0].value if 'content' in entry else entry.summary

        frontmatter = f"""---
title: "{title}"
date: {date.strftime('%Y-%m-%dT%H:%M:%SZ')}
draft: false
---
"""
        filename = f"{date.strftime('%Y-%m-%d')}-{slug}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(frontmatter + content)
            print(f"Created {filename}")
        else:
            print(f"Skipped {filename} (already exists)")
    except Exception as e:
        print(f"Error processing entry {entry.title}: {e}")
