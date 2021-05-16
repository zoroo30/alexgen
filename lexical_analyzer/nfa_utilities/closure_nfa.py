from lexical_analyzer.nfa_utilities.merge import merge
import copy


def closure_translate(nfa1):
    counter = 1

    dict = {}
    for state in nfa1.transition_table.keys():
        dict[state] = counter
        counter += 1

    for state in nfa1.transition_table.keys():
        for inp in nfa1.transition_table[state]:
            for i in range(len(nfa1.transition_table[state][inp])):
                nfa1.transition_table[state][inp][i] = dict[
                    nfa1.transition_table[state][inp][i]
                ]

    nfa1_new_tt = {}
    for state in list(nfa1.transition_table.keys()):
        nfa1_new_tt[dict[state]] = nfa1.transition_table[state]
    nfa1.transition_table = nfa1_new_tt

    nfa1.initial_state = dict[nfa1.initial_state]

    new_final_states = set()
    for item in nfa1.final_states:
        new_final_states.add(dict[item])

    nfa1.final_states = new_final_states

    return nfa1, counter


def closure_nfa(nfa_inp, type):

    nfa = copy.deepcopy(nfa_inp)

    nfa, counter = closure_translate(nfa)

    if len(nfa.final_states) != 1:
        raise ValueError("nfa has more than 1 final stat :\\, send welp")

    # add new final state

    nfa.transition_table[counter] = {}

    # addding from e from origanl final state to oringal inital state
    nfa.transition_table[next(iter(nfa.final_states))] = merge(
        nfa.transition_table[next(iter(nfa.final_states))],
        {"": [counter, nfa.initial_state]},
    )

    # nfa.transition_table[next(iter(nfa.final_states))] = Merge(nfa.transition_table[next(iter(nfa.final_states))], {"":[nfa.initial_state]},)

    # add new final stat
    nfa.final_states = set()
    nfa.final_states.add(counter)

    # nfa.visualize()

    # add another inital state and make it point to oringal inital and new final
    if type == "*":
        nfa.transition_table[0] = {"": [nfa.initial_state, counter]}
    elif type == "+":
        nfa.transition_table[0] = {"": [nfa.initial_state]}
    else:
        raise ValueError("didnt provide type for closure you noob")

    nfa.initial_state = 0

    # update final
    nfa.transition_table[counter] = {}
    for inp in nfa.alphabet:
        nfa.transition_table[counter] = merge(nfa.transition_table[counter], {inp: []})

    return nfa