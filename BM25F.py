from os import linesep
from subprocess import PIPE
from subprocess import Popen
import urllib.request


class BM25F(object):
    pass


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


class mecab(object):
    def __init__(self,
                 binary,
                 stem_filter=set(),
                 pos_filter=set()):
        self.mecab = Popen([
                               binary,
                               '--node-format=%H\n',
                               '--eos-format=',
                           ],
                           stdin=PIPE,
                           stdout=PIPE)
        self.stem_filter = stem_filter
        self.pos_filter = pos_filter

    def parse(self, string):
        string = string.replace(linesep, ' ')
        self.mecab.stdin.write(string.encode('utf-8'))
        self.mecab.stdin.write(linesep.encode('utf-8'))
        out, err = self.mecab.communicate()
        assert None == err
        lines = out.decode('utf-8').split(linesep)
        assert '' == lines.pop()
        result = []
        for line in lines:
            l = line.split(',', 7)
            pos, stem = l[0:4], l[6]
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

    def read_japanese(self, string):
        pass


class bag_dict(dict):
    pass


class bag_jag(list):
    pass


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
