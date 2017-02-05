#!/usr/bin/env python
# coding: utf-8

from BM25F.core import param_dict
from os import system
import unittest


class TestMisc(unittest.TestCase):
    def test_example_ja(self):
        self.assertEqual(0, system('python example_ja.py'))

    def test_readme_includes_example_ja(self):
        with open('README.md', encoding='utf-8') as f:
            readme = f.read()
        with open('example_ja.py', encoding='utf-8') as f:
            example = f.read()
        self.assertTrue(example in readme)

    def test_flake8(self):
        self.assertEqual(0, system('flake8'))

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
