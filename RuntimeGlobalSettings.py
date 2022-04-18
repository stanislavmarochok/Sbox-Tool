#!/usr/bin/python

class RuntimeGlobalSettings:
    _instance = None

    @staticmethod
    def getInstance():
        if RuntimeGlobalSettings._instance == None:
            RuntimeGlobalSettings()
        return RuntimeGlobalSettings._instance

    def __init__(self):
        if RuntimeGlobalSettings._instance != None:
            raise Exception('RuntimeGlobalSettings is a singleton!')
        else:
            self.disabled_output_console = False
            self.disabled_output_files = False
            self.number_of_sboxes = 1
            self.power_size_of_sbox = 4

            RuntimeGlobalSettings._instance = self
