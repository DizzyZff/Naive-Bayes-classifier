from learn import *


class Test():
    def __init__(self, filename, split):
        self.filename = filename
        self.split = split
        self.train = TrainData(filename, split)
        self.train_data = self.train.data
        self.test_data = self.train.test_data
        self.words =[]
        self.log_cat_bio = {}

    def normalize(self):
        for data in self.train_data:
            for d in data:
                d = d.lower()
        for data in self.test_data:
            for d in data:
                d = d.lower()
                for word in d.split():
                    word = word.strip('.,!?;:')
                    print(word)
                    if word in self.train.words:
                        self.words.append(word)

    def get_log_cat_bio(self):
        for bio in self.test_data:
            self.log_cat_bio[bio] = {}
            for cat in self.train.catagories:
            # L(C | B) = L(C) + ∑ W ∈ B L(W | C)
                self.log_cat_bio[bio][cat] = self.train.log_cat_bio[cat]
                for word in self.words:
                    self.log_cat_bio[bio][cat] += self.train.log_word_cat_bio[word][cat]
        print(self.log_cat_bio)
        return self.log_cat_bio

    def prediction(self):
        self.get_log_cat_bio()
        for data in self.test_data:
            for d in data:
                d = d.lower()
                for word in d.split():
                    word = word.strip('.,!?;:')
                    if word in self.train.words:
                        self.words.append(word)
        print(self.words)
        return self.words
