from poetry_generator.architecture.experts.poem_making_experts.poem_making_expert import PoemMakingExpert
from poetry_generator.structures.phrase import Phrase


class OverflowExpert(PoemMakingExpert):
    """Making overflow from phrase - breaking it to next line"""

    def __init__(self, blackboard):
        super(OverflowExpert, self).__init__(blackboard, "Overflow Expert")

    '''select phrases longer than goal for the line and break them'''

    def generate_phrase(self):
        if len(self.blackboard.pool.poem) < len(self.blackboard.syllables) - 1:
            goal_syls = self.blackboard.syllables[len(self.blackboard.pool.poem)]
            next_goal_syls = self.blackboard.syllables[len(self.blackboard.pool.poem) + 1]
            # Count syls in phrase

            def count_syls(phrase):
                return sum([w.syllables for w in phrase])
            for phrase in self.blackboard.pool.phrases:
                if phrase.count_syllables() >= goal_syls + next_goal_syls:
                    self.blackboard.pool.next_line.append(
                        Phrase(phrase.words[int(goal_syls / 2):]))
                    new_phrase = phrase.words[:int(goal_syls / 2)]
                    return new_phrase
