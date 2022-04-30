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

    result_df['sboxes_count'] = result_df['sboxes_count'].astype(int)
    result_df['sboxes_size'] = result_df['sboxes_size'].astype(int)
    
    print(result_df)
    for max_item in [4, 6, 8, 10]:
        result_df[f'sboxes_count_with_max_item_{max_item}'] = result_df[f'sboxes_count_with_max_item_{max_item}'].fillna(0).astype(int)

    print(result_df.head())


def process_file(csv_filename, csv_folder):
    full_path = f'{csv_folder}/{csv_filename}'
    df = pd.read_csv(full_path)
    time_elapsed_column = df['time_elapsed']
    
    # delete ending '.csv' from the filename
    clean_csv_filename = csv_filename[:-4]

    result = {}
    result['filename'] = csv_filename
    result['average_time'] = get_average_time_taken_for_sbox_generation(time_elapsed_column)
    result['all_time'] = get_all_time_taken_for_sboxes_generation(time_elapsed_column)
    result['sboxes_count'] = get_sboxes_count(clean_csv_filename)
    result['sboxes_size'] = 2 ** get_sboxes_size(clean_csv_filename)

    max_items_column = df['max_item']
    max_items = get_sboxes_count_with_max_item(max_items_column)
    print(max_items)
    for max_item in max_items.keys():
        result[f'sboxes_count_with_max_item_{max_item}'] = max_items.get(f'{max_item}')

        # TODO: get 2 columns - max_item and max_item_count
        max_items_count_for_max_item = get_sboxes_count_with_max_item_count_for_max_item(max_item, max_items_column, df['max_item_count'])
        for max_item_count in max_items_count_for_max_item.keys():
            result[f'sboxes_count_with_max_item_count_{max_item_count}'] = max_items_count_for_max_item.get(f'{max_item_count}')

    return result


def get_sboxes_count_with_max_item(max_items):
    max_item_result = {}
    for item in max_items:
        if max_item_result.get(str(item)) is None:
            max_item_result[str(item)] = 0
        max_item_result[str(item)] += 1
    return max_item_result


def get_sboxes_count_with_max_item_count_for_max_item(max_item, max_item_column, max_items_count_column):
    max_item_count_result = {}
    for max_item_count_index in range(len(max_items_count_column)):
        max_item_count = max_items_count_column[max_item_count_index]
        if max_item_count_result.get(str(max_item_count)) is None:
            max_item_count_result[f'{max_item_count}'] = 0
        
        if int(max_item_column[max_item_count_index]) == int(max_item):
            max_item_count_result[f'{max_item_count}'] += 1
    return max_item_count_result


def get_average_time_taken_for_sbox_generation(time_elapsed_column):
    return time_elapsed_column.mean()


def get_all_time_taken_for_sboxes_generation(time_elapsed_column):
    return time_elapsed_column.sum()


def get_sboxes_count(csv_filename):
    filename_parts = csv_filename.split('_')
    sboxes_count_part = filename_parts[1]
    sboxes_count_str = sboxes_count_part[1:]
    return int(sboxes_count_str)


def get_sboxes_size(csv_filename):
    filename_parts = csv_filename.split('_')
    sboxes_size_part = filename_parts[2]
    sboxes_size_str = sboxes_size_part[1:]
    return int(sboxes_size_str)

run_processing_data()

