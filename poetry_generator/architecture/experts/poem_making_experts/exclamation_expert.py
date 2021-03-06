from random import choice
from copy import deepcopy

from poetry_generator.structures.word import Word
from poetry_generator.architecture.experts.poem_making_experts.poem_making_expert import PoemMakingExpert


class ExclamationExpert(PoemMakingExpert):
    """Adding exclamation to phrases"""

    def __init__(self, blackboard):
        super(
            ExclamationExpert,
            self).__init__(
            blackboard,
            "Exclamation Expert")

    def generate_phrase(self):
        try:
            phrase = deepcopy(choice(self.blackboard.pool.phrases_dict))[0].words
        except IndexError:
            return
        if phrase[-1].name not in ["!", "?"]:
            phrase.append(Word("!"))
        return phrase
