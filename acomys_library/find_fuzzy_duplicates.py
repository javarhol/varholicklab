import json
import difflib
import string

def normalize_string(s):
    if not s: return ""
    s = s.lower().translate(str.maketrans('', '', string.punctuation))
    return " ".join(s.split())

def main():
    with open('acomys_library.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)

    # 1. Exact DOI duplicates
    doi_map = {}
    doi_duplicates = []
    
    # 2. Fuzzy Title duplicates
    title_map = {}
    fuzzy_title_duplicates = []
    
    # Keep track of already matched to avoid showing A=B and B=A
    seen_pairs = set()

    # Pre-compute normalized titles
    for p in papers:
        p['norm_title'] = normalize_string(p.get('title', ''))

    for i in range(len(papers)):
        p1 = papers[i]
        
        # Check DOI
        doi1 = p1.get('links', {}).get('doi', '')
        if doi1:
            if doi1 in doi_map:
                # duplicate!
                p2 = doi_map[doi1]
                pair = tuple(sorted([p1['id'], p2['id']]))
                if pair not in seen_pairs:
                    doi_duplicates.append((p1, p2))
                    seen_pairs.add(pair)
            else:
                doi_map[doi1] = p1

        # Check fuzzy title against already processed papers (O(N^2) but N is small)
        for j in range(i):
            p2 = papers[j]
            pair = tuple(sorted([p1['id'], p2['id']]))
            if pair in seen_pairs:
                continue
                
            t1 = p1['norm_title']
            t2 = p2['norm_title']
            
            # Simple length check first for speed
            if not t1 or not t2: continue
            if abs(len(t1) - len(t2)) > 15: continue
            
            # Fuzzy match
            ratio = difflib.SequenceMatcher(None, t1, t2).ratio()
            if ratio > 0.90:
                fuzzy_title_duplicates.append((p1, p2, ratio))
                seen_pairs.add(pair)

    # Output results
    with open('duplicate_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"=== Exact DOI Duplicates: {len(doi_duplicates)} ===\n\n")
        for p1, p2 in doi_duplicates:
            f.write(f"Paper 1: [{p1['id']}] {p1.get('title')}\n")
            f.write(f"Paper 2: [{p2['id']}] {p2.get('title')}\n")
            f.write(f"DOI: {p1.get('links', {}).get('doi')}\n")
            f.write("-" * 50 + "\n")
            
        f.write(f"\n=== Fuzzy Title Duplicates (>90% match): {len(fuzzy_title_duplicates)} ===\n\n")
        # sort by ratio descending
        fuzzy_title_duplicates.sort(key=lambda x: x[2], reverse=True)
        for p1, p2, ratio in fuzzy_title_duplicates:
            f.write(f"Match Ratio: {ratio:.2f}\n")
            f.write(f"Paper 1: [{p1['id']}] {p1.get('title')}\n")
            f.write(f"Paper 2: [{p2['id']}] {p2.get('title')}\n")
            f.write("-" * 50 + "\n")
            
    print(f"Found {len(doi_duplicates)} DOI duplicates and {len(fuzzy_title_duplicates)} fuzzy title duplicates.")
    print("Results saved to duplicate_report.txt")

if __name__ == "__main__":
    main()
