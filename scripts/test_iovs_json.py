import json

with open('acomys_library.json', 'r') as f:
    papers = json.load(f)

print("Checking JSON for IOVS...")
iovs_count = 0
for p in papers:
    venue = p.get('venue')
    if venue and 'investigative ophthalmology' in venue.lower():
        print(p.get('publication_year'), p.get('title'))
        iovs_count += 1
print(f"Total IOVS: {iovs_count}")
