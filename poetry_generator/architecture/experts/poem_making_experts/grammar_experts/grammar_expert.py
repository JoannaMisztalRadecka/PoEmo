import pattern.en as en
from random import choice
from nltk.parse.generate import generate
from nltk.grammar import Nonterminal

from poetry_generator.architecture.experts.poem_making_experts.poem_making_expert import PoemMakingExpert


class GrammarExpert(PoemMakingExpert):
    """Expert generating sentences from defined CFG grammar"""

    def __init__(
            self,
            blackboard,
            name,
            importance=1):
        super(GrammarExpert, self).__init__(blackboard=blackboard, name=name, importance=importance)
        # self.person = self.blackboard.person
        self.tense = self.blackboard.tense
        self.persons = {"1sg": ["I", "me", "my"],
                        "2sg": ["you", "you", "your"],
                        "3sg": choice([["she", "her", "her"], ["he", "him", "his"]]),
                         "1sgp": ["I", "me", "my"],
                         "2sgp": ["you", "you", "your"],
                       "3sgp": choice([["she", "her", "her"], ["he", "him", "his"]])}
        # self.persons = {1: ["I", "me", "my"], 2: ["you", "you", "your"], 4: [
        #     "he", "him", "his"], 3: ["she", "her", "her"]}
        self.eva = ["be", "seem", "look", "feel"]
        self.atv = ["like", "hate", "love", "know", "need", "see"]

        """ eva - emotional verb active
            evp - emotional verb passive
            ej - emotion adjective
            en - emotional noun
            atv - attitude verb
        """
        self.grammar = None

    def produce(self, grammar, symbol):
        words = []

        productions = grammar.productions(symbol)
        production = choice(productions)
        for sym in production.rhs():
            if isinstance(sym, Nonterminal):
                words.extend(self.produce(grammar, sym))

            else:
                words.append(sym)

        return words

    def replace_pos(self, pos, word, phrase):
        for w in phrase:
            if w == pos:
                phrase[phrase.index(w)] = word
                return phrase
        return phrase

    def conjugate(self, verb):
        try:
            return en.conjugate(verb, tense=self.tense)
        except:
            return verb

    ''' Generate phrase according to grammar and lexical rules'''

    def generate_phrase(self):
        super(GrammarExpert, self).generate_phrase()
        self.productions = list(generate(self.grammar, start=self.grammar.start(), n=100))
