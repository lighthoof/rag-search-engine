import os
import pickle
from cli.lib.keyword_search import tokenize, load_movies

class InvertedIndex:
    def __add_document(self, doc_id, text):
        tokens = tokenize(text)
        for token in tokens:
            if token in self.index:
                self.index[token].append(doc_id)
            else:
                self.index[token] = [doc_id]

    def get_documents(self, term):
        return sorted(self.index[term])

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
        
        self.__handle_data_dump()

    def __handle_data_dump(self):
        with open("cache/index.pkl","wb") as index_file:
            pickle.dump(self.index,index_file)
        with open("cache/docmap.pkl","wb") as docmap_file:
            pickle.dump(self.docmap,docmap_file)

    def __init__(self):
        self.index = {}
        self.docmap = {}