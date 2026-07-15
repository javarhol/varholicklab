import json
import re
from collections import Counter

with open('acomys_library.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

suspicious_papers = []

for p in papers:
    title = p.get('title', '').lower()
    abstract = p.get('abstract', '').lower()
    full_text = title + " " + abstract
    
    reasons = []
    
    # 1. Check if 'acomys' or 'spiny m' is actually in the text
    # OpenAlex might match full text, but we only want title/abstract matches.
    if 'acomys' not in full_text and 'spiny m' not in full_text:
        reasons.append("Does not mention acomys or spiny mice in title/abstract")
        
    # 2. Check for Erratum/Corrigendum/Index
    if 'erratum' in title or 'corrigendum' in title or 'index of' in title:
        reasons.append("Looks like an erratum or index")
        
    # 3. Check for garbled abstracts (high length, low unique words)
    words = abstract.split()
    if len(words) > 50:
        unique_words = len(set(words))
        if unique_words / len(words) < 0.2: # Less than 20% unique words
            reasons.append("Abstract appears garbled/OCR corrupted")
            
    # 4. Very short titles
    if len(title.split()) <= 1 and 'acomys' not in title:
        reasons.append("Title is unusually short")

    if reasons:
        suspicious_papers.append({
            'title': p.get('title'),
            'reasons': reasons
        })

print(f"Found {len(suspicious_papers)} suspicious papers out of {len(papers)}")
for s in suspicious_papers[:10]:
    print(f"- {s['title']} ({', '.join(s['reasons'])})")
