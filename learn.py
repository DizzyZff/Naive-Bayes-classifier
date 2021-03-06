"""
The format of this file is as follows:
Separate biographies are separated by 1 or more blank lines.
In each biography, the first line is the name of the person. The second line is the category (a single
word). The remaining lines are the biography. You may assume that the characters in the file are
all a-z, A-Z, comma, period, and white space; there are no numbers and no other punctuation.
"""
import math
import string


class TrainData:
    def __init__(self, filename, split):
        self.filename = filename
        self.split = split
        self.data = [[]]
        self.test_data = [[]]
        self.categories = []
        self.occ_cat = {}
        self.occ_word_in_cat = {}
        self.words = []
        self.freq_cat = {}
        self.freq_word_in_cat = {}
        self.prob_cat = {}
        self.prob_word_in_cat = {}
        self.log_cat = {}
        self.log_word_in_cat = {}
        self.read_file()
        self.get_words()
        self.categories = self.get_categories()
        self.occ_cat = self.get_occ_cat()
        self.occ_word_in_cat = self.get_occ_word_in_cat()
        self.freq_cat = self.get_freq_cat()
        self.freq_word_in_cat = self.get_freq_word_in_cat()
        self.prob_cat, self.prob_word_in_cat = self.get_prob()
        self.log_cat, self.log_word_in_cat = self.negative_log()

    def read_file(self):
        with open(self.filename, 'r') as f:
            for line in f:
                if line == '\n':
                    self.data.append([])
                else:
                    self.data[-1].append(line.strip())
        split = self.split
        self.test_data = self.data[split:]
        self.data = self.data[:split]

        for data in self.data:
            if len(data) > 3:
                data[2] = " ".join(data[2:])
                pop = len(data) - 3
                for i in range(pop):
                    data.pop()
        for data in self.test_data:
            if len(data) > 3:
                data[2] = " ".join(data[2:])
                pop = len(data) - 3
                for i in range(pop):
                    data.pop()
        #remove empty lists
        self.data = [x for x in self.data if x]
        self.test_data = [x for x in self.test_data if x]

    def get_words(self):
        stopwords = open('stopwords.txt', 'r').read().split()
        for data in self.data:
            for d in data:
                # strip punctuation
                d = d.translate(str.maketrans('', '', string.punctuation))
                for word in d.split():
                    word = word.lower()
                    if word not in self.words and word not in stopwords and len(word) > 2:
                        self.words.append(word)
        return self.words

    def get_data(self):
        return self.data

    def get_categories(self):
        self.categories = [x[1] for x in self.data if x != []]
        # count duplicates
        self.occ_cat = {}
        for cat in self.categories:
            if cat in self.occ_cat:
                self.occ_cat[cat] += 1
            else:
                self.occ_cat[cat] = 1
        self.categories = list(set(self.categories))
        return self.categories

    def get_occ_cat(self):
        return self.occ_cat

    def get_occ_word_in_cat(self):
        for cat in self.categories:
            self.occ_word_in_cat[cat] = {}
            for word in self.words:
                self.occ_word_in_cat[cat][word] = 0
        for cat in self.categories:
            for line in self.data:
                if line != [] and line[1] == cat:
                    for words in line[2:]:
                        for word in words.split():
                            word = word.strip('.,!?;:')
                            word = word.lower()
                            if word in self.occ_word_in_cat[cat]:
                                self.occ_word_in_cat[cat][word] += 1
                    for word in line[0].split():
                        word = word.strip('.,!?;:')
                        word = word.lower()
                        if word in self.occ_word_in_cat[cat]:
                            self.occ_word_in_cat[cat][word] += 1
        return self.occ_word_in_cat

    def get_freq_cat(self):
        for cat in self.categories:
            self.freq_cat[cat] = self.occ_cat[cat] / len(self.data)
        return self.freq_cat

    def get_freq_word_in_cat(self):
        for x in self.occ_word_in_cat:
            self.freq_word_in_cat[x] = {}
            for y in self.occ_word_in_cat[x]:
                self.freq_word_in_cat[x][y] = self.occ_word_in_cat[x][y] / self.occ_cat[x]
        return self.freq_word_in_cat

    def get_prob(self):
        epsilon = 0.1
        for cat in self.categories:
            self.prob_cat[cat] = (self.freq_cat[cat] + epsilon) / (1 + len(self.categories) * epsilon)
            self.prob_word_in_cat[cat] = {}
            for word in self.words:
                self.prob_word_in_cat[cat][word] = (self.freq_word_in_cat[cat][word] + epsilon) / (1 + 2 * epsilon)
        return self.prob_cat, self.prob_word_in_cat

    def negative_log(self):
        for cat in self.categories:
            self.log_cat[cat] = -math.log(self.prob_cat[cat], 2)
            self.log_word_in_cat[cat] = {}
            for word in self.words:
                self.log_word_in_cat[cat][word] = -math.log(self.prob_word_in_cat[cat][word], 2)
        return self.log_cat, self.log_word_in_cat
#end class