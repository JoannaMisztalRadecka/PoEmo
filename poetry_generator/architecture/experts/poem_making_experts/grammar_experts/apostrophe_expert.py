from random import choice

from poetry_generator.structures.word import Word
from poetry_generator.architecture.experts.poem_making_experts.poem_making_expert import PoemMakingExpert


class ApostropheExpert(PoemMakingExpert):
    """Making apostrophes of given noun "Oh ... !" - adding hypernym """

    def __init__(self, blackboard):
        super(
            ApostropheExpert,
            self).__init__(
            blackboard,
            "Apostrophe Expert",
            2)
        self.apostrophes = [Word("O"), Word("Oh")]

    def generate_phrase(self):
        noun = choice(list(self.blackboard.pool.nouns))
        apostrophe = choice(self.apostrophes)
        try:
            hypernyms = self.blackboard.pool.hypernyms[noun]
            hypernym = choice(hypernyms)
            epithets = list(self.blackboard.pool.epithets[noun])
            epithet = choice(epithets)
        except:
            return
        verse = [apostrophe, noun, Word("the"), epithet, hypernym]
        return verse
