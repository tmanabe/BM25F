#!/usr/bin/env python
# coding: utf-8

from BM25F import Normalizer
from BM25F import param_dict
from BM25F import PosFilter
from BM25F import StemFilter
from BM25F import Tokenizer
from os import system
import unittest


class TestMisc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stem_filter = StemFilter()
        cls.pos_filter = PosFilter()

    def test_example(self):
        self.assertEqual(0, system('python example.py'))

    def test_readme_includes_example(self):
        with open('README.md', encoding='utf-8') as f:
            readme = f.read()
        with open('example.py', encoding='utf-8') as f:
            example = f.read()
        self.assertTrue(example in readme)

    def test_normalzier(self):
        n = Normalizer()
        self.assertEqual('abc', n.normalize('ＡＢＣ'))
        self.assertEqual('カラー', n.normalize('カラー'))
        self.assertEqual('モニタ', n.normalize('モニター'))
        self.assertEqual('モニター', n.normalize('モニターー'))
        self.assertEqual('モニタの', n.normalize('モニターの'))
        self.assertEqual('イーメール', n.normalize('イーメール'))

    def test_stem_filter(self):
        self.assertTrue('ある' in self.stem_filter)
        self.assertFalse('テスト' in self.stem_filter)

    def test_pos_filter(self):
        self.assertTrue('助詞-格助詞-一般' in self.pos_filter)
        self.assertFalse('名詞-一般' in self.pos_filter)

    def test_tokenizer(self):
        m = Tokenizer()
        self.assertEqual([
            ('テスト', '名詞-サ変接続'),
            ('データ', '名詞-一般'),
        ], m.tokenize_smartly('テストデータ'))

    def test_tokenizer_with_stem_filter(self):
        m = Tokenizer(stem_filter=self.stem_filter)
        self.assertEqual([
            ('テスト', '名詞-サ変接続'),
            ('データ', '名詞-一般'),
        ], m.tokenize_smartly('その他テストデータ'))

    def test_tokenizer_with_pos_filter(self):
        m = Tokenizer(pos_filter=self.pos_filter)
        self.assertEqual([
            ('テスト', '名詞-サ変接続'),
            ('データ', '名詞-一般'),
        ], m.tokenize_smartly('テストのデータ'))

    def test_param_dict(self):
        d = {'title': 10}
        pd = param_dict(d=d, default=1)
        self.assertEqual(10, pd['title'])
        self.assertEqual(1, pd['body'])

    def test_param_dict_omit_d(self):
        pd = param_dict(default=1)
        self.assertEqual(1, pd['title'])
        self.assertEqual(1, pd['body'])

    def test_param_dict_omit_default(self):
        d = {'title': 10}
        pd = param_dict(d=d)
        self.assertEqual(10, pd['title'])
        self.assertEqual(None, pd['body'])


if __name__ == '__main__':
    unittest.main()
