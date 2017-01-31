import nltk
import os
import pickle

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
                                               if a[0] == word.name and a[1] == 'NOUN' and b[1] == 'VERB']
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

    def _add_epithets(self, word, pool):
        epithets = set([Word(w, "JJ") for w in self._find_epithets(word)])
        if word not in pool.epithets:
            pool.epithets[word] = []
        pool.epithets[word] += list(epithets)
        return epithets

    def _add_verbs(self, word, pool):
        verbs = set([Word(w, "V") for w in self._find_verbs(word)])
        pool.verbs[word] = list(verbs)
        return verbs

    '''Adding nouns for adjectives to pool'''

    def _add_comparisons(self, adj, pool):

        comparisons = set([Word(w, "N") for w in self._find_comparisons(adj)])
        pool.comparisons[adj] = comparisons
        return comparisons

    def __get_best_collocations(self, word, word_bigrams, N=20):
        words = nltk.ConditionalFreqDist(word_bigrams)[word.name]
        best_bigrams = sorted(words.items(), key=lambda (k, v): v, reverse=True)[:N]

        return dict(best_bigrams).keys()

    def generate_words(self, pool):
        super(CollocationExpert, self).generate_words(pool)
        counter = 0
        for w in pool.nouns:
            eps = self._add_epithets(w, pool)
            vs = self._add_verbs(w, pool)
            le = len(eps)
            lv = len(vs)
            counter += le + lv
        for adj in pool.adjectives:
            comps = self._add_comparisons(adj, pool)
            counter += len(comps)
        return counter
