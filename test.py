from learn import *


class Test():
    def __init__(self, filename, split):
        self.filename = filename
        self.split = split
        self.train = TrainData(filename, split)
        self.train_data = self.train.data
        self.test_data = self.train.test_data
        self.words = []
        self.log_cat_bio = {}
        self.pred = {}
        self.normalize()
        self.get_log_cat_bio()
        self.prediction()

    def normalize(self):
        for data in self.train_data:
            for d in data:
                d = d.lower()
        for data in self.test_data:
            for d in data:
                d = d.lower()
                #strip punctuation
                d = d.translate(str.maketrans('', '', string.punctuation))
                for word in d.split():
                    if word not in self.words and word in self.train.words:
                        self.words.append(word)

    def get_log_cat_bio(self):
        for bio in self.test_data:
            self.log_cat_bio[bio[0]] = {}
            for cat in self.train.categories:
                self.log_cat_bio[bio[0]][cat] = self.train.log_cat[cat]
                for word in self.words:
                    if word in bio[0].split() or word in bio[2].split():
                        self.log_cat_bio[bio[0]][cat] += self.train.log_word_in_cat[cat][word]
        return self.log_cat_bio

    def prediction(self):
        temp = 0
        for b in self.log_cat_bio:
            for c in self.log_cat_bio[b]:
                if self.log_cat_bio[b][c] > temp:
                    temp = self.log_cat_bio[b][c]
                    self.pred[b] = c
        return self.pred


x = Test('bioCorpus.txt', 0.8)
print(x.log_cat_bio)
print(x.pred)



