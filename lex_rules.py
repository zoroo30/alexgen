import re


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

	#zabt el reg def first - aka - zabt el digits
	for key1 in regdef:
		for key2 in regdef:
			regdef[key2] = regdef[key2].replace(key1, regdef[key1]) 
	
	# this is to match digits b4 mathching digits idk if its good or not
	regdef = dict(sorted(list(regdef.items()),reverse=True, key = lambda key : len(key[0])))

	# subustitude
	for key_def in regdef:
		for key_ex in regex.keys():
			regex[key_ex]=regex[key_ex].replace(str(key_def),"("+regdef[key_def]+")")

	# add dot indication

	OPERATORS = ['+', '-', '*', '(', ')','.','|'] # set of operators

	#print(regex)

	for key in regex.keys():

		put_dot = []

		#print(key)

		for i in range(len(regex[key])-1):
			# maybe add if ) thne auto add .
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

		counter=1
		for j in put_dot:
			regex[key] = regex[key][:j+counter] + "." + regex[key][j+counter:]
			counter+=1

		regex[key] = regex[key].strip()
		#print(regex[key])
		#print("")
		#print(temp)


	

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
	ref_dict = construct_helper_dict(keywords, punctuation)

	"""
	print(regex)
	print(regdef)
	print(regdef_simplifid)
	print(keywords)
	print(punctuation)
	print(ref_dict)
	"""
	stuff(regex,regdef)

	return regex, regdef_simplifid, keywords, punctuation, ref_dict

if __name__ == '__main__':


	regex, regdef, keywords, punctuation,id_lexeme = generate_rules("rules.txt")


	print(regex)
	print(regdef)
	#print(keywords)
	#print(punctuation)
	#print(lexeme_id)
	print(id_lexeme)
