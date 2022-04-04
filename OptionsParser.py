#!/usr/bin/sage -python

import argparse

# own libraries
from SboxGenerator import SboxGeneratorMethods
from SboxAnalyzer import AnalyzeCriteria
from Logger import Logger


class Options:
    def __init__(self):
        self

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

        # sbox options
        self.generation_options = GenerationOptions()

        # properties to analyze
        self.analyze_options = AnalyzeCriteria()

        # export results options
        self.export_options = ExportOptions()

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
        sbox_options_group.add_argument('-n', type=int, action='store', nargs='?', const=1,
            help='Number of SBoxes to be generated. Default n = 1.')
        sbox_options_group.add_argument('-s', type=int, action='store', nargs='?', const=16,
            help='Size of SBox (power of 2). Default s = 4.')
        sbox_options_group.add_argument('-b', '--sbox', type=str, action='store',
            help='SBox (use \'\').')

        sbox_analyzing_group = parser.add_argument_group('S-box analyzing options.')
        sbox_analyzing_group.add_argument('--ddt', action='store_true',
            help='Analyze difference distribution table of SBoxes')
        # sbox_analyzing_group.add_argument('')

        sbox_export_group = parser.add_argument_group('export results options')
        sbox_export_group.add_argument('--export_csv', action='store_true',
            help='Export generated SBoxes to CSV')
        # sbox_export_group.add_argument('--export_csv', action='store_true'. nargs='?', const=0,
        #     help='Export generated SBoxes to CSV')

        parser.add_argument('--version', action='version',
            help='Version of Sbox Tool.', version='%(prog)s ' + str(self.version))

        parser.add_argument('--verbose', action='store_true',
            help='Print all the processes on to console.')

        return parser

    def parse_args(self, args):
        logger = Logger.getLogger(verbose=True)
        logger.log('...Parsing options...')

        if args.random or args.evolute or args.affine or args.ddt:
            logger.log('SBox source: generation')
            logger.log('Generation method: ', end='')
            sbox = None
            if args.random:
                method = SboxGeneratorMethods.RandomGeneration
                logger.log('Random generation')
            elif args.evolute:
                method = SboxGeneratorMethods.EvolutionaryGeneration
                logger.log('Evolutionary generation')
            elif args.affine:
                method = SboxGeneratorMethods.MathematicalConstruction
                logger.log('Mathematical construction')
            elif args.ddt:
                method = SboxGeneratorMethods.DDTConstruction
                logger.log('Randomized algorithm to construct S-boxes with required spectrum based on Difference Distribution Table properties')

        if method and (args.n is None or args.s is None):
            if args.n is None:
                n = 1
            if args.s is None:
                s = 4

        if method == None and args.sbox == None:
            parser.error('Select a method for S-Boxes generation or provide some SBox for analyzing.')

        if args.n:
            n = int(args.n)

        if args.s:
            s = int(args.s)

        if args.sbox:
            sbox = args.sbox

        if args.export_csv:
            export_csv = args.export_csv

        if args.verbose:
            verbose = args.verbose
        else:
            verbose = False

        logger.log(f'Number of SBoxes to generate: {n}')
        logger.log(f'Size of SBoxes (power of 2): {s}')

        logger.log(f'Verbose: {verbose}')

        logger.log('...End of parsing options...\n')

        # -------------------------- save parameters

        self.generation_options.generation_method = method
        self.generation_options.number_of_sboxes = n
        self.generation_options.size_of_sboxes = s

        return self
