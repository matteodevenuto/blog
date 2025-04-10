import feedparser
import os
from datetime import datetime
import html

# Substack RSS feed URL
RSS_URL = "https://matteodevenuto.substack.com/feed"
# Output directory relative to the repo root
OUTPUT_DIR = "content/blog/"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fetch RSS feed
feed = feedparser.parse(RSS_URL)

# Process each entry
for entry in feed.entries:
    # Extract post details
    title = html.unescape(entry.title)
    slug = entry.link.split('/')[-1]  # Substack post slug from URL
    date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
    content = entry.content[0].value if 'content' in entry else entry.summary

    # Hugo frontmatter
    frontmatter = f"""---
title: "{title}"
date: {date.strftime('%Y-%m-%dT%H:%M:%SZ')}
draft: false
---
"""

    # Filename (e.g., 2025-04-10-my-post.md)
    filename = f"{date.strftime('%Y-%m-%d')}-{slug}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Write file if it doesn’t exist
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.write(frontmatter + content)
        print(f"Created {filename}")
    else:
        print(f"Skipped {filename} (already exists)")
