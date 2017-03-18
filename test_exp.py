#!/usr/bin/env python
# coding: utf-8

from BM25F.exp import bag_dict
from BM25F.exp import bag_jag
from BM25F.exp import bag_of_words
from BM25F.ja import Tokenizer
import unittest


class TestExp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tokenizer = Tokenizer()

    def test_bag_of_words(self):
        bow = bag_of_words()
        self.assertEqual(0, bow['unknown'])
        bow['test'] += 1
        self.assertEqual(1, bow['test'])
        bow['data'] = 10
        self.assertEqual(10, bow['data'])
        self.assertEqual(11, len(bow))

    def test_bag_of_words_from_string_in_japanese(self):
        bow = bag_of_words().read(self.tokenizer, 'テスト用のテストデータ')
        self.assertEqual(2, bow['テスト'])
        self.assertEqual(1, bow['用'])
        self.assertEqual(1, bow['の'])
        self.assertEqual(1, bow['データ'])

    def test_bag_dict(self):
        bd = bag_dict()
        self.assertEqual(bag_of_words(), bd['unknown'])

    def test_bag_dict_from_string_dict_in_japanese(self):
        bd = bag_dict().read(self.tokenizer, {
            'title': 'テスト',
            'body': 'データ',
        })
        bow_title = bag_of_words()
        bow_title['テスト'] = 1
        bow_body = bag_of_words()
        bow_body['データ'] = 1
        self.assertEqual(bow_title, bd['title'])
        self.assertEqual(bow_body, bd['body'])

    def test_bag_dict_from_string_dict_without_tokenizer(self):
        bd = bag_dict().read(self.tokenizer, {
            '_id': 'テスト用のデータ001',
            '~pv': 123.0,
        })
        bow = bag_of_words()
        bow['テスト用のデータ001'] = 1
        self.assertEqual(bow, bd['_id'])
        bow = bag_of_words()
        bow[123.0] = 1
        self.assertEqual(bow, bd['~pv'])

    def test_bag_dict_reduce(self):
        bd = bag_dict().read(self.tokenizer, {
            'title': 'テストデータ',
            'body': 'テスト',
            'anchor': 'データ',
        })
        bow = bag_of_words()
        bow['テスト'] = 2
        bow['データ'] = 2
        self.assertEqual(bow, bd.reduce())

    def test_bag_jag(self):
        bj = bag_jag()
        bd0 = bag_dict().read(self.tokenizer, {
            'title': 'テストデータ',
            'body': 'テスト',
            'anchor': 'モニタ',
        })
        bd1 = bag_dict().read(self.tokenizer, {
            'title': 'テストデータ',
            'body': 'テスト',
        })
        bd2 = bag_dict().read(self.tokenizer, {
            'body': 'テスト',
        })
        bd3 = bag_dict().read(self.tokenizer, {})
        bj.append(bd0).append(bd1).append(bd2).append(bd3)
        self.assertEqual(4, len(bj))
        self.assertEqual(3, bj.df['テスト'])
        self.assertEqual(2, bj.df['データ'])
        self.assertEqual(1, bj.df['モニタ'])
        self.assertEqual(0, bj.df['ダミー'])
        self.assertEqual(4, bj.total_len['title'])
        self.assertEqual(3, bj.total_len['body'])
        self.assertEqual(1, bj.total_len['anchor'])


if __name__ == '__main__':
    unittest.main()
