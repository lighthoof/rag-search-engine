import unittest
from helpers import load_movies
from cli.lib.keyword_search import search_command

class TestSearch(unittest.TestCase):
    movies = load_movies
    limit = 5

    def __get_titles(self, movies):
        return [movie.get("title") for movie in movies if "title" in movie]

    def test_keyword(self):
        query = "Great"

        found = search_command(query, self.limit)
        result = self.__get_titles(found)
        self.assertIn("The Land Before Time II: The Great Valley Adventure", result)
        self.assertIn("The First Great Train Robbery", result)

    def test_processed(self):
        query = "country"

        found = search_command(query, self.limit)
        result = self.__get_titles(found)
        self.assertIn("No Country for Old Men", result)
        self.assertIn("The Wonderful Country", result)
        self.assertIn("The Country Bears", result)

    def test_punctuation(self):
        query = "magic charlie"

        found = search_command(query, 10)
        result = self.__get_titles(found)
        self.assertIn("It's Magic, Charlie Brown", result)

    def test_tokenization(self):
        query = "furious fast"

        found = search_command(query, self.limit)
        result = self.__get_titles(found)
        self.assertIn("Furious Seven", result)
        self.assertIn("Fast and Furious", result)
        self.assertIn("Faster, Pussycat! Kill! Kill!", result)

    def test_stop_words(self):
        query = "the hot shot"

        found = search_command(query, self.limit)
        result = self.__get_titles(found)
        self.assertIn("Hot Potato", result)
        self.assertIn("Hotel Chevalier", result)
        self.assertIn("Killshot", result)

    def test_stemming(self):
        query = "running"

        found = search_command(query, self.limit)
        result = self.__get_titles(found)
        self.assertIn("Virginia's Run", result)
        self.assertIn("Take the Money and Run", result)
        self.assertIn("Woman on the Run", result)