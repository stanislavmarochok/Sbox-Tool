#!/usr/bin/sage -python

import pandas as pd
import os

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

        if not os.path.exists('output'):
            os.mkdir('output')

        df.to_csv(f'output/{filename}')
        return True
