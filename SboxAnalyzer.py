#!/usr/bin/python

import enum
import pandas as pd

from Logger import Logger
from SboxGenerator import SboxResult


# interface with methods
"""
An interface with contains common methods for analyzers
"""
class ICriterionAnalyzer:
    def analyze(self, sbox):
        print(f'Analyzing SBox: {sbox}')


# implementation of the Difference Distribution Table analyzer
"""
Analyze S-Box for the following properties:
    - maximal item in the difference distribution table of the sbox
    - number of maximal items in the table
    - number of zero items in the table
"""
class DifferenceDistributionTableAnalyzer(ICriterionAnalyzer):
    def __init__(self):
        self.name = 'Difference Distribution Table Analyzer'
        self.logger = Logger(log_files=['sbox_analyzer', 'log'])

    def analyze(self, sbox):
        logger = self.logger
        # logger.log(f'Difference Distribution Table analysis of SBox: {sbox}')

        # calculate DDT
        ddt = self.difference_distribution_table(sbox)

        full_size_of_sbox = len(sbox)

        # retrieving items
        ddt_items = self.countItemsInDdtWithZeroRowColumn(ddt, full_size_of_sbox)
        # self.printDdt(ddt)

        # retrieving stats from DDT items (items count)
        result = self.getStatsFromDdtItems(ddt_items)
        return result

    def countItemsInDdt(self, ddt, full_size_of_sbox, start_from_row_column = 1):
        # create an array to store number of each item in the DDT
        items = [0] * (full_size_of_sbox + 1)
        for row_index in range(start_from_row_column, full_size_of_sbox):
            for column_index in range(start_from_row_column, full_size_of_sbox):
                items[ddt[row_index][column_index]] += 1

        return items

    def countItemsInDdtWithZeroRowColumn(self, ddt, full_size_of_sbox):
        return self.countItemsInDdt(ddt, full_size_of_sbox, 1)

    def getStatsFromDdtItems(self, ddt_items):
        max_item = 0
        max_item_count = 0
        zero_items_count = ddt_items[0]

        # going backwards from the end, excluding the last item (we don't count it)
        for i in range(len(ddt_items) - 1, -1, -1):
            if ddt_items[i] != 0:
                max_item = i
                max_item_count = ddt_items[i]
                break

        result = {}
        result['max_item'] = max_item
        result['max_item_count'] = max_item_count
        result['zero_items_count'] = zero_items_count

        return result
    
    def difference_distribution_table(self, sbox):
        sbox_length = len(sbox)
        ddt = [[0] * sbox_length for _ in range(sbox_length)]

        for i, x in enumerate(sbox):
            for j, y in enumerate(sbox):
                xor_in = i ^ j
                xor_out = x ^ y
                ddt[xor_in][xor_out] += 1

        return ddt


    def printDdt(self, ddt):
        logger = self.logger
        logger.logInfo('Difference distribution table:')
        for row in ddt:
            for item in row:
                logger.logInfo('{: >3}'.format(item), end='')
            logger.logInfo()


# implementation of the Bijection analyzer
"""
Analyze S-Box for the property of bijection.
An n x n SBox is bijective if it has all different output values from interval [0, 2**n - 1].
"""
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


# implementation of the Nonlinearity analyzer
"""
Analyze S-Box for the property of nonlinearity.
"""
class NonlinearityAnalyzer(ICriterionAnalyzer):
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


class AnalyzeCriteria:
    def __init__(self):
        self.analyzeCriteria = []
        self.analyzeCriteria.append(DifferenceDistributionTableAnalyzer())
        self.analyzeCriteria.append(BijectionAnalyzer())
        self.analyzeCriteria.append(NonlinearityAnalyzer())

        # TODO: add more analyzing criteria here

    def printCriteria(self):
        logger = Logger(log_files=['sbox_analyzer', 'log'])
        logger.logInfo('')
        logger.logInfo('Analyzing criteria:')
        for index, criterion in enumerate(self.analyzeCriteria):
            logger.logInfo(f'{index}. {criterion.name}')
        logger.logInfo('')


class SboxAnalyzer:
    def __init__(self):
        self.logger = Logger(log_files=['sbox_analyzer', 'log'])

    def analyzeSboxesWithCriteria(self, sboxes : SboxResult, criteria : AnalyzeCriteria):
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

    def analyzeCriterion(self, sageSbox, criterion : ICriterionAnalyzer):
        return criterion.analyze(sageSbox)

    def getSboxString(self, sbox):
        sboxStr = []
        for i in sbox:
            sboxStr.append(str(i))
        return '[' + ', '.join(sboxStr) + ']'

    def analyzeStatsOfSboxes(self, analyzed_sboxes):
        result = {}

        result['max_items'] = self.getSboxesStatsForCriteria(analyzed_sboxes, 'max_item')

        return result

    def getSboxesStatsForCriteria(self, analyzed_sboxes, criteriaName):
        items_count = {}
        items = analyzed_sboxes.get(criteriaName)
        if items == None:
            self.logger.logError(f'{criteriaName} of analyzed SBoxes is None!')

        for index, item in enumerate(items):
            if items_count.get(item) is None:
                items_count[item] = 0
            items_count[item] += 1
        result = {f'{criteriaName}': [], 'sboxes_count': []}
        for key, value in items_count.items():
            result[criteriaName].append(key)
            result['sboxes_count'].append(value)

        return result
