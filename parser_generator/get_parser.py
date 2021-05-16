from parser_generator.grammar_input_handler import GrammarInputHandler
from parser_generator.parser_generator import ParserGenerator


def get_parser(grammar_file_path):
    grammar = GrammarInputHandler(grammar_file_path)
    # print(grammar.grammar)

    # print(grammar.terminals)

    # print(grammar.non_terminals)
    parser_generator = ParserGenerator(grammar)

    parser = parser_generator.generate()

    return parser
