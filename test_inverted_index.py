import unittest
import json
import os
import sys
from classes.inverted_index import InvertedIndex

class TestInvertedIndex(unittest.TestCase):
    #movies = load_movies()
    searchIndex = InvertedIndex()

    def test_add_document(self):
        self.searchIndex._InvertedIndex__add_document(0,"The Grand Army of the Republic")
        expected = '{"grand": [0], "armi": [0], "republ": [0]}'
        result = json.dumps(self.searchIndex.index)
        self.assertEqual(result, expected)

    def test_get_documents(self):
        self.searchIndex._InvertedIndex__add_document(-1,"The Grand Army of the Republic")
        expected = [-1,0]
        result = self.searchIndex.get_documents("grand")
        self.assertEqual(result, expected)

    #@unittest.skip("takes 25 seconds , reducing iteration time while developing")
    def test_build(self):
        builtIndex = InvertedIndex()
        builtIndex.build()
        expected = 4651
        result = builtIndex.get_documents("merida")[0]
        self.assertEqual(result, expected)

    def test_save_and_load(self):
        self.searchIndex.build()
        self.searchIndex.save()
        self.assertTrue(os.path.isfile("cache/index.pkl"))
        self.assertTrue(os.path.isfile("cache/docmap.pkl"))

        self.searchIndex.index = {}
        self.searchIndex.docmap = {}
        self.searchIndex.load()

        expected = 3439
        result = self.searchIndex.get_documents("karnstein")[0]
        self.assertEqual(result, expected)        