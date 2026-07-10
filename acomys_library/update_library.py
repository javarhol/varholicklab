import json
import requests
import time
import re
import os
import difflib
import string

def normalize_string(s):
    if not s: return ""
    s = s.lower().translate(str.maketrans('', '', string.punctuation))
    return " ".join(s.split())

def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join([word for pos, word in word_positions])

def passes_filters(title, abstract, journal, doi):
    title_lower = title.lower()
    abstract_lower = abstract.lower()
    journal_lower = journal.lower()
    doi_lower = doi.lower()

    # 1. Neacomys Exclusion
    if 'neacomys' in title_lower or 'neacomys' in abstract_lower:
        return False
        
    # 2. Figshare / Zenodo Exclusion
    if 'figshare' in journal_lower or 'figshare' in doi_lower or 'zenodo' in journal_lower or 'zenodo' in doi_lower:
        return False
        
    # 3. Archives / specific exclusions
    if 'hash://md5' in title_lower or 'versioned archive' in title_lower or 'trouble in flatland' in title_lower:
        return False
        
    # 4. Cyrillic and CJK Exclusions
    if re.search(r'[А-Яа-я]', title):
        return False
    if re.search(r'[\u3040-\u30ff\u4e00-\u9fff]', title):
        return False
        
    # 5. Occurance Downloads
    if 'occurrence download' in title_lower:
        return False
        
    # 6. Threshold filter (at least 2 mentions if not in title)
    title_match = ('acomys' in title_lower or 'spiny m' in title_lower)
    if not title_match:
        acomys_count = abstract_lower.count('acomys') + abstract_lower.count('spiny m')
        if acomys_count < 2:
            return False

    return True

def categorize_paper(title, abstract, config):
    text = f"{title} {abstract}"
    assigned_topics = set()
    
    for category, keywords in config.items():
        for kw in keywords:
            escaped_kw = re.escape(kw.lower()).replace(r'\ ', r'\s+').replace(r'\*', r'\w*')
            pattern = r'(?<!\w)' + escaped_kw + r'(?!\w)'
            if re.search(pattern, text.lower()):
                assigned_topics.add(category)
                break
                
    # Explicit Tissue tag rule
    if "General Regeneration & Wound Healing" not in assigned_topics:
        # Strip all Tissue tags
        assigned_topics = {cat for cat in assigned_topics if not cat.startswith("Tissue:")}
        
    return list(assigned_topics)

def main():
    print("Loading existing database...")
    if os.path.exists('acomys_library.json'):
        with open('acomys_library.json', 'r', encoding='utf-8') as f:
            existing_papers = json.load(f)
    else:
        existing_papers = []
        
    with open('categories_config.json', 'r', encoding='utf-8') as f:
        categories_config = json.load(f)
        
    existing_by_doi = {}
    existing_norm_titles = []
    for p in existing_papers:
        doi = p.get('links', {}).get('doi', '')
        if doi:
            existing_by_doi[doi] = p
        
        t = normalize_string(p.get('title', ''))
        if t:
            existing_norm_titles.append(t)
    
    base_url = 'https://api.openalex.org/works'
    params = {
        'filter': 'title_and_abstract.search:"spiny mouse"|"spiny mice"|acomys',
        'per-page': 200,
        'page': 1
    }
    
    new_papers = []
    print("Fetching papers from OpenAlex...")
    while True:
        try:
            res = requests.get(base_url, params=params).json()
            if 'results' not in res or len(res['results']) == 0:
                break
                
            for work in res['results']:
                title = work.get('title')
                if not title:
                    continue
                    
                primary_location = work.get('primary_location')
                doi = work.get('doi') or ""
                
                # Check for DOI duplicate
                if doi and doi in existing_by_doi:
                    # Double check if the title is vaguely similar to prevent bad DOI merges
                    existing_title = normalize_string(existing_by_doi[doi].get('title', ''))
                    norm_t = normalize_string(title)
                    if existing_title and norm_t:
                        ratio = difflib.SequenceMatcher(None, existing_title, norm_t).ratio()
                        if ratio > 0.5:
                            continue # True duplicate
                
                # Check for fuzzy title duplicate
                norm_t = normalize_string(title)
                if norm_t in existing_norm_titles:
                    continue
                
                matches = difflib.get_close_matches(norm_t, existing_norm_titles, n=1, cutoff=0.90)
                if matches:
                    continue
                    
                abstract = reconstruct_abstract(work.get('abstract_inverted_index'))
                
                journal = primary_location.get('source').get('display_name', '') if primary_location and primary_location.get('source') else ""
                
                pdf = ""
                landing_page = ""
                if primary_location:
                    pdf = primary_location.get('pdf_url') or ""
                    landing_page = primary_location.get('landing_page_url') or ""
                if not pdf and work.get('open_access', {}).get('oa_url'):
                    pdf = work.get('open_access', {}).get('oa_url')

                if not passes_filters(title, abstract, journal, doi):
                    continue

                # Authors
                authorships = work.get('authorships', [])
                author_names = [a.get('author', {}).get('display_name') for a in authorships if a.get('author', {}).get('display_name')]
                
                topics = categorize_paper(title, abstract, categories_config)
                
                paper = {
                    "id": work.get('id', '').split('/')[-1],
                    "title": title,
                    "authors": ", ".join(author_names),
                    "year": work.get('publication_year'),
                    "journal": journal,
                    "topics": topics,
                    "abstract": abstract,
                    "blurb": "",
                    "links": {
                        "doi": doi,
                        "pdf": pdf,
                        "landing_page": landing_page
                    },
                    "is_abstract_only": False,
                    "related_articles": []
                }
                new_papers.append(paper)
                existing_papers.append(paper)
                
                existing_norm_titles.append(norm_t)
                if doi:
                    existing_by_doi[doi] = paper
                
            meta = res.get('meta', {})
            if len(res['results']) < params['per-page'] or meta.get('page') * params['per-page'] >= meta.get('count'):
                break
            params['page'] += 1
            time.sleep(0.1)
        except Exception as e:
            print(f"Error fetching page: {e}")
            break
            
    print(f"Found {len(new_papers)} new valid papers.")
    
    # Re-calculate related articles across the full library
    for paper in existing_papers:
        related = []
        for other in existing_papers:
            if paper['id'] != other['id']:
                common_topics = set(paper['topics']).intersection(set(other['topics']))
                if len(common_topics) >= 2:
                    related.append(other['id'])
            if len(related) >= 3:
                break
        paper['related_articles'] = related

    existing_papers.sort(key=lambda x: x.get('year') if x.get('year') else 0, reverse=True)
    
    with open('acomys_library.json', 'w', encoding='utf-8') as f:
        json.dump(existing_papers, f, indent=2, ensure_ascii=False)
        
    # Write report for email
    if new_papers:
        with open('new_papers_report.txt', 'w', encoding='utf-8') as f:
            f.write(f"The Acomys Library has been automatically updated. Here are the {len(new_papers)} new papers:\n\n")
            for p in new_papers:
                f.write(f"### {p['title']}\n")
                f.write(f"**Authors:** {p['authors']}\n")
                f.write(f"**Journal:** {p['journal']} ({p['year']})\n")
                link = p['links'].get('doi') or p['links'].get('landing_page') or f"https://openalex.org/{p['id']}"
                f.write(f"**Link:** {link}\n\n")
    else:
        with open('new_papers_report.txt', 'w', encoding='utf-8') as f:
            f.write("NO_NEW_PAPERS")

if __name__ == "__main__":
    main()
