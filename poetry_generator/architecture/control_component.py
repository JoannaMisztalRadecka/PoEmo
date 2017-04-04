import logging
import json

from experts.poem_making_experts import exclamation_expert

from experts.generating_experts import wordnet_expert, emotion_expert, collocation_expert
from experts.evaluation_experts import syllables_expert, diversity_expert, rhymes_expert
from experts.poem_making_experts.grammar_experts import apostrophe_expert, comparison_expert, \
    epithet_expert, metaphore_expert, oxymoron_expert, rhetorical_expert, sentence_expert
from experts.poem_making_experts import overflow_expert, repetition_expert
from experts.keywords_expert import KeyWordsExpert
from poetry_generator.architecture.blackboard import Blackboard



class ControlComponent(object):
    """Control of experts priorities and actions, ending process"""

    def __init__(self, input_text, template):
        logging.basicConfig(level=logging.INFO)
        logging.info("Making blackboard...")
        temp = [int(s) for s in json.loads(template)]
        self.blackboard = Blackboard(input_text, temp)
        logging.info(self.blackboard.text)

    def _init_experts(self):
        self.keyword = KeyWordsExpert(self.blackboard)
        self.keyword.get_keyphrases()

        # generating experts ###
        logging.info("Words generating experts...")
        self.word_generating_experts = []
        self.word_generating_experts.append(self.keyword)
        self.word_generating_experts.append(
            wordnet_expert.WordNetExpert(self.blackboard))
        self.word_generating_experts.append(
            emotion_expert.EmotionExpert(self.blackboard))
        self.word_generating_experts.append(
            collocation_expert.CollocationExpert(
                self.blackboard))

        # Poem making experts... ###
        logging.info("Poem making experts...")
        self.poem_making_experts = []
        # self.poem_making_experts.append(self.keyword)
        self.poem_making_experts.append(
            epithet_expert.EpithetExpert(
                self.blackboard))
        self.poem_making_experts.append(
            apostrophe_expert.ApostropheExpert(
                self.blackboard))
        self.poem_making_experts.append(
            sentence_expert.SentenceExpert(
                self.blackboard))
        self.poem_making_experts.append(
            comparison_expert.ComparisonExpert(
                self.blackboard))
        self.poem_making_experts.append(
            exclamation_expert.ExclamationExpert(
                self.blackboard))
       # self.poem_making_experts.append(NGramExpert.NGramExpert(self.blackboard))
       #  self.poem_making_experts.append(
       #      repetition_expert.RepetitionExpert(
       #          self.blackboard))
        # self.poem_making_experts.append(
        #     overflow_expert.OverflowExpert(
        #         self.blackboard))
        self.poem_making_experts.append(
            rhetorical_expert.RhetoricalExpert(
                self.blackboard))
        self.poem_making_experts.append(
            metaphore_expert.MetaphoreExpert(
                self.blackboard))
        self.poem_making_experts.append(
            oxymoron_expert.OxymoronExpert(
                self.blackboard))

        logging.info("Control experts...")
        self.syllables = syllables_expert.SyllablesExpert(self.blackboard)
        self.diversity = diversity_expert.DiversityExpert(self.blackboard)
        self.rhymes = rhymes_expert.RhymesExpert(self.blackboard)
        self.emotion = emotion_expert.EmotionExpert(self.blackboard)

        self.train_experts()

    def train_experts(self):
        for e in self.word_generating_experts:
            e.train()

    def _generate_pool(self):
        # generate words... ###
        for wg_e in self.word_generating_experts:
            wg_e.generate_words()
        logging.info(self.blackboard.pool)

        ### generating phrases... ###
        logging.info("Making phrases...")
        if len(self.blackboard.pool.nouns) > 0:
            for i in range(50):
                for e in self.poem_making_experts:
                    try:
                        e.add_phrase()
                    except Exception as a:
                        logging.info("Warning - couldn't add phrase by expert: {}".format(a))
        # logging.info(self.blackboard.pool.phrases_dict)

        for line in range(len(self.blackboard.syllables)):
            if self.blackboard.syllables[line] > 0:
                ### making phrases ###
                logging.info("Selecting line " + str(line))
                poem_lines = self.syllables.select_phrases(line)
                poem_line = self.diversity.select_phrase(poem_lines)
                self.blackboard.pool.poem.append(poem_line)
            else:
                self.blackboard.pool.poem.append([' '])

    def make_poem(self):
        try:
            self._init_experts()
            self.keyword.get_keyphrases()

            self._generate_pool()
            logging.info(self.blackboard.pool)
            poem = self.blackboard.pool.str_poem()
            logging.info(self.blackboard.pool.print_experts())
            logging.info(poem)

            return poem

        except Exception:
            return "Couldn't generate a poem from given inspiration..."
