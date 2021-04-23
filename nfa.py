# nfa example
# transition_table = {0: {"0": [0], "1": [0, 1]}, 1: {"0": [2], "1": [2]}, 2: {"0": [], "1": []}}
# nfa = NFA(0, {2}, ["0", "1"], tt)


class NFA:
    def __init__(self, initial_state, final_states, inputs, transition_table):
        self.inputs = frozenset(inputs)
        self.initial_state = initial_state
        self.final_states = final_states
        self.transition_table = transition_table

    def isFinal(self, state):
        return state in self.final_states

    def __str__(self):
        return "<NFA initial_state:%s final_states:%s, transition_table:%s>" % (
            self.initial_state,
            self.final_states,
            self.transition_table,
        )
