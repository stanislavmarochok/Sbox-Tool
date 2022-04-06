#!/usr/bin/sage --python

import random as random_for_shuffle_numbers

from sage.all import *
from sage.crypto.sbox import SBox
from SboxAnalyzer import DifferenceDistributionTableAnalyzer

class PartiallySmoothDifferenceTable:
    def generateSbox(self, full_size_of_sbox):
        partial_sbox = []
        limit = 100
        counter = 0

        while counter < limit:
            new_sbox = self.addItemToSbox(partial_sbox, full_size_of_sbox)
            print(new_sbox)
            if new_sbox is not False:
                return new_sbox
            counter += 1

        return new_sbox

    def addItemToSbox(self, partial_sbox, full_size_of_sbox):
        partial_sbox_pairs = self.getPairsForPartialSbox(partial_sbox, full_size_of_sbox)

        print()
        print('-----------------------------------------------------')
        print('Adding a new item to partial SBox')
        print(partial_sbox)
        print(f'Requested size of SBox: {full_size_of_sbox}')

        # if we have the whole SBox filled and it satisfies the conditions
        if len(partial_sbox) == full_size_of_sbox:
            return partial_sbox

        # get available numbers
        all_numbers = [1 for _ in range(full_size_of_sbox)]
        for i, x in partial_sbox_pairs:
            if isinstance(x, int):
                all_numbers[x] = 0
        available_numbers = [i for i in range(len(all_numbers)) if all_numbers[i] == 1]
        print('Available numbers:')
        print(available_numbers)

        random_for_shuffle_numbers.shuffle(available_numbers)

        # go through all available numbers
        for i in available_numbers:
            new_partial_sbox = [i for i in partial_sbox]
            new_partial_sbox.append(i) # adding a new item to SBox
            print('New partial SBox')
            print(new_partial_sbox)

            if self.satisfies_conditions(new_partial_sbox, full_size_of_sbox) is False:
                print('Validation failed!')
                continue

            new_sbox = self.addItemToSbox(new_partial_sbox, full_size_of_sbox)
            # this could happen if with all the new numbers we still don't have a good sbox
            # which satisfies all the conditions we want
            if new_sbox is False:
                continue

            return new_sbox

        return False

    def satisfies_conditions(self, partial_sbox, full_size_of_sbox):
        analyzer = DifferenceDistributionTableAnalyzer()

        partial_ddt = self.partialDdt(partial_sbox, full_size_of_sbox)
        # self.printDdt(partial_ddt, self.getPairsForPartialSbox(partial_sbox, full_size_of_sbox))
        ddt_items = analyzer.countItemsInDdt(partial_ddt, full_size_of_sbox)
        ddt_stats = analyzer.getStatsFromDdtItems(ddt_items)

        print('DDT items:')
        print(ddt_items)

        # parse result output
        max_item = ddt_stats.get('max_item')
        max_item_count = ddt_stats.get('max_item_count')
        zero_items_count = ddt_stats.get('zero_items_count')

        print(f'Max item: {max_item}')

        # checking conditions
        if max_item > 4:
            return False

        return True

    def partialDdt(self, partial_sbox, full_size_of_sbox):
        partial_sbox_length = full_size_of_sbox
        ddt = [[0] * partial_sbox_length for _ in range(partial_sbox_length)]

        sbox_pairs = self.getPairsForPartialSbox(partial_sbox, full_size_of_sbox)
        print(sbox_pairs)
        for (i, x) in sbox_pairs:
            if not isinstance(x, int):
                continue

            for (j, y) in sbox_pairs:
                xor_in = i ^ j

                if not isinstance(y, int):
                    continue

                xor_out = x ^ y
                ddt[xor_in][xor_out] += 1

        return ddt

    def getPairsForPartialSbox(self, partial_sbox_array, full_sbox_length):
        pairs = []
        for i in range(full_sbox_length):
            if i < len(partial_sbox_array):
                pairs.append((i, partial_sbox_array[i]))
            else:
                pairs.append((i, '\0'))
        return pairs

    def getSboxValueForPair(self, pairs, pair_index):
        for i, y in pairs:
            if i == pair_index:
                return y
        return None

    def printDdt(self, ddt, sbox_pairs):
        print('SBox in pairs:')
        print(sbox_pairs)
        print('Difference distribution table:')
        for row in ddt:
            for item in row:
                print('{: >3}'.format(item), end='')
            print()
