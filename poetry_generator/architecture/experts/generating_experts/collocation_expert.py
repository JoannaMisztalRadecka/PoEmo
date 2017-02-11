import nltk
import os
import pickle
from pattern import en

from poetry_generator.structures.word import Word
from poetry_generator.architecture.experts.generating_experts.word_generating_expert import WordGeneratingExpert
from poetry_generator.settings import resources_dir


class CollocationExpert(WordGeneratingExpert):
    """Generating most common contexts for words for words"""

    def __init__(self, blackboard):
        super(
            CollocationExpert,
            self).__init__(
            blackboard,
            "Collocation Expert")
        self.word_tag_pairs = []

    def train(self):
        bigram_pickle_file = os.path.join(resources_dir, 'bigram.pickle')
        try:
            with open(bigram_pickle_file,'rb') as f:
                self.word_tag_pairs = pickle.load(f)

        except IOError:
            tagged_words = nltk.corpus.brown.tagged_words(tagset='universal')
            self.word_tag_pairs = list(nltk.bigrams(tagged_words))
            with open(bigram_pickle_file,'w') as f:
                pickle.dump(self.word_tag_pairs,f)


    '''Finding verbs for noun '''

    def _find_verbs(self, word):
        word_bigrams = [(a[0], b[0]) for a, b in self.word_tag_pairs
                                               if a[0] == word.name and a[1] == 'NOUN' and b[1] == 'VERB'
                                               and en.conjugate(b[0], "inf") not in ('be', 'have')]
        return self.__get_best_collocations(word, word_bigrams)

    '''Finding adjectives for noun'''

    def _find_epithets(self, word):
        word_bigrams = [(b[0], a[0]) for (a, b) in self.word_tag_pairs
                        if b[0] == word.name and b[1] == 'NOUN' and a[1] == 'ADJ']
        epithets = self.__get_best_collocations(word, word_bigrams)
        return epithets

    '''Finding nouns described by adjective'''

    def _find_comparisons(self, adjective):
        word_bigrams = [(a[0], b[0]) for (a, b) in self.word_tag_pairs
                        if a[0] == adjective.name and b[1] == 'NOUN' and a[1] == 'ADJ']
        comparisons = self.__get_best_collocations(adjective, word_bigrams)
        return comparisons

    '''Adding epithets for noun to pool'''

    def _add_epithets(self, word):
        epithets = set([Word(w, "JJ") for w in self._find_epithets(word)])
        if word not in self.blackboard.pool.epithets:
            self.blackboard.pool.epithets[word] = []
        self.blackboard.pool.epithets[word] += list(epithets)
        return epithets

    def _add_verbs(self, word):
        verbs = set([Word(w, "V") for w in self._find_verbs(word)])
        self.blackboard.pool.verbs[word] = list(verbs)
        return verbs

    '''Adding nouns for adjectives to pool'''

    def _add_comparisons(self, adj):

        comparisons = set([Word(w, "N") for w in self._find_comparisons(adj)])
        self.blackboard.pool.comparisons[adj] = comparisons
        return comparisons

    def __get_best_collocations(self, word, word_bigrams, n=20):
        words = nltk.ConditionalFreqDist(word_bigrams)[word.name]
        best_bigrams = sorted(words.items(), key=lambda (k, v): v, reverse=False)[:n]

        return dict(best_bigrams).keys()

    def generate_words(self):
        super(CollocationExpert, self).generate_words()
        counter = 0
        for w in self.blackboard.pool.nouns:
            eps = self._add_epithets(w)
            vs = self._add_verbs(w)
            le = len(eps)
            lv = len(vs)
            counter += le + lv
        for adj in self.blackboard.pool.adjectives:
            comps = self._add_comparisons(adj)
            counter += len(comps)
        return counter
