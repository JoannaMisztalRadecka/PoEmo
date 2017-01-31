from random import choice

from nltk import CFG
from nltk.parse.generate import generate

from poetry_generator.structures.word import Word
from poetry_generator.architecture.experts.poem_making_experts.grammar_experts.grammar_expert import GrammarExpert


class SentenceExpert(GrammarExpert):
    """Expert generating sentences from defined CFG grammar"""

    def __init__(self, blackboard):
        super(
            SentenceExpert,
            self).__init__(
            blackboard,
            "Sentence Expert"
            )
        self.eva = ["be", "look", "feel"]
        self.atv = ["like", "hate", "love", "know", "need", "see"]

        """ eva - emotional verb active
            evp - emotional verb passive
            ej - emotion adjective
            en - emotional noun
            atv - attitude verb
        """
        self.grammar = CFG.fromstring("""
            S -> P | EP | Person ATV NP
            P -> NP VP
            EP -> Person EVA EJ | NP EVP Pron EJ | ENP VP
            ENP ->  EN OF NP
            NP -> Det N | Det JJ N | Det EJ JJ N | Det EJ N | Det EN
            VP -> V | V ERB | ERB V
            Det -> 'the'
            N -> 'n'
            V -> 'v'
            EVA -> 'eva'
            EVP -> 'makes'
            EN -> 'en'
            EJ -> 'ej'
            JJ -> 'adj'
            ERB -> 'erb'
            ATV -> 'atv'
            Person -> 'person'
            Pron -> 'pron'
            OF -> 'of'
            CC -> 'and' | 'but' | 'because' | 'so'
            """)

    ''' Generate phrase according to grammar and lexical rules'''

    def generate_phrase(self, pool):
        super(SentenceExpert, self).generate_phrase(pool)
        phrase = choice(self.productions)
        noun = choice(list(pool.nouns))
        try:
            replace_words = {
                'n': [noun],
                'v': [
                    Word(
                        self.conjugate(
                            v.name)) for v in list(
                        pool.verbs[noun])],
                'adj': pool.epithets[noun],
                'atv': [
                    Word(
                        self.conjugate(
                            v)) for v in self.atv],
                'eva': [
                    Word(
                        self.conjugate(
                            v)) for v in self.eva],
                'ej': pool.emotional_adjectives,
                'en': pool.emotional_nouns,
                'erb': pool.emotional_adverbs,
                'person': [
                    Word(
                        self.persons[
                            self.tense][0])],
                'pron': [
                    Word(
                        self.persons[
                            self.tense][1])]}
        except IndexError:
            return
        for pos in replace_words:
            while pos in phrase:
                words = replace_words[pos]
                if len(words) > 0:
                    word = choice(words)
                    phrase = self.replace_pos(pos, word, phrase)
                else:
                    return
        for w in phrase:
            if not isinstance(w, Word):
                phrase[phrase.index(w)] = Word(w)
        return phrase
