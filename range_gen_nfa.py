from nfa import *
from or_nfa import nfa_or_op


def range_gen_nfa(nfa1,nfa2):

	# i adjusted it to accept nfa as inputs
	first_char = next(iter(nfa1.inputs))
	last_char = next(iter(nfa2.inputs))

	# if order is wrong swap
	if first_char > last_char:
		first_char, last_char = last_char, first_char

	counter = 1
	inputs = []
	tt = {}
	total = (ord(last_char)-ord(first_char) + 1)*2+1
	final_states = {total}

	tt[total] ={}

	tt[0]={}
	tt[0][""]=[]

	for i in range(ord(first_char), ord(last_char)+1):
		tt[0][""].append(counter)
		inputs.append(chr(i))
		tt[total][chr(i)]=[]

		tt[counter] = {}

		tt[counter][chr(i)] =[counter+1]
		tt[counter+1] ={}
		tt[counter+1][""]=[total]
		counter +=2

	nfa = NFA(0, final_states, inputs, tt)

	return nfa

if __name__ == '__main__':


	tt1 = {0: { "C": [1]}, 1: {}}
	nfa1 = NFA(0, {1}, ["C"], tt1)

	#nfa1.visualize()

	tt2 = {0: { "A": [1]}, 1: {}}
	nfa2 = NFA(0, {1}, ["A"], tt1)

	print(range_gen_nfa(nfa1,nfa2).visualize())

