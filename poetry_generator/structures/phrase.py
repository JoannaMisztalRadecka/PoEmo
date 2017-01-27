import copy

from poetry_generator.structures.word import Word


class Phrase(object):
    """Idea- phrase generated by expert to fill poem line"""

    def __init__(self, words=None):
        self.words = []
        if words is not None:
            if isinstance(words[0], Word):  # if list of Word
                self.words = copy.deepcopy(words)
            else:  # if list of strings
                for w in words:
                    self.words.append(Word(w))
        else:
            self.words = []
        #self.syllables = self.count_syllables()
        #self.pos_tags = self.find_POS()
        # print "syllables: ", self.syllables

    def find_POS(self):
        return [w.pos for w in self.words]

    def count_syllables(self):
        sum = 0
        for w in self.words:
            sum += w.syllables
        return sum

    def __str__(self):
        return " ".join([w.name for w in self.words])

    def __repr__(self):
        return " ".join([w.name for w in self.words])

    def __hash__(self):
        return str(self)
