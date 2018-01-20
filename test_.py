#!/usr/bin/env python
# coding: utf-8

from BM25F.core import param_dict
from BM25F.prf import prf_result
from os import system
import unittest


class TestMisc(unittest.TestCase):
    def test_example_en(self):
        self.assertEqual(0, system('python example_en.py'))

    def test_example_ja(self):
        self.assertEqual(0, system('python example_ja.py'))

    def test_readme_includes_example_en(self):
        with open('README.md', encoding='utf-8') as f:
            readme = f.read()
        with open('example_en.py', encoding='utf-8') as f:
            example = f.read()
        self.assertTrue(example in readme)

    def test_readme_includes_example_ja(self):
        with open('README.md', encoding='utf-8') as f:
            readme = f.read()
        with open('example_ja.py', encoding='utf-8') as f:
            example = f.read()
        self.assertTrue(example in readme)

    def test_flake8(self):
        self.assertEqual(0, system('flake8'))

    def test_param_dict(self):
        pd = param_dict(d={'title': 10}, default=1)
        self.assertEqual(10, pd['title'])
        self.assertEqual(1, pd['body'])

    def test_param_dict_omit_d(self):
        pd = param_dict(default=1)
        self.assertEqual(1, pd['title'])
        self.assertEqual(1, pd['body'])

    def test_param_dict_omit_default(self):
        pd = param_dict({'title': 10})
        self.assertEqual(10, pd['title'])
        self.assertEqual(None, pd['body'])

    def test_prf_result(self):
        pr = prf_result({'keyword': 1.23})
        self.assertEqual(1.23, pr['keyword'])
        self.assertEqual(0.0, pr['word'])

    def test_prf_result_iadd(self):
        pr = prf_result({'keyword': 1.23})
        pr += pr
        self.assertEqual(2.46, pr['keyword'])

    def test_prf_result_isub(self):
        pr = prf_result({'keyword': 1.23})
        pr -= pr
        self.assertEqual(0.0, pr['keyword'])

    def test_prf_result_imul(self):
        pr = prf_result({'keyword': 1.23})
        pr *= 2.0
        self.assertEqual(2.46, pr['keyword'])
        pr *= 0.25
        self.assertEqual(0.615, pr['keyword'])

    def test_prf_result_sort(self):
        pr = prf_result({'keyword': 1.23, 'key': 2.34, 'word': 0.0})
        self.assertEqual(['key', 'keyword', 'word'], pr.sort())


if __name__ == '__main__':
    unittest.main()
