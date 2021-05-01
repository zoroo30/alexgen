import re



def infix_to_postfix(expression): #input expression
    
    OPERATORS = set(['+', '-', '*', '(', ')','.','|'])  # set of operators
    PRIORITY = {'|':1, '.':2, '+':3 ,'*':3, '-':4} # dictionary having priorities 
    
    stack = [] # initially stack empty
    output = '' # initially output empty

    for ch in expression:
        if ch not in OPERATORS:  # if an operand then put it directly in postfix expression
            output+= ch

        elif ch=='(':  # else operators should be put in stack
            stack.append('(')

        elif ch==')':
            while stack and stack[-1]!= '(':
                output+=stack.pop()
            stack.pop()

        else:
            # lesser priority can't be on top on higher or equal priority    
            # so pop and put in output   
            while stack and stack[-1]!='(' and PRIORITY[ch]<=PRIORITY[stack[-1]]:
                output+=stack.pop()

            stack.append(ch)
    while stack:
        output+=stack.pop()

    return output


def extract_symbols(regdef):
	sym = {}
	for k,v in regdef.items():
		if k == "letter":
			sym[k] = []
			v = v.split("|")
			for  a in v:
				sym[k].append(a.split("-"))
		elif k == "digit":
			sym[k] = []
			sym[k].append(v.split("-"))
		else:
			sym[k] = v
	return sym


def stuff(regex,regdef):

	# substitute regdef from regdef
	# for example 'digit': '0-9', 'digits': 'digit*' -> 'digit': '0-9', 'digits': '0-9*'
	for key1 in regdef:
		for key2 in regdef:
			regdef[key2] = regdef[key2].replace(key1, regdef[key1]) 
	
	# sort the def dict by longest 
	# this is to match the longest keyworkd first, mathch digits b4 mathching digit 
	regdef = dict(sorted(list(regdef.items()),reverse=True, key = lambda key : len(key[0])))

	# subustitude regex from regdef and encapsulate the subs by brackets
	for key_def in regdef:
		for key_ex in regex.keys():
			regex[key_ex]=regex[key_ex].replace(str(key_def),"("+regdef[key_def]+")")

	# as i said in postfix stuff i need smth to tell me that im doing the concat operation
	# so this is my attempt to add a dot "."  to indicate the concat oepration

	OPERATORS = ['+', '-', '*', '(', ')','.','|'] # set of operators

	for key in regex.keys():

		# i save the index of where i want to add a dot so that i dont modify the len of the string while doing the operations
		put_dot = []


		for i in range(len(regex[key])-1):

			if regex[key][i] ==")" and regex[key][i+1] not in OPERATORS:
				put_dot.append(i)

			elif regex[key][i+1] =="(" and regex[key][i] not in OPERATORS or regex[key][i+1] =="(" and regex[key][i-1]=="\\":
				put_dot.append(i)

			elif  regex[key][i]  in ["*","+"] and (regex[key][i+1] not in OPERATORS or regex[key][i+1]=="\\"):
				put_dot.append(i)

			elif  regex[key][i]==")"  in OPERATORS and regex[key][i+1]=="(":
				put_dot.append(i)

			elif regex[key][i+1] not in OPERATORS and regex[key][i] not in OPERATORS:
				if regex[key][i]=='\\':
					continue

				put_dot.append(i)

		#each time i add a dot i increadse the counter bec i changed the len of the string
		counter=1

		for j in put_dot:
			regex[key] = regex[key][:j+counter] + "." + regex[key][j+counter:]
			counter+=1
		

	

def construct_helper_dict(*args):
	ref_dict = {}
	total_list = []
	for l in args:
		total_list += l

	for c in range(len(total_list)):
		ref_dict[c] = total_list[c]

	return ref_dict



def generate_rules(fname):
	regex = {}
	postfix_regex = {}
	regdef = {}
	keywords = []
	punctuation = []
	try:
		with open(fname, 'r') as f:
			file_text = f.readlines()
	except:
		print("An Error occured opening the file")


	for line in file_text:

		#Check Regular Expression
		if re.search(r'\w+[:]\s', line):
			line_tmp = line.replace(" ","").strip().split(":")
			# ADDED 
			regex[line_tmp[0]] = line_tmp[1].replace(".", "\\.").replace("-", "\\-")

		#Check Regular Definition
		elif re.search(r'\w+\s[=]', line):
			line_tmp = line.replace(" ","").strip().split("=")
			regdef[line_tmp[0]] = line_tmp[1]

		#Check Keywords 	
		elif re.search(r'\A[{]', line):
			line_tmp = line[1:-2].strip().split()
			for l in line_tmp:
				keywords.append(l)

		#Check Punctuation
		elif re.search(r'\A\[', line):
			line_tmp = line[1:-2].strip().split()
			for l in line_tmp:
				# ADDED 
				if l ==".":
					l = '\\.'
				elif l =="-":
					l = '\\-'
				punctuation.append(l)
		else:
			print("Error, Rule not recognized")
			continue

	regdef_simplifid = extract_symbols(regdef)
	ref_dict = construct_helper_dict(keywords, punctuation, regex)

	# remove backslashes from stuff like \\. or \\(
	# note the ref_dict is used for labeling the nfa so we dont need backslashes here
	for key in ref_dict.keys():
		if ref_dict[key][0]=="\\" and len(ref_dict) > 1:
			ref_dict[key] = ref_dict[key][1:]

	"""
	print(regex)
	print(regdef)
	print(regdef_simplifid)
	print(keywords)
	print(punctuation)
	print(ref_dict)
	"""
	stuff(regex,regdef)

	for key in regex.keys():
		postfix_regex[key] = infix_to_postfix(regex[key])


	# removed regdef_simplifid
	return regex,postfix_regex, keywords, punctuation, ref_dict

if __name__ == '__main__':


	regex,postfix_regex, keywords, punctuation,id_lexeme = generate_rules("rules.txt")
	print("`"*50)

	print(regex)
	#print(regdef)
	print(keywords)
	print(punctuation)
	#print(lexeme_id)
	print(id_lexeme)

	print("~"*50)

	print(punctuation)
	print(punctuation[1])