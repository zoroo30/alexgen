from nfa import *
from lex_rules import *

from Finalcombine import combine_NFA

regex,postfix_regex, keywords, postfix_keywords, punctuation, postfix_punctuation, id_lexeme = generate_rules("rules.txt")


lexeme_id = {v: k for k, v in id_lexeme.items()}

nfa_list = []

print(id_lexeme)
print(lexeme_id)



for i in range(len(postfix_keywords)):
	id = lexeme_id[keywords[i]]
	nfa = NFA(postfix=postfix_keywords[i])
	nfa.final_states = {next(iter(nfa.final_states)):id}
	nfa_list.append(nfa)
	pass


for i in range(len(postfix_punctuation)):
	id = lexeme_id[punctuation[i]]
	nfa = NFA(postfix=postfix_punctuation[i])
	nfa.final_states = {next(iter(nfa.final_states)):id}
	nfa_list.append(nfa)
	pass


for key in postfix_regex:
	id = lexeme_id[key]
	nfa = NFA(postfix=postfix_regex[key])
	nfa.final_states = {next(iter(nfa.final_states)):id}
	nfa_list.append(nfa)	
	pass


final_nfa = combine_NFA(nfa_list)
print(final_nfa)
#final_nfa.visualize()
