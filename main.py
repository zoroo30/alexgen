from nfa import *
from lex_rules import generate_rules
from range_gen_nfa import range_gen_nfa
from or_nfa import  nfa_or_op
from closure_nfa import closure_nfa
from infix_postfix import infix_to_postfix


# closure nfa uses
#closure_nfa(nfa,"*")
#closure_nfa(nfa,"+")

# normal nfa can be genrated normally 3ady as we usually do
# to create nfa with postifx -> NFA(postfix="AAAA")

regex,postfix_regex, keywords, punctuation,id_lexeme = generate_rules("rules.txt")


lexeme_id = {v: k for k, v in id_lexeme.items()}

"""
print(regex)
print("")

print(postfix_regex)
print("")

print(keywords)
print("")

print(punctuation)
print("")

print(id_lexeme)
print("")
"""

#print(lexeme_id)

nfa_list = []

print(postfix_regex)

print("````````````````````````````````````````")


"""
for key in postfix_regex.keys():
	pass
	print(key)
	print(postfix_regex[key])

	nfa_list = NFA(postfix=postfix_regex[key])
	#print(infix_to_postfix(regex[key]))
	#print("")

		#TODO add ifnal states lexme id stuf
		#temp_nfa.final_states = {next(iter(temp_nfa.final_states)):lexeme_id[key]}

print(nfa_list)

"""
	