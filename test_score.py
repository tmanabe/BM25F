#!/usr/bin/env python
# coding: utf-8

from BM25F.core import batch
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
        cls.bd0 = bag_dict().read(tokenizer, {
            '_id': '0',
            'title': 'テストデータ',
            'body': 'テスト',
            'anchor': 'モニタ',
        })
        cls.bj.append(cls.bd0)
        cls.bd1 = bag_dict().read(tokenizer, {
            '_id': '1',
            'title': 'テストデータ',
            'body': 'テスト',
        })
        cls.bj.append(cls.bd1)
        cls.bd2 = bag_dict().read(tokenizer, {
            '_id': '2',
            'body': 'テスト',
        })
        cls.bj.append(cls.bd2)
        cls.bd3 = bag_dict().read(tokenizer, {
            '_id': '3',
        })
        cls.bj.append(cls.bd3)
        cls.query = bag_of_words()
        cls.query['テスト'] = 1
        cls.query['モニタ'] = 1

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

    def test_weight_continuous(self):
        tokenizer = Tokenizer()
        bj = bag_jag()
        bd0 = bag_dict().read(tokenizer, {'~pv': 1})
        bj.append(bd0)
        bd1 = bag_dict().read(tokenizer, {'~pv': 10})
        bj.append(bd1)
        bd2 = bag_dict().read(tokenizer, {'~pv': 100})
        bj.append(bd2)
        self.assertEqual((1 * 1.0), weight('ダミー', bd0, bj))
        self.assertEqual((10 * 1.0), weight('ダミー', bd1, bj))
        self.assertEqual((100 * 1.0), weight('ダミー', bd2, bj))

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

    def test_entropy_cache(self):
        obj = batch('_id', self.query, self.bj)
        self.assertEqual(
            log((4 - 3 + 0.5) / (3 + 0.5)),
            obj.entropy_cache['テスト'])
        self.assertEqual(
            log((4 - 1 + 0.5) / (1 + 0.5)),
            obj.entropy_cache['モニタ'])

    def test_bm25f(self):
        self.assertAlmostEqual(
            1.37142857142857 / (1.2 + 1.37142857142857) * -0.84729786038720 +
            0.30769230769230 / (1.2 + 0.30769230769230) * 0.84729786038720,
            bm25f(self.query, self.bd0, self.bj))

    def test_bm25f_batch(self):
        obj = batch('_id', self.query, self.bj)
        bds = [self.bd0, self.bd1, self.bd2, self.bd3]
        expected1 = ['3']
        self.assertEqual(expected1, obj.top(1, bds))
        expected3 = ['3', '0', '2']
        self.assertEqual(expected3, obj.top(3, bds))
        expected5 = ['3', '0', '2', '1']
        self.assertEqual(expected5, obj.top(5, bds))

    def test_k1(self):
        self.assertAlmostEqual(
            1.37142857142857 / (2.0 + 1.37142857142857) * -0.84729786038720 +
            0.30769230769230 / (2.0 + 0.30769230769230) * 0.84729786038720,
            bm25f(self.query, self.bd0, self.bj, k1=2.0))


if __name__ == '__main__':
    unittest.main()
