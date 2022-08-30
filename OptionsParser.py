#!/usr/bin/python

import argparse

# own libraries
from SboxGenerator import SboxGeneratorMethods
from SboxAnalyzer import AnalyzeCriteria
from Logger import Logger
from RuntimeGlobalSettings import RuntimeGlobalSettings


class GenerationOptions:
    def __init__(self):
        self.number_of_sboxes = 1
        self.size_of_sboxes = 16

        self.generation_method = SboxGeneratorMethods.RandomGeneration
        self.generate_new_sboxes = True


class OptionsParser:
    def __init__(self):
        self.parser = None
        self.version = 0.1

        self.logger = Logger(log_files=['options_parser', 'log'])

        # sbox options
        self.generation_options = GenerationOptions()

        # properties to analyze
        self.analyze_options = AnalyzeCriteria()

    """
    Parse the arguments from the input
    """

    def get_parser(self):
        parser = argparse.ArgumentParser(description='SBox tool', prog='SBox Generating & Analyzing Tool')

        generation_methods_group = parser.add_argument_group('Options of methods of generation')
        generation_methods_group.add_argument('--random-generation', action='store_true', dest='random_generation',
                                              help='Use random method for S-box generation.')
        generation_methods_group.add_argument('--prescribed-ddt', action='store_true', dest='prescribed_ddt',
                                              help='Use prescribed difference distribution table algorithm for S-box generation.')
        generation_methods_group.add_argument('--generation-timeout', type=int, action='store',
                                              dest='generation_timeout', default=None,
                                              help='Timeout for generation of 1 SBox')

        sbox_options_group = parser.add_argument_group('Options of SBoxes generation')
        sbox_options_group.add_argument('--sboxes-count', type=int, action='store', dest='n', default=1,
                                        help='Number of SBoxes to be generated. Default n = 1.')
        sbox_options_group.add_argument('--sboxes-size', type=int, action='store', dest='s', default=4,
                                        help='Size of SBox (power of 2). Default s = 4.')

        sbox_analyzing_group = parser.add_argument_group('S-box analyzing options.')
        sbox_analyzing_group.add_argument('--prescribed-ddt-max-item', type=int, action='store',
                                          dest='prescribed_ddt_max_item', default=4,
                                          help='Parameter of `satisfies_conditions` function in `Prescribed DDT` generation method, defines custom max_item in a difference distribution table of a partial SBox to satisfy conditions')
        sbox_analyzing_group.add_argument('--analyze-ddt', action='store_true', default=False, dest='analyze_ddt',
                                          help='Enable analyzing the difference distribution table of SBox (SBoxes)')
        sbox_analyzing_group.add_argument('--analyze-bijection', action='store_true', default=False,
                                          dest='analyze_bijection',
                                          help='Enable analyzing the bijection property of SBox (SBoxes)')

        sbox_export_group = parser.add_argument_group('Options of export of the result')
        sbox_export_group.add_argument('--dEC', action='store_true', default=False,
                                       help='Disable export of generated SBoxes to CSV')

        output_options_group = parser.add_argument_group('Options of output')
        output_options_group.add_argument('--dC', action='store_true',
                                          help='Disable printing logs on the screen (console output).')
        output_options_group.add_argument('--dF', action='store_true', help='Disable printing logs to files.')
        output_options_group.add_argument('-oF', metavar='', dest='output_folder', default='output',
                                          help='Folder where outputs will be saved.')

        parser.add_argument('--version', action='version', help='Version of Sbox Tool.',
                            version='%(prog)s ' + str(self.version))

        self.parser = parser

        return parser

    def parse_args(self, args):
        logger = self.logger
        # disabled output on screen if there was specified the option
        if args.dC:
            logger.disabled_output_console = args.dC
        if args.dF:
            logger.disabled_output_files = args.dF

        global_settings = RuntimeGlobalSettings.getInstance()
        global_settings.output_folder = args.output_folder

        logger.logInfo('...Parsing options...')

        # method = SboxGeneratorMethods.RandomGeneration

        logger.logInfo('SBox source: generation')
        logger.logInfo('Generation method: ')

        method = None
        if args.random_generation:
            method = SboxGeneratorMethods.RandomGeneration
            logger.logInfo('Random generation')
        elif args.prescribed_ddt:
            method = SboxGeneratorMethods.PrescribedDDT
            logger.logInfo('Randomized algorithm to construct S-boxes with prescribed difference distribution table')

        if method is None:
            error_msg = 'Select a method for S-Boxes generation or provide some SBox for analyzing.'
            logger.logError(error_msg)
            self.parser.error(error_msg)

        global_settings.generation_method = method
        global_settings.generation_timeout = args.generation_timeout

        n = None
        s = None

        if args.n:
            n = int(args.n)

        if args.s:
            s = int(args.s)

        global_settings.disabled_export_csv = args.dEC

        global_settings.prescribed_ddt_max_item = args.prescribed_ddt_max_item

        disabled_output_console = False
        if args.dC:
            disabled_output_console = args.dC

        disabled_output_files = False
        if args.dF:
            disabled_output_files = args.dF

        if args.analyze_ddt:
            self.analyze_options.addAnalyzeCriterion('difference_distribution_table')
            global_settings.analyzeCriteria['difference_distribution_table'] = args.analyze_ddt
        if args.analyze_bijection:
            self.analyze_options.addAnalyzeCriterion('bijection')
            global_settings.analyzeCriteria['bijection'] = args.analyze_bijection

        logger.logInfo(f'Number of SBoxes to generate: {n}')
        global_settings.number_of_sboxes = n

        logger.logInfo(f'Size of SBoxes (power of 2): {s}')
        global_settings.power_size_of_sbox = s

        logger.logInfo(f'Disabled output console: {disabled_output_console}')
        global_settings.disabled_output_console = disabled_output_console
        logger.disabled_output_console = global_settings.disabled_output_console

        logger.logInfo(f'Disabled output files: {disabled_output_files}')
        global_settings.disabled_output_files = disabled_output_files
        logger.disabled_output_files = global_settings.disabled_output_files

        logger.logInfo(f'Output folder: {args.output_folder}')
        global_settings.output_folder = args.output_folder

        logger.logInfo('...End of parsing options...')
        logger.logInfo()

        # -------------------------- save parameters

        self.generation_options.generation_method = method
        self.generation_options.number_of_sboxes = n
        self.generation_options.size_of_sboxes = s

        return self
