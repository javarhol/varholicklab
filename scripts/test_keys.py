import json

with open('acomys_library.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

for p in papers:
    if not p.get('links', {}).get('doi') and not p.get('links', {}).get('pdf'):
        print(p.keys())
        print(p.get('id'))
        break
