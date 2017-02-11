from random import choice
from pattern import en
from nltk import CFG

from poetry_generator.architecture.experts.poem_making_experts.grammar_experts.grammar_expert import GrammarExpert
from poetry_generator.structures.word import Word


class RhetoricalExpert(GrammarExpert):
    """Making rhetorical questions"""

    def __init__(self, blackboard, tense="present"):
        super(
            RhetoricalExpert,
            self).__init__(
            blackboard,
            "Rhetorical Expert")
        self.grammar = CFG.fromstring("""
            S -> WHAT BE Det NP | WHY BE Det N SO JJ
            NP -> JJ N | N
            JJ -> 'adj'
            N -> 'n'
            Det -> 'the'
            BE -> 'be'
            SO -> 'so'
            WHAT -> 'what'
            WHY -> 'why'
            """)

    def generate_phrase(self):
        super(RhetoricalExpert, self).generate_phrase()
        phrase = choice(self.productions)
        phrase.append("?")
        noun = choice(self.blackboard.pool.epithets.keys())
        try:
            adj = choice(self.blackboard.pool.epithets[noun])
        except:
            return
        replace_words = {'adj': adj, 'n': noun, 'be': en.conjugate("be", tense=self.tense.replace("1", "3").replace("2", "3"))}
        for pos in replace_words:
            while pos in phrase:
                try:
                    phrase = self.replace_pos(pos, replace_words[pos], phrase)
                except:
                    return
        for w in phrase:
            if not isinstance(w, Word):
                phrase[phrase.index(w)] = Word(w)
        return phrase
