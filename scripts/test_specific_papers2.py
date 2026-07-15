import json

with open('acomys_library.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

for p in papers:
    t = p.get('title', '')
    if "Spatial Transcriptomics" in t or "Trouble in Flatland IV" in t:
        print("TITLE:", t)
        print("LINKS:", p.get('links'))
        print("ID:", p.get('id'))
