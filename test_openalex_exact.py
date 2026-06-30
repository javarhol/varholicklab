import requests

def get_count(filter_str):
    url = f"https://api.openalex.org/works?filter={filter_str}&per-page=1"
    res = requests.get(url).json()
    return res.get('meta', {}).get('count', 0)

print("Title and abstract acomys:", get_count("title_and_abstract.search:acomys"))

# Exact phrase matching in OpenAlex
# URL encoding might be needed, but requests handles params if passed properly.
url = "https://api.openalex.org/works"
params = {'filter': 'title_and_abstract.search:"spiny mouse"|"spiny mice"|acomys'}
print("Exact phrase combinations:", requests.get(url, params=params).json().get('meta', {}).get('count', 0))

params2 = {'filter': 'title_and_abstract.search:acomys'}
print("Just acomys:", requests.get(url, params=params2).json().get('meta', {}).get('count', 0))

