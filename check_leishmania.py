import json

with open('acomys_library.json', 'r') as f:
    papers = json.load(f)

for p in papers:
    if "Potential Reservoir Host of Leishmania major" in p.get('title', ''):
        print("TITLE:", p.get('title'))
        print("TOPICS:", p.get('topics'))
        print("ABSTRACT:", p.get('abstract'))
