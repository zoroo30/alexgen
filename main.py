# from dfa import DFA
# from lexer import Lexer
from lex_rules import generate_nfa

final_nfa, id_lexeme = generate_nfa("inputs/lexical.txt")

# dfa = DFA(final_nfa)
# dfa.labels = id_lexeme

# lexer = Lexer("program.txt", dfa)
# lexer.analyze()
# lexer.writeOutput()

# final_nfa.visualize("test.html", id_lexeme)
# dfa.visualize("dfa.html", id_lexeme, False)
