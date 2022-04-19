#!/usr/bin/sage -python

import pandas as pd
import os

from RuntimeGlobalSettings import RuntimeGlobalSettings

class ExportHelper:
    def __init__(self):
        self.filename = 'test'

    def __init__(self, filename):
        self.filename = filename

    @staticmethod
    def exportDataToCsv(obj, filename):
        if obj is None:
            return False

        df = pd.DataFrame(obj)

        settings = RuntimeGlobalSettings.getInstance()
        output_folder = settings.output_folder

        if not os.path.exists(f'{output_folder}'):
            os.mkdir(f'{output_folder}')

        df.to_csv(f'{output_folder}/{filename}')
        return True
