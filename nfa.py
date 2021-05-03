from fa import FA


class NFA(FA):
    def __init__(self, initial_state, final_states, alphabet, transition_table):
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.dead_states = set()
        self.transition_table = transition_table

    def isFinal(self, states_set):
        """return true if final state exist in states_set
        also return its label
        if multiple states are final state return the smallest label (heighst priority)
        """
        final_for = float("inf")
        for state in states_set:
            if state in self.final_states and self.final_states[state] < final_for:
                final_for = self.final_states[state]
        return final_for != float("inf"), final_for

    def __str__(self):
        return (
            "<NFA initial_state:%s final_states:%s, alphabet:%s, transition_table:%s>"
            % (
                self.initial_state,
                self.final_states,
                self.alphabet,
                self.transition_table,
            )
        )