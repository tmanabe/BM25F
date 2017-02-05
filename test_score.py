#!/usr/bin/env python
# coding: utf-8

from BM25F.core import bm25f
from BM25F.core import entropy
from BM25F.core import param_dict
from BM25F.core import weight
from BM25F.exp import bag_dict
from BM25F.exp import bag_jag
from BM25F.exp import bag_of_words
from BM25F.ja import Tokenizer
from math import log
import unittest


class TestScore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tokenizer = Tokenizer()
        cls.bj = bag_jag()
        cls.bd0 = bag_dict().read_japanese(tokenizer, {
            'title': 'テストデータ',
            'body': 'テスト',
            'anchor': 'モニタ',
        })
        cls.bj.append(cls.bd0)
        cls.bd1 = bag_dict().read_japanese(tokenizer, {
            'title': 'テストデータ',
            'body': 'テスト',
        })
        cls.bj.append(cls.bd1)
        cls.bd2 = bag_dict().read_japanese(tokenizer, {
            'body': 'テスト',
        })
        cls.bj.append(cls.bd2)
        cls.bd3 = bag_dict().read_japanese(tokenizer, {})
        cls.bj.append(cls.bd3)

    def test_weight(self):
        self.assertEqual(
            (1 * 1.0) / ((1 - 0.75) + 0.75 * 2 / (4 / 4)) +
            (1 * 1.0) / ((1 - 0.75) + 0.75 * 1 / (3 / 4)) +
            (0 * 1.0) / ((1 - 0.75) + 0.75 * 1 / (1 / 4)),
            # ~ 1.3714285714285714
            weight('テスト', self.bd0, self.bj))
        self.assertEqual(
            (0 * 1.0) / ((1 - 0.75) + 0.75 * 2 / (4 / 4)) +
            (0 * 1.0) / ((1 - 0.75) + 0.75 * 1 / (3 / 4)) +
            (1 * 1.0) / ((1 - 0.75) + 0.75 * 1 / (1 / 4)),
            # ~ 0.3076923076923077
            weight('モニタ', self.bd0, self.bj))

    def test_boost(self):
        boost = param_dict(default=1.0)
        boost['title'] = 100
        boost['body'] = 0.1
        self.assertEqual(
            (1 * 100) / ((1 - 0.75) + 0.75 * 2 / (4 / 4)) +
            (1 * 0.1) / ((1 - 0.75) + 0.75 * 1 / (3 / 4)) +
            (0 * 1.0) / ((1 - 0.75) + 0.75 * 1 / (1 / 4)),
            weight('テスト', self.bd0, self.bj, boost=boost))

    def test_b(self):
        b = param_dict(default=0.75)
        b['title'] = 0.50
        b['body'] = 1.00
        self.assertEqual(
            (1 * 1.0) / ((1 - 0.50) + 0.50 * 2 / (4 / 4)) +
            (1 * 1.0) / ((1 - 1.00) + 1.00 * 1 / (3 / 4)) +
            (0 * 1.0) / ((1 - 0.75) + 0.75 * 1 / (1 / 4)),
            weight('テスト', self.bd0, self.bj, b=b))

    def test_entropy(self):
        self.assertEqual(
            log((4 - 3 + 0.5) / (3 + 0.5)),
            # ~ -0.8472978603872037
            entropy('テスト', self.bj))
        self.assertEqual(
            log((4 - 1 + 0.5) / (1 + 0.5)),
            # ~ 0.8472978603872037
            entropy('モニタ', self.bj))

    def test_bm25f(self):
        query = bag_of_words()
        query['テスト'] = 1
        query['モニタ'] = 1
        self.assertAlmostEqual(
            1.37142857142857 / (1.2 + 1.37142857142857) * -0.84729786038720 +
            0.30769230769230 / (1.2 + 0.30769230769230) * 0.84729786038720,
            bm25f(query, self.bd0, self.bj))

    def test_k1(self):
        query = bag_of_words()
        query['テスト'] = 1
        query['モニタ'] = 1
        self.assertAlmostEqual(
            1.37142857142857 / (2.0 + 1.37142857142857) * -0.84729786038720 +
            0.30769230769230 / (2.0 + 0.30769230769230) * 0.84729786038720,
            bm25f(query, self.bd0, self.bj, k1=2.0))


if __name__ == '__main__':
    unittest.main()
