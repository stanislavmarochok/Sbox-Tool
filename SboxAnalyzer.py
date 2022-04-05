#!/usr/bin/sage -python

import enum
import pandas as pd

from sage.all import *
from sage.crypto.sbox import SBox
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

    def analyze(self, sageSbox):
        logger = Logger.getLogger(verbose=True)
        # logger.log(f'Difference Distribution Table analysis of SBox: {sbox}')

        # calculate DDT
        ddt = sageSbox.difference_distribution_table()

        sboxLength = 2 ** (len(sageSbox))

        # retrieving items
        ddt_items = self.countItemsInDdt(ddt, sboxLength)

        # retrieving stats from DDT items (items count)
        result = self.getStatsFromDdtItems(ddt_items)
        return result

    def countItemsInDdt(self, ddt, sboxLength):
        # create an array to store number of each item in the DDT
        items = [0] * (sboxLength + 1)
        for row in ddt:
            for item in row:
                items[item] += 1

        return items

    def getStatsFromDdtItems(self, ddt_items):
        max_item = 0
        max_item_count = 0
        zero_items_count = ddt_items[0]

        # going backwards from the end, excluding the last item (we don't count it)
        for i in range(len(ddt_items) - 2, -1, -1):
            if ddt_items[i] != 0:
                max_item = i
                max_item_count = ddt_items[i]
                break

        result = {}
        result['max_item'] = max_item
        result['max_item_count'] = max_item_count
        result['zero_items_count'] = zero_items_count

        return result

# implementation of the Bijection analyzer
"""
Analyze S-Box for the property of bijection.
An n x n SBox is bijective if it has all different output values from interval [0, 2**n - 1].
"""
class BijectionAnalyzer(ICriterionAnalyzer):
    def __init__(self):
        self.name = 'Bijection Analyzer'

    def analyze(self, sageSbox):
        is_bijective = True
        sboxLength = 2 ** len(sageSbox)
        values = [0] * (sboxLength + 1)
        for i in range(sboxLength):
            values[sageSbox[i]] += 1
            if values[sageSbox[i]] > 1:
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

    def analyze(self, sageSbox):
        nonlinearity = sageSbox.nonlinearity()

        result = {}
        result['nonlinearity'] = nonlinearity

        return result


class AnalyzeCriteria:
    def __init__(self):
        self.analyzeCriteria = []
        self.analyzeCriteria.append(DifferenceDistributionTableAnalyzer())
        self.analyzeCriteria.append(BijectionAnalyzer())
        self.analyzeCriteria.append(NonlinearityAnalyzer())

        # TODO: add more analyzing criteria here

    def printCriteria(self):
        logger = Logger.getLogger(verbose=True)
        logger.log('Analyzing criteria:')
        for index, criterion in enumerate(self.analyzeCriteria):
            logger.log(f'{index}. {criterion.name}')

        logger.log('')


class SboxAnalyzer:
    @staticmethod
    def analyzeSboxesWithCriteria(sboxes : SboxResult, criteria : AnalyzeCriteria):
        analyzeResult = {}

        criteria.printCriteria()

        # create SBox column
        analyzeResult['SBoxes'] = []
        for sbox in sboxes:
            _sbox = sbox.sbox
            print(_sbox)
            sboxStr = SboxAnalyzer.getSboxString(_sbox)
            analyzeResult['SBoxes'].append(sboxStr)

            if sbox.meta_data is not None:
                for _meta_data_key, _meta_data_value in sbox.meta_data.items():
                    SboxAnalyzer.addItemToDict(analyzeResult, _meta_data_key, _meta_data_value)

        for criterion in criteria.analyzeCriteria:
            for sbox in sboxes:
                sageSbox = SBox(_sbox)
                # TODO: check if analyzing DifferenceDistributionTable is correct (probably NOT)
                sboxCriterionAnalyzeResult = SboxAnalyzer.analyzeCriterion(sageSbox, criterion)
                if type(sboxCriterionAnalyzeResult) is dict:
                    for result_key, result_value in sboxCriterionAnalyzeResult.items():
                        SboxAnalyzer.addItemToDict(analyzeResult, result_key, result_value)
                else:
                    # this must not happen, but to be sure
                    SboxAnalyzer.addItemToDict(analyzeResult, criterion.name, sboxCriterionAnalyzeResult)

        return analyzeResult

    @staticmethod
    def addItemToDict(_dict, name, item):
        if _dict.get(name) is None:
            _dict[name] = []
        _dict[name].append(item)

    @staticmethod
    def analyzeCriterion(sageSbox, criterion : ICriterionAnalyzer):
        return criterion.analyze(sageSbox)

    @staticmethod
    def getSboxString(sbox):
        sboxStr = []
        for i in sbox:
            sboxStr.append(str(i))
        return '[' + ', '.join(sboxStr) + ']'
