import numpy as np
from sentence_transformers import SentenceTransformer
from lib.semantic_search import SemanticSearch
from lib.helpers import load_movies, SEARCH_LIMIT

def verify_model():
    search = SemanticSearch()
    print(f"Model loaded: {search.model}")
    print(f"Max sequence length: {search.model.max_seq_length}")

def embed_text(text: str):
    search = SemanticSearch()
    embedding = search.generate_embedding(text)

    print(f"Text: {text}")
    print(f"First 3 dimensions: {embedding[:3]}")
    print(f"Dimensions: {embedding.shape[0]}")

def verify_embeddings():
    search = SemanticSearch()
    data = load_movies()
    movies = []

    for movie in data["movies"]:
        movies.append(movie)

    embeddings = search.load_or_create_embeddings(movies)

    print(f"Number of docs:   {len(movies)}")
    print(f"Embeddings shape: {embeddings.shape[0]} vectors in {embeddings.shape[1]} dimensions")

def embed_query_text(query: str):
    search = SemanticSearch()
    embedding = search.generate_embedding(query)
    
    print(f"Query: {query}")
    print(f"First 3 dimensions: {embedding[:3]}")
    print(f"Shape: {embedding.shape}")


def search(query: str, limit=SEARCH_LIMIT):
    search = SemanticSearch()
    movies = load_movies()["movies"]

    search.load_or_create_embeddings(movies)

    results = search.search(query, limit)

    return results