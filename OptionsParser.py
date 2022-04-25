#!/usr/bin/python

import argparse

# own libraries
from SboxGenerator import SboxGeneratorMethods
from SboxAnalyzer import AnalyzeCriteria
from Logger import Logger
from RuntimeGlobalSettings import RuntimeGlobalSettings

class CommonOptions:
    def __init__(self):
        self.disabled_output_console = False
        self.disabled_output_files = False

class GenerationOptions:
    def __init__(self):
        self.number_of_sboxes = 1
        self.size_of_sboxes = 16

        self.generation_method = SboxGeneratorMethods.RandomGeneration
        self.generate_new_sboxes = True

class ExportOptions:
    def __init__(self):
        self.export_csv = True

class OptionsParser:
    def __init__(self):
        self.version = 0.1
        self.verbose = False
        self.logger = Logger(log_files=['options_parser', 'log'])

        # sbox options
        self.generation_options = GenerationOptions()

        # properties to analyze
        self.analyze_options = AnalyzeCriteria()

        # export results options
        self.export_options = ExportOptions()

        # common options
        self.common_options = CommonOptions()

    """
    Parse the arguments from the input
    """
    def get_parser(self):
        parser = argparse.ArgumentParser(description='SBox tool', prog='SBox Generating & Analyzing Tool')

        generation_methods_group = parser.add_argument_group('methods of generation')
        generation_methods_group.add_argument('-r', '--random', action='store_true',
            help='Use random method for S-box generation.')
        generation_methods_group.add_argument('-e', '--evolute', action='store_true',
            help='Use evolutionary method for S-box generation.')
        generation_methods_group.add_argument('-a', '--affine', action='store_true',
            help='Use mathematical construction for S-box generation.')
        generation_methods_group.add_argument('-ddt', '--partially-smooth', action='store_true',
            help='Use Partially smooth difference table randomized algorithm for S-box generation.')


        sbox_options_group = parser.add_argument_group('S-box options')
        sbox_options_group.add_argument('-n', type=int, action='store', default=1,
            help='Number of SBoxes to be generated. Default n = 1.')
        sbox_options_group.add_argument('-s', type=int, action='store', default=4,
            help='Size of SBox (power of 2). Default s = 4.')
        sbox_options_group.add_argument('-b', '--sbox', type=str, action='store',
            help='SBox (use \'\').')

        sbox_analyzing_group = parser.add_argument_group('S-box analyzing options.')
        sbox_analyzing_group.add_argument('--ddt', action='store_true',
            help='Analyze difference distribution table of SBoxes')

        sbox_analyzing_group.add_argument('--ddt-limit', type=int, action='store', dest='ddt_limit', default=None,
            help='Limit for DDT generation method')

        sbox_analyzing_group.add_argument('--ddt-max-item', type=int, action='store', dest='ddt_max_item', default=4,
            help='Parameter of `satisfies_conditions` function in DDT generation method, defines custom max_item in a difference distribution table of a partial SBox to satisfy conditions')

        sbox_export_group = parser.add_argument_group('export results options')
        sbox_export_group.add_argument('--dEC', action='store_true', default=False,
            help='Disable export of generated SBoxes to CSV')

        parser.add_argument('--version', action='version',
            help='Version of Sbox Tool.', version='%(prog)s ' + str(self.version))

        parser.add_argument('--dC', action='store_true',
            help='Disable printing logs on the screen (console output).')

        parser.add_argument('--dF', action='store_true',
            help='Disable printing logs to files.')

        parser.add_argument('--output-folder', metavar='', dest='output_folder', default='output',
                help='Define custom output folder.')

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

        if args.random or args.evolute or args.affine or args.ddt:
            logger.logInfo('SBox source: generation')
            logger.logInfo('Generation method: ')
            sbox = None
            if args.random:
                method = SboxGeneratorMethods.RandomGeneration
                logger.logInfo('Random generation')
            elif args.evolute:
                method = SboxGeneratorMethods.EvolutionaryGeneration
                logger.logInfo('Evolutionary generation')
            elif args.affine:
                method = SboxGeneratorMethods.MathematicalConstruction
                logger.logInfo('Mathematical construction')
            elif args.ddt:
                method = SboxGeneratorMethods.DDTConstruction
                logger.logInfo('Randomized algorithm to construct S-boxes with required spectrum based on Difference Distribution Table properties')
        else:
            method = SboxGeneratorMethods.RandomGeneration
        
        global_settings.generation_method = method
        
        if method == None and args.sbox == None:
            error_msg = 'Select a method for S-Boxes generation or provide some SBox for analyzing.'
            logger.logError(error_msg)
            parser.error(error_msg)

        if args.n:
            n = int(args.n)

        if args.s:
            s = int(args.s)

        if args.sbox:
            sbox = args.sbox

        global_settings.disabled_export_csv = args.dEC

        if args.ddt_limit is None:
            args.ddt_limit = n
        global_settings.ddt_limit = args.ddt_limit

        global_settings.ddt_max_item = args.ddt_max_item

        disabled_output_console = False
        if args.dC:
            disabled_output_console = args.dC

        disabled_output_files = False
        if args.dF:
            disabled_output_files = args.dF

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
