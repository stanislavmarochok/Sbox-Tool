#!/usr/bin/python

import pandas as pd
import numpy as np
import os

def run_processing_data():
    csv_folder = './output/sboxes_datasets'
    csv_filenames = os.listdir(csv_folder)

    pd.set_option('display.max_columns', 10)

    # process the files with pandas

    result_df = pd.DataFrame()
    for csv_filename in csv_filenames:
        new_row = process_file(csv_filename, csv_folder)
        result_df = result_df.append(new_row, ignore_index=True)

    result_df['number_of_sboxes'] = result_df['number_of_sboxes'].astype(int)
    result_df['sboxes_size'] = result_df['sboxes_size'].astype(int)

    print(result_df.head())


def process_file(csv_filename, csv_folder):
    full_path = f'{csv_folder}/{csv_filename}'
    df = pd.read_csv(full_path)
    time_elapsed_column = df['time_elapsed']
    
    clean_csv_filename = csv_filename[:-4]

    result = {}
    result['filename'] = csv_filename
    result['average_time'] = get_average_time_taken_for_sbox_generation(time_elapsed_column)
    result['all_time'] = get_all_time_taken_for_sboxes_generation(time_elapsed_column)
    result['number_of_sboxes'] = get_number_of_sboxes(clean_csv_filename)
    result['sboxes_size'] = 2 ** get_sboxes_count(clean_csv_filename)

    return result


def get_average_time_taken_for_sbox_generation(time_elapsed_column):
    return time_elapsed_column.mean()


def get_all_time_taken_for_sboxes_generation(time_elapsed_column):
    return time_elapsed_column.sum()


def get_number_of_sboxes(csv_filename):
    filename_parts = csv_filename.split('_')
    number_of_sboxes_part = filename_parts[1]
    number_of_sboxes_str = number_of_sboxes_part[1:]
    return int(number_of_sboxes_str)


def get_sboxes_count(csv_filename):
    filename_parts = csv_filename.split('_')
    sboxes_count_part = filename_parts[2]
    sboxes_count_str = sboxes_count_part[1:]
    return int(sboxes_count_str)

run_processing_data()

