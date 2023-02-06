#!/usr/bin/python3

import enum
import numpy as np
import time

from Logger import Logger


class SboxGeneratorMethods(enum.Enum):
    RandomGeneration = 1,
    EvolutionaryGeneration = 2,
    MathematicalConstruction = 3.
    PrescribedDDT = 4


class SboxResult:
    def __init__(self, sbox):
        self.sbox = sbox
        self.meta_data = {}
        self.error = False

        try:
            if self.sbox == -1 or self.sbox == False:
                self.error = True
        except:
            pass

    def addMetaData(self, _meta_data_item, _value):
        if self.meta_data is None:
            self.meta_data = {}

        self.meta_data[_meta_data_item] = _value


class SboxGenerator:
    def __init__(self):
        self.logger = Logger(log_files=['sbox_generator', 'log'], disabled_output_console=False,
                             disabled_output_files=False)

    def generateSboxes(self, number_of_sboxes, size_of_sboxes, generation_method: SboxGeneratorMethods):
        generated_sboxes_result = []
        for index_of_sbox in range(number_of_sboxes):
            generated_sbox_result = self.generateSbox(2 ** size_of_sboxes, generation_method)
            if generated_sbox_result.error == False:
                generated_sboxes_result.append(generated_sbox_result)

        return generated_sboxes_result

    def generateSbox(self, size_of_sbox, generation_method):
        logger = self.logger

        method = self.random_generation
        if generation_method == SboxGeneratorMethods.RandomGeneration:
            method = self.random_generation
        elif generation_method == SboxGeneratorMethods.EvolutionaryGeneration:
            method = self.evolutionary_generation
        elif generation_method == SboxGeneratorMethods.MathematicalConstruction:
            method = self.mathematical_generation
        elif generation_method == SboxGeneratorMethods.PrescribedDDT:
            method = self.prescribed_ddt

        if method is None:
            logger.logInfo('Error: Generation method not recognized!')
            return False

        start_time = time.time()
        generated_sbox = method(size_of_sbox)
        end_time = time.time()
        time_elapsed = end_time - start_time

        sbox_generator_result = SboxResult(generated_sbox)
        sbox_generator_result.addMetaData('time_elapsed', time_elapsed)
        sbox_generator_result.addMetaData('generation_method', generation_method.name)
        return sbox_generator_result

    def random_generation(self, size_of_sbox):
        new_sbox = np.random.RandomState().permutation(size_of_sbox)
        self.logger.logInfo(f"New S-box: {new_sbox}")
        return new_sbox

    def evolutionary_generation(self, size_of_sbox):
        # TODO: finish the method
        return self.random_generation(size_of_sbox)

    def mathematical_generation(self, size_of_sbox):
        # TODO: finish the method
        return self.random_generation(size_of_sbox)

    def prescribed_ddt(self, size_of_sbox):
        # TODO: finish the method
        from generators.PrescribedDDT import PrescribedDDT as gen
        generator = gen()
        return generator.generateSbox(size_of_sbox)
