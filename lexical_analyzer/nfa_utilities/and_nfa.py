from lexical_analyzer.nfa_utilities.merge import merge


def and_translate(nfa1, nfa2):
    counter = 0

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

    ############################################
    dict = {}

    for state in nfa2.transition_table.keys():
        dict[state] = counter
        counter += 1

    for state in list(nfa2.transition_table.keys()):
        for inp in nfa2.transition_table[state]:
            for i in range(len(nfa2.transition_table[state][inp])):
                nfa2.transition_table[state][inp][i] = dict[
                    nfa2.transition_table[state][inp][i]
                ]

    nfa2_new_tt = {}
    for state in list(nfa2.transition_table.keys()):
        nfa2_new_tt[dict[state]] = nfa2.transition_table[state]
    nfa2.transition_table = nfa2_new_tt

    nfa2.initial_state = dict[nfa2.initial_state]

    new_final_states = set()
    for item in nfa2.final_states:
        new_final_states.add(dict[item])

    nfa2.final_states = new_final_states

    return nfa1, nfa2


def and_nfa(nfa1, nfa2):

    if nfa1 == None:  # if one NFA is none return the other as combined
        return nfa2
    if nfa2 == None:  # same as above
        return nfa1

    new_alphabet = nfa1.alphabet.union(nfa2.alphabet)

    nfa1, nfa2 = and_translate(nfa1, nfa2)

    # if 1 final state
    if len(nfa1.final_states) == 1:
        nfa1_final_state = next(iter(nfa1.final_states))
        nfa2_intial_state = nfa2.initial_state

        for state in nfa1.transition_table.keys():
            for inp in nfa1.transition_table[state]:
                for i in range(len(nfa1.transition_table[state][inp])):
                    if nfa1.transition_table[state][inp][i] == nfa1_final_state:
                        nfa1.transition_table[state][inp][i] = nfa2_intial_state
                    # print(nfa1.transition_table[state][inp][i])# = dict[nfa2.transition_table[state][inp][i]]

        nfa1.transition_table.pop(next(iter(nfa1.final_states)))

        return (
            nfa1.initial_state,
            nfa2.final_states,
            new_alphabet,
            merge(nfa1.transition_table, nfa2.transition_table),
        )

    # more than 1 final state
    else:
        for state in nfa1.final_states:
            nfa1.transition_table[state][""] = [nfa2.initial_state]
        return (
            nfa1.initial_state,
            nfa2.final_states,
            new_alphabet,
            merge(nfa1.transition_table, nfa2.transition_table),
        )