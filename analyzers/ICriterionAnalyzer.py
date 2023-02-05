class ICriterionAnalyzer:
    """
    An interface with contains common methods for analyzers
    """

    def analyze(self, sbox):
        print(f'Analyzing SBox: {sbox}')