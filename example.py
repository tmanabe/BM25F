#!/usr/bin/env python
# coding: utf-8

import BM25F

tokenizer = BM25F.Tokenizer(stem_filter=BM25F.StemFilter(),
                            pos_filter=BM25F.PosFilter())

bj = BM25F.bag_jag()

bd0 = BM25F.bag_dict().read_japanese(tokenizer, {
    'title': 'テストデータ',
    'body': 'テスト',
    'anchor': 'モニタ',
})
bj.append(bd0)

bd1 = BM25F.bag_dict().read_japanese(tokenizer, {
    'title': 'テストデータ',
    'body': 'テスト',
})
bj.append(bd1)

bd2 = BM25F.bag_dict().read_japanese(tokenizer, {
    'body': 'テスト',
})
bj.append(bd2)

bd3 = BM25F.bag_dict().read_japanese(tokenizer, {})
bj.append(bd3)

query = BM25F.bag_of_words()
query['テスト'] = 1
query['モニタ'] = 1

boost = BM25F.param_dict(default=1.0)
boost['title'] = 100
boost['body'] = 0.1

k1 = 1.2

b = BM25F.param_dict(default=0.75)
b['title'] = 0.50
b['body'] = 1.00

print(BM25F.bm25f(query, bd0, bj, boost=boost, k1=k1, b=b))
