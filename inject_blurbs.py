import json
import re

# Read publications.html
with open('publications.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We look for blocks containing an h4 (title) and the subsequent p with class text-gray-500 containing the blurb
# <h4 class="text-xl font-semibold text-gray-800 mb-2">Title</h4>
# <p class="text-gray-600 mb-2">Authors</p>
# <p class="text-sm text-gray-500 mb-3">Blurb</p>

blurbs = {}
pattern = re.compile(r'<h4[^>]*>(.*?)</h4>\s*<p[^>]*>.*?</p>\s*<p class="text-sm text-gray-500 mb-3">\s*(.*?)\s*</p>', re.DOTALL)
matches = pattern.findall(html)

for title, blurb in matches:
    clean_title = re.sub(r'<[^>]+>', '', title).strip().lower()
    clean_blurb = re.sub(r'<[^>]+>', '', blurb).strip()
    # Normalize title for matching
    clean_title = re.sub(r'[^\w\s]', '', clean_title)
    if clean_blurb:
        blurbs[clean_title] = clean_blurb

print(f"Found {len(blurbs)} blurbs in publications.html")

# Read JSON
with open('acomys_library.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

matched = 0
for paper in papers:
    t = paper.get('title', '')
    if t:
        clean_t = re.sub(r'<[^>]+>', '', t).strip().lower()
        clean_t = re.sub(r'[^\w\s]', '', clean_t)
        
        # Exact or substring match
        for bt, blurb in blurbs.items():
            if bt in clean_t or clean_t in bt:
                paper['blurb'] = blurb
                matched += 1
                break

print(f"Matched and injected {matched} blurbs.")

with open('acomys_library.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=2, ensure_ascii=False)
