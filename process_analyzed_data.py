#!/usr/bin/python3

import pandas as pd
import numpy as np
import os

from ExportHelper import ExportHelper

def process_data():
    csv_folder = './output/sboxes_datasets'
    csv_filenames = os.listdir(csv_folder)

    pd.set_option('display.max_columns', 10)

    result_df = pd.DataFrame()
    for csv_filename in csv_filenames:
        new_row = process_file(csv_filename, csv_folder)
        result_df = result_df.append(new_row, ignore_index=True)

    result_df['sboxes_count'] = result_df['sboxes_count'].astype(int)
    result_df['sboxes_size'] = result_df['sboxes_size'].astype(int)

    columns = [column_name for column_name in result_df.columns if 'sboxes_count_with' in column_name]
    for column_name in columns:
        result_df[column_name] = result_df[column_name].fillna(0).astype(int)

    print(result_df)

    exportHelper = ExportHelper()
    exportHelper.exportDataframeToCsvToFolder(result_df, 'output', 'sboxes_datasets_processed', 'statistics.csv')


def process_file(csv_filename, csv_folder):
    full_path = f'{csv_folder}/{csv_filename}'
    df = pd.read_csv(full_path)
    time_elapsed_column = df['time_elapsed']

    clean_csv_filename = csv_filename[:-4]

    result = {}
    result['filename'] = csv_filename
    result['average_time'] = get_average_time_taken_for_sbox_generation(time_elapsed_column)
    result['all_time'] = get_all_time_taken_for_sboxes_generation(time_elapsed_column)
    result['sboxes_count'] = get_sboxes_count(clean_csv_filename)
    result['sboxes_size'] = 2 ** get_sboxes_size(clean_csv_filename)

    max_items_column = df['max_item']
    max_items = get_sboxes_count_with_max_item(max_items_column)
    for max_item in max_items.keys():
        result[f'sboxes_count_with_max_item_{max_item}'] = max_items.get(f'{max_item}')

        max_items_count_for_max_item = get_sboxes_count_with_max_item_count_for_max_item(max_item, max_items_column, df['max_item_count'])
        for max_item_count in max_items_count_for_max_item.keys():
            result[f'sboxes_count_with_max_item_{max_item}_max_item_count_{max_item_count}'] = max_items_count_for_max_item.get(f'{max_item_count}')

    zero_items_count = get_sboxes_count_with_zero_items_count(max_item, df['zero_items_count'])
    for zero_items_value in zero_items_count.keys():
        result[f'sboxes_count_with_zero_items_value_{zero_items_value}'] = zero_items_count.get(f'{zero_items_value}')

    return result


def get_sboxes_count_with_max_item(max_items):
    max_item_result = {}
    for item in max_items:
        if max_item_result.get(str(item)) is None:
            max_item_result[str(item)] = 0
        max_item_result[str(item)] += 1
    return max_item_result


def get_sboxes_count_with_zero_items_count(max_item, zero_items_count_column):
    zero_items_count_result = {}
    for zero_items_count_index in range(len(zero_items_count_column)):
        zero_items_count = zero_items_count_column[zero_items_count_index]
        if zero_items_count_result.get(str(zero_items_count)) is None:
            zero_items_count_result[f'{zero_items_count}'] = 0

        zero_items_count_result[f'{zero_items_count}'] += 1
    return zero_items_count_result


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

process_data()

