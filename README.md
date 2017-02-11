# BM25F
A variant of BM25F in Python.

## Requirements
- flake8 (for testing)
- janome (for BM25F.ja)
- stemming (for BM25F.en)

## Example
```python
#!/usr/bin/env python
# coding: utf-8

import BM25F.core
import BM25F.en
import BM25F.exp

tokenizer = BM25F.en.Tokenizer(token_filter=BM25F.en.TokenFilter())

bj = BM25F.exp.bag_jag()

bd0 = BM25F.exp.bag_dict().read(tokenizer, {
    'title': 'data-for-testing',
    'body': 'tests\'',
    'anchor': 'QUERIES',
})
bj.append(bd0)

bd1 = BM25F.exp.bag_dict().read(tokenizer, {
    'title': 'TestData\'s',
    'body': 'Do a test',
})
bj.append(bd1)

bd2 = BM25F.exp.bag_dict().read(tokenizer, {
    'body': 'Test.',
})
bj.append(bd2)

bd3 = BM25F.exp.bag_dict().read(tokenizer, {
    'title': 'example',
})
bj.append(bd3)

query = BM25F.exp.bag_of_words().read(tokenizer, 'query EXAMPLE')

boost = BM25F.core.param_dict(default=1.0)
boost['title'] = 100
boost['body'] = 0.1

k1 = 2.0

b = BM25F.core.param_dict(default=0.75)
b['title'] = 0.50
b['body'] = 1.00

scorer = BM25F.core.batch(query, bj, boost, k1, b)
print(scorer.top(2, [bd0, bd1, bd2, bd3]))
```

## 例
```python
#!/usr/bin/env python
# coding: utf-8

import BM25F.core
import BM25F.exp
import BM25F.ja

tokenizer = BM25F.ja.Tokenizer(stem_filter=BM25F.ja.StemFilter(),
                               pos_filter=BM25F.ja.PosFilter())

bj = BM25F.exp.bag_jag()

bd0 = BM25F.exp.bag_dict().read(tokenizer, {
    'title': 'テストのデータ',
    'body': 'テスト',
    'anchor': 'クエリー',
})
bj.append(bd0)

bd1 = BM25F.exp.bag_dict().read(tokenizer, {
    'title': 'ﾃｽﾄﾃﾞｰﾀ',
    'body': 'テストします',
})
bj.append(bd1)

bd2 = BM25F.exp.bag_dict().read(tokenizer, {
    'body': 'テスト。',
})
bj.append(bd2)

bd3 = BM25F.exp.bag_dict().read(tokenizer, {
    'title': '例',
})
bj.append(bd3)

query = BM25F.exp.bag_of_words().read(tokenizer, '例のクエリ')

boost = BM25F.core.param_dict(default=1.0)
boost['title'] = 100
boost['body'] = 0.1

k1 = 2.0

b = BM25F.core.param_dict(default=0.75)
b['title'] = 0.50
b['body'] = 1.00

scorer = BM25F.core.batch(query, bj, boost, k1, b)
print(scorer.top(2, [bd0, bd1, bd2, bd3]))
```
