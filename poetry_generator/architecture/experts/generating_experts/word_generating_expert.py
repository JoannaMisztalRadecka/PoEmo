from poetry_generator.architecture.experts.expert import Expert


class WordGeneratingExpert(Expert):
    """Expert adding words to pool"""

    def __init__(self, blackboard, name):
        super(WordGeneratingExpert, self).__init__(blackboard, name)

    """Return size of generated words """

    def generate_words(self):
        # print "Generating words ", self.name
        pass

    """ Return how many ideas can produce for pool """

    def estimate_ideas_size(self):
        # print "Estimating ideas... ", self.name
        size = self.generate_words()

        return size

    def train(self):
        pass