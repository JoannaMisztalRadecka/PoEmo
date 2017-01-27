import en

import nltk

from poetry_generator.utils.keyphrase_extractor import get_keyphrases
from poetry_generator.architecture.experts.poem_making_experts.poem_making_expert import PoemMakingExpert
from poetry_generator.architecture.experts.generating_experts.word_generating_expert import WordGeneratingExpert
from poetry_generator.architecture.pool_of_ideas import PoolOfIdeas
from poetry_generator.structures.word import Word


class KeyWordsExpert(PoemMakingExpert, WordGeneratingExpert):
    """Expert extracting keyphrases, making pools, extracting keywords and adding them to pool"""

    def __init__(self, blackboard):
        super(KeyWordsExpert, self).__init__(blackboard, "Keywords Expert")

    def add_keywords(self, pool, phrase):
        nouns = en.sentence.find(phrase, "NN")
        adjs = en.sentence.find(phrase, "JJ")
        for n in nouns:
            wn = Word(en.noun.singular(n[0][0]), "NN")
            pool.nouns.add(wn)
            pool.epithets[wn] = []
            jn = "JJ " + wn.name
            epithets = en.sentence.find(phrase, jn)
            pool.epithets[wn] += [Word(e[0][0], e[0][1]) for e in epithets]
        pool.adjectives |= set([Word(w[0][0], w[0][1]) for w in adjs])

    def generate_phrase(self, pool):
        """Parse string phrase to list of words with tags """
        phrase = pool.title
        tokens = nltk.word_tokenize(phrase)
        pos_phrase = nltk.pos_tag(tokens)
        new_phrase = [Word(w[0], w[1]) for w in pos_phrase]
        return new_phrase

    def _tokenize_sentences(self):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(self.blackboard.text)
        return sentences

    def _get_phrase_sents(self, pool):
        kp = self.generate_phrase(pool)
        sents = []
        for s in self.blackboard.sentences:
            contains = True
            for k in kp:
                if k.name not in s.lower():
                    contains = False
                    break
            if contains is True:
                sents.append(s)
        pool.sentences = sents

    def get_keyphrases(self):
        keyphrases = list(
            set(get_keyphrases(self.blackboard.text)))
        self.blackboard.keyphrases = keyphrases
        self.blackboard.sentences = self._tokenize_sentences()
        # create space for generation from each keyphrase
        kp = keyphrases[0]
        pool_kp = PoolOfIdeas(kp, self.blackboard.syllables)
        pool_kp.sentences = self.blackboard.sentences
        self.blackboard.pool = pool_kp
        for kp in self.blackboard.keyphrases:
            self.add_keywords(self.blackboard.pool, kp)
