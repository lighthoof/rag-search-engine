import json
import string
from nltk.stem import PorterStemmer

def load_movies():
    with open("data/movies.json", "r") as file:
        return json.load(file)

def load_stopwords():
    with open("data/stopwords.txt", "r") as file:
        return [preprocess_text(word) for word in file.read().splitlines()]

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))

    return text

def tokenize(text: str) -> list[str]:
    text = preprocess_text(text)
    tokens = text.split()
    not_empty_tokens = [token for token in tokens if token]
    clean_tokens = [token for token in not_empty_tokens if token not in STOPWORDS]

    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in clean_tokens]

    return stemmed_tokens

def tokenize_term(term: str) -> str:
    token = tokenize(term)

    if len(token) != 1:
        raise Exception

    return "".join(token)



STOPWORDS = load_stopwords()
BM25_K1 = 1.5
BM25_B = 0.75
SEARCH_LIMIT = 5

CACHE_DIR = "cache"