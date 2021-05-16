from lexical_analyzer.dfa import DFA
from lexical_analyzer.lexer import Lexer
from lexical_analyzer.lex_rules import generate_nfa


def get_lexer():
    final_nfa, id_tokens = generate_nfa("lexical.txt")
    final_nfa.labels = id_tokens

    dfa = DFA(final_nfa)
    dfa.labels = id_tokens

    lexer = Lexer("program.txt", dfa)
    lexer.analyze()
    lexer.writeOutput()

    return lexer, final_nfa, dfa
