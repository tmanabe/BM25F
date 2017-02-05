from math import log


class param_dict(dict):
    def __new__(self, d={}, default=None):
        self = dict.__new__(self)
        self.update(d)
        self.default = default
        return self

    def __missing__(self, key):
        return self.default


def weight(word,  # intuitively is a query keyword
           bd,  # is a document
           bj,  # is a document collection
           boost=param_dict(default=1.0),  # field name -> boost
           b=param_dict(default=0.75)):  # field name -> length deboost
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
          boost=param_dict(default=1.0),
          k1=1.2,
          b=param_dict(default=0.75)):
    result = 0.0
    for (word, count) in bow.items():
        w = weight(word, bd, bj, boost, b)
        e = entropy(word, bj)
        result += count * w / (k1 + w) * e
    return result
