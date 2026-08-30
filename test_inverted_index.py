import unittest
import json
import os
import sys
from classes.inverted_index import InvertedIndex

class TestInvertedIndex(unittest.TestCase):
    #movies = load_movies()
    docTestIndex = InvertedIndex()
    fullTestIndex = InvertedIndex()
    fullTestIndex.build()

    def test_add_document(self):
        self.docTestIndex._InvertedIndex__add_document(0,"The Grand Army of the Republic")
        expected = '{"grand": [0], "armi": [0], "republ": [0]}'
        result = json.dumps(self.docTestIndex.index)
        self.assertEqual(result, expected)

    def test_get_documents(self):
        self.docTestIndex._InvertedIndex__add_document(-1,"The Grand Army of the Republic")
        expected = [-1,0]
        result = self.docTestIndex.get_documents("grand")
        self.assertEqual(result, expected)

    def test_get_tf(self):
        expected1 = 1
        result1 = self.fullTestIndex.get_tf(424, "bear")
        expected2 = 4
        result2 = self.fullTestIndex.get_tf(424, "trapper")

        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)


    #@unittest.skip("takes 25 seconds , reducing iteration time while developing")
    def test_build(self):
        expected = 4651
        result = self.fullTestIndex.get_documents("merida")[0]
        self.assertEqual(result, expected)

    #@unittest.skip("takes 25 seconds , reducing iteration time while developing")
    def test_save_and_load(self):
        self.fullTestIndex.save()
        self.assertTrue(os.path.isfile("cache/index.pkl"))
        self.assertTrue(os.path.isfile("cache/docmap.pkl"))

        self.fullTestIndex.index = {}
        self.fullTestIndex.docmap = {}
        self.fullTestIndex.load()

        expected = 3439
        result = self.fullTestIndex.get_documents("karnstein")[0]
        self.assertEqual(result, expected)        