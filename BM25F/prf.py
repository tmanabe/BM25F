from BM25F.core import batch
from BM25F.core import bm25f
from BM25F.core import param_dict


class prf_result(dict):
    def __new__(self, d={}):
        self = dict.__new__(self)
        self.update(d)
        return self

    def __missing__(self, key):
        return 0.0

    def __iadd__(self, other):
        for word, score in other.items():
            if word in self:
                self[word] += score
            else:
                self[word] = score
        return self

    def __isub__(self, other):
        for word, score in other.items():
            if word in self:
                self[word] -= score
            else:
                self[word] = -score
        return self

    def __imul__(self, multi):
        for word in self:
            self[word] *= multi
        return self

    def sort(self):
        return sorted(self.keys(), key=lambda w: -self[w])


def characterize(bd,  # this document
                 bj,  # in this document collection
                 boost=param_dict(default=batch.BOOST),
                 k1=batch.K1,
                 b=param_dict(default=batch.B)):
    words = set()
    for bow in bd.values():
        for w in bow.keys():
            words.add(w)
    pr = prf_result()
    for w in words:
        pr[w] = bm25f({w: 1}, bd, bj, boost, k1, b)
    return pr
