import json
import string
from nltk.stem import PorterStemmer

def load_movies():
    with open("data/movies.json", "r") as file:
        return json.load(file)

def load_stopwords():
    with open("data/stopwords.txt", "r") as file:
        return [preprocess_text(word) for word in file.read().splitlines()]

def search_command(query: str, limit: int) -> list[dict]:
    data = load_movies()
    stopwords = load_stopwords()
    results = []

    query_tokens = tokenize(preprocess_text(query))

    for movie in data["movies"]:
        title_tokens = tokenize(preprocess_text(movie["title"]))
        #if [token for token in query_tokens if token in title_tokens]:
        if has_matching_tokens(query_tokens,title_tokens):
            results.append(movie)
            if len(results) >= limit:
                break

    return results

def build_command():
    pass

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))

    return text

def tokenize(text: str) -> list[str]:
    tokens = text.split()
    not_empty_tokens = [token for token in tokens if token]
    clean_tokens = [token for token in not_empty_tokens if token not in STOPWORDS]

    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in clean_tokens]

    return stemmed_tokens

def has_matching_tokens(query_tokens: list[str], title_tokens: list[str]) -> bool:
    for qt in query_tokens:
            for tt in title_tokens:
                if qt in tt:
                    return True

    return False

STOPWORDS = load_stopwords()