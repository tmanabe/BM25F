from janome.tokenizer import Tokenizer as OriginalTokenizer
import re
import unicodedata
import urllib.request


class normalizer(object):
    def katakana(self, string):
        return re.sub(
            r'([ァ-タダ-ヶー]{3})ー([^ァ-タダ-ヶー]|$)',
            r'\1\2',
            string)

    def lower(self, string):
        return string.lower()

    def nfkc(self, string):
        return unicodedata.normalize('NFKC', string)

    def normalize(self, string):
        return self.lower(self.katakana(self.nfkc(string)))


class _filter(set):
    def __init__(self):
        path, _ = urllib.request.urlretrieve(self.URL)
        with open(path, encoding='utf-8') as f:
            for l in f:
                if l[0] in ('\n', '#'):
                    continue
                self.add(l.rstrip())


class stem_filter(_filter):
    URL = 'https://raw.githubusercontent.com' \
          '/apache/lucene-solr/master' \
          '/solr/example/files/conf/lang/stopwords_ja.txt'


class pos_filter(_filter):
    URL = 'https://raw.githubusercontent.com' \
          '/apache/lucene-solr/master' \
          '/solr/example/files/conf/lang/stoptags_ja.txt'


class Tokenizer(OriginalTokenizer):
    def __init__(self,
                 stem_filter=set(),
                 pos_filter=set()):
        super().__init__()
        self.normalizer = normalizer()
        self.stem_filter = stem_filter
        self.pos_filter = pos_filter

    def tokenize_smartly(self, string):
        string = self.normalizer.normalize(string)
        # string = string.replace(linesep, ' ')
        result = []
        for line in self.tokenize(string):
            pos, stem = line.part_of_speech.split(','), line.base_form
            if stem in self.stem_filter:
                continue
            while pos[-1] == '*':
                pos.pop()
            pos = '-'.join(pos)
            if pos in self.pos_filter:
                continue
            result.append((stem, pos))
        return result


class param_dict(dict):
    def __new__(self, d={}, default=None):
        self = dict.__new__(self)
        self.update(d)
        self.default = default
        return self

    def __missing__(self, key):
        return self.default


class bag_of_words(dict):
    def __missing__(self, word):
        return 0

    def __init__(self):
        super().__init__(self)

    def __len__(self):
        return sum(self.values())

    def read_japanese(self, tokenizer, string):
        for (stem, pos) in tokenizer.tokenize_smartly(string):
            self[stem] += 1
        return self


class bag_dict(dict):
    def __missing__(self, field_name):
        self[field_name] = bag_of_words()
        return self[field_name]

    def read_japanese(self, tokenizer, d):
        for (field_name, string) in d.items():
            self[field_name].read_japanese(tokenizer, string)
        return self

    def reduce(self):
        result = bag_of_words()
        for bow in self.values():
            for (word, count) in bow.items():
                result[word] += count
        return result


class bag_jag(object):
    def __init__(self, l=[]):
        self.body = [] + l
        self.df = bag_of_words()

    def __len__(self):
        return len(self.body)

    def append(self, bd):
        self.body.append(bd)
        for word in bd.reduce().keys():
            self.df[word] += 1
        return self


def entropy(w,  # intuitively is a query keyword
            bj):  # is a document collection
    return 0.0


def weight(w,
           bd,  # is a document
           bj,
           boost=param_dict(default=1.0),  # field name -> boost
           b=param_dict(default=0.75)):  # field name -> length deboost
    return 0.0


def bm25f(bow,  # is a query
          bd,
          bj,
          boost=param_dict(default=1.0),
          k1=1.2,
          b=param_dict(default=0.75)):
    return 0.0
