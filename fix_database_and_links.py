import json
import re

# 1. Update categories_config.json
with open('categories_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

if "aav" not in config["Tools & Techniques"]:
    config["Tools & Techniques"].extend(["aav", "spatial transcriptomics"])

with open('categories_config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2)


# 2. Filter acomys_library.json
with open('acomys_library.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

new_papers = []

for p in papers:
    title = p.get('title', '')
    journal = (p.get('journal', '') or '').lower()
    doi = p.get('links', {}).get('doi', '') or ''
    
    # Exclude Zenodo
    if 'zenodo' in journal.lower() or 'zenodo' in doi.lower():
        continue
        
    # Exclude Trouble in Flatland
    if 'trouble in flatland' in title.lower():
        continue
        
    # Exclude Japanese/Chinese (CJK characters)
    # \u3040-\u30ff (Hiragana/Katakana), \u4e00-\u9fff (Kanji)
    if re.search(r'[\u3040-\u30ff\u4e00-\u9fff]', title):
        continue
        
    new_papers.append(p)

with open('acomys_library.json', 'w', encoding='utf-8') as f:
    json.dump(new_papers, f, indent=2, ensure_ascii=False)

print(f"Removed {len(papers) - len(new_papers)} papers (zenodo, CJK titles, flatland).")
