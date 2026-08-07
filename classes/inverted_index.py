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
        pass

    def __handle_data_dump(self):
        pass

    def __init__(self):
        self.index = {}
        self.docmap = {}