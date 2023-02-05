from Logger import Logger
from RuntimeGlobalSettings import RuntimeGlobalSettings
from analyzers.Bijection import BijectionAnalyzer
from analyzers.DifferenceDistributionTable import DifferenceDistributionTableAnalyzer
from analyzers.Nonlinearity import NonlinearityAnalyzer


class AnalyzeCriteria:
    def __init__(self):
        self.settings = RuntimeGlobalSettings.getInstance()
        self.analyzeCriteria = []

    def addAnalyzeCriterion(self, criterionName):
        if criterionName == 'difference_distribution_table':
            self.analyzeCriteria.append(DifferenceDistributionTableAnalyzer())
        elif criterionName == 'bijection':
            self.analyzeCriteria.append(BijectionAnalyzer())
        elif criterionName == 'nonlinearity':
            self.analyzeCriteria.append(NonlinearityAnalyzer())

    def printCriteria(self):
        logger = Logger(log_files=['sbox_analyzer', 'log'])
        logger.logInfo('')
        logger.logInfo('Analyzing criteria:')
        for index, criterion in enumerate(self.analyzeCriteria):
            logger.logInfo(f'{index}. {criterion.name}')
        logger.logInfo('')
