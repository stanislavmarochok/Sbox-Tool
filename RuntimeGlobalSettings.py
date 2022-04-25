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
            self.number_of_sboxes = 1
            self.power_size_of_sbox = 4
            self.output_folder = 'output'
            self.generation_method = SboxGeneratorMethods.RandomGeneration

            self.disabled_export_csv = False
            self.disabled_output_console = False
            self.disabled_output_files = False

            self.ddt_limit = None
            self.ddt_max_item = 4

            RuntimeGlobalSettings._instance = self
