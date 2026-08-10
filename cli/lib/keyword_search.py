import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import helpers as hlp
from classes.inverted_index import InvertedIndex


def search_command(query: str, limit: int) -> list[dict]:
    data = hlp.load_movies()
    stopwords = hlp.load_stopwords()
    results = []

    query_tokens = hlp.tokenize(query)
    for movie in data["movies"]:
        title_tokens = hlp.tokenize(movie["title"])
        #if [token for token in query_tokens if token in title_tokens]:
        if hlp.has_matching_tokens(query_tokens, title_tokens):
            results.append(movie)
            if len(results) >= limit:
                break

    return results

def build_command():
    iIndex = InvertedIndex()
    iIndex.build()
    iIndex.save()

