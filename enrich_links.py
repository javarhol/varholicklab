import json
import requests
import time

with open('acomys_library.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

updated_count = 0

for p in papers:
    links = p.get('links', {})
    # If DOI and PDF are missing, but we have an OpenAlex ID
    if not links.get('doi') and not links.get('pdf') and not links.get('landing_page'):
        id_val = p.get('id', '')
        if id_val.startswith('W') or id_val.startswith('https://openalex.org/'):
            # Strip https://openalex.org/ to just get the W... ID
            clean_id = id_val.split('/')[-1]
            try:
                res = requests.get(f'https://api.openalex.org/works/{clean_id}').json()
                primary = res.get('primary_location')
                if primary and primary.get('landing_page_url'):
                    p.setdefault('links', {})['landing_page'] = primary.get('landing_page_url')
                    updated_count += 1
                time.sleep(0.1) # respect rate limit
            except Exception as e:
                pass

with open('acomys_library.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=2, ensure_ascii=False)

print(f"Successfully enriched {updated_count} papers with landing page links.")
