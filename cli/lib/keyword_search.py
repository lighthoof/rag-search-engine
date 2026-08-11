import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from helpers import tokenize
from classes.inverted_index import InvertedIndex


def search_command(query: str, limit: int) -> list[dict]:
    searchIndex = InvertedIndex()
    try:
        searchIndex.load()
    except Exception:
        print("Index files do not exist, please build an index first")
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

