from nfa import NFA
from dfa import DFA


def main():
    # NFA
    initial_state = {0}
    final_states = {0: 0}
    alphabet = {"a", "b"}
    transition_table = {
        0: {"": {1}},
        1: {"a": {1, 2}, "b": {2}},
        2: {"a": {0, 2}, "b": {3}},
        3: {"b": {1}},
    }

    nfa_1 = NFA(initial_state, final_states, alphabet, transition_table)
    dfa = DFA(nfa_1)

    nfa_1.visualize("nfa.html")
    dfa.visualize("dfa.html")


if __name__ == "__main__":
    main()
