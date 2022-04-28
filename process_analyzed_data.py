#!/usr/bin/python

import pandas as pd
import numpy as np
import os

def run_processing_data():
    csv_folder = './output/sboxes_datasets'
    csv_filenames = os.listdir(csv_folder)

    pd.set_option('display.max_columns', 10)

    # process the files with pandas

    columns = ['filename', 'average_time', 'all_time']

    result_df = pd.DataFrame(columns=columns)
    for csv_filename in csv_filenames:
        new_row = process_file(csv_filename, csv_folder)
        result_df = result_df.append(new_row, ignore_index=True)

    print(result_df.head())


def process_file(csv_filename, csv_folder):
    full_path = f'{csv_folder}/{csv_filename}'
    df = pd.read_csv(full_path)
    time_elapsed_column = df['time_elapsed']

    result = {}
    result['filename'] = csv_filename
    result['average_time'] = get_average_time_taken_for_sbox_generation(time_elapsed_column)
    result['all_time'] = get_all_time_taken_for_sboxes_generation(time_elapsed_column)

    return result


def get_average_time_taken_for_sbox_generation(time_elapsed_column):
    return time_elapsed_column.mean()


def get_all_time_taken_for_sboxes_generation(time_elapsed_column):
    return time_elapsed_column.sum()

run_processing_data()

