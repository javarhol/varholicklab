import json
import os
import requests
import time

def main():
    if not os.path.exists('papers_pdf'):
        os.makedirs('papers_pdf')
        
    try:
        with open('acomys_library.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)
    except FileNotFoundError:
        print("Error: acomys_library.json not found.")
        return

    indexed_ids = set()
    try:
        with open('search_index.json', 'r', encoding='utf-8') as f:
            search_index = json.load(f)
            for chunk in search_index:
                if 'id' in chunk:
                    indexed_ids.add(chunk['id'])
    except FileNotFoundError:
        print("Notice: search_index.json not found. Will download all missing PDFs.")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Accept': 'application/pdf'
    }

    print(f"Total papers in database: {len(papers)}")
    
    downloaded = 0
    skipped = 0
    failed = 0

    for p in papers:
        paper_id = p.get('id', '')
        pdf_url = p.get('links', {}).get('pdf', '')
        
        if not pdf_url:
            continue
            
        if paper_id in indexed_ids:
            skipped += 1
            continue

        file_path = os.path.join('papers_pdf', f"{paper_id}.pdf")
        
        if os.path.exists(file_path):
            skipped += 1
            continue
            
        print(f"Downloading {paper_id} from {pdf_url} ...")
        
        try:
            res = requests.get(pdf_url, headers=headers, stream=True, timeout=10)
            if res.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in res.iter_content(1024):
                        f.write(chunk)
                downloaded += 1
            else:
                print(f"  -> Failed: HTTP {res.status_code}")
                failed += 1
        except Exception as e:
            print(f"  -> Failed with error: {e}")
            failed += 1
            
        time.sleep(0.5)

    print(f"\nFinished!")
    print(f"Downloaded: {downloaded}")
    print(f"Skipped (already exist): {skipped}")
    print(f"Failed: {failed}")

if __name__ == "__main__":
    main()
