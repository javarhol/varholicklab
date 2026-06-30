import json
import requests
import re

with open('acomys_library.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

# 1. Deduplicate and remove occurrence downloads
cleaned_papers = []
seen_titles = set()

for paper in papers:
    t = paper.get('title', '')
    if not t:
        continue
        
    clean_t = t.lower().strip()
    
    if 'occurrence download' in clean_t:
        continue
        
    if clean_t in seen_titles:
        continue
        
    seen_titles.add(clean_t)
    cleaned_papers.append(paper)

print(f"Removed {len(papers) - len(cleaned_papers)} duplicate/occurrence papers.")
papers = cleaned_papers

# 2. Enrich missing abstracts via Crossref
missing_abstracts = [p for p in papers if not p.get('abstract') and p.get('links', {}).get('doi')]
print(f"Found {len(missing_abstracts)} papers with a DOI but missing an abstract. Attempting to fetch...")

enriched = 0
for i, p in enumerate(missing_abstracts):
    doi = p['links']['doi'].replace('https://doi.org/', '')
    try:
        res = requests.get(f"https://api.crossref.org/works/{doi}").json()
        abstract = res.get('message', {}).get('abstract', '')
        if abstract:
            # Crossref abstracts often come with JATS XML tags like <jats:title>Abstract</jats:title><jats:p>...</jats:p>
            clean_abstract = re.sub(r'<[^>]+>', '', abstract).strip()
            p['abstract'] = clean_abstract
            enriched += 1
    except Exception as e:
        pass
    if i > 0 and i % 50 == 0:
        print(f"Processed {i}/{len(missing_abstracts)}...")

print(f"Successfully fetched and enriched {enriched} missing abstracts.")

# 3. Add ARVO 2026 abstracts manually
arvo_papers = [
    {
        "id": "ARVO_2026_1",
        "title": "Inhibition of immune cells in the Acomys retina: A method for investigating the role of microglia in the retinal damage response of spiny mice",
        "authors": "D Buendia-Castillo, JD Bills, AW Seifert, AC Morris",
        "year": 2026,
        "journal": "Investigative Ophthalmology & Visual Science",
        "topics": ["Tissue: Retina & Visual System", "Immunology & Infection", "Neuroscience & Behavior"],
        "abstract": "",
        "blurb": "",
        "links": {"doi": "", "pdf": ""},
        "is_abstract_only": True,
        "related_articles": []
    },
    {
        "id": "ARVO_2026_2",
        "title": "Response to Optic Nerve Injury in the Spiny Mouse",
        "authors": "JD Bills, AC Morris",
        "year": 2026,
        "journal": "Investigative Ophthalmology & Visual Science",
        "topics": ["Tissue: Nervous System", "Tissue: Retina & Visual System", "General Regeneration & Wound Healing"],
        "abstract": "",
        "blurb": "",
        "links": {"doi": "", "pdf": ""},
        "is_abstract_only": True,
        "related_articles": []
    },
    {
        "id": "ARVO_2026_3",
        "title": "African spiny mice: Ocular surface structure and scarless corneal wound healing",
        "authors": "VJ Coulson-Thomas, PAG Montoya, Y Carrillo",
        "year": 2026,
        "journal": "Investigative Ophthalmology & Visual Science",
        "topics": ["Tissue: Retina & Visual System", "General Regeneration & Wound Healing", "Tissue: Skin & Hair"],
        "abstract": "",
        "blurb": "",
        "links": {"doi": "", "pdf": ""},
        "is_abstract_only": True,
        "related_articles": []
    }
]

# Only add if not already in there
for arvo in arvo_papers:
    if arvo['title'].lower().strip() not in seen_titles:
        papers.insert(0, arvo) # Put at the top since it's newest
        print(f"Added ARVO paper: {arvo['title']}")

with open('acomys_library.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=2, ensure_ascii=False)

