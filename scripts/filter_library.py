import json
import re

with open('acomys_library.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

new_papers = []

for p in papers:
    title = p.get('title', '').lower()
    abstract = p.get('abstract', '').lower()
    journal = (p.get('journal', '') or '').lower()
    
    links = p.get('links') or {}
    doi = (links.get('doi') or '').lower()
    
    # 1. Remove Figshare
    if 'figshare' in journal or 'figshare' in doi:
        continue
        
    # 2. Remove Archives and md5
    if 'hash://md5' in title or 'versioned archive' in title:
        continue
        
    # 3. Threshold Filtering
    # Does "acomys" or "spiny m" appear in Title?
    title_match = ('acomys' in title or 'spiny m' in title)
    
    if not title_match:
        # Check abstract frequency
        acomys_count = abstract.count('acomys') + abstract.count('spiny m')
        if acomys_count < 2:
            continue
            
    new_papers.append(p)

with open('acomys_library.json', 'w', encoding='utf-8') as f:
    json.dump(new_papers, f, indent=2, ensure_ascii=False)

print(f"Removed {len(papers) - len(new_papers)} papers that failed threshold/figshare/archive filters.")
