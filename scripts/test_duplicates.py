import json
from collections import Counter

with open('acomys_library.json', 'r') as f:
    papers = json.load(f)

titles = [p.get('title', '').lower().strip() for p in papers]
title_counts = Counter(titles)

print("Most duplicated titles:")
for t, c in title_counts.most_common(5):
    print(f"{c}: {t}")

print("\nChecking for 'occurrence download'")
for p in papers:
    if 'occurrence download' in p.get('title', '').lower():
        print(p.get('title'), p.get('id'))
