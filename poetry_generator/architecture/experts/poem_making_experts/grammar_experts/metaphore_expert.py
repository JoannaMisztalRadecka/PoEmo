from random import choice
from nltk import CFG, ChartParser


from poetry_generator.structures.word import Word
from poetry_generator.architecture.experts.poem_making_experts.grammar_experts.grammar_expert import GrammarExpert


class MetaphoreExpert(GrammarExpert):
    """Generating metaphores"""

    def __init__(self, blackboard, tense="present", person=3):
        super(
            MetaphoreExpert,
            self).__init__(
            blackboard,
            "Metaphore Expert",
            importance=2)
        self.grammar = CFG.fromstring("""
            S -> Person BE LIKE NP
            NP -> Det JJ N | Det N
            Person -> 'person'
            JJ -> 'adj'
            N -> 'n'
            Det -> 'the'
            BE -> 'be'
            LIKE -> 'like'
            """)

    def generate_phrase(self, pool):
        super(MetaphoreExpert, self).generate_phrase(pool)
        phrase = choice(self.productions)
        try:
            noun = choice([n for n in pool.nouns if len(pool.epithets[n]) > 0])
            adj = choice(pool.epithets[noun])
        except IndexError:
            return

        replace_words = {
            'adj': adj,
            'n': noun,
            'be': self.conjugate(
                "be"),
            'person': self.persons[
                self.tense][0]}
        for pos in replace_words:
            while pos in phrase:
                # try:
                phrase = self.replace_pos(pos, replace_words[pos], phrase)
                # except:
                #     return
        for w in phrase:
            if not isinstance(w, Word):
                phrase[phrase.index(w)] = Word(w)
        return phrase
