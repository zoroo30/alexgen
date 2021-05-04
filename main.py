from dfa import DFA
from lexer import Lexer
from lex_rules import generate_nfa


def main():
    # NFA
#     labels = {
#         0: "p1",
#         1: "p2",
#         2: "p3",
#     }
#     initial_state = {0}
#     final_states = {3: 0, 7: 1, 10: 2}
#     alphabet = {"a", "b"}
#     transition_table = {
#         0: {"": {1, 4, 8}},
#         1: {"b": {2}},
#         2: {"a": {3}},
#         3: {},
#         4: {"b": {5}},
#         5: {"a": {6}},
#         6: {"b": {7}},
#         7: {},
#         8: {"b": {9}},
#         9: {"": {10}, "b": {9}},
#         10: {"a": {10}},
#     }

#     nfa_1 = NFA(initial_state, final_states, alphabet, transition_table)

#     dfa = DFA(nfa_1)
#     dfa.labels = labels
    # nfa_1.visualize("nfa.html", labels)
    # dfa.visualize("dfa.html", labels)

#     lexer = Lexer("program.txt", dfa)
#     lexer.analyze()
#     lexer.writeOutput()


    final_nfa, id_lexeme = generate_nfa("inputs/lexical.txt")

    dfa = DFA(final_nfa)
    dfa.labels = id_lexeme

    lexer = Lexer("program.txt", dfa)
    lexer.analyze()
    lexer.writeOutput()

    final_nfa.visualize("test.html", id_lexeme)
    dfa.visualize("dfa.html", id_lexeme, False)


if __name__ == "__main__":
    main()
