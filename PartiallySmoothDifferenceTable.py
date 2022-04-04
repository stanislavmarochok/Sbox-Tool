#!/usr/bin/sage --python

from sage.all import *
from sage.crypto.sbox import SBox
from SboxAnalyzer import DifferenceDistributionTableAnalyzer

class PartiallySmoothDifferenceTable:
    def generateSbox(self, full_size_of_sbox):
        sbox = [3, 14, 0, 5, 1, 8, 15, 13, 2, 12, 4, 7, 9, 6, 10, 11]
        limit = 100

        print(f'size of sbox: {full_size_of_sbox}')

        """
        while len(X) < full_size_of_sbox:
            if counter > limit:
                return []
            # continue algorithm here

        """

        self.satisfies_conditions(sbox, full_size_of_sbox)
        print('Generating partially smooth difference table')

        # temporary solution
        return sbox

    def satisfies_conditions(self, partial_sbox, full_size_of_sbox):
        analyzer = DifferenceDistributionTableAnalyzer()

        partial_ddt = self.partialDdt(partial_sbox, full_size_of_sbox)
        ddt_items = analyzer.countItemsInDdt(partial_ddt, full_size_of_sbox)
        ddt_stats = analyzer.getStatsFromDdtItems(ddt_items)

        # parse result output
        max_item = ddt_stats.get('max_item')
        max_item_count = ddt_stats.get('max_item_count')
        zero_items_count = ddt_stats.get('zero_items_count')

        # checking conditions
        if max_item > 2:
            return False

        return True

    @staticmethod
    def partialDdt(partial_sbox, full_size_of_sbox):
        # TODO: calculate partial ddt here
        partial_sbox_length = full_size_of_sbox
        ddt = [[0] * partial_sbox_length for _ in range(partial_sbox_length)]

        for i in range(partial_sbox_length):
            y = partial_sbox

        print(ddt)
        return ddt
