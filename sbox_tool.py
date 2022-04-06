#!/usr/bin/sage -python

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


# -------------------------------- Main program section

options_parser = OptionsParser()
parser = options_parser.get_parser()
options = options_parser.parse_args(parser.parse_args())

sboxes = []
if options.generation_options.generate_new_sboxes:
    generator = SboxGenerator()
    generated_sboxes_result = generator.generateSboxes(options.generation_options.number_of_sboxes, options.generation_options.size_of_sboxes, options.generation_options.generation_method)
# TODO: handle an input of prepared S-Boxes

analyzed_sboxes = SboxAnalyzer.analyzeSboxesWithCriteria(generated_sboxes_result, options.analyze_options)
sboxes_stats = SboxAnalyzer.analyzeStatsOfSboxes(analyzed_sboxes)
print(analyzed_sboxes)

# TODO: add columns with analyze criteria 

export_result = ExportHelper.exportDataToCsv(analyzed_sboxes, 'analyzed_sboxes.csv')
export_stats = ExportHelper.exportDataToCsv(sboxes_stats, 'sbox_stats.csv')

