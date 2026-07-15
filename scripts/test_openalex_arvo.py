import requests
import json

url = "https://api.openalex.org/works"
params = {
    'filter': 'title_and_abstract.search:acomys',
    'per-page': 200
}
res = requests.get(url, params=params).json()

iovs_count = 0
for w in res.get('results', []):
    venue = w.get('primary_location', {}).get('source', {})
    if venue and venue.get('display_name'):
        if 'investigative' in venue.get('display_name').lower():
            print(w.get('publication_year'), w.get('title'))
            iovs_count += 1
print(f"Found {iovs_count} IOVS papers")
