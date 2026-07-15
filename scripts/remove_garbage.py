import json

with open('acomys_library.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

new_papers = []
for p in papers:
    if "What a Difference a Couple Hundred Million Years Can Make" in p.get('title', ''):
        continue
    # Let's also filter out things where abstract is clearly garbled (very few unique words but very long)
    # This specific one is definitely garbage.
    new_papers.append(p)

with open('acomys_library.json', 'w', encoding='utf-8') as f:
    json.dump(new_papers, f, indent=2, ensure_ascii=False)

print(f"Removed {len(papers) - len(new_papers)} papers.")
