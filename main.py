from nfa import *
from lex_rules import generate_rules
from range_gen_nfa import range_gen_nfa
from combine_nfa import nfa_or_list, nfa_or_op
from closure_nfa import closure_nfa
from infix_postfix import infix_to_postfix
#closure_nfa(nfa,"*")
#closure_nfa(nfa,"+")


regex, regdef, keywords, punctuation,id_lexeme = generate_rules("rules.txt")


lexeme_id = {v: k for k, v in id_lexeme.items()}

#print(regex)
#print(regdef)
#print(keywords)
#print(punctuation)
#print(lexeme_id)
#print(id_lexeme)

nfa_dict = {}


for key in regex.keys():
	print(key)
	print(regex[key])
	print(infix_to_postfix(regex[key]))
	print("")
for key in regdef.keys():


	#print(key)
	if type(regdef[key]) == list:
		temp_nfa = nfa_or_list(range_gen_nfa(regdef[key]))
		
		#TODO add ifnal states lexme id stuf
		#temp_nfa.final_states = {next(iter(temp_nfa.final_states)):lexeme_id[key]}
	
	else:
		temp_nfa = closure_nfa(nfa_dict[regdef[key][0:-1]], regdef[key][-1] )
	
	nfa_dict[key]=temp_nfa



for item in nfa_dict.values():
	pass
	#item.visualize()

