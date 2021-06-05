from parser_generator.grammar_visualizer import GrammarVisualizer
from parser_generator.grammar_preprocessor import GrammarPreprocessor
from parser_generator.grammar_input_handler import GrammarInputHandler
from parser_generator.parser_generator import ParserGenerator
import pandas as pd


def get_parser(grammar_file_path, preprocess=True, visulize=False):
    visulaizer = GrammarVisualizer()

    grammar = GrammarInputHandler(grammar_file_path)
    if visulize:
        visulaizer.set_grammar(grammar.grammar)
        visulaizer.draw_transition_diagrams()

    if preprocess:
        grammar = GrammarPreprocessor(grammar)
        if visulize:
            visulaizer.set_grammar(grammar.grammar)
            visulaizer.draw_transition_diagrams(
                output_file="transition_diagrams_ll1.html"
            )

    parser_generator = ParserGenerator(grammar)
    parser = parser_generator.generate()

    return parser
