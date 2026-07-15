import requests
import json

res = requests.get('https://api.openalex.org/works/W2937396402').json()
print("DOI:", res.get('doi'))
print("Primary Location:", json.dumps(res.get('primary_location'), indent=2))
print("Best OA location:", json.dumps(res.get('best_oa_location'), indent=2))
print("Locations:", len(res.get('locations', [])))
if res.get('locations'):
    for loc in res.get('locations'):
        print("  - landing page:", loc.get('landing_page_url'))
