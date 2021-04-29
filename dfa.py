from nfa import NFA
from utilities.partition_refinement import PartitionRefinement
from utilities.sets import getElement


class DFA:
    def __init__(self, nfa):
        self.alphabet = nfa.alphabet
        self.initial_state = nfa.initial_state
        self.final_state = {}
        self.transition_table = self._getTransitionTable(nfa)
        self.state_id = 0
        self._minimize()
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
            self.final_state[current_state] = final_for

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
        for state in self.final_state:
            mapped_state = states_dict[state]
            final_states[mapped_state] = self.final_state[state]

        initial_state = states_dict[frozenset(self.initial_state)]

        self.transition_table = transition_table
        self.final_state = final_states
        self.initial_state = initial_state

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
        for state in pr:
            transition_table.setdefault(state, {})
            for ch in self.alphabet:
                transition_table[state].setdefault(
                    ch, pr[self.transition_table[getElement(state)][ch]]
                )

        final_states = {}
        for state in self.final_state:
            final_states[pr[state]] = self.final_state[state]

        initial_state = pr[self.initial_state]
        return transition_table, final_states, initial_state

    def _minimize(self):
        # initialize minimized transition table
        transition_table = {}

        # initialize partion refinement data structure (all states start at one subset)
        pr = PartitionRefinement(self.transition_table.keys())

        # split final states based on thier label
        final_states_splitted = {}
        for state in self.final_state:
            final_states_splitted.setdefault(self.final_state[state], set()).add(state)

        for states_set in final_states_splitted:
            pr.refine(final_states_splitted[states_set])

        old_sets_count = 1
        while old_sets_count < len(pr):
            old_sets_count = len(pr)

            refinements = self._getRefinements(pr)
            for refinement in refinements:
                for r in refinement.values():
                    pr.refine(r)

            # print(pr._sets.values())

        pr.freeze()

        (
            self.transition_table,
            self.final_state,
            self.initial_state,
        ) = self._createTransitionTable(pr)

        self.state_id = 0
        # print(self.transition_table)
        # self._relaxeStateNames()

        return transition_table

    def __str__(self):
        return (
            "<DFA initial_state:%s final_state:%s, alphabet:%s, transition_table:%s>"
            % (
                self.initial_state,
                self.final_state,
                self.alphabet,
                self.transition_table,
            )
        )


{
    frozenset({8}): {"a": frozenset({1}), "b": frozenset({5})},
    frozenset({2}): {"a": frozenset({2}), "b": frozenset({3})},
    frozenset({6}): {"a": frozenset({7}), "b": frozenset({8})},
    frozenset({5}): {"a": frozenset({2}), "b": frozenset({6})},
    frozenset({0}): {"a": frozenset({1}), "b": frozenset({5})},
    frozenset({3}): {"a": frozenset({2}), "b": frozenset({4})},
    frozenset({7}): {"a": frozenset({7}), "b": frozenset({7})},
    frozenset({4}): {"a": frozenset({1}), "b": frozenset({1})},
    frozenset({1}): {"a": frozenset({2}), "b": frozenset({3})},
}