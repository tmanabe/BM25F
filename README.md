# BM25F
A variant of BM25F in Python.

## Example
```python
#!/usr/bin/env python
# coding: utf-8

import BM25F.core
import BM25F.exp
import BM25F.ja

tokenizer = BM25F.ja.Tokenizer(stem_filter=BM25F.ja.StemFilter(),
                               pos_filter=BM25F.ja.PosFilter())

bj = BM25F.exp.bag_jag()

bd0 = BM25F.exp.bag_dict().read_japanese(tokenizer, {
    'title': 'テストデータ',
    'body': 'テスト',
    'anchor': 'モニタ',
})
bj.append(bd0)

bd1 = BM25F.exp.bag_dict().read_japanese(tokenizer, {
    'title': 'テストデータ',
    'body': 'テスト',
})
bj.append(bd1)

bd2 = BM25F.exp.bag_dict().read_japanese(tokenizer, {
    'body': 'テスト',
})
bj.append(bd2)

bd3 = BM25F.exp.bag_dict().read_japanese(tokenizer, {})
bj.append(bd3)

query = BM25F.exp.bag_of_words()
query['テスト'] = 1
query['モニタ'] = 1

boost = BM25F.core.param_dict(default=1.0)
boost['title'] = 100
boost['body'] = 0.1

k1 = 1.2

b = BM25F.core.param_dict(default=0.75)
b['title'] = 0.50
b['body'] = 1.00

print(BM25F.core.bm25f(query, bd0, bj, boost=boost, k1=k1, b=b))
```

## Requirement
- janome
