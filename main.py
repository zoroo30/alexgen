from lexical_analyzer_generator.get_lexer import get_lexer
from parser_generator.get_parser import get_parser
from parser_generator.testing_tokens import TestingTokens
import os, sys, getopt

os.environ["LEXER_INPUT_FOLDER"] = "inputs/"
os.environ["LEXER_OUTPUT_FOLDER"] = "outputs/lexer/"
os.environ["PARSER_INPUT_FOLDER"] = "inputs/"
os.environ["PARSER_OUTPUT_FOLDER"] = "outputs/parser/"


def get_system_parameters(argv):
    lexical_rules_file = ""
    program_file = ""
    grammar_file = ""
    if len(argv) >= 1:
        lexical_rules_file = argv[0]
    if len(argv) >= 2:
        program_file = argv[1]
    if len(argv) >= 3:
        grammar_file = argv[2]
    print('lexical file is "', lexical_rules_file)
    print('program file is "', program_file)
    print('grammar file is "', grammar_file)
    return lexical_rules_file, program_file, grammar_file


def main(argv):
    lexical_rules_file, program_file, grammar_file = get_system_parameters(argv)

    # get lexer from phase 1
    if lexical_rules_file:
        lexer = get_lexer(lexical_rules_file, True, True)
    else:
        print("you have to enter the lexical_rules file path")

    # analyze program file and generate lexer output
    if program_file:
        lexer.analyze_file(program_file)
        lexer.analyze()
        lexer.writeOutput()

    # parser needs get_next_token function
    if grammar_file:
        parser = get_parser(grammar_file, True, True)
        parser.set_input_src(lexer.get_next_token)
        parser.parse()
        parser.writeOutput()

    # parser = get_parser("grammar.txt")
    # parser.set_input_src()
    # parser.parse()


if __name__ == "__main__":
    main(sys.argv[1:])
