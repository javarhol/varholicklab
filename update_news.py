#!/usr/bin/env python3
"""
Rebuild the news sections of index.html and news.html from news.json.

Usage:
    python update_news.py

How it works:
    1. Reads news.json (array of news items, newest first)
    2. Generates HTML cards for each item
    3. Replaces everything between <!-- NEWS_ITEMS_START --> and <!-- NEWS_ITEMS_END -->
       in index.html (top 3 items) and news.html (all items)

news.json format — each item can have:
    "date"      (required) — e.g. "March 2026"
    "title"     (required) — headline text
    "body"      (required) — paragraph text (HTML like <i> is fine)
    "link"      (optional) — URL for a "Learn More" style link
    "link_text" (optional) — label for the link (default "Learn More")
"""

import json, re, sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NEWS_JSON  = os.path.join(SCRIPT_DIR, "news.json")
INDEX_HTML = os.path.join(SCRIPT_DIR, "index.html")
NEWS_HTML  = os.path.join(SCRIPT_DIR, "news.html")

START_MARKER = "<!-- NEWS_ITEMS_START -->"
END_MARKER   = "<!-- NEWS_ITEMS_END -->"


def load_news():
    with open(NEWS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def make_card(item, is_latest=False):
    """Return an HTML card string for one news item."""
    extra_class = "relative" if is_latest else ""
    badge = ""
    if is_latest:
        badge = (
            '\n                        <span class="absolute top-3 right-3 bg-blue-600 '
            'text-white text-xs font-bold px-2 py-1 rounded-full">Latest</span>'
        )

    link_html = ""
    if item.get("link"):
        text = item.get("link_text", "Learn More")
        link_html = (
            f' <a href="{item["link"]}" class="text-blue-600 hover:text-blue-800 '
            f'font-medium" target="_blank" rel="noopener noreferrer">{text}</a>'
        )

    return f"""                    <!-- News Item: {item["title"][:50]} -->
                    <div class="bg-gray-50 rounded-lg shadow-md p-6 transform hover:scale-105 transition duration-300 ease-in-out {extra_class}">{badge}
                        <p class="text-sm text-gray-500 mb-2">{item["date"]}</p>
                        <h3 class="text-xl font-semibold text-gray-800 mb-3">{item["title"]}</h3>
                        <p class="text-gray-700 text-sm mb-4">
                            {item["body"]}{link_html}
                        </p>
                    </div>"""


def rebuild(html_path, cards_html):
    """Replace everything between NEWS_ITEMS_START and NEWS_ITEMS_END."""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.escape(START_MARKER) + r'.*?' + re.escape(END_MARKER)
    replacement = START_MARKER + '\n' + cards_html + '\n                    ' + END_MARKER

    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count == 0:
        print(f"  WARNING: Could not find {START_MARKER} / {END_MARKER} in {os.path.basename(html_path)}")
        return False

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def main():
    news = load_news()
    if not news:
        print("news.json is empty — nothing to do.")
        sys.exit(0)

    # Build cards for all items (first one gets "Latest" badge)
    all_cards = []
    for i, item in enumerate(news):
        all_cards.append(make_card(item, is_latest=(i == 0)))

    # index.html: top 3 only
    index_cards = "\n".join(all_cards[:3])
    ok1 = rebuild(INDEX_HTML, index_cards)

    # news.html: all items
    news_cards = "\n".join(all_cards)
    ok2 = rebuild(NEWS_HTML, news_cards)

    if ok1:
        print(f"  ✓ index.html updated ({min(3, len(news))} items)")
    if ok2:
        print(f"  ✓ news.html  updated ({len(news)} items)")
    print(f"\nDone — {len(news)} total news items in news.json.")


if __name__ == "__main__":
    main()
