# nfa example
# transition_table = {0: {"0": [0], "1": [0, 1]}, 1: {"0": [2], "1": [2]}, 2: {"0": [], "1": []}}
# nfa = NFA(0, {2}, ["0", "1"], tt)
from pyvis.network import Network
import random
import copy


OPERATORS_1 = set(['+', '*', ])  # set of operators
OPERATORS_2 = set(['-', '.', '|'])


class NFA:
	def __init__(self, initial_state=0, final_states={}, alphabet=[], transition_table={}, postfix=None):

		if postfix == None:
			self.initial_state = initial_state
			self.final_states = final_states
			self.transition_table = transition_table
			self.alphabet = frozenset(alphabet)
		else:
			# TODO BASEM
			#print(postfix)

			stack = []

			i = 0
			while i < (len(postfix)):
				#print(postfix[i])

				if postfix[i] == "\\":

					# if \L we agreed that this is EPS char
					if postfix[i+1] =="L":
						tt_temp = {0: {"": [1]}, 1: {}}
						nfa_temp = NFA(0, {1}, "", tt_temp)
						stack.append(nfa_temp)
					else:
						tt_temp = {0: {postfix[i+1]: [1]}, 1: {}}
						nfa_temp = NFA(0, {1}, postfix[i+1], tt_temp)
						stack.append(nfa_temp)

					i += 2
					continue

				if postfix[i] in OPERATORS_1:
					operand_1 = stack.pop()
					stack.append(closure_nfa(operand_1, postfix[i]))

				elif postfix[i] in OPERATORS_2:
					operand_2_2 = stack.pop()
					operand_2_1 = stack.pop()

					if postfix[i] == "-":
						stack.append(range_gen_nfa(operand_2_1, operand_2_2))

					elif postfix[i] == ".":

						stack.append(and_nfa(operand_2_1, operand_2_2))

					elif postfix[i] == "|":
						#print(operand_2_1)
						#print(operand_2_2)

						#operand_2_1.visualize()
						#operand_2_2.visualize()

						stack.append(nfa_or_op(operand_2_1, operand_2_2))

				#add if thing is /

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
				raise ValueError('stack should have only 1 nfa left before poping')

			final_nfa = stack.pop()

			self.alphabet = final_nfa.alphabet
			self.initial_state = final_nfa.initial_state
			self.final_states = final_nfa.final_states
			self.transition_table = final_nfa.transition_table
			self.alphabet = frozenset(final_nfa.alphabet)

			pass

	def isFinal(self, state):
		return state in self.final_states

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

	def visualize(self):
		g = Network(height="100%", width="100%", directed=True)

		g.set_edge_smooth("dynamic")
		for state in self.transition_table:
			border_width = 1
			color = "#dedede"

			if state in self.final_states:
				border_width = 5
				color = "red"

			if state == self.initial_state:
				color = "#6492ee"

			g.add_node(
				state,
				label=state,
				shape="circle",
				color=color,
				borderWidth=border_width,
			)

		for state in self.transition_table:
			for ch in self.transition_table[state]:
				if type(self).__name__ == "NFA":
					for s in self.transition_table[state][ch]:
						g.add_edge(
							state,
							s,
							label=ch,
							arrowStrikethrough=False,
						)
				else:
					g.add_edge(
						state,
						self.transition_table[state][ch],
						label=ch,
						arrowStrikethrough=False,
					)

		n = random.random()
		g.show("out"+str(n)+".html")


def range_gen_nfa(nfa1, nfa2):

	# i adjusted it to accept nfa as alphabet
	first_char = next(iter(nfa1.alphabet))
	last_char = next(iter(nfa2.alphabet))

	# if order is wrong swap
	if first_char > last_char:
		first_char, last_char = last_char, first_char

	counter = 1
	alphabet = []
	tt = {}
	total = (ord(last_char)-ord(first_char) + 1)*2+1
	final_states = {total}

	tt[total] = {}

	tt[0] = {}
	tt[0][""] = []

	for i in range(ord(first_char), ord(last_char)+1):
		tt[0][""].append(counter)
		alphabet.append(chr(i))
		tt[total][chr(i)] = []

		tt[counter] = {}

		tt[counter][chr(i)] = [counter+1]
		tt[counter+1] = {}
		tt[counter+1][""] = [total]
		counter += 2

	nfa = NFA(0, final_states, alphabet, tt)

	return nfa


def closure_translate(nfa1):
	counter = 1

	dict = {}
	for state in nfa1.transition_table.keys():
		dict[state] = counter
		counter += 1

	for state in nfa1.transition_table.keys():
		for inp in nfa1.transition_table[state]:
			for i in range(len(nfa1.transition_table[state][inp])):
				nfa1.transition_table[state][inp][i] = dict[nfa1.transition_table[state][inp][i]]

	nfa1_new_tt = {}
	for state in list(nfa1.transition_table.keys()):
			nfa1_new_tt[dict[state]] = nfa1.transition_table[state]
	nfa1.transition_table = nfa1_new_tt

	nfa1.initial_state = dict[nfa1.initial_state]

	new_final_states = set()
	for item in nfa1.final_states:
		new_final_states.add(dict[item])

	nfa1.final_states = new_final_states

	return nfa1, counter


def Merge(dict1, dict2):
	res = {**dict1, **dict2}
	return res


def closure_nfa(nfa_inp, type):

	nfa = copy.deepcopy(nfa_inp)

	nfa, counter = closure_translate(nfa)

	if len(nfa.final_states) != 1:
		raise ValueError('nfa has more than 1 final stat :\\, send welp')

	#add new final state

	nfa.transition_table[counter] = {}

	#addding from e from origanl final state to oringal inital state
	nfa.transition_table[next(iter(nfa.final_states))] = Merge(
		nfa.transition_table[next(iter(nfa.final_states))], {"": [counter, nfa.initial_state]},)

	#nfa.transition_table[next(iter(nfa.final_states))] = Merge(nfa.transition_table[next(iter(nfa.final_states))], {"":[nfa.initial_state]},)

	# add new final stat
	nfa.final_states = set()
	nfa.final_states.add(counter)

	#nfa.visualize()

	# add another inital state and make it point to oringal inital and new final
	if type == "*":
		nfa.transition_table[0] = {"": [nfa.initial_state, counter]}
	elif type == "+":
		nfa.transition_table[0] = {"": [nfa.initial_state]}
	else:
		raise ValueError('didnt provide type for closure you noob')

	nfa.initial_state = 0

	# update final
	nfa.transition_table[counter] = {}
	for inp in nfa.alphabet:
		nfa.transition_table[counter] = Merge(
			nfa.transition_table[counter], {inp: []})

	return nfa


def and_translate(nfa1, nfa2):
    counter = 0

    dict = {}
    for state in nfa1.transition_table.keys():
        dict[state] = counter
        counter += 1

    for state in nfa1.transition_table.keys():
        for inp in nfa1.transition_table[state]:
            for i in range(len(nfa1.transition_table[state][inp])):
                nfa1.transition_table[state][inp][i] = dict[nfa1.transition_table[state][inp][i]]

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
                nfa2.transition_table[state][inp][i] = dict[nfa2.transition_table[state][inp][i]]

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

    #if 1 final state
    if len(nfa1.final_states) == 1:
        nfa1_final_state = next(iter(nfa1.final_states))
        nfa2_intial_state = nfa2.initial_state

        for state in nfa1.transition_table.keys():
            for inp in nfa1.transition_table[state]:
                for i in range(len(nfa1.transition_table[state][inp])):
                    if nfa1.transition_table[state][inp][i] == nfa1_final_state:
                        nfa1.transition_table[state][inp][i] = nfa2_intial_state
                    #print(nfa1.transition_table[state][inp][i])# = dict[nfa2.transition_table[state][inp][i]]

        nfa1.transition_table.pop(next(iter(nfa1.final_states)))

        return NFA(nfa1.initial_state, nfa2.final_states, new_alphabet, Merge(nfa1.transition_table, nfa2.transition_table))

    # more than 1 final state
    else:
        for state in nfa1.final_states:
            nfa1.transition_table[state][""] = [nfa2.initial_state]
        return NFA(nfa1.initial_state, nfa2.final_states, new_alphabet, Merge(nfa1.transition_table, nfa2.transition_table))


def nfa_or_op(nfa1, nfa2):  # OR operations between exctly 2 NFAs

	if nfa1 == None:
		return nfa2
	elif nfa2 == None:
		return nfa1

	# adds the states of 1 NFA to the combined merged tt
	def add_states(nfa, merged_dict, stateTranslator, num):

		# A function that adjusts the output state names for one state in the old NFA
		def translate_states(tt, state, stateTranslator, num):
			for key in tt[state].keys():  # loop over all the possible alphabet for the state
				# loop over all the output states we go to from the the current possible input
				for i, output_state in enumerate(tt[state][key]):
					# change its name using the Translator mapping
					tt[state][key][i] = stateTranslator[str(
						output_state) + num]
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
			translator[str(state)+'1'] = counter
			counter += 1  # increment counter

		for state in tt2.keys():  # same as previous loop but for the seconfd NFA
			translator[str(state)+'2'] = counter
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

	old_to_new_state_translator, stateCounter = create_translator(  # create the ampping between old state names and new names for both NFAs
		stateCounter, nfa1.transition_table, nfa2.transition_table)

	#print(old_to_new_state_translator)

	merged_tt, old_final_states1 = add_states(  # add states of NFA 1 to the combined merged
		nfa1, merged_tt, old_to_new_state_translator, '1')

	# add the first state number of first nfa as an output of initial state
	state_num = old_to_new_state_translator[str(nfa1.initial_state) + '1']
	merged_tt[0][""].append(state_num)

	# add the first state number of second nfa as an output of initial state
	state_num = old_to_new_state_translator[str(nfa2.initial_state) + '2']
	merged_tt[0][""].append(state_num)

	merged_tt, old_final_states2 = add_states(  # add states of NFA 2 to the combined merged
		nfa2, merged_tt, old_to_new_state_translator, '2')

	# add the final state to the cmbined merged
	merged_tt[stateCounter] = final_state_dict

	final_states = old_final_states1.union(old_final_states2)
	# CHANGE THE -1 STATE AND RENAMES IT TO STATE COUNTER
	for state in final_states:
		merged_tt[state][''] = [stateCounter]

	new = NFA(0, {stateCounter}, new_alphabet, merged_tt)  # init the new NFA

	return new  # return the new NFA


if __name__ == '__main__':

	#nfa =NFA(postfix="ac-AC-|ac-AC-|02-|*.")

	NFA(postfix="ab|")
	#nfa.visualize()

	pass
