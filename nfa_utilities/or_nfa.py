def nfa_or_op(nfa1, nfa2):  # OR operations between exctly 2 NFAs

    if nfa1 == None:
        return nfa2
    elif nfa2 == None:
        return nfa1

    # adds the states of 1 NFA to the combined merged tt
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
        old_final_states = set()
        for state in nfa_states:  # loop over states
            # get the new name from the translator
            new_state_number = stateTranslator[str(state) + num]
            # adjust all the names of the output states using the translator
            translate_states(nfa.transition_table, state, stateTranslator, num)
            # add the previous output of the state after we adjusted the names
            merged_dict[new_state_number] = nfa.transition_table[state]
            if nfa.isFinal(state):  # if the state is final
                # add the new name of the old final state so make it point to the final state of the combined NFA at the end
                old_final_states.add(new_state_number)
        # return the merged dict and old final states
        return merged_dict, old_final_states

    # function that creates a mapping ebtween old and new state names for both NFAs
    def create_translator(counter, tt1, tt2):
        translator = {}  # initialize dict
        for state in tt1.keys():  # loop over NFA 1 states
            # assign a new name equal to counter
            translator[str(state) + "1"] = counter
            counter += 1  # increment counter

        for state in tt2.keys():  # same as previous loop but for the seconfd NFA
            translator[str(state) + "2"] = counter
            counter += 1

        # return the mapping dict and the counter value which will be the name of the final state in the combined NFA
        return translator, counter

    if nfa1 == None:  # if one NFA is none return the other as combined
        return nfa2
    if nfa2 == None:  # same as above
        return nfa1

    # combine the alphabet of both NFAs using union
    new_alphabet = nfa1.alphabet.union(nfa2.alphabet)

    # add the things in lecture first then loop over the two state list and add them .. try to do good
    final_state_dict = {}  # initialize the output state dict if the final state
    for input in new_alphabet:  # for all alphabet in this combined NFA
        final_state_dict[str(input)] = []  # Put an empty array

    # add in the merged tt an initial state and put for it epsilon output that sends to teh first state of first NFA
    merged_tt = {0: {"": []}}

    stateCounter = 1  # initialize state counters

    (
        old_to_new_state_translator,
        stateCounter,
    ) = create_translator(  # create the ampping between old state names and new names for both NFAs
        stateCounter, nfa1.transition_table, nfa2.transition_table
    )

    # print(old_to_new_state_translator)

    (
        merged_tt,
        old_final_states1,
    ) = add_states(  # add states of NFA 1 to the combined merged
        nfa1, merged_tt, old_to_new_state_translator, "1"
    )

    # add the first state number of first nfa as an output of initial state
    state_num = old_to_new_state_translator[str(nfa1.initial_state) + "1"]
    merged_tt[0][""].append(state_num)

    # add the first state number of second nfa as an output of initial state
    state_num = old_to_new_state_translator[str(nfa2.initial_state) + "2"]
    merged_tt[0][""].append(state_num)

    (
        merged_tt,
        old_final_states2,
    ) = add_states(  # add states of NFA 2 to the combined merged
        nfa2, merged_tt, old_to_new_state_translator, "2"
    )

    # add the final state to the cmbined merged
    merged_tt[stateCounter] = final_state_dict

    final_states = old_final_states1.union(old_final_states2)
    # CHANGE THE -1 STATE AND RENAMES IT TO STATE COUNTER
    for state in final_states:
        merged_tt[state][""] = [stateCounter]

    return 0, {stateCounter}, new_alphabet, merged_tt
