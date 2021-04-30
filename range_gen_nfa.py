from nfa import *
from combine_nfa import nfa_or_list, nfa_or_op


def range_gen_nfa(list_of_lists):
	nfa_out =[]
	for inp_list in list_of_lists:

		first_char = inp_list[0]
		last_char = inp_list[1]
		counter = 1
		inputs = []
		tt = {}
		total = (ord(last_char)-ord(first_char) + 1)*2+1
		final_states = {total}

		#print("final",total)
		tt[total] ={}

		tt[0]={}
		tt[0][""]=[]

		for i in range(ord(first_char), ord(last_char)+1):
			#final_states.add(counter)
			#tt[0]=["aaa"]
			tt[0][""].append(counter)
			inputs.append(chr(i))
			tt[total][chr(i)]=[]

			tt[counter] = {}

			tt[counter][chr(i)] =[counter+1]
			tt[counter+1] ={}
			tt[counter+1][""]=[total]
			counter +=2

		#tt[0]["e"] = list(final_states)
		#print(final_states)
		#print(inputs)
		#print(tt)

		nfa = NFA(0, final_states, inputs, tt)
		nfa_out.append(nfa)

	return nfa_out

if __name__ == '__main__':
	#test case
	inp = [['0','2']]

	print(nfa_or_list(range_gen_nfa(inp)).visualize())


	

	#print(range_gen_nfa(inp)[1])
	#print(nfa_or_list(range_gen_nfa(inp)))
	#print(combine_NFA(range_gen_nfa(inp)))