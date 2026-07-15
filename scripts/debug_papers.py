import json

with open('acomys_library.json', 'r') as f:
    papers = json.load(f)

titles_to_find = [
    "Plague and tularemia surveillance",
    "Rodent Kidney Explant Culture",
    "What a Difference a Couple Hundred Million Years Can Make",
    "Three new species of spiny mice, genusNeacomys"
]

for p in papers:
    t = p.get('title', '')
    for search_t in titles_to_find:
        if search_t.lower() in t.lower():
            print("="*60)
            print("TITLE:", t)
            print("TOPICS:", p.get('topics'))
            print("ABSTRACT:", p.get('abstract'))
