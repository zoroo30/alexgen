# adds the states of a NFA to the combined merged tt
def add_states(nfa, merged_dict, stateTranslator, num):

    # A function that adjusts the output state names for one state in the old NFA
    def translate_states(tt, state, stateTranslator, num):
        for key in tt[
            state
        ].keys():  # loop over all the possible alphabet for the state
            # loop over all the output states we go to from the the current possible input
            for i, output_state in enumerate(tt[state][key]):
                # change its name using the Translator mapping
                tt[state][key][i] = stateTranslator[str(output_state) + num]
        return

    nfa_states = nfa.transition_table.keys()  # get all states of the NFA
    old_final_states = {}
    for state in nfa_states:  # loop over states
        # get the new name from the translator
        new_state_number = stateTranslator[str(state) + num]
        # adjust all the names of the output states using the translator
        translate_states(nfa.transition_table, state, stateTranslator, num)
        # add the previous output of the state after we adjusted the names
        merged_dict[new_state_number] = nfa.transition_table[state]
        if nfa.isFinal(state):  # if the state is final
            # add the new name of the old final state so make it point to the final state of the combined NFA at the end
            old_final_states[new_state_number] = nfa.final_states[state]
    # return the merged dict and old final states
    return merged_dict, old_final_states


# function that recieves a list of NFAs and combines them all into a single one
def combine_nfa(nfa_list):
    def create_translator(counter, tt, idx):
        translator = {}  # initialize dict
        for state in tt.keys():  # loop over NFA 1 states
            # assign a new name equal to counter
            translator[str(state) + idx] = counter
            counter += 1  # increment counter

        # return the mapping dict and the counter value which will be the name of the final state in the combined NFA
        return translator, counter

    # add in the merged tt an initial state and put for it epsilon output that sends to teh first state of each NFA
    merged_tt = {0: {"": []}}

    stateCounter = 1  # initialize state counters

    new_alphabet = set()
    final_states = {}
    for idx, nfa in enumerate(nfa_list):
        # combine the alphabet of both NFAs using union
        new_alphabet = new_alphabet.union(nfa.alphabet)

        # add the first state number of next nfa as an output of initial state
        merged_tt[0][""].append(stateCounter)

        (
            old_to_new_state_translator,
            stateCounter,
        ) = create_translator(  # create the ampping between old state names and new names for both NFAs
            stateCounter, nfa.transition_table, str(idx)
        )

        (
            merged_tt,
            old_final_states,
        ) = add_states(  # add states of current NFA to the combined merged
            nfa, merged_tt, old_to_new_state_translator, str(idx)
        )

        # final_states = final_states.union(old_final_states)
        final_states = {**final_states, **old_final_states}

    return 0, final_states, new_alphabet, merged_tt
