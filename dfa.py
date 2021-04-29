from nfa import NFA


class DFA:
    def __init__(self, nfa):
        self.alphabet = nfa.alphabet
        self.initial_state = nfa.initial_state
        self.final_states = {}
        self.transition_table = self._getTransitionTable(nfa)
        self.state_id = 0
        self._relaxeStateNames()

    def _getEClousre(self, transition_table, states_set):
        """return the e_clousre of states_set using the transition_table"""
        e_clousre = set()
        states_set = set(states_set)
        while states_set:
            state = states_set.pop()
            if not state in e_clousre:
                e_clousre.add(state)
                state = transition_table[state]
                if "" in state:
                    for s in state[""]:
                        if not s in e_clousre:
                            states_set.add(s)
        return frozenset(e_clousre)

    def _getTransitions(self, transition_table, states_set):
        """given a state return a dictionary of it transitions"""
        transitions = {}
        for ch in self.alphabet:
            transitions[ch] = set()
            for s in states_set:
                s = transition_table[s]
                if ch in s:
                    transitions[ch] = transitions[ch].union(s[ch])
            transitions[ch] = self._getEClousre(transition_table, transitions[ch])
        return transitions

    def _getTransitionRecord(self, nfa, current_state, transition_table):
        """recursive function to fill the transition table"""

        # base case
        if current_state in transition_table:
            return transition_table

        # flag to detect initial state
        is_initial_state = current_state == self.initial_state

        # add state to transition table
        current_state = self._getEClousre(nfa.transition_table, current_state)
        transitions = self._getTransitions(nfa.transition_table, current_state)
        transition_table[current_state] = transitions

        # update initial state with its e clousre
        if is_initial_state:
            self.initial_state = current_state

        # if final add to final states
        is_final, final_for = nfa.isFinal(current_state)
        if is_final:
            self.final_states[current_state] = final_for

        # add new states apeared in this record to the transition table
        for ch in transition_table[current_state]:
            self._getTransitionRecord(
                nfa, transition_table[current_state][ch], transition_table
            )

    def _relaxeStateNames(self):
        """convert state keys to numbers"""
        states_dict = {}

        for state in self.transition_table:
            states_dict[state] = self.state_id
            self.state_id += 1

        transition_table = {}
        for state in states_dict:
            mapped_state = states_dict[state]
            transition_table[mapped_state] = {}
            for ch in self.alphabet:
                transition_table[mapped_state][ch] = states_dict[
                    self.transition_table[state][ch]
                ]

        final_states = {}
        for state in self.final_states:
            mapped_state = states_dict[state]
            final_states[mapped_state] = self.final_states[state]

        initial_state = states_dict[frozenset(self.initial_state)]

        self.transition_table = transition_table
        self.final_states = final_states
        self.initial_state = initial_state

    def _getTransitionTable(self, nfa):
        transition_table = {}
        self._getTransitionRecord(nfa, frozenset(self.initial_state), transition_table)
        return transition_table

    def _minimize(self):
        transition_table = {}
        return transition_table

    def __str__(self):
        return (
            "<DFA initial_state:%s final_states:%s, alphabet:%s, transition_table:%s>"
            % (
                self.initial_state,
                self.final_states,
                self.alphabet,
                self.transition_table,
            )
        )
