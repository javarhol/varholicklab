import requests

def get_count(filter_str):
    url = f"https://api.openalex.org/works?filter={filter_str}&per-page=1"
    res = requests.get(url).json()
    return res.get('meta', {}).get('count', 0)

print("Default search 'acomys':", get_count("default.search:acomys"))
print("Title and abstract 'acomys':", get_count("title_and_abstract.search:acomys"))
print("Title and abstract 'spiny mouse' OR 'acomys':", get_count("title_and_abstract.search:acomys|spiny mouse"))
print("Title and abstract 'spiny mice' OR 'acomys':", get_count("title_and_abstract.search:acomys|spiny mice"))
print("Title and abstract 'spiny mouse' OR 'spiny mice' OR 'acomys':", get_count("title_and_abstract.search:acomys|spiny mouse|spiny mice"))

