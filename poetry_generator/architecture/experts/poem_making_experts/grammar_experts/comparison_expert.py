import pattern.en as en
from random import choice

from nltk import parse_cfg, ChartParser

from poetry_generator.structures.word import Word
from poetry_generator.architecture.experts.poem_making_experts.grammar_experts.grammar_expert import GrammarExpert


class ComparisonExpert(GrammarExpert):
    """Making comparisons "as...as...", "... like a/an ..." """

    def __init__(self, blackboard):

        super(
            ComparisonExpert,
            self).__init__(
            blackboard=blackboard,
            name="Comparison Expert",
            importance=3)
        self.grammar = parse_cfg("""
            S -> AS JJ AS Det N | JJ LIKE Det N
            JJ -> 'adj'
            N -> 'n'
            Det -> 'det'
            LIKE -> 'like'
            AS -> 'as'
            """)

    def generate_phrase(self, pool):
        try:
            adj = choice(list(pool.adjectives))
            parser = ChartParser(self.grammar)
            gr = parser.grammar()
            phrase = self.produce(gr, gr.start())
            noun = choice(list(pool.comparisons[adj]))
            if en.pluralize(noun.name) == noun.name:
                article = "the"
            else:
                article = en.referenced(noun.name).split(" ")[0]
            replace_words = {'adj': adj, 'n': noun, 'det': article}
            for pos in replace_words:
                while pos in phrase:
                    try:
                        phrase = self.replace_pos(
                            pos, replace_words[pos], phrase)
                    except:
                        return
            for w in phrase:
                if not isinstance(w, Word):
                    phrase[phrase.index(w)] = Word(w)
            return phrase
        except:
            return
