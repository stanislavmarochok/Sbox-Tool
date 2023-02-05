from Logger import Logger
from analyzers.ICriterionAnalyzer import ICriterionAnalyzer


class DifferenceDistributionTableAnalyzer(ICriterionAnalyzer):
    """
    Analyze S-Box for the following properties:
        - maximal item in the difference distribution table of the sbox
        - number of maximal items in the table
        - number of zero items in the table
    """

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

    def countItemsInDdt(self, ddt, full_size_of_sbox, start_from_row_column=1):
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