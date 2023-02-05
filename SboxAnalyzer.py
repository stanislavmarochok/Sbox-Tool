#!/usr/bin/python

from Logger import Logger
from RuntimeGlobalSettings import RuntimeGlobalSettings
from analyzers.AnalyzeCriteria import AnalyzeCriteria
from analyzers.ICriterionAnalyzer import ICriterionAnalyzer


class SboxAnalyzer:
    def __init__(self):
        self.settings = RuntimeGlobalSettings.getInstance()
        self.logger = Logger(log_files=['sbox_analyzer', 'log'])

    def analyzeSboxesWithCriteria(self, sboxes, criteria: AnalyzeCriteria):
        analyzeResult = {}

        criteria.printCriteria()

        # create SBox column
        analyzeResult['SBoxes'] = []
        for sbox in sboxes:
            _sbox = sbox.sbox
            sboxStr = self.getSboxString(_sbox)
            analyzeResult['SBoxes'].append(sboxStr)

            if sbox.meta_data is not None:
                for _meta_data_key, _meta_data_value in sbox.meta_data.items():
                    self.addItemToDict(analyzeResult, _meta_data_key, _meta_data_value)

        for criterion in criteria.analyzeCriteria:
            for sbox in sboxes:
                _sbox = sbox.sbox
                # sageSbox = SBox(_sbox)
                # TODO: check if analyzing DifferenceDistributionTable is correct (probably NOT)
                sboxCriterionAnalyzeResult = self.analyzeCriterion(_sbox, criterion)
                if type(sboxCriterionAnalyzeResult) is dict:
                    for result_key, result_value in sboxCriterionAnalyzeResult.items():
                        self.addItemToDict(analyzeResult, result_key, result_value)
                else:
                    # this must not happen, but to be sure
                    self.addItemToDict(analyzeResult, criterion.name, sboxCriterionAnalyzeResult)

        return analyzeResult

    def addItemToDict(self, _dict, name, item):
        if _dict.get(name) is None:
            _dict[name] = []
        _dict[name].append(item)

    def analyzeCriterion(self, sbox, criterion: ICriterionAnalyzer):
        return criterion.analyze(sbox)

    def getSboxString(self, sbox):
        sboxStr = []
        for i in sbox:
            sboxStr.append(str(i))
        return '[' + ', '.join(sboxStr) + ']'

    def analyzeStatsOfSboxes(self, analyzed_sboxes):
        result = {}

        if self.settings.analyzeCriteria.get('difference_distribution_table') == True:
            result['max_items'] = self.getSboxesStatsForCriteria(analyzed_sboxes, 'max_item')

        return result

    def getSboxesStatsForCriteria(self, analyzed_sboxes, criteriaName):
        items_count = {}
        items = analyzed_sboxes.get(criteriaName)
        if items == None:
            self.logger.logError(f'{criteriaName} of analyzed SBoxes is None!')
            return {}

        for index, item in enumerate(items):
            if items_count.get(item) is None:
                items_count[item] = 0
            items_count[item] += 1
        result = {f'{criteriaName}': [], 'sboxes_count': []}
        for key, value in items_count.items():
            result[criteriaName].append(key)
            result['sboxes_count'].append(value)

        return result
