#!/usr/bin/python

import pandas as pd
import os

from RuntimeGlobalSettings import RuntimeGlobalSettings


class ExportHelper:
    def __init__(self):
        pd.set_option('display.max_column', 10)
        pass

    def exportDataToCsv(self, obj, filename):
        df = pd.DataFrame(obj)
        df.to_csv(f'{filename}.csv')
        return True

    def exportDataframeToCsvToFolder(self, df, output_folder, output_subfolder, filename):
        if not os.path.exists(f'{output_folder}'):
            os.mkdir(f'{output_folder}')

        if not os.path.exists(f'{output_folder}/{output_subfolder}'):
            os.mkdir(f'{output_folder}/{output_subfolder}')

        full_filename = f'{output_folder}/{output_subfolder}/{filename}'
        df.to_csv(full_filename)

    def exportAnalyzedSboxes(self, obj, output_folder=None, output_subfolder=None, filename=None):
        if obj is None:
            print('There is nothing to export.')
            return False

        settings = RuntimeGlobalSettings.getInstance()
        if settings.disabled_export_csv == True:
            return False

        settings = RuntimeGlobalSettings.getInstance()
        if output_folder is None:
            output_folder = settings.output_folder

        if output_subfolder is None:
            output_subfolder = 'sboxes_datasets'

        if not os.path.exists(f'{output_folder}'):
            os.mkdir(f'{output_folder}')

        if not os.path.exists(f'{output_folder}/{output_subfolder}'):
            os.mkdir(f'{output_folder}/{output_subfolder}')

        if filename is None:
            filename = self.getFilename()

        self.exportDataToCsv(obj, f'{output_folder}/{output_subfolder}/{filename}')

    def exportSboxesStats(self, sbox_stats):
        for key, value in sbox_stats.items():
            settings = RuntimeGlobalSettings.getInstance()
            output_folder = settings.output_folder
            output_subfolder = 'sbox_stats'

            if not os.path.exists(f'{output_folder}'):
                os.mkdir(f'{output_folder}')

            if not os.path.exists(f'{output_folder}/{output_subfolder}'):
                os.mkdir(f'{output_folder}/{output_subfolder}')

            filename = self.getFilename()
            self.exportDataToCsv(value, f'{output_folder}/{output_subfolder}/stats_{filename}_{key}')

    def getFilename(self):
        settings = RuntimeGlobalSettings.getInstance()
        if settings.generation_method.name == 'PrescribedDDT':
            return f'{settings.generation_method.name}_n{settings.number_of_sboxes}_s{settings.power_size_of_sbox}_prescribedDdMaxItem{settings.prescribed_ddt_max_item}'
        else:
            return f'{settings.generation_method.name}_n{settings.number_of_sboxes}_s{settings.power_size_of_sbox}'
