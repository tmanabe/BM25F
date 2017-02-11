import heapq
from math import log


class param_dict(dict):
    def __new__(self, d={}, default=None):
        self = dict.__new__(self)
        self.update(d)
        self._default = default
        return self

    def __missing__(self, key):
        return self._default


class batch(object):  # For batch scoring
    BOOST = 1.0
    K1 = 1.2
    B = 0.75

    def __init__(self,
                 id,
                 bow,
                 bj,
                 boost=param_dict(default=BOOST),
                 k1=K1,
                 b=param_dict(default=B)):
        self.id = id
        self.bow = bow
        self.bj = bj
        self.boost = boost
        self.k1 = k1
        self.b = b
        self.entropy_cache = {}
        for word in bow:
            self.entropy_cache[word] = entropy(word, self.bj)

    def bm25f(self, bd):
        result = 0.0
        for (word, count) in self.bow.items():
            w = weight(word, bd, self.bj, self.boost, self.b)
            e = self.entropy_cache[word]
            result += count * w / (self.k1 + w) * e
        return result

    def top(self, k, bds):
        q = []
        for i, bd in enumerate(bds):
            assert 1 == len(bd[self.id])
            id = list(bd[self.id].keys())[0]
            trpl = (self.bm25f(bd), i, id)
            if len(q) < k:
                heapq.heappush(q, trpl)
            else:
                heapq.heappushpop(q, trpl)
        q.sort()
        q.reverse()
        return [trpl[-1] for trpl in q]


def weight(word,  # intuitively is a query keyword
           bd,  # is a document
           bj,  # is a document collection
           boost=param_dict(default=batch.BOOST),  # field name -> boost
           b=param_dict(default=batch.B)):  # field name -> length deboost
    result = 0.0
    for (fn, bow) in bd.items():
        numer = bow[word] * boost[fn]
        denom = 1 - b[fn]
        denom += b[fn] * len(bow) / (bj.total_len[fn] / len(bj))
        result += numer / denom
    return result


def entropy(word, bj):
    numer = len(bj) - bj.df[word] + 0.5
    denom = bj.df[word] + 0.5
    return log(numer / denom)


def bm25f(bow,  # is a query
          bd,
          bj,
          boost=param_dict(default=batch.BOOST),
          k1=batch.K1,
          b=param_dict(default=batch.B)):
    dummy = list(bd.keys())[0]
    return batch(dummy, bow, bj, boost, k1, b).bm25f(bd)
