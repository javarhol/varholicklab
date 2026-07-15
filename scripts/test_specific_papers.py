import json

with open('acomys_library.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

titles = [
    "Possibilities of modeling endocrinopathies",
    "De Novo Regeneration of Rete Ridges",
    "Chigger mites (Acariformes",
    "Functional heart recovery"
]

for p in papers:
    t = p.get('title', '')
    for st in titles:
        if st.lower() in t.lower():
            print("="*60)
            print("TITLE:", t)
            print("ABSTRACT:", p.get('abstract'))
            print("TOPICS:", p.get('topics'))
            print("LINKS:", p.get('links'))
            print("JOURNAL:", p.get('journal'))

figshare_count = sum(1 for p in papers if 'figshare' in (p.get('journal', '') or '').lower())
print(f"Total figshare items: {figshare_count}")

no_links = sum(1 for p in papers if not p.get('links', {}).get('doi') and not p.get('links', {}).get('pdf'))
print(f"Total papers with NO links: {no_links}")

