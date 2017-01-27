import random

from poetry_generator.architecture.experts.poem_making_experts.poem_making_expert import PoemMakingExpert


class EpithetExpert(PoemMakingExpert):
    """Expert adding adjective epithets to nouns"""

    def __init__(self, blackboard):
        super(EpithetExpert, self).__init__(blackboard, "Epithet Expert", 5)

    ''' Making epithet phrase of epithet (or two) and noun'''

    def generate_phrase(self, pool):
        noun = random.choice(list(pool.nouns))
        number_of_epithets = random.randrange(1, 3)
        epithets = []
        try:
            for e in range(number_of_epithets):
                epithet = random.choice(pool.epithets[noun])
                epithets.append(epithet)
            epithets.append(noun)
            return epithets
        except:
            # print "No epithets found"
            return
