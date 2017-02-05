from BM25F.ja import _Filter
from re import split
from re import sub
from stemming.porter2 import stem


class Normalizer(object):
    def alphanumer(self, string):
        string = sub(r'([a-zA-Z])([0-9])', r'\1 \2', string)
        return sub(r'([0-9])([a-zA-Z])', r'\1 \2', string)

    def camelcase(self, string):
        return sub(r'([a-z])([A-Z])', r'\1 \2', string)

    def delimiter(self, string):
        return sub(r'\W', r' ', string)

    def lower(self, string):
        return string.lower()

    def normalize(self, string):
        string = self.posessive(string)
        string = self.alphanumer(self.camelcase(self.delimiter(string)))
        return self.lower(string)

    def posessive(self, string):
        string = sub(r'\'s(\W|$)', r'\1', string)
        return sub(r's\'(\W|$)', r'\1', string)


class TokenFilter(_Filter):
    URL = 'https://raw.githubusercontent.com' \
          '/apache/lucene-solr/master' \
          '/solr/example/files/conf/lang/stopwords_en.txt'


class Tokenizer(object):
    def __init__(self,
                 token_filter=set()):
        super().__init__()
        self.normalizer = Normalizer()
        self.token_filter = token_filter

    def tokenize_smartly(self, string):
        string = self.normalizer.normalize(string)
        result = []
        for token in split(r'\s', string):
            if token == '' or token in self.token_filter:
                continue
            result.append((stem(token),))
        return result
