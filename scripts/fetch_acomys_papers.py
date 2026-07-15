import requests
import json
import time

def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join([word for pos, word in word_positions])

def fetch_acomys_papers():
    base_url = 'https://api.openalex.org/works'
    params = {
        'filter': 'title_and_abstract.search:"spiny mouse"|"spiny mice"|acomys',
        'per-page': 200,
        'page': 1
    }
    
    papers = []
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
                
                # Authors
                authorships = work.get('authorships', [])
                author_names = [a.get('author', {}).get('display_name') for a in authorships if a.get('author', {}).get('display_name')]
                authors_str = ", ".join(author_names)
                
                # Year & Journal
                year = work.get('publication_year')
                journal = ""
                primary_location = work.get('primary_location')
                if primary_location and primary_location.get('source'):
                    journal = primary_location.get('source').get('display_name', '')
                
                # Links
                doi = work.get('doi')
                pdf = ""
                landing_page = ""
                if primary_location:
                    if primary_location.get('pdf_url'):
                        pdf = primary_location.get('pdf_url')
                    if primary_location.get('landing_page_url'):
                        landing_page = primary_location.get('landing_page_url')
                
                if not pdf and work.get('open_access', {}).get('oa_url'):
                    pdf = work.get('open_access', {}).get('oa_url')
                    
                # Abstract
                abstract = reconstruct_abstract(work.get('abstract_inverted_index'))
                
                # Preprints / Abstracts
                work_type = work.get('type')
                is_abstract_only = False
                if work_type in ['preprint', 'dissertation'] or not journal:
                    is_abstract_only = True
                # Sometimes conference papers/abstracts are labeled as such
                # if 'abstract' in title.lower() or work_type == 'dataset':
                #   is_abstract_only = True
                
                # Topics
                topics = []
                for concept in work.get('concepts', []):
                    # Only take highly relevant topics
                    if concept.get('score', 0) > 0.5:
                        topics.append(concept.get('display_name'))
                
                # Fallback to main topics
                if not topics and work.get('topics'):
                    for topic in work.get('topics', []):
                        if topic.get('score', 0) > 0.5:
                            topics.append(topic.get('display_name'))

                paper = {
                    "id": work.get('id', '').split('/')[-1],
                    "title": title,
                    "authors": authors_str,
                    "year": year,
                    "journal": journal,
                    "topics": topics[:3], # Top 3 topics
                    "abstract": abstract,
                    "blurb": "",
                    "links": {
                        "doi": doi,
                        "pdf": pdf,
                        "landing_page": landing_page
                    },
                    "is_abstract_only": is_abstract_only,
                    "related_articles": [] # Can be populated later or dynamically
                }
                papers.append(paper)
            
            print(f"Fetched page {params['page']} (Total so far: {len(papers)})")
            
            # Pagination
            meta = res.get('meta', {})
            if len(res['results']) < params['per-page'] or meta.get('page') * params['per-page'] >= meta.get('count'):
                break
                
            params['page'] += 1
            time.sleep(0.1) # Respect API limits
        except Exception as e:
            print(f"Error fetching page {params['page']}: {e}")
            break

    print(f"Calculating related articles for {len(papers)} fetched papers...")
    
    # ---------------------------------------------------------
    # NEW: Deduplication and cleanup
    # ---------------------------------------------------------
    cleaned_papers = []
    seen_titles = set()
    
    for paper in papers:
        t = paper.get('title', '')
        if not t:
            continue
            
        clean_t = t.lower().strip()
        
        # Remove Occurrence Downloads
        if 'occurrence download' in clean_t:
            continue
            
        # Deduplicate by exact title
        if clean_t in seen_titles:
            continue
            
        seen_titles.add(clean_t)
        cleaned_papers.append(paper)
        
    papers = cleaned_papers
    # ---------------------------------------------------------

    # Calculate related articles very simply based on shared topics (just IDs)
    for paper in papers:
        related = []
        for other in papers:
            if paper['id'] != other['id']:
                common_topics = set(paper['topics']).intersection(set(other['topics']))
                if len(common_topics) >= 2:
                    related.append(other['id'])
            if len(related) >= 3:
                break
        paper['related_articles'] = related

    print(f"Saving {len(papers)} papers to acomys_library.json")
    # Sort by year descending
    papers.sort(key=lambda x: x['year'] if x['year'] else 0, reverse=True)
    
    with open('acomys_library.json', 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    fetch_acomys_papers()
