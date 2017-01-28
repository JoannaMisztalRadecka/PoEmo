from pattern.en import tag, singularize
import pattern.en as en
from pattern.search import search

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

        sent = en.Sentence(en.parse(phrase))
        nouns = search('NN', sent)
        pool.nouns.update(set(Word(en.singularize(n[0].string)) for n in nouns))
        adjs = search('JJ', sent)
        pool.adjectives.update(set(Word(en.lemma(a[0].string)) for a in adjs))

        try:
            nps = search('NP', sent)
            for np in nps:
                pool.epithets.update({Word(en.singularize(w.string), "NN"): [Word(jj.string, "JJ") for jj in np if "JJ" in jj.tag] for w in np if "NN" in w.tag})
        except IndexError:
            pass

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
        # keyphrases = list(
        #     set(get_keyphrases(self.blackboard.text)))
        #
        # self.blackboard.keyphrases = keyphrases
        self.blackboard.sentences = self._tokenize_sentences()

        # create space for generation from each keyphrase
        # kp = keyphrases[0]
        pool_kp = PoolOfIdeas("", self.blackboard.syllables)
        pool_kp.sentences = self.blackboard.sentences
        self.blackboard.pool = pool_kp
        for kp in self.blackboard.sentences:
            self.add_keywords(self.blackboard.pool, kp)
