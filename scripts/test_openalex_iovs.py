import requests

url = "https://api.openalex.org/works"
# Let's search OpenAlex broadly for Acomys and IOVS
params = {
    'filter': 'default.search:acomys',
    'per-page': 50
}
res = requests.get(url, params=params).json()

iovs_count = 0
for w in res.get('results', []):
    venue = w.get('primary_location', {}).get('source', {})
    if venue and venue.get('display_name'):
        if 'ophthalmology' in venue.get('display_name').lower():
            print(w.get('title'))
            iovs_count += 1
            
print(f"Found {iovs_count} ophthalmology papers in first 50 default search.")
