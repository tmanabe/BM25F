import json


class bag_of_words(dict):
    def __missing__(self, word):
        return 0

    def __len__(self):
        return sum(self.values())

    def __iadd__(self, d):
        for word, count in d.items():
            self[word] += count
        return self

    def read(self, tokenizer, string):
        for tpl in tokenizer.tokenize_smartly(string):
            self[tpl[0]] += 1
        return self


class bag_dict(dict):
    def __missing__(self, field_name):
        self[field_name] = bag_of_words()
        return self[field_name]

    def __iadd__(self, d):
        for fn, bow in d.items():
            if fn[0] == '~':  # Continuous
                assert 1 == len(bow)
                k = list(bow.keys())[0]
                bow = {float(k): bow[k]}
            self[fn] += bow
        return self

    def read(self, tokenizer, d):
        for (field_name, string) in d.items():
            if field_name[0] in ('_', '~'):  # Protect from tokenizer
                self[field_name][string] += 1
            else:
                self[field_name].read(tokenizer, string)
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
        self.total_len = bag_of_words()

    def __len__(self):
        return len(self.body)

    def __iadd__(self, other):
        self.body += other.body
        self.df += other.df
        self.total_len += other.total_len
        return self

    def append(self, bd):
        self.body.append(bd)
        for word in bd.reduce().keys():
            if isinstance(word, str):
                self.df[word] += 1
        for (field_name, bow) in bd.items():
            self.total_len[field_name] += len(bow)
        return self

    def read(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            self.df += json.loads(f.readline())
            self.total_len += json.loads(f.readline())
            for l in f.readlines():
                bd = bag_dict()
                bd += json.loads(l)
                self.body.append(bd)
        return self

    def write(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.df, ensure_ascii=False))
            f.write('\n')
            f.write(json.dumps(self.total_len, ensure_ascii=False))
            f.write('\n')
            for bd in self.body:
                f.write(json.dumps(bd, ensure_ascii=False))
                f.write('\n')
        return self
