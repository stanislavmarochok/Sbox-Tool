#!/usr/bin/sage -python

import enum
import numpy as np
import time

from Logger import Logger

class SboxGeneratorMethods(enum.Enum):
    RandomGeneration = 1,
    EvolutionaryGeneration = 2,
    MathematicalConstruction = 3.
    DDTConstruction = 4

class SboxResult:
    def __init__(self, sbox):
        self.sbox = sbox
        self.meta_data = {}

    def addMetaData(self, _meta_data_item, _value):
        if self.meta_data is None:
            self.meta_data = {}

        self.meta_data[_meta_data_item] = _value

class SboxGenerator:
    def generateSboxes(self, number_of_sboxes, size_of_sboxes, generation_method : SboxGeneratorMethods):
        generated_sboxes_result = []
        for index_of_sbox in range(number_of_sboxes):
            generated_sbox_result = self.generateSbox(2 ** size_of_sboxes, generation_method)
            generated_sboxes_result.append(generated_sbox_result)

        return generated_sboxes_result

    def generateSbox(self, size_of_sbox, generation_method):
        logger = Logger.getLogger(verbose=True)

        method = self.random_generation
        if generation_method == SboxGeneratorMethods.RandomGeneration:
            method = self.random_generation
        elif generation_method == SboxGeneratorMethods.EvolutionaryGeneration:
            method = self.volutionary_generation
        elif generation_method == SboxGeneratorMethods.MathematicalConstruction:
            method = self.mathematical_generation
        elif generation_method == SboxGeneratorMethods.DDTConstruction:
            method = self.ddt_generation

        if method is None:
            logger.log('Error: Generation method not recognized!')
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
        return np.random.RandomState().permutation(size_of_sbox)

    def evolutionary_generation(self, size_of_sbox):
        # TODO: finish the method
        return self.random_generation(size_of_sbox)

    def mathematical_generation(self, size_of_sbox):
        # TODO: finish the method
        return self.random_generation(size_of_sbox)

    def ddt_generation(self, size_of_sbox):
        # TODO: finish the method
        from PartiallySmoothDifferenceTable import PartiallySmoothDifferenceTable as gen
        generator = gen()
        return generator.generateSbox(size_of_sbox)
