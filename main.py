from lexical_analyzer.get_lexer import get_lexer
import os

os.environ["LEXER_INPUT_FOLDER"] = "inputs/"
os.environ["LEXER_OUTPUT_FOLDER"] = "outputs/lexer/"


def main():
    # lexer, final_nfa, dfa = get_lexer()
    # final_nfa.visualize("nfa.html")
    # dfa.visualize("dfa.html", False)

    lexer, _, _ = get_lexer()

    next_token = lexer.get_next_token()
    while next_token != "$":
        print(next_token)
        next_token = lexer.get_next_token()


if __name__ == "__main__":
    main()
