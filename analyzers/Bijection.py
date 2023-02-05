# implementation of the Bijection analyzer
"""
Analyze S-Box for the property of bijection.
An n x n SBox is bijective if it has all different output values from interval [0, 2**n - 1].
"""
from analyzers.ICriterionAnalyzer import ICriterionAnalyzer


class BijectionAnalyzer(ICriterionAnalyzer):
    def __init__(self):
        self.name = 'Bijection Analyzer'

    def analyze(self, sbox):
        is_bijective = True
        sboxLength = len(sbox)
        values = [0] * (sboxLength + 1)
        for i in range(sboxLength):
            values[sbox[i]] += 1
            if values[sbox[i]] > 1:
                is_bijective = False
                break

        result = {}
        result['is_bijective'] = is_bijective

        return result
