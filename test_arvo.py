import json

with open('acomys_library.json', 'r') as f:
    papers = json.load(f)

print("Checking for IOVS / ARVO abstracts...")
iovs_count = 0
for p in papers:
    venue = p.get('venue', '') or ''
    title = p.get('title', '') or ''
    if 'investigative ophthalmology' in venue.lower() or 'arvo' in title.lower():
        iovs_count += 1
        print(title)

print(f"Total IOVS/ARVO papers found: {iovs_count}")
