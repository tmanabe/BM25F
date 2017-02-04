#!/usr/bin/env python
# coding: utf-8

from BM25F import stem_filter
from BM25F import pos_filter
from BM25F import mecab
from BM25F import param_dict
import unittest


class TestRange(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.stem_filter = stem_filter()
        cls.pos_filter = pos_filter()

    def test_stem_filter(self):
        self.assertTrue('ある' in self.stem_filter)
        self.assertFalse('テスト' in self.stem_filter)

    def test_pos_filter(self):
        self.assertTrue('助詞-格助詞-一般' in self.pos_filter)
        self.assertFalse('名詞-一般' in self.pos_filter)

    def test_mecab(self):
        m = mecab(r'C:\Program Files (x86)\MeCab\bin\mecab.exe')
        self.assertEqual([
            ('テスト', '名詞-サ変接続'),
            ('データ', '名詞-一般'),
        ], m.parse('テストデータ'))

    def test_mecab_with_stem_filter(self):
        m = mecab(r'C:\Program Files (x86)\MeCab\bin\mecab.exe',
                  stem_filter=self.stem_filter)
        self.assertEqual([
            ('テスト', '名詞-サ変接続'),
            ('データ', '名詞-一般'),
        ], m.parse('その他テストデータ'))

    def test_mecab_with_pos_filter(self):
        m = mecab(r'C:\Program Files (x86)\MeCab\bin\mecab.exe',
                  pos_filter=self.pos_filter)
        self.assertEqual([
            ('テスト', '名詞-サ変接続'),
            ('データ', '名詞-一般'),
        ], m.parse('テストのデータ'))

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
