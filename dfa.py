from nfa import NFA
from fa import FA
from utilities.partition_refinement import PartitionRefinement
from utilities.sets import getElement


class DFA(FA):
    def __init__(self, nfa, minimize=True, relax=True):
        self.alphabet = nfa.alphabet
        self.initial_state = nfa.initial_state
        self.final_states = {}
        self.dead_states = set()
        self.transition_table = self._getTransitionTable(nfa)
        self.state_id = 0
        self.labels = {}
        if minimize:
            self._minimize()
        if relax:
            self._relaxeStateNames()

        self.current_state = self.initial_state

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
        if is_initial_state:
            current_state = self._getEClousre(nfa.transition_table, current_state)

        # add state to transition table
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

        dead_states = set()
        for state in self.dead_states:
            if not state in self.final_states:
                dead_states.add(states_dict[state])

        self.transition_table = transition_table
        self.final_states = final_states
        self.initial_state = initial_state
        self.dead_states = dead_states

    def _getTransitionTable(self, nfa):
        transition_table = {}
        self._getTransitionRecord(nfa, frozenset(self.initial_state), transition_table)
        return transition_table

    def _getRefinements(self, pr):
        refinements = []

        # loop on partitions
        for i, states_set in enumerate(pr):
            refinements.append({})

            # loop on states in a partition
            for state in states_set:
                refined = False

                # loop on every refinement set
                for r in refinements[i]:
                    refinment_mismatch = False

                    # loop on char in the alphabet
                    for ch in self.alphabet:

                        # apply input ch to the state and to an element in the refinement set
                        # if they both go to a state in the same set then do nothing
                        if (
                            pr[self.transition_table[state][ch]]
                            != pr[
                                self.transition_table[getElement(refinements[i][r])][ch]
                            ]
                        ):

                            # if they go to a different sets then a mismatch happend
                            refinment_mismatch = True
                            break

                    #  if not a mismatch that means we have found the refinement set for this state
                    if not refinment_mismatch:
                        refinements[i][r].add(state)
                        refined = True
                        break

                # if the state not refiened after looping through all refinement sets
                # create new refinement set for it
                if not refined:
                    newset = {state}
                    refinements[i][id(newset)] = newset

        return refinements

    def _createTransitionTable(self, pr):
        transition_table = {}
        dead_states = set()
        for state in pr:
            transition_table.setdefault(state, {})
            is_dead_state = True
            for ch in self.alphabet:
                transition_table[state].setdefault(
                    ch, pr[self.transition_table[getElement(state)][ch]]
                )
                if state != pr[self.transition_table[getElement(state)][ch]]:
                    is_dead_state = False

            if is_dead_state:
                dead_states.add(state)

        if dead_states:
            self.dead_states = dead_states

        final_states = {}
        for state in self.final_states:
            final_states[pr[state]] = self.final_states[state]

        initial_state = pr[self.initial_state]
        return transition_table, final_states, initial_state

    def _minimize(self):
        # initialize minimized transition table
        transition_table = {}

        # initialize partion refinement data structure (all states start at one subset)
        pr = PartitionRefinement(self.transition_table.keys())

        # split final states based on thier label
        final_states_splitted = {}
        for state in self.final_states:
            final_states_splitted.setdefault(self.final_states[state], set()).add(state)

        for states_set in final_states_splitted:
            pr.refine(final_states_splitted[states_set])

        old_sets_count = 1
        while old_sets_count < len(pr):
            old_sets_count = len(pr)

            refinements = self._getRefinements(pr)
            for refinement in refinements:
                for r in refinement.values():
                    pr.refine(r)

        pr.freeze()

        (
            self.transition_table,
            self.final_states,
            self.initial_state,
        ) = self._createTransitionTable(pr)

        self.state_id = 0

        return transition_table

    def apply(self, ch):
        self.current_state = self.transition_table[self.current_state][ch]
        if self.current_state in self.dead_states:
            self.current_state = self.initial_state
            raise Exception("Dead state!")

        if self.current_state in self.final_states:
            return self.labels[self.final_states[self.current_state]]

        return None
