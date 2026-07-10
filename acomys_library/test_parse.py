import re
def parse_bib_titles_dois(bib_path):
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = []
    # simplistic split by @
    raw_entries = content.split('\n@')
    for raw in raw_entries[1:10]:
        title_match = re.search(r'title\s*=\s*[\{"](.*?)(?<!\\)[\}"]', raw, re.IGNORECASE | re.DOTALL)
        doi_match = re.search(r'doi\s*=\s*[\{"](.*?)(?<!\\)[\}"]', raw, re.IGNORECASE)
        
        title = title_match.group(1).replace('\n', ' ') if title_match else ""
        print("RAW TITLE:", title)
            
parse_bib_titles_dois('Paperpile - Acomys Library - Jul 10.bib')
