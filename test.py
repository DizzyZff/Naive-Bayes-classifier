from learn import *


class Test:
    def __init__(self, filename, split):
        self.filename = filename
        self.split = split
        self.train = TrainData(filename, split)
        self.train_data = self.train.data
        self.test_data = self.train.test_data
        self.ap = {}
        self.words = []
        self.log_cat_bio = {}
        self.pred = {}
        self.smallst = {}
        self.output_string = ""
        self.normalize()
        self.get_log_cat_bio()
        self.smallest_log_cat()
        self.actual_proba()
        self.print_pred()

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

    def smallest_log_cat(self):
        array = []
        for name in self.log_cat_bio:
            for cat in self.train.categories:
                array.append(self.log_cat_bio[name][cat])
            self.smallst[name] = min(array)
            array = []
        return self.smallst

    def actual_proba(self):
        name_sum = {}
        for name in self.log_cat_bio:
            name_sum[name] = 0
            self.pred[name] = {}
            for cat in self.train.categories:
                self.pred[name][cat] = 2**(self.smallst[name] - self.log_cat_bio[name][cat])
                print(self.pred[name][cat])
                name_sum[name] += self.pred[name][cat]
                print(name_sum[name])
        for name in self.log_cat_bio:
            for cat in self.train.categories:
                self.pred[name][cat] = self.pred[name][cat] / name_sum[name]
        return self.pred

    def print_pred(self):
        actual = {}
        accuracy = 0
        temp = 0
        for bio in self.test_data:
            actual[bio[0]] = bio[1]
        for name in self.pred:
            self.output_string += name + ".  Prediction: "
            temp = 0
            for cat in self.pred[name]:
                if self.pred[name][cat] > temp:
                    temp = self.pred[name][cat]
            for cat in self.pred[name]:
                if self.pred[name][cat] == temp:
                    self.output_string += cat + ".   "
                    if cat == actual[name]:
                        accuracy += 1
                        self.output_string += "Right.   \n"
                    else:
                        self.output_string += "Wrong.   \n"
            for cat in self.pred[name]:
                # 2 decimal places
                self.output_string += cat + ": " + str(round(self.pred[name][cat]*100, 2)) + "%   "
            self.output_string += "\n\n"
        self.output_string += "Accuracy: " + str(accuracy) + " out of " + str(len(self.test_data)) + " = " + str(accuracy/len(self.test_data))
        return self.output_string
#end of class Test






