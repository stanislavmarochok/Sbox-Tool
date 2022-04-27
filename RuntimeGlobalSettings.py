#!/usr/bin/python

class RuntimeGlobalSettings:
    _instance = None

    @staticmethod
    def getInstance():
        if RuntimeGlobalSettings._instance == None:
            RuntimeGlobalSettings()
        return RuntimeGlobalSettings._instance

    def __init__(self):
        from SboxGenerator import SboxGeneratorMethods

        if RuntimeGlobalSettings._instance != None:
            raise Exception('RuntimeGlobalSettings is a singleton!')
        else:
            self.number_of_sboxes = None
            self.power_size_of_sbox = None
            self.output_folder = None
            self.generation_method = SboxGeneratorMethods.RandomGeneration
            self.generation_timeout = None

            self.disabled_export_csv = False
            self.disabled_output_console = False
            self.disabled_output_files = False

            self.analyzeCriteria = {}
            self.analyzeCriteria['difference_distribution_table'] = False
            self.analyzeCriteria['bijection'] = False
            self.analyzeCriteria['nonlinearity'] = False

            self.prescribed_ddt_max_item = None

            RuntimeGlobalSettings._instance = self
