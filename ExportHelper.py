#!/usr/bin/sage -python

import pandas as pd
import os

from RuntimeGlobalSettings import RuntimeGlobalSettings

class ExportHelper:
    def exportDataToCsv(self, obj, filename):
        if obj is None:
            return False

        settings = RuntimeGlobalSettings.getInstance()
        if settings.disabled_export_csv == True:
            return False

        df = pd.DataFrame(obj)

        settings = RuntimeGlobalSettings.getInstance()
        output_folder = settings.output_folder

        if not os.path.exists(f'{output_folder}'):
            os.mkdir(f'{output_folder}')

        df.to_csv(f'{output_folder}/{filename}')
        return True

    def exportSboxesStats(self, sbox_stats):
        for key, value in sbox_stats.items():
            settings = RuntimeGlobalSettings.getInstance()
            output_folder = settings.output_folder

            if not os.path.exists(f'{output_folder}'):
                os.mkdir(f'{output_folder}')

            if not os.path.exists(f'{output_folder}/sbox_stats'):
                os.mkdir(f'{output_folder}/sbox_stats')

            self.exportDataToCsv(value, f'sbox_stats/stats_{key}.csv')
