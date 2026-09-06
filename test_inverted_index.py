import unittest
import json
import os
import sys
from helpers import tokenize_term
from classes.inverted_index import InvertedIndex

class TestInvertedIndex(unittest.TestCase):
    docTestIndex = InvertedIndex()
    fullTestIndex = InvertedIndex()
    #loading instead of building to reduce iteration time
    fullTestIndex.load()
    #fullTestIndex.build()

    def test_add_document(self):
        self.docTestIndex._InvertedIndex__add_document(0,"The Grand Army of the Republic")
        expected = {"grand": [0], "armi": [0], "republ": [0]}
        result = json.loads(json.dumps(self.docTestIndex.index))
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

    def test_get_idf(self):
        expected1 = 5.52
        result1 = round(self.fullTestIndex.get_idf(tokenize_term("grizzly")), 2)
        expected2 = 3.29
        result2 = round(self.fullTestIndex.get_idf(tokenize_term("actor")), 2)
        expected3 = 0.76
        result3 = round(self.fullTestIndex.get_idf(tokenize_term("man")), 2)

        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)
    
    def test_get_tfidf(self):
        expected1 = 24.13
        result1 = round(self.fullTestIndex.get_tfidf(424, "trapper"), 2)
        expected2 = 2.14
        result2 = round(self.fullTestIndex.get_tfidf(424, "push"), 2)

        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_get_bm25_idf(self):
        expected1 = 5.55
        result1 = round(self.fullTestIndex.get_bm25_idf(tokenize_term("grizzly")), 2)
        expected2 = 3.29
        result2 = round(self.fullTestIndex.get_bm25_idf(tokenize_term("actor")), 2)
        expected3 = 0.95
        result3 = round(self.fullTestIndex.get_bm25_idf(tokenize_term("love")), 2)

        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)

    def test_get_bm25tf(self):
        expected1 = 2.35
        result1 = round(self.fullTestIndex.get_bm25_tf(1, tokenize_term("anbuselvan")), 2)
        expected2 = 2.24
        result2 = round(self.fullTestIndex.get_bm25_tf(1, tokenize_term("maya")), 2)
        expected3 = 2.09
        result3 = round(self.fullTestIndex.get_bm25_tf(1, tokenize_term("police")), 2)

        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)

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