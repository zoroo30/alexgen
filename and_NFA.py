class NFA:
    def __init__(self, initial_state, final_states, inputs, transition_table):
        self.inputs = frozenset(inputs)
        self.initial_state = initial_state
        self.final_states = final_states
        self.transition_table = transition_table

    def isFinal(self, state):
        return state in self.final_states

    def __str__(self):
        x = "<NFA initial_state:%s final_states:%s \n" % (
            self.initial_state,
            self.final_states
        )

        for state in self.transition_table:
            x+="state:[%s] " %(state)
            for inp in self.transition_table[state]:
                x+="%s->%s , "% (inp,self.transition_table[state][inp])
            x+="\n"

        return x


def and_translate(nfa1,nfa2):
    counter = 0

    dict={}
    for state in nfa1.transition_table.keys():
        dict[state] = counter
        counter +=1

    for state in nfa1.transition_table.keys():
        for inp in nfa1.transition_table[state]:
            for i in range(len(nfa1.transition_table[state][inp])):
                nfa1.transition_table[state][inp][i] = dict[nfa1.transition_table[state][inp][i]]

    nfa1_new_tt = {}
    for state in list(nfa1.transition_table.keys()):
            nfa1_new_tt[dict[state]] = nfa1.transition_table[state]
    nfa1.transition_table = nfa1_new_tt

    nfa1.initial_state=dict[nfa1.initial_state]

    new_final_states = set()
    for item in nfa1.final_states:
        new_final_states.add(dict[item])

    nfa1.final_states= new_final_states

    ############################################
    if len(nfa1.final_states) == 1 :    
        counter -=1

    for state in nfa2.transition_table.keys():
        dict[state] = counter
        counter +=1

    for state in list(nfa2.transition_table.keys()):
        for inp in nfa2.transition_table[state]:
            for i in range(len(nfa2.transition_table[state][inp])):
                nfa2.transition_table[state][inp][i] = dict[nfa2.transition_table[state][inp][i]]

    nfa2_new_tt = {}
    for state in list(nfa2.transition_table.keys()):
            nfa2_new_tt[dict[state]] = nfa2.transition_table[state]
    nfa2.transition_table = nfa2_new_tt

    nfa2.initial_state=dict[nfa2.initial_state]

    new_final_states = set()
    for item in nfa2.final_states:
        new_final_states.add(dict[item])

    nfa2.final_states= new_final_states

    return nfa1, nfa2

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def and_nfa(nfa1,nfa2):

    if nfa1 == None:  # if one NFA is none return the other as combined
        return nfa2
    if nfa2 == None:  # same as above
        return nfa1

    new_inputs = nfa1.inputs.union(nfa2.inputs)

    nfa1, nfa2= and_translate(nfa1,nfa2)

    


    #if 1 final state
    if len(nfa1.final_states) == 1 :
        nfa1.transition_table.pop(next(iter(nfa1.final_states)))
        return NFA(nfa1.initial_state, nfa2.final_states, new_inputs, Merge(nfa1.transition_table, nfa2.transition_table))

    # more than 1 final state
    else:
        for state in nfa1.final_states:
            nfa1.transition_table[state]["e"]=[nfa2.initial_state]
        return NFA(nfa1.initial_state, nfa2.final_states, new_inputs, Merge(nfa1.transition_table, nfa2.transition_table))

    
#tt1 = {0: {"0": [0], "1": [1]}, 1: {"0": [2], "1": [2]}, 2: {"0": [], "1": []}}
#nfa1 = NFA(0, {2}, ["0", "1"], tt1)


# multiplle finals
tt1 = {0: {"0": [0], "1": [1]}, 1: {"0": [2], "1": [3]}, 2: {"0": [], "1": []}, 3: {"0": [], "1": []}}
nfa1 = NFA(0, {2,3}, ["0", "1"], tt1)

tt2 = {0: {"0": [0], "1": [1]}, 1: {"0": [2], "1": [2]}, 2: {"0": [], "1": []}}
nfa2 = NFA(0, {2}, ["0", "1"], tt2)

print(and_nfa(nfa1, nfa2))