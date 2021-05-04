from fa import FA
from nfa_utilities import range_gen_nfa, closure_nfa, and_nfa, nfa_or_op


class NFA(FA):
    def __init__(
        self,
        initial_state=0,
        final_states={},
        alphabet=[],
        transition_table={},
        postfix=None,
    ):

        if postfix != None:
            self._generateFromPostfix(postfix)
            return

        self._generateFromTransitionTable(
            initial_state, final_states, transition_table, alphabet
        )

    def _generateFromTransitionTable(
        self, initial_state, final_states, transition_table, alphabet
    ):
        self.initial_state = initial_state
        self.final_states = final_states
        self.transition_table = transition_table
        self.alphabet = frozenset(alphabet)
        self.dead_states = set()

    def _generateFromPostfix(self, postfix):
        stack = []
        OPERATORS_1 = set(["+", "*"])
        OPERATORS_2 = set(["-", ".", "|"])

        i = 0
        while i < (len(postfix)):

            if postfix[i] == "\\":

                # if \L we agreed that this is EPS char
                if postfix[i + 1] == "L":
                    tt_temp = {0: {"": [1]}, 1: {}}
                    nfa_temp = NFA(0, {1}, "", tt_temp)
                    stack.append(nfa_temp)
                else:
                    tt_temp = {0: {postfix[i + 1]: [1]}, 1: {}}
                    nfa_temp = NFA(0, {1}, postfix[i + 1], tt_temp)
                    stack.append(nfa_temp)

                i += 2
                continue

            if postfix[i] in OPERATORS_1:
                operand_1 = stack.pop()
                stack.append(self._closure(operand_1, postfix[i]))

            elif postfix[i] in OPERATORS_2:
                operand_2_2 = stack.pop()
                operand_2_1 = stack.pop()

                if postfix[i] == "-":
                    stack.append(self._rangeGen(operand_2_1, operand_2_2))

                elif postfix[i] == ".":
                    stack.append(self._and(operand_2_1, operand_2_2))

                elif postfix[i] == "|":
                    stack.append(self._or(operand_2_1, operand_2_2))

            # add if thing is /

            # this is a character that i need to transform to NFA then push on stack
            # but i realized i cant do that bec of the '-' operations as its takes input 2 char
            # 2 options ; 1- change in the range to accept nfa
            else:

                tt_temp = {0: {postfix[i]: [1]}, 1: {}}
                nfa_temp = NFA(0, {1}, postfix[i], tt_temp)

                stack.append(nfa_temp)

                pass
                #
            i += 1

        if len(stack) != 1:
            raise ValueError("stack should have only 1 nfa left before poping")

        final_nfa = stack.pop()

        self._generateFromTransitionTable(
            final_nfa.initial_state,
            final_nfa.final_states,
            final_nfa.transition_table,
            final_nfa.alphabet,
        )

    def isFinal(self, state):
        return state in self.final_states

    def isFinalSet(self, states_set):
        """return true if final state exist in states_set
        also return its label
        if multiple states are final state return the smallest label (heighst priority)
        """
        final_for = float("inf")
        for state in states_set:
            if state in self.final_states and self.final_states[state] < final_for:
                final_for = self.final_states[state]
        return final_for != float("inf"), final_for

    def _rangeGen(self, nfa_1, nfa_2):
        initial_state, final_states, alphabet, tt = range_gen_nfa(nfa_1, nfa_2)
        return NFA(initial_state, final_states, alphabet, tt)

    def _closure(self, nfa_inp, type):
        return closure_nfa(nfa_inp, type)

    def _and(self, nfa_1, nfa_2):
        initial_state, final_states, alphabet, tt = and_nfa(nfa_1, nfa_2)
        return NFA(initial_state, final_states, alphabet, tt)

    def _or(self, nfa_1, nfa_2):
        initial_state, final_states, alphabet, tt = nfa_or_op(nfa_1, nfa_2)
        return NFA(initial_state, final_states, alphabet, tt)

    def __str__(self):
        x = "<NFA initial_state:%s final_states:%s alphabet:%s \n transition_table:%s \n" % (
            self.initial_state,
            self.final_states,
            self.alphabet,
            self.transition_table,
        )

        for state in self.transition_table:
            x += "state:[%s] " % (state)
            for inp in self.transition_table[state]:
                if inp == "":
                    x += "%s->%s , " % ("EPS", self.transition_table[state][inp])
                else:
                    x += "%s->%s , " % (inp, self.transition_table[state][inp])
            x += "\n"

        return x
