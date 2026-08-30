import os
import pickle
from collections import Counter
from helpers import tokenize, load_movies

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}
        self.term_frequencies: dict[int, Counter] = {}

    def __add_document(self, doc_id, text):
        tokens = tokenize(text)
        for token in tokens:
            #adding document IDs to index
            if token in self.index:
                self.index[token].append(doc_id)
            else:
                self.index[token] = [doc_id]

            #check and populate doc_id into terms frequency attribute
            if doc_id not in self.term_frequencies:
                self.term_frequencies[doc_id] = Counter()

            #incrementing the counter for tokens
            self.term_frequencies[doc_id][token] += 1

    def get_documents(self, term):
        doc_ids = self.index.get(term, [])
        return sorted(doc_ids)

    def get_tf(self, doc_id, term):
        if term in self.term_frequencies[doc_id]:
            return self.term_frequencies[doc_id][term]
        else:
            return 0

    def build(self):
        data = load_movies()
        for movie in data["movies"]:
            self.docmap[movie["id"]] = movie
            self.__add_document(movie["id"],f"{movie['title']} {movie['description']}")

    def save(self):
        if not os.path.exists("cache"):
            try:
                os.mkdir("cache")
            except PermissionError:
                print(f"Permission denied: Unable to create cache directory.")
        
        with open("cache/index.pkl","wb") as index_file:
            pickle.dump(self.index,index_file)
        with open("cache/docmap.pkl","wb") as docmap_file:
            pickle.dump(self.docmap,docmap_file)
        with open("cache/term_frequencies.pkl","wb") as frequencies_file:
            pickle.dump(self.term_frequencies,frequencies_file)
            
    
    def load(self):
        if not (os.path.isfile("cache/index.pkl") and os.path.isfile("cache/docmap.pkl")):
            raise Exception("index files do not exist")
        
        with open("cache/index.pkl","rb") as index_file:
            self.index = pickle.load(index_file)
        with open("cache/docmap.pkl","rb") as docmap_file:
            self.docmap = pickle.load(docmap_file)
        with open("cache/term_frequencies.pkl","rb") as frequencies_file:
            self.term_frequencies = pickle.load(frequencies_file)
                