import json
import string

def load_movies():
    with open("data/movies.json", "r") as file:
        return json.load(file)

def search_command(query: str, limit: int) -> list[dict]:
    data = load_movies()
    results = []
    for movie in data["movies"]:
        query_tokens = tokenize(preprocess_text(query))
        title_tokens = tokenize(preprocess_text(movie["title"]))
        #if [token for token in query_tokens if token in title_tokens]:
        if has_matching_tokens(query_tokens,title_tokens):
            results.append(movie)
            if len(results) >= limit:
                break

    return results

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))

    return text

def tokenize(text: str) -> list[str]:
    tokens = text.split()
    clean_tokens = [token for token in tokens if token]

    return clean_tokens

def has_matching_tokens(query_tokens: list[str], title_tokens: list[str]) -> bool:
    for qt in query_tokens:
            for tt in title_tokens:
                if qt in tt:
                    return True

    return False