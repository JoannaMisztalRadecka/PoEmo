from nltk.corpus import wordnet as wn

from poetry_generator.structures.word import Word
from poetry_generator.architecture.experts.generating_experts.word_generating_expert import WordGeneratingExpert


class WordNetExpert(WordGeneratingExpert):
    """Expert generating related words from WordNet"""

    def __init__(self, blackboard):
        super(WordNetExpert, self).__init__(blackboard, "WNExpert")

    def _find_synonyms(self, word, pool):
        synonyms = []
        try:
            synonyms = set(Word(w, word.pos)
                            for w in wn.synsets(word.name)[0].lemma_names())

        except IndexError as e:
            pass

        if word.pos.startswith("N"):
            pool.nouns |= set(synonyms)
        # elif word.pos.startswith("V"):
        #     pool.verbs |= synonyms
        elif word.pos.startswith("JJ"):
            pool.adjectives |= synonyms
        pool.synonyms[word.name] += [s.name for s in synonyms]
        return synonyms

    def _find_hyponym(self, word, pool):
        hyponyms = []
        try:
            hyponyms = set(Word(w.name().split('.')[0], word.pos)
                            for w in wn.synsets(word.name)[0].hyponyms())

        except IndexError as e:
            pass

        if word.pos.startswith("N"):
            pool.nouns |= set(hyponyms)
        # elif word.pos.startswith("V"):
        #     pool.verbs |= hyponyms
        elif word.pos.startswith("JJ"):
            pool.adjectives |= hyponyms
        pool.hyponyms[word.name] += [h.name for h in hyponyms]
        return hyponyms

    def _find_hypernyms(self, word, pool):
        hypernyms = []
        try:
            hypernyms = set(Word(w.name().split('.')[0], word.pos)
                            for w in wn.synsets(word.name)[0].hypernyms())

        except IndexError as e:
            pass

        if word.pos.startswith("N"):
            pool.nouns |= set(hypernyms)
        # elif word.pos.startswith("V"):
        #     pool.verbs |= hypernyms
        elif word.pos.startswith("JJ"):
            pool.adjectives |= hypernyms
        pool.hypernyms[word.name] += [h.name for h in hypernyms]
        return hypernyms

    def _find_antonyms(self, word, pool):
        antonyms = []
        try:
            antonyms = set(Word(a.name(), word.pos) for a in wn.synsets(word.name)[0].lemmas()[0].antonyms())
        except IndexError as e:
            pass

        if word.pos.startswith("N"):
            pool.nouns |= set(antonyms)
        # elif word.pos.startswith("V"):
        #     pool.verbs |= antonyms
        elif word.pos.startswith("JJ"):
            pool.adjectives |= antonyms
        pool.antonyms[word.name] += [a.name for a in antonyms]
        return antonyms

    def generate_words(self, pool):
        super(WordNetExpert, self).generate_words(pool)
        counter = 0
        words = set()
        words |= pool.nouns
        words |= pool.adjectives
        nouns = set()
        nouns |= pool.nouns
        pool.synonyms = {w.name: [] for w in words}
        pool.antonyms = {w.name: [] for w in words}
        pool.hypernyms = {w.name: [] for w in words}
        for w in words:
            syns = self._find_synonyms(w, pool)
            ants = self._find_antonyms(w, pool)

            counter += len(syns)
            counter += len(ants)
        for w in nouns:
            hyps = self._find_hypernyms(w, pool)

            counter += len(hyps)
        return counter
