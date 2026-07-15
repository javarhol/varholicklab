import json
import re

with open('acomys_library.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

strict_papers = []

for p in papers:
    title = p.get('title', '')
    abstract = p.get('abstract', '')
    text = (title + " " + abstract).lower()
    
    # 1. Must mention acomys or spiny mouse/mice
    if 'acomys' not in text and 'spiny m' not in text:
        continue
        
    # 2. Exclude erratum/corrigendum
    if 'erratum' in title.lower() or 'corrigendum' in title.lower():
        continue
        
    # 3. Exclude garbled abstracts
    words = abstract.split()
    if len(words) > 50:
        unique_words = len(set(words))
        if unique_words / len(words) < 0.2:
            continue
            
    strict_papers.append(p)

with open('acomys_library.json', 'w', encoding='utf-8') as f:
    json.dump(strict_papers, f, indent=2, ensure_ascii=False)

print(f"Removed {len(papers) - len(strict_papers)} more papers that failed strict validation.")
