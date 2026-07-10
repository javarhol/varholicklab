import os
import json
import re
import fitz # PyMuPDF
from thefuzz import fuzz, process

def clean_text(text):
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text, max_words=150):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i+max_words])
        if len(chunk) > 50: # Ignore tiny chunks
            chunks.append(chunk)
    return chunks

def match_filename_to_paper(filename, papers_list):
    # If the filename is an exact ID (e.g., W12345.pdf)
    base_name = filename.replace('.pdf', '')
    for p in papers_list:
        if p['id'] == base_name:
            return p
            
    # Otherwise it's a Paperpile name like "Smith et al 2023 - Title..."
    if ' - ' in base_name:
        title_part = base_name.split(' - ', 1)[1]
        # Remove trailing ... if Paperpile truncated it
        title_part = title_part.replace('...', '').strip()
    else:
        title_part = base_name
        
    # Fuzzy match the title against all papers
    choices = [p['title'] for p in papers_list]
    best_match, score = process.extractOne(title_part, choices, scorer=fuzz.token_set_ratio)
    
    if score >= 80:
        for p in papers_list:
            if p['title'] == best_match:
                return p
    return None

def main():
    print("Loading library database...")
    try:
        with open('acomys_library.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)
    except Exception as e:
        print("Could not load acomys_library.json", e)
        return

    pdf_dir = 'papers_pdf'
    if not os.path.exists(pdf_dir):
        print("papers_pdf directory not found.")
        return

    search_index = []
    
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    print(f"Found {len(pdf_files)} PDFs to process.")

    matched_count = 0
    unmatched_count = 0

    for i, filename in enumerate(pdf_files):
        print(f"[{i+1}/{len(pdf_files)}] Processing {filename} ...")
        
        paper_meta = match_filename_to_paper(filename, papers)
        if not paper_meta:
            print(f"  -> WARNING: Could not match {filename} to database. Skipping.")
            unmatched_count += 1
            continue
            
        matched_count += 1
        filepath = os.path.join(pdf_dir, filename)
        
        try:
            doc = fitz.open(filepath)
            full_text = ""
            for page in doc:
                full_text += page.get_text("text") + " "
            
            clean = clean_text(full_text)
            chunks = chunk_text(clean)
            
            for chunk_idx, chunk in enumerate(chunks):
                search_index.append({
                    "id": paper_meta['id'],
                    "title": paper_meta['title'],
                    "authors": paper_meta['authors'],
                    "year": paper_meta['year'],
                    "journal": paper_meta['journal'],
                    "chunk_id": chunk_idx,
                    "text": chunk
                })
        except Exception as e:
            print(f"  -> Error reading PDF: {e}")

    print(f"\nExtracted {len(search_index)} text chunks from {matched_count} papers.")
    if unmatched_count > 0:
        print(f"Warning: {unmatched_count} PDFs could not be matched to the library.")

    # Save search index
    with open('search_index.json', 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False)
        
    print("Successfully saved search_index.json")

if __name__ == "__main__":
    main()
