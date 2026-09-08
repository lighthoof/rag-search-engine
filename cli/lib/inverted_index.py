import os
import pickle
import math
from collections import Counter
from cli.lib.helpers import tokenize, load_movies, BM25_K1, BM25_B, CACHE_DIR

class InvertedIndex:
    def __init__(self):
        self.index_cache = os.path.join(CACHE_DIR, "index.pkl")
        self.docmap_cache = os.path.join(CACHE_DIR, "docmap.pkl")
        self.tf_cache = os.path.join(CACHE_DIR, "term_frequencies.pkl")
        self.doclength_cache = os.path.join(CACHE_DIR, "doc_lengths.pkl")

        self.index: dict[str, int] = {}
        self.docmap: dict[int, dict] = {}
        self.term_frequencies: dict[int, Counter] = {}
        self.doc_lengths: dict[int, float] = {}

    def __add_document(self, doc_id, text):
        tokens = tokenize(text)
        for token in set(tokens):
            #adding document IDs to index
            if token in self.index:
                self.index[token].append(doc_id)
            else:
                self.index[token] = [doc_id]

        #check and populate doc_id into terms frequency attribute
        if doc_id not in self.term_frequencies:
            self.term_frequencies[doc_id] = Counter()

        #incrementing the counter for tokens
        self.term_frequencies[doc_id].update(tokens)

        #store token count in documents
        self.doc_lengths[doc_id] = len(tokens)

    def __get_avg__doc_length(self) -> float:
        return sum(self.doc_lengths.values()) / len(self.doc_lengths) if self.doc_lengths else 0.0

    def get_documents(self, token):
        doc_ids = self.index.get(token, set())
        return sorted(doc_ids)

    def get_tf(self, doc_id, token):
        if token in self.term_frequencies[doc_id]:
            return self.term_frequencies[doc_id][token]
        else:
            return 0

    def get_idf(self, token):
        doc_count = len(self.docmap)
        hit_count = len(self.get_documents(token))
        return math.log((doc_count + 1) / (hit_count + 1))

    def get_tfidf(self, doc_id, token):
        tf = self.get_tf(doc_id, token)
        idf = self.get_idf(token)

        return tf * idf

    def get_bm25_idf(self, token: str) -> float:
        doc_count = len(self.docmap)
        hit_count = len(self.get_documents(token))

        return math.log((doc_count - hit_count + 0.5) / (hit_count + 0.5) + 1)
    
    def get_bm25_tf(self, doc_id, token, k1=BM25_K1, b=BM25_B):
        length_norm = 1 - b + b * (self.doc_lengths[doc_id] / self.__get_avg__doc_length())
        tf = self.get_tf(doc_id, token)
        return (tf * (k1 + 1) / (tf + k1 * length_norm))

    def build(self):
        data = load_movies()
        for movie in data["movies"]:
            self.docmap[movie["id"]] = movie
            self.__add_document(movie["id"],f"{movie['title']} {movie['description']}")

    def save(self):
        if not os.path.exists(CACHE_DIR):
            try:
                os.mkdir(CACHE_DIR)
            except PermissionError:
                print(f"Permission denied: Unable to create cache directory.")
        
        with open(self.index_cache,"wb") as index_file:
            pickle.dump(self.index,index_file)
        with open(self.docmap_cache,"wb") as docmap_file:
            pickle.dump(self.docmap,docmap_file)
        with open(self.tf_cache,"wb") as frequencies_file:
            pickle.dump(self.term_frequencies,frequencies_file)
        with open(self.doclength_cache,"wb") as doclength_file:
            pickle.dump(self.doc_lengths,doclength_file)
            
    
    def load(self):
        if not (os.path.isfile(self.index_cache) and os.path.isfile(self.docmap_cache)):
            raise Exception("Index files do not exist, please build an index first")
        
        with open(self.index_cache,"rb") as index_file:
            self.index = pickle.load(index_file)
        with open(self.docmap_cache,"rb") as docmap_file:
            self.docmap = pickle.load(docmap_file)
        with open(self.tf_cache,"rb") as frequencies_file:
            self.term_frequencies = pickle.load(frequencies_file)
        with open(self.doclength_cache,"rb") as doclength_file:
            self.doc_lengths = pickle.load(doclength_file)

    def bm25(self, doc_id: int, token: str) -> float:
        tf = self.get_bm25_tf(doc_id, token)
        idf = self.get_bm25_idf(token)

        return tf * idf

    def bm25_search(self, query: str, limit: int) -> {}:
        tokens = tokenize(query)
        scores: dict[dict, float] = {}
        
        for doc_id in self.docmap:
            bm25_total = 0.0
            for token in tokens:
                bm25_total += self.bm25(doc_id, token)         
            scores[doc_id] = bm25_total

        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_scores[:limit])

