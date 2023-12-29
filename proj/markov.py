import math
from hashtable import Hashtable

HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:
    def __init__(self, k, text, use_hashtable):
        """
        Construct a new k-order markov model using the text 'text'.
        """
        self.k = k
        self.alphabet = set(text)  # Set of unique characters
        self.S = len(self.alphabet)
        self.model = self.build_model(text, use_hashtable)

    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        """
        log_prob = 0
        # The retrieval of values using get with a default of 0
        for i in range(len(s)):
            k_string = (s[i:] + s[:self.k])[0:self.k]
            k_plus_1_string = (s[i:] + s[:self.k+1])[0:self.k+1]

            # Getting values with a default
            M = self.model.get(k_plus_1_string, 0)
            N = self.model.get(k_string, 0)
            log_prob += math.log((M + 1) / (N + self.S))
        return log_prob
    
    
    def build_model(self, text, use_hashtable):
        if use_hashtable:
            model = Hashtable(HASH_CELLS, 0, TOO_FULL, GROWTH_RATIO)
        else:
            model = {}

        text += text[:self.k]  # append the beginning to the end for wrap-around
        for i in range(len(text) - self.k):  # adjust the range to avoid index error
            k_string = text[i:i+self.k]
            k_plus_1_string = text[i:i+self.k+1]

            # Update counts
            if use_hashtable:
                # Getting and setting values in Hashtable
                model[k_string] = model[k_string] + 1
                model[k_plus_1_string] = model[k_plus_1_string] + 1
            else:
                # Getting values with a default for dicts
                model[k_string] = model.get(k_string, 0) + 1
                model[k_plus_1_string] = model.get(k_plus_1_string, 0) + 1
        return model


def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    """
    # Train models for each speaker
    speaker_A_model = Markov(k, speech1, use_hashtable)
    speaker_B_model = Markov(k, speech2, use_hashtable)

    # Calculate normalized log probabilities for speech3
    prob_A = speaker_A_model.log_probability(speech3) / len(speech3)
    prob_B = speaker_B_model.log_probability(speech3) / len(speech3)

    # Identify most likely speaker
    most_likely_speaker = "A" if prob_A > prob_B else "B"

    return (prob_A, prob_B, most_likely_speaker)
