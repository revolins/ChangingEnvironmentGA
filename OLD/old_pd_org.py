"""
Obsolete classes from pd_org.py
"""

class StochasticPDGenotype(object):
    def __init__(self, probability=.5, number_of_bits_of_memory=0):
        self.probability = probability
        self.number_of_bits_of_memory = number_of_bits_of_memory