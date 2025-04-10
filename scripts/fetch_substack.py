import feedparser
import os
from datetime import datetime
import html
import requests

RSS_URL = "https://matteodevenuto.substack.com/feed"
OUTPUT_DIR = "content/blog/"
PROXY_URL = "https://api.allorigins.win/get?url="

def fetch_feed_with_proxy(url):
    try:
        # Use proxy to fetch the RSS feed
        proxy_url = f"{PROXY_URL}{url}"
        response = requests.get(proxy_url)
        print(f"Proxy HTTP Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'contents' in data:
                feed = feedparser.parse(data['contents'])
                print(f"Feed fetched successfully, entries: {len(feed.entries)}")
                return feed
            else:
                print("No 'contents' in proxy response")
                return None
        else:
            print(f"Proxy failed: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"Proxy request error: {e}")
        return None

os.makedirs(OUTPUT_DIR, exist_ok=True)

feed = fetch_feed_with_proxy(RSS_URL)
if feed is None or not hasattr(feed, 'entries'):
    print("No valid feed data retrieved. Exiting.")
else:
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
