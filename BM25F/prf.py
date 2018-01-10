from BM25F.core import batch
from BM25F.core import bm25f
from BM25F.core import param_dict


class result(dict):
    def __new__(self, d={}):
        self = dict.__new__(self)
        self.update(d)
        return self

    def __missing__(self, key):
        return 0.0


def characterize(bd,  # this document
                 bj,  # in this document collection
                 boost=param_dict(default=batch.BOOST),
                 k1=batch.K1,
                 b=param_dict(default=batch.B)):
    words = set()
    for bow in bd.values():
        for w in bow.keys():
            words.add(w)
    r = result()
    for w in words:
        r[w] = bm25f({w: 1}, bd, bj, boost, k1, b)
    return r
