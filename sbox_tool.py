#!/usr/bin/python3

# own libraries
from ExportHelper import ExportHelper
from OptionsParser import OptionsParser
from SboxAnalyzer import SboxAnalyzer
from SboxGenerator import SboxGenerator


class SBoxTool:
    def __init__(self):
        pass

    def run_tool(self):
        # -------------------------------- Main program section
        self.options_parser = OptionsParser()
        parser = self.options_parser.get_parser()
        options = self.options_parser.parse_args(parser.parse_args())

        sboxes = []
        if options.generation_options.generate_new_sboxes:
            self.generator = SboxGenerator()
            generated_sboxes_result = self.generator.generateSboxes(
                    options.generation_options.number_of_sboxes,
                    options.generation_options.size_of_sboxes,
                    options.generation_options.generation_method)
        # TODO: handle an input of prepared S-Boxes

        self.sbox_analyzer = SboxAnalyzer()
        analyzed_sboxes = self.sbox_analyzer.analyzeSboxesWithCriteria(generated_sboxes_result, options.analyze_options)
        sboxes_stats = self.sbox_analyzer.analyzeStatsOfSboxes(analyzed_sboxes)

        # TODO: add columns with analyze criteria 
        self.export_helper = ExportHelper()
        export_result = self.export_helper.exportAnalyzedSboxes(analyzed_sboxes)
        export_stats = self.export_helper.exportSboxesStats(sboxes_stats)


if __name__ == '__main__':
    sboxTool = SBoxTool()
    sboxTool.run_tool()
