import os
import numpy as np
from sentence_transformers import SentenceTransformer
from lib.helpers import CACHE_DIR

class SemanticSearch:
    def __init__(self):
        self.embedding_cache = os.path.join(CACHE_DIR, "movie_embeddings.npy")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embeddings = None
        self.documents = None
        self.document_map = {}

    def generate_embedding(self, text: str):
        if len(text.strip()) == 0:
            raise ValueError("Empty text for embedding")

        embeddings = self.model.encode([text])
        return embeddings[0]
    
    def build_embeddings(self, documents: list[dict]):
        self.documents = documents
        self.__populate_docmap(documents)

        movies = []
        for doc in documents:
            movies.append(f"{doc['title']}:{doc['description']}")
        
        self.embeddings = self.model.encode(movies, show_progress_bar=True)
        np.save(self.embedding_cache, self.embeddings)

        return self.embeddings

    def load_or_create_embeddings(self, documents: list[dict]):
        self.documents = documents
        self.__populate_docmap(documents)

        if os.path.exists(self.embedding_cache):
            self.embeddings = np.load(self.embedding_cache)
            if len(self.embeddings) == len(documents):
                return self.embeddings
        else:
            return self.build_embeddings(documents)

    def search(self, query: str, limit: int):
        if self.embeddings is None or len(self.embeddings) == 0:
            raise ValueError("No embeddings loaded. Call `load_or_create_embeddings` first.")

        query_emb = self.generate_embedding(query)
        similarities = []
        for doc_emb, doc  in zip(self.embeddings, self.documents):
            similarity = cosine_similarity(query_emb, doc_emb)
            similarities.append((similarity, doc))
        similarities.sort(reverse=True, key=lambda x: x[0])
        similarities = similarities[:limit]

        results = []
        for sim, doc in similarities:
            results.append({"score":sim,"title":doc["title"],"description":doc["description"]})
        
        return results

    def __populate_docmap(self, documents: list[dict]):
        for doc in documents:
            self.document_map[doc["id"]] = doc


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)