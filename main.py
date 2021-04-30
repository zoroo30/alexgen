from nfa import NFA
from dfa import DFA


def main():
    # NFA
    initial_state = {0}
    final_states = {2: 0}
    alphabet = {0, 1}
    transition_table = {
        0: {0: {1}, 1: {5}},
        1: {0: {6}, 1: {2}},
        2: {0: {0}, 1: {2}},
        3: {0: {2}, 1: {6}},
        4: {0: {7}, 1: {5}},
        5: {0: {2}, 1: {6}},
        6: {0: {6}, 1: {4}},
        7: {0: {6}, 1: {2}},
    }

    nfa_1 = NFA(initial_state, final_states, alphabet, transition_table)
    dfa = DFA(nfa_1)

    nfa_1.visualize("nfa.html")
    dfa.visualize("dfa.html")


if __name__ == "__main__":
    main()
