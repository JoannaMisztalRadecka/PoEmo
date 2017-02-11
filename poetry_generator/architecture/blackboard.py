from random import randint, choice
from unidecode import unidecode
from pattern import en

from poetry_generator.architecture.pool_of_ideas import PoolOfIdeas


class Blackboard(object):
    """Public blackboard with current state of poem and partial solutions"""

    def __init__(self, input_text, syllables):
        self.text = unidecode(input_text)
        self.poem = []
        self.syllables = syllables
        self.keyphrases = []
        self.pool_of_ideas = {}
        self._pool = None
        self.pool = property(self.get_pool, self.set_pool)
        self.tense = choice(["1sg", "2sg", "3sg", "1sgp", "2sgp", "3gp"])
        # self.tense = choice(["past", "present"])
        # self.person = randint(1, 3)
        # print "Tense: ", self.tense, " Person: ", self.person
        self.sentences = []
        self.poem = []
        self.phrases_dict = []
        self.ngram_seed = []
        self.next_line = []

    ### triggers ###

    def get_pool(self):
        return self._pool

    def set_pool(self, value):
        self._pool = value

    def __str__(self):
        s = "\n Poem: \n"
        for l in self.poem:
            for w in l:
                s += w.__str__()
                s += " "
            s += "\n"
        return s

    def __repr__(self):
        s = "Poem: \n"
        for l in self.poem:
            for w in l:
                s += w.__str__()
            s += "\n"
        return s
