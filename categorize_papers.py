import json
import re

with open('categories_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

with open('acomys_library.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

BASIC_BIOLOGY_CATEGORIES = {
    "General Regeneration & Wound Healing"
}

filtered_papers = []

for paper in papers:
    title = paper.get('title', '')
    
    # 1. Remove Russian / Cyrillic titles
    if re.search(r'[А-Яа-я]', title):
        continue
        
    text = (title + " " + paper.get('abstract', '')).lower()
    
    # 1.5 Remove Neacomys (bristly mice, distinct from Acomys but sometimes called spiny mice)
    if 'neacomys' in text:
        continue
        
    assigned_topics = set()
    
    # Keyword matching
    for category, keywords in config.items():
        for kw in keywords:
            # Handle special cases with punctuation like "sp. nov"
            # We construct a regex that allows boundaries around the keyword
            # By replacing spaces with \s+ and escaping the rest, we ensure exact phrase match.
            # \b doesn't work well if the keyword starts/ends with non-word chars (like a dot).
            # So we use a more robust boundary: (?<!\w)keyword(?!\w)
            
            # Escape the keyword, but allow variable whitespace and wildcards
            escaped_kw = re.escape(kw.lower()).replace(r'\ ', r'\s+').replace(r'\*', r'\w*')
            pattern = r'(?<!\w)' + escaped_kw + r'(?!\w)'
            
            if re.search(pattern, text):
                assigned_topics.add(category)
                break
                
    # 2. Filter Tissue tags based on basic biology / regeneration presence
    has_basic_bio = any(cat in assigned_topics for cat in BASIC_BIOLOGY_CATEGORIES)
    
    if not has_basic_bio:
        # Remove any category starting with "Tissue: "
        assigned_topics = {cat for cat in assigned_topics if not cat.startswith("Tissue:")}
                
    if not assigned_topics:
        assigned_topics.add("General Biology")
        
    paper['topics'] = list(assigned_topics)
    filtered_papers.append(paper)

with open('acomys_library.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_papers, f, indent=2, ensure_ascii=False)

print(f"Total papers before Neacomys filter: {len(papers)}")
print(f"Total papers after filter: {len(filtered_papers)}")
