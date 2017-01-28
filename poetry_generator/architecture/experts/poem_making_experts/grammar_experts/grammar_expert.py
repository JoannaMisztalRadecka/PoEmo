import pattern.en as en
from random import choice

from poetry_generator.architecture.experts.poem_making_experts.poem_making_expert import PoemMakingExpert


class GrammarExpert(PoemMakingExpert):
    """Expert generating sentences from defined CFG grammar"""

    def __init__(
            self,
            blackboard,
            name,
            tense="present",
            person=1,
            importance=1):
        super(GrammarExpert, self).__init__(blackboard=blackboard, name=name, importance=importance)
        self.person = self.blackboard.person
        self.tense = self.blackboard.tense
        self.persons = {1: ["I", "me", "my"], 2: ["you", "you", "your"], 4: [
            "he", "him", "his"], 3: ["she", "her", "her"]}
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

    def conjugate(self, verb, pers='3'):
        try:
            if self.tense == "present":
                return en.conjugate(verb, tense=en.PRESENT_3RD_PERSON_SINGULAR)
            elif self.tense == "past":
                return en.conjugate(verb, tense=en.PAST_3RD_PERSON_SINGULAR)
        except:
            return verb

    ''' Generate phrase according to grammar and lexical rules'''

    def generate_phrase(self, pool):
        super(GrammarExpert, self).generate_phrase(pool)
