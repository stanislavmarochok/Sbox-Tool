#!/usr/bin/sage -python

import pandas as pd

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

        df.to_csv(filename)
        return True
