from lexical_analyzer_generator.dfa import DFA
from lexical_analyzer_generator.lexer import Lexer
from lexical_analyzer_generator.lex_rules import generate_nfa


def get_lexer(lexical_rules_file_path, visualize_nfa=False, visualize_dfa=False):
    final_nfa, id_tokens = generate_nfa(lexical_rules_file_path)
    final_nfa.labels = id_tokens

    dfa = DFA(final_nfa)
    dfa.labels = id_tokens

    if visualize_nfa:
        final_nfa.visualize("nfa.html")

    if visualize_dfa:
        dfa.visualize("dfa.html", False)

    lexer = Lexer(dfa)

    return lexer
