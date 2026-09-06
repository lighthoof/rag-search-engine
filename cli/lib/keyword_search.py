import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from helpers import (
    tokenize, 
    tokenize_term, 
    BM25_K1, 
    BM25_B, 
    SEARCH_LIMIT,
    )
from classes.inverted_index import InvertedIndex


def search_command(query: str, limit: int) -> list[dict]:
    searchIndex = InvertedIndex()
    searchIndex.load()
    results = []

    query_tokens = tokenize(query)
    for qt in query_tokens:
        doc_ids = searchIndex.get_documents(qt)
        if doc_ids:
            for doc_id in doc_ids:
                results.append(searchIndex.docmap[doc_id])
                if len(results) >= limit:
                    return results

    return results

def build_command():
    iIndex = InvertedIndex()
    iIndex.build()
    iIndex.save()

def tf_command(doc_id: int, term: str) -> int:
    searchIndex = InvertedIndex()
    searchIndex.load()
    
    return searchIndex.get_tf(doc_id, tokenize_term(term))

def idf_command(term: str) -> float:
    searchIndex = InvertedIndex()
    searchIndex.load()

    return searchIndex.get_idf(tokenize_term(term))

def tfidf_command(doc_id: int, term: str) -> float:
    searchIndex = InvertedIndex()
    searchIndex.load()
    
    return searchIndex.get_tfidf(doc_id, tokenize_term(term))

def bm25_idf_command(term: str) -> float:
    searchIndex = InvertedIndex()
    searchIndex.load()

    return searchIndex.get_bm25_idf(tokenize_term(term))

def bm25_tf_command(doc_id: int, term: str, k1=BM25_K1, b=BM25_B) -> float:
    searchIndex = InvertedIndex()
    searchIndex.load()

    return searchIndex.get_bm25_tf(doc_id, tokenize_term(term), k1, b)

def bm25_search_command(query: str, limit=SEARCH_LIMIT):
    searchIndex = InvertedIndex()
    searchIndex.load()
    
    bm25_results = searchIndex.bm25_search(query, limit)
    movies = {}
    for key, value in bm25_results.items():
        movies[key] = searchIndex.docmap[key]
    
    return bm25_results, movies