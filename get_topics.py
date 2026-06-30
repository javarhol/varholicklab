import json
from collections import Counter

with open('acomys_library.json', 'r') as f:
    papers = json.load(f)

topics = Counter()
for paper in papers:
    for t in paper.get('topics', []):
        topics[t] += 1

print(f"Total unique topics: {len(topics)}")
print("Top 50 topics:")
for t, count in topics.most_common(50):
    print(f"{count}: {t}")
