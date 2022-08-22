#!/usr/bin/sage -python

import pandas as pd
import numpy as np
import os
import json

import sage.all
from sage.crypto.sbox import SBox

from ExportHelper import ExportHelper
from SboxAnalyzer import DifferenceDistributionTableAnalyzer


def process_files():
    csv_folder = './output/sboxes_datasets'
    csv_filenames = os.listdir(csv_folder)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    result_df = pd.DataFrame()
    for csv_filename in csv_filenames:
        df = pd.read_csv(f'{csv_folder}/{csv_filename}')
        sboxes = df['SBoxes']
        print('\n##########################')
        print(csv_filename)
        print()
        for sbox in sboxes:
            linear_props = get_linear_properties_for_sbox(sbox)
            print(' - - - - - - - - - - - - - - - - ')
            print(sbox)
            print(linear_props)
            print()


def get_linear_properties_for_sbox(sbox):
    sboxArr = json.loads(sbox)
    sageSbox = SBox(sboxArr)

    lat = sageSbox.linear_approximation_table()
    lat_items = analyzer.countItemsInDdt(lat, len(sboxArr))
    # lat_stats = analyzer.getStatsFromDdtItems(lat_items)
    return lat_items


analyzer = DifferenceDistributionTableAnalyzer()
process_files()
