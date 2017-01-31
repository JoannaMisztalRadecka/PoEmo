import pattern.en as en
from random import choice
from nltk.parse.generate import generate

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
        self.persons = {en.PRESENT_1ST_PERSON_SINGULAR: ["I", "me", "my"],
                        en.PRESENT_2ND_PERSON_SINGULAR: ["you", "you", "your"],
                        en.PRESENT_3RD_PERSON_SINGULAR: choice([["she", "her", "her"], ["he", "him", "his"]]),
                         en.PAST_1ST_PERSON_SINGULAR: ["I", "me", "my"], en.PAST_2ND_PERSON_SINGULAR: ["you", "you", "your"],
                       en.PAST_3RD_PERSON_SINGULAR: choice([["she", "her", "her"], ["he", "him", "his"]])}
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

        productions = grammar.productions(lhs=symbol)
        production = choice(productions)
        for sym in production.rhs():
            if isinstance(sym, str):
                words.append(sym)
            else:
                words.extend(self.produce(grammar, sym))
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

    def generate_phrase(self, pool):
        super(GrammarExpert, self).generate_phrase(pool)
        self.productions = list(generate(self.grammar, start=self.grammar.start(), n=100))
