
OPERATORS = set(['+', '-', '*','.','|','(',')'])  # set of operators

def put_dot(string):
	put_dot = []


	for i in range(len(string)-1):

		if string[i] ==")" and string[i+1] not in OPERATORS:
			put_dot.append(i)

		elif  string[i-1]=="\\" and string[i+1] not in OPERATORS:
			put_dot.append(i)

		elif string[i+1] =="(" and string[i] not in OPERATORS or string[i+1] =="(" and string[i-1]=="\\":
			put_dot.append(i)

		elif  string[i]  in ["*","+"] and (string[i+1] not in OPERATORS or string[i+1]=="\\" or string[i+1]=="("):
			put_dot.append(i)

		elif  string[i]==")"  in OPERATORS and string[i+1]=="(":
			put_dot.append(i)

		elif string[i+1] not in OPERATORS and string[i] not in OPERATORS:
			if string[i]=='\\':
				continue

			put_dot.append(i)

	#each time i add a dot i increadse the counter bec i changed the len of the string
	counter=1

	for j in put_dot:
		string = string[:j+counter] + "." + string[j+counter:]
		counter+=1
	print(string)


print(put_dot("AAAA"))