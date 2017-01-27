from poetry_generator.architecture.experts.expert import Expert
from poetry_generator.structures.phrase import Phrase


class PoemMakingExpert(Expert):
    """experts generating phrases to pool"""

    def __init__(self, blackboard, name, importance=1):
        super(PoemMakingExpert, self).__init__(blackboard, name)
        self.counter = 0
        self.importance = importance

    def add_phrase(self, pool):
        # print "Adding phrase: " + self.name
        if not self.precondition:
            return
        for i in range(self.importance):
            phrase = Phrase(self.generate_phrase(pool))
            # print phrase
            if len(phrase.words) > 0:
                pool.phrases_dict.append((phrase, self))

    def generate_phrase(self, pool):
        """ Generate phrase according to grammar and lexical rules"""
        # print "Generating phrase by expert: ", self.name
        pass
