from parser_generator.grammar_input_handler import GrammarInputHandler
from parser_generator.parser_generator import ParserGenerator
import pandas as pd


def get_parser(grammar_file_path):
    grammar = GrammarInputHandler(grammar_file_path)
    # print(grammar.grammar)
    # print("\n".join(f'{v:9,} {k}' for k, v in grammar.grammar.items()))
    df = pd.DataFrame(grammar.grammar.items(), columns=[" ", "Productions"])
    # print(grammar.non_terminals)
    #df = pd.DataFrame(grammar.non_terminals, columns=[" ", "Productions"])
    # print(df)
    # print(grammar.terminals)

    # print(grammar.non_terminals)
    parser_generator = ParserGenerator(grammar)
    # print("created")
    parser = parser_generator.generate()
    # print("generated")

    return parser
