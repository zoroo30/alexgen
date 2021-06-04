from lexical_analyzer_generator.get_lexer import get_lexer
from parser_generator.get_parser import get_parser
from parser_generator.testing_tokens import TestingTokens
import os

os.environ["LEXER_INPUT_FOLDER"] = "inputs/"
os.environ["LEXER_OUTPUT_FOLDER"] = "outputs/lexer/"
os.environ["PARSER_INPUT_FOLDER"] = "inputs/"
os.environ["PARSER_OUTPUT_FOLDER"] = "outputs/parser/"


def main():
    # get lexer from phase 1
    lexer = get_lexer("lexical.txt")

    # analyze program file and generate lexer output
    lexer.analyze_file("case1.txt")
    lexer.analyze()
    lexer.writeOutput()

    # parser needs get_next_token function
    parser = get_parser("input_CFG_LL.txt")
    parser.set_input_src(lexer.get_next_token)
    parser.parse()
    # parser.write_output()

    # parser = get_parser("grammar.txt")
    # parser.set_input_src()
    # parser.parse()


if __name__ == "__main__":
    main()
