import random

from poetry_generator.utils.affect_utils import calculate_arousal, calculate_valence, get_emotion, get_emotion_distance,\
    make_wn_affect_tree, find_affect_synsets_for_emotion
from poetry_generator.architecture.experts.generating_experts.word_generating_expert import *
from poetry_generator.utils.utils import tokenize_sentences
from poetry_generator.structures.word import Word
from poetry_generator.architecture.experts.evaluation_experts.control_expert import ControlExpert


class EmotionExpert(WordGeneratingExpert, ControlExpert):
    """Adding words which make the poem closer given emotional value"""

    def __init__(self, blackboard):
        super(EmotionExpert, self).__init__(blackboard, "Emotion expert")
        self.optimism_rate = 1

    '''calculate sentiments for long texts '''

    def calculate_text_sentiment(self, text):
        # Sentiment calculation for each sentence
        sentences = tokenize_sentences(text)
       # print "Rating text sentiment..."
        sentiments_valence = {s: calculate_valence(s) for s in sentences}
        pos_sent = sum([s[0] for s in sentiments_valence.values()])
        neg_sent = sum([s[1] for s in sentiments_valence.values()])
        valence = (self.optimism_rate * pos_sent +
                   (2 - self.optimism_rate) * neg_sent)
        sentiments_arousal = {s: calculate_arousal(s) for s in sentences}
        arousal = sum(sentiments_arousal.values()) / \
            float(len(sentiments_arousal))
        return ((valence, arousal))

    def calculate_phrase_sentiment(self, phrases):
        # print "Rating phrases sentiment..."
        valence_list = []
        arousal_list = []
        for p in phrases:
            valence_list.append(calculate_valence(p))
            arousal_list.append(calculate_arousal(p))
        # list average

        def avg(list):
            return float(sum(list) / len(list))

        pos_sent = avg([p[0] for p in valence_list])
        neg_sent = avg([p[1] for p in valence_list])
        valence = (self.optimism_rate * pos_sent +
                   (2 - self.optimism_rate) * neg_sent)
        arousal = avg(arousal_list)
        # print "Valence: " + str(valence)
        # print "arousal: " + str(arousal)
        return ((valence, arousal))

    '''finding emotion for valence, arousal'''

    def get_emotion(self, xxx_todo_changeme):
        (valence, arousal) = xxx_todo_changeme
        emotion = get_emotion(valence, arousal)
        # print "The emotional state is " + emotion
        return emotion

    def generate_affect_words(self, emotion):
       # print "Generating affect words..."
        affect_tree = make_wn_affect_tree()
        affect_words = find_affect_synsets_for_emotion(emotion, affect_tree)
        # print affect_words
        return set(affect_words)

    def find_emotional_words(self, pool):
        # try:
        text_sentiment = self.calculate_phrase_sentiment(pool.sentences)
        emotion = self.get_emotion(text_sentiment)
        pool.emotion = emotion
        affect_knowledge = [Word(e)
                            for e in self.generate_affect_words(emotion)]
        return affect_knowledge
        # except:
        #     print "Couldn't generate affect words."

    '''Add words from knowledge to blackboard'''

    def generate_words(self, pool):
        if len(pool.nouns) == 0:
            return 0
        super(EmotionExpert, self).generate_words(pool)
        self.optimism_rate = random.uniform(0.7, 1.3)
        # print "Optimism rate is " + str(self.optimism_rate)
        knowledge = self.find_emotional_words(pool)
        for e in knowledge:
            if e.pos.startswith("N"):
                pool.emotional_nouns.append(e)
            elif e.pos.startswith("J"):
                pool.emotional_adjectives.append(e)
            elif e.pos.startswith("R"):
                pool.emotional_adverbs.append(e)
        return len(knowledge)

    '''Controls if the emotional state of phrase is the same as poem'''

    def emotion_phrase_evaluation(self, phrase):

        try:
            (v, a) = self.calculate_phrase_sentiment(
                [" ".join([w.name for w in phrase.words])])
            eval = get_emotion_distance(v, a, self.blackboard.pool.emotion)
            return eval
        except:
            return 100000

    def evaluate_lines(self, line_nr):
        phrases_eval = {i: self.emotion_phrase_evaluation(self.blackboard.pool.phrases_dict[i][0])
                        for i in range(len(self.blackboard.pool.phrases_dict))}
        return phrases_eval
