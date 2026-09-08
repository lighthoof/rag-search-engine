from sentence_transformers import SentenceTransformer
from lib.semantic_search import SemanticSearch

def verify_model():
    search = SemanticSearch()
    print(f"Model loaded: {search.model}")
    print(f"Max sequence length: {search.model.max_seq_length}")