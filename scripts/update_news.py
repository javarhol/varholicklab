#!/usr/bin/env python3
"""
Rebuild the news sections of index.html and news.html from news.json.

Usage:
    python scripts/update_news.py

How it works:
    1. Reads news.json (array of news items, newest first)
    2. Generates HTML for each item
    3. Replaces everything between <!-- NEWS_ITEMS_START --> and <!-- NEWS_ITEMS_END -->
         - index.html: compact <li> rows for the top 3 items (date + title, linking to news.html#slug)
         - news.html:  full <article class="news-item"> cards for every item

news.json format — each item can have:
    "date"      (required) — e.g. "March 2026"
    "title"     (required) — headline text
    "body"      (required) — paragraph text (HTML like <i> is fine)
    "link"      (optional) — URL for a "Learn More" style link
    "link_text" (optional) — label for the link (default "Learn More")
"""

import json, re, os, unicodedata

ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS_JSON  = os.path.join(ROOT, "news.json")
INDEX_HTML = os.path.join(ROOT, "index.html")
NEWS_HTML  = os.path.join(ROOT, "news.html")

START_MARKER = "<!-- NEWS_ITEMS_START -->"
END_MARKER   = "<!-- NEWS_ITEMS_END -->"
HOME_COUNT   = 3
INDENT       = " " * 20


def load_news():
    with open(NEWS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"<[^>]+>", "", text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "item"


def unique_slugs(items):
    seen, out = {}, []
    for it in items:
        s = slugify(it["title"])
        if s in seen:
            seen[s] += 1
            s = f"{s}-{seen[s]}"
        else:
            seen[s] = 1
        out.append(s)
    return out


def make_compact(item, slug):
    """Home-page row: date + title linking into news.html."""
    return (
        f'{INDENT}<li><span class="when">{item["date"]}</span>'
        f'<a class="what" href="news.html#{slug}">{item["title"]}</a></li>'
    )


def make_card(item, slug, is_latest=False):
    """News-page card."""
    tag = ' <span class="tag">Latest</span>' if is_latest else ""
    link_html = ""
    if item.get("link"):
        text = item.get("link_text", "Learn More")
        link_html = (
            f' <a href="{item["link"]}" class="inline-link" '
            f'target="_blank" rel="noopener noreferrer">{text}</a>'
        )
    return (
        f'{INDENT}<article class="news-item" id="{slug}">\n'
        f'{INDENT}    <p class="when">{item["date"]}</p>\n'
        f'{INDENT}    <h3>{item["title"]}{tag}</h3>\n'
        f'{INDENT}    <p>{item["body"]}{link_html}</p>\n'
        f'{INDENT}</article>'
    )


def rebuild(html_path, inner):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)
    replacement = START_MARKER + "\n" + inner + "\n" + INDENT + END_MARKER
    new_content, count = re.subn(pattern, lambda m: replacement, content, flags=re.DOTALL)
    if count == 0:
        print(f"  WARNING: Could not find {START_MARKER} / {END_MARKER} in {os.path.basename(html_path)}")
        return False
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def main():
    items = load_news()
    slugs = unique_slugs(items)
    print(f"Loaded {len(items)} news items from news.json")

    home = "\n".join(make_compact(it, s) for it, s in list(zip(items, slugs))[:HOME_COUNT])
    full = "\n".join(make_card(it, s, is_latest=(i == 0)) for i, (it, s) in enumerate(zip(items, slugs)))

    if rebuild(INDEX_HTML, home):
        print(f"  index.html: top {min(HOME_COUNT, len(items))} items")
    if rebuild(NEWS_HTML, full):
        print(f"  news.html: {len(items)} items")


if __name__ == "__main__":
    main()
