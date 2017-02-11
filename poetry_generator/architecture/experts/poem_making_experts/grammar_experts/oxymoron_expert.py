from random import choice

from poetry_generator.structures.word import Word
from poetry_generator.architecture.experts.poem_making_experts.poem_making_expert import PoemMakingExpert


class OxymoronExpert(PoemMakingExpert):
    """Making oxymoron (words with opposite meaning, antonyms) by enumarating antonyms or adding antonym epithet"""

    def __init__(self, blackboard):
        super(OxymoronExpert, self).__init__(blackboard, "Oxymoron Expert", 2)

    def generate_phrase(self):
        try:
            word = choice(list(self.blackboard.pool.antonyms))
            antonym = choice(list(self.blackboard.pool.antonyms[word]))
            phrase = []
            phrase.append(word)
            phrase.append(choice(["and", "or", "but"]))
            phrase.append(antonym)
            return phrase
        except:
            return
