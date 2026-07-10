import json
import re

def main():
    try:
        with open('acomys_library.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)
    except FileNotFoundError:
        print("Error: acomys_library.json not found.")
        return

    bib_entries = []

    for p in papers:
        # Create an ID for the bib entry
        bib_id = str(p.get('id', '')).replace('W', 'OA_').replace(' ', '_').replace('https://openalex.org/', '')
        
        title = p.get('title', '').replace('{', '\\{').replace('}', '\\}')
        
        # Zotero prefers 'and' to separate authors
        authors_str = p.get('authors', '')
        if isinstance(authors_str, list):
            authors_str = " and ".join(authors_str)
        else:
            authors_str = " and ".join([a.strip() for a in authors_str.split(',') if a.strip()])
        
        year = p.get('year', '')
        journal = p.get('journal', '')
        if not journal:
            journal = "Preprint or Abstract"
            
        abstract = (p.get('abstract') or '').replace('\n', ' ')
        doi = (p.get('links', {}).get('doi') or '').replace('https://doi.org/', '')
        url = p.get('links', {}).get('landing_page') or ''

        entry = f"@article{{{bib_id},\n"
        entry += f"  title = {{{title}}},\n"
        entry += f"  author = {{{authors_str}}},\n"
        entry += f"  year = {{{year}}},\n"
        entry += f"  journal = {{{journal}}},\n"
        
        if doi:
            entry += f"  doi = {{{doi}}},\n"
        if url:
            entry += f"  url = {{{url}}},\n"
        if abstract:
            entry += f"  abstract = {{{abstract}}},\n"
            
        entry += "}\n"
        bib_entries.append(entry)

    with open('acomys_library.bib', 'w', encoding='utf-8') as f:
        f.write("\n".join(bib_entries))

    print(f"Successfully exported {len(bib_entries)} papers to acomys_library.bib")

if __name__ == "__main__":
    main()
