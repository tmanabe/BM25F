class bag_of_words(dict):
    def __missing__(self, word):
        return 0

    def __init__(self):
        super().__init__(self)

    def __len__(self):
        return sum(self.values())

    def read(self, tokenizer, string):
        for (stem, pos) in tokenizer.tokenize_smartly(string):
            self[stem] += 1
        return self


class bag_dict(dict):
    def __missing__(self, field_name):
        self[field_name] = bag_of_words()
        return self[field_name]

    def read(self, tokenizer, d):
        for (field_name, string) in d.items():
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

    def append(self, bd):
        self.body.append(bd)
        for word in bd.reduce().keys():
            self.df[word] += 1
        for (field_name, bow) in bd.items():
            self.total_len[field_name] += len(bow)
        return self
