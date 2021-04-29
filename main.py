from nfa import NFA
from dfa import DFA


def main():
    # NFA
    initial_state = {0}
    final_states = {1: 0, 2: 0}
    alphabet = {"a", "b"}
    transition_table = {
        0: {"a": {1}, "b": {0}},
        1: {"a": {2}, "b": {1}},
        2: {"a": {1}, "b": {2}},
        3: {"a": {1}, "b": {2}},
    }

    nfa_1 = NFA(initial_state, final_states, alphabet, transition_table)
    dfa = DFA(nfa_1)
    print(dfa)
    # dfa._minimize()
    # print(dfa)


if __name__ == "__main__":
    main()
