
from analyzers.ICriterionAnalyzer import ICriterionAnalyzer


class NonlinearityAnalyzer(ICriterionAnalyzer):
    """
    Analyze S-Box for the property of nonlinearity.
    """
    def __init__(self):
        self.name = 'Nonlinearity Analyzer'

    def analyze(self, _sbox):
        nonlinearity = self.isNonlinearSbox(_sbox)

        result = {}
        result['nonlinearity'] = nonlinearity

        return result

    def isNonlinearSbox(self, _sbox):
        # TODO: finish this method
        return True