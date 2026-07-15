import json

with open('acomys_library.json', 'r') as f:
    papers = json.load(f)

for p in papers:
    if "Couple Hundred Million Years" in p.get('title', ''):
        print("TITLE:", p.get('title'))
        print("ABSTRACT:", p.get('abstract'))
