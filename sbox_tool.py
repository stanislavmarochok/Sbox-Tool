#!/usr/bin/python

import sys
import argparse
import numpy as np
import pandas as pd

# own libraries
from ExportHelper import ExportHelper
from SboxAnalyzer import SboxAnalyzer
from OptionsParser import OptionsParser
from SboxGenerator import SboxGenerator
from SboxGenerator import SboxResult
from Logger import Logger


def run_tool():
    # -------------------------------- Main program section
    options_parser = OptionsParser()
    parser = options_parser.get_parser()
    options = options_parser.parse_args(parser.parse_args())

    sboxes = []
    if options.generation_options.generate_new_sboxes:
        generator = SboxGenerator()
        generated_sboxes_result = generator.generateSboxes(
                options.generation_options.number_of_sboxes,
                options.generation_options.size_of_sboxes,
                options.generation_options.generation_method)
    # TODO: handle an input of prepared S-Boxes

    sbox_analyzer = SboxAnalyzer()
    analyzed_sboxes = sbox_analyzer.analyzeSboxesWithCriteria(generated_sboxes_result, options.analyze_options)
    sboxes_stats = sbox_analyzer.analyzeStatsOfSboxes(analyzed_sboxes)

    logger = Logger(log_files=['main_func', 'log'])
    logger.logInfo(analyzed_sboxes)

    # TODO: add columns with analyze criteria 

    export = ExportHelper()
    export_result = export.exportDataToCsv(analyzed_sboxes, 'analyzed_sboxes.csv')
    export_stats = export.exportSboxesStats(sboxes_stats)


if __name__ == '__main__':
    run_tool()
