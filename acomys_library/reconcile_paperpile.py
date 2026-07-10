import json
import difflib
import string
import re

def normalize_string(s):
    if not s: return ""
    # remove latex formatting commands
    s = re.sub(r'\\[a-zA-Z]+', '', s)
    s = s.lower().translate(str.maketrans('', '', string.punctuation))
    return " ".join(s.split())

def parse_bib_titles_dois(bib_path):
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = []
    raw_entries = content.split('\n@')
    
    for raw in raw_entries[1:]:
        lines = raw.split('\n')
        title = ""
        doi = ""
        in_title = False
        
        for line in lines:
            line_strip = line.strip()
            if line_strip.lower().startswith('title'):
                in_title = True
                # extract everything after =
                val = line_strip.split('=', 1)[1].strip()
                title += val + " "
                if (val.endswith(',') and (val.count('{') == val.count('}'))) or (val.endswith('",') and val.count('"') % 2 == 0):
                    in_title = False
            elif in_title:
                title += line_strip + " "
                if (line_strip.endswith(',') and (title.count('{') == title.count('}'))) or (line_strip.endswith('",')):
                    in_title = False
            
            if line_strip.lower().startswith('doi'):
                val = line_strip.split('=', 1)[1].strip()
                # strip {}, "", and trailing comma
                val = val.strip('{},"')
                doi = val
                
        if title:
            # clean up title
            title = title.strip('{}," ')
            # if it ends with , strip it
            if title.endswith(','): title = title[:-1]
            title = title.strip('{}," ')
            # remove braces
            title = title.replace('{', '').replace('}', '')
            
            entries.append({'title': normalize_string(title), 'doi': doi, 'raw_title': title})
            
    return entries

def main():
    bib_entries = parse_bib_titles_dois('Paperpile - Acomys Library - Jul 10.bib')
    print(f"Found {len(bib_entries)} entries in Paperpile bib.")
    
    with open('acomys_library.json', 'r', encoding='utf-8') as f:
        json_papers = json.load(f)
        
    print(f"Found {len(json_papers)} entries in our JSON.")
    
    for jp in json_papers:
        jp['norm_title'] = normalize_string(jp.get('title', ''))

    json_by_doi = {}
    json_by_exact_title = {}
    for jp in json_papers:
        doi = jp.get('links', {}).get('doi', '')
        if doi:
            if doi not in json_by_doi:
                json_by_doi[doi] = []
            json_by_doi[doi].append(jp)
            
        t = jp['norm_title']
        if t:
            if t not in json_by_exact_title:
                json_by_exact_title[t] = []
            json_by_exact_title[t].append(jp)

    final_kept_papers = []
    matched_json_ids = set()
    
    unmatched_bibs = []
    
    for bib in bib_entries:
        best_jp = None
        
        # 1. match by DOI
        if bib['doi'] and bib['doi'] in json_by_doi:
            for jp in json_by_doi[bib['doi']]:
                if jp['id'] not in matched_json_ids:
                    best_jp = jp
                    break
                    
        # 2. match by exact title
        if not best_jp and bib['title'] in json_by_exact_title:
            for jp in json_by_exact_title[bib['title']]:
                if jp['id'] not in matched_json_ids:
                    best_jp = jp
                    break

        # 3. fuzzy match
        if not best_jp:
            b_title = bib['title']
            b_len = len(b_title)
            best_score = -1
            
            for jp in json_papers:
                if jp['id'] in matched_json_ids: continue
                j_title = jp['norm_title']
                if not j_title: continue
                
                # length filter
                if abs(len(j_title) - b_len) > 20:
                    continue
                
                ratio = difflib.SequenceMatcher(None, b_title, j_title).ratio()
                if ratio > best_score:
                    best_score = ratio
                    best_jp = jp
                    
            if best_score < 0.85:
                best_jp = None
                
        if best_jp:
            final_kept_papers.append(best_jp)
            matched_json_ids.add(best_jp['id'])
        else:
            unmatched_bibs.append(bib['raw_title'])

    print(f"\nFinal Kept Papers: {len(final_kept_papers)}")
    print(f"Papers removed as duplicates/unmatched: {len(json_papers) - len(final_kept_papers)}")
    print(f"Unmatched Bib entries: {len(unmatched_bibs)}")
    
    if len(unmatched_bibs) < 20:
        for t in unmatched_bibs:
            print(f" - {t}")
            
    with open('acomys_library.json', 'w', encoding='utf-8') as f:
        json.dump(final_kept_papers, f, indent=2, ensure_ascii=False)
        
if __name__ == "__main__":
    main()
