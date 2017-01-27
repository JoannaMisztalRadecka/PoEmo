import en

from poetry_generator.structures.word import Word
from poetry_generator.architecture.experts.generating_experts.word_generating_expert import WordGeneratingExpert


class WordNetExpert(WordGeneratingExpert):
    """Expert generating related words from WordNet"""

    def __init__(self, blackboard):
        super(WordNetExpert, self).__init__(blackboard, "WNExpert")

    def _find_synonyms(self, word, pool):
        synonyms = []
        try:
            if word.pos.startswith("N"):
                synonyms = [Word(w, "NN")
                            for w in en.noun.senses(word.name)[0]]
                pool.nouns |= set(synonyms)
            elif word.pos.startswith("V"):
                synonyms = set([Word(w, "V")
                                for w in en.verb.senses(word.name)[0]])
                pool.verbs |= synonyms
            elif word.pos.startswith("JJ"):
                synonyms = set([Word(w, "JJ")
                                for w in en.adjective.senses(word.name)[0]])
                pool.adjectives |= synonyms

        except IndexError as e:
            pass
            # print "Couldn't find synonyms {}".format(word)
        return synonyms

    def _find_hyponym(self, word, pool):
        try:
            if word.pos.startswith("N"):
                pool.nouns |= set([Word(w, "NN")
                                   for w in en.noun.hyponym(word.name)[0]])
            elif word.pos.startswith("V"):
                pool.verbs |= set([Word(w, "V")
                                   for w in en.verb.hyponym(word.name)[0]])
            elif word.pos.startswith("JJ"):
                pool.adjectives |= set(
                    [Word(w, "JJ") for w in en.adjective.hyponym(word.name)[0]])
        except IndexError as e:
            pass
            # print "Couldn't find hyponyms {}".format(word)

    def _find_hypernym(self, word, pool):
        hypernyms = []
        try:
            if word.pos.startswith("N"):
                h = en.noun.hypernym(word.name)
                hypernyms = [Word(w, "NN") for w in h[0]]
            elif word.pos.startswith("V"):
                h = en.verb.hypernym(word.name)
                hypernyms = [Word(w, "V") for w in h[0]]
            elif word.pos.startswith("JJ"):
                h = en.adjective.hypernym(word.name)
                hypernyms = [Word(w, "JJ") for w in h[0]]
            pool.hypernyms[word] = hypernyms
        except IndexError as e:
           pass
            # print "Couldn't find hypernyms {}".format(word)
        return hypernyms

    def _find_antonym(self, word, pool):
        antonyms = []
        try:
            if word.pos.startswith("N"):
                h = en.noun.antonym(word.name)
                antonyms = [Word(w, "NN") for w in h[0]]
            elif word.pos.startswith("V"):
                h = en.verb.antonym(word.name)
                antonyms = [Word(w, "V") for w in h[0]]
            elif word.pos.startswith("JJ"):
                h = en.adjective.antonym(word.name)
                antonyms = [Word(w, "JJ") for w in h[0]]
            pool.antonyms[word] = antonyms
        except IndexError as e:
            pass
            # print "Couldn't find antonyms  {}".format(word)
        return antonyms

    def generate_words(self, pool):
        super(WordNetExpert, self).generate_words(pool)
        counter = 0
        words = set()
        words |= pool.nouns
        words |= pool.adjectives
        for w in words:
            syns = self._find_synonyms(w, pool)
            ants = self._find_antonym(w, pool)
            counter += len(syns)
            counter += len(ants)
        for w in pool.nouns:
            hyps = self._find_hypernym(w, pool)
            counter += len(hyps)
        return counter
