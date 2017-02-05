#!/usr/bin/env python
# coding: utf-8

from BM25F.en import Normalizer
from BM25F.en import TokenFilter
from BM25F.en import Tokenizer
import unittest


class TestEnglish(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.token_filter = TokenFilter()

    def test_normalzier(self):
        n = Normalizer()
        self.assertEqual('manabe', n.normalize('Manabes\''))
        self.assertEqual('tomohiro lib', n.normalize('Tomohiro\'s lib'))
        self.assertEqual('hot spot', n.normalize('hot-spot'))
        self.assertEqual('1947 32', n.normalize('1947-32'))
        self.assertEqual('camel case', n.normalize('CamelCase'))
        self.assertEqual('fem 3000 bot', n.normalize('Fem3000Bot'))
        self.assertEqual('abc', n.normalize('ABC'))

    def test_token_filter(self):
        self.assertTrue('and' in self.token_filter)
        self.assertFalse('test' in self.token_filter)

    def test_tokenizer(self):
        m = Tokenizer()
        self.assertEqual([
            ('test',),
            ('data',),
        ], m.tokenize_smartly(' testing data '))

    def test_tokenizer_with_stem_filter(self):
        m = Tokenizer(token_filter=self.token_filter)
        self.assertEqual([
            ('test',),
            ('data',),
        ], m.tokenize_smartly('test on data'))


if __name__ == '__main__':
    unittest.main()
