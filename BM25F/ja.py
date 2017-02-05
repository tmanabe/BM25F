from janome.tokenizer import Tokenizer as OriginalTokenizer
from re import sub
import unicodedata
import urllib.request


class Normalizer(object):
    def katakana(self, string):
        return sub(
            r'([ァ-タダ-ヶー]{3})ー([^ァ-タダ-ヶー]|$)',
            r'\1\2',
            string)

    def lower(self, string):
        return string.lower()

    def nfkc(self, string):
        return unicodedata.normalize('NFKC', string)

    def normalize(self, string):
        return self.lower(self.katakana(self.nfkc(string)))


class _Filter(set):
    def __init__(self):
        path, _ = urllib.request.urlretrieve(self.URL)
        with open(path, encoding='utf-8') as f:
            for l in f:
                if l[0] in ('\n', '#'):
                    continue
                self.add(l.rstrip())


class StemFilter(_Filter):
    URL = 'https://raw.githubusercontent.com' \
          '/apache/lucene-solr/master' \
          '/solr/example/files/conf/lang/stopwords_ja.txt'


class PosFilter(_Filter):
    URL = 'https://raw.githubusercontent.com' \
          '/apache/lucene-solr/master' \
          '/solr/example/files/conf/lang/stoptags_ja.txt'


class Tokenizer(OriginalTokenizer):
    def __init__(self,
                 stem_filter=set(),
                 pos_filter=set()):
        super().__init__()
        self.normalizer = Normalizer()
        self.stem_filter = stem_filter
        self.pos_filter = pos_filter

    def tokenize_smartly(self, string):
        string = self.normalizer.normalize(string)
        result = []
        for token in self.tokenize(string):
            pos, stem = token.part_of_speech.split(','), token.base_form
            if stem == '*':
                stem = token.surface
            if stem in self.stem_filter:
                continue
            while pos[-1] == '*':
                pos.pop()
            pos = '-'.join(pos)
            if pos in self.pos_filter:
                continue
            result.append((stem, pos))
        return result
