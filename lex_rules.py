import re
from nfa import NFA
from nfa_utilities import combine_nfa


def infix_to_postfix(expression):  # input expression

    OPERATORS = set(["+", "-", "*", ".", "|", "(", ")"])  # set of operators
    PRIORITY = {
        "|": 1,
        ".": 2,
        "+": 4,
        "*": 4,
        "-": 4,
    }  # dictionary having priorities

    stack = []  # initially stack empty
    output = ""  # initially output empty

    i = 0
    while i < len(expression):

        ch = expression[i]

        if ch == "\\":
            ch = expression[i + 1]
            output += "\\" + ch
            i += 2
            continue

        if (
            ch not in OPERATORS
        ):  # if an operand then put it directly in postfix expression
            output += ch

        elif ch == "(":  # else operators should be put in stack
            stack.append("(")

        elif ch == ")":
            while stack and stack[-1] != "(":
                output += stack.pop()
            stack.pop()

        else:
            # lesser priority can't be on top on higher or equal priority
            # so pop and put in output
            while stack and stack[-1] != "(" and PRIORITY[ch] <= PRIORITY[stack[-1]]:
                output += stack.pop()
            stack.append(ch)
        i += 1

    while stack:
        output += stack.pop()

    return output


def extract_symbols(regdef):
    sym = {}
    for k, v in regdef.items():
        if k == "letter":
            sym[k] = []
            v = v.split("|")
            for a in v:
                sym[k].append(a.split("-"))
        elif k == "digit":
            sym[k] = []
            sym[k].append(v.split("-"))
        else:
            sym[k] = v
    return sym


OPERATORS = [
    "+",
    "-",
    "*",
    "(",
    ")",
    ".",
    "|",
]  # set of operators


def put_dot(string):
    put_dot = []
    i = 0
    while i < (len(string) - 1):
        # print(string[i])

        if string[i] == ")" and (
            string[i + 1] not in OPERATORS or string[i + 1] == "("
        ):
            put_dot.append(i)

        elif string[i] == "\\":
            try:
                if string[i + 2] not in OPERATORS:
                    put_dot.append(i + 1)
                    i += 2
                    continue
            except:
                pass

        elif (
            string[i + 1] == "("
            and string[i] not in OPERATORS
            or string[i + 1] == "("
            and string[i - 1] == "\\"
        ):
            put_dot.append(i)

        elif string[i] in ["*", "+"] and (
            string[i + 1] not in OPERATORS
            or string[i + 1] == "\\"
            or string[i + 1] == "("
        ):
            put_dot.append(i)

        elif string[i + 1] not in OPERATORS and string[i] not in OPERATORS:
            if string[i] == "\\":
                i += 1
                continue

            put_dot.append(i)
        i += 1

    # each time i add a dot i increadse the counter bec i changed the len of the string
    counter = 1

    for j in put_dot:
        string = string[: j + counter] + "." + string[j + counter :]
        counter += 1

    return string.strip()


def stuff(regex, regdef):

    # substitute regdef from regdef
    # for example 'digit': '0-9', 'digits': 'digit*' -> 'digit': '0-9', 'digits': '0-9*'
    for key1 in regdef:
        for key2 in regdef:
            regdef[key2] = regdef[key2].replace(key1, regdef[key1])

    # sort the def dict by longest
    # this is to match the longest keyworkd first, mathch digits b4 mathching digit
    regdef = dict(
        sorted(list(regdef.items()), reverse=True, key=lambda key: len(key[0]))
    )

    # subustitude regex from regdef and encapsulate the subs by brackets
    for key_def in regdef:
        for key_ex in regex.keys():
            regex[key_ex] = regex[key_ex].replace(
                str(key_def), "(" + regdef[key_def] + ")"
            )

    # as i said in postfix stuff i need smth to tell me that im doing the concat operation
    # so this is my attempt to add a dot "."  to indicate the concat oepration

    for key in regex.keys():
        regex[key] = put_dot(regex[key])


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
    postfix_keywords = []

    punctuation = []
    postfix_punctuation = []
    try:
        with open(fname, "r") as f:
            file_text = f.readlines()
    except:
        print("An Error occured opening the file")

    for line in file_text:

        # Check Regular Expression
        if re.search(r"\w+[:]\s", line):
            line_tmp = line.replace(" ", "").strip().split(":", 1)
            # ADDED
            regex[line_tmp[0]] = line_tmp[1].replace(".", "\\.").replace("-", "\\-")

        # Check Regular Definition
        elif re.search(r"\w+\s[=]", line):
            line_tmp = line.replace(" ", "").strip().split("=", 1)
            regdef[line_tmp[0]] = line_tmp[1]

        # Check Keywords
        elif re.search(r"\A[{]", line):
            line_tmp = line[1:-2].strip().split()
            for l in line_tmp:
                keywords.append(l)

        # Check Punctuation
        elif re.search(r"\A\[", line):
            line_tmp = line[1:-2].strip().split()
            for l in line_tmp:
                # ADDED
                if l == ".":
                    l = "\\."
                elif l == "-":
                    l = "\\-"
                punctuation.append(l)
        else:
            print("Error, Rule not recognized")
            continue

    # regdef_simplifid = extract_symbols(regdef)
    ref_dict = construct_helper_dict(keywords, punctuation, regex)

    stuff(regex, regdef)

    for key in regex.keys():
        postfix_regex[key] = infix_to_postfix(regex[key])

    for i in range(len(keywords)):
        postfix_keywords.append(infix_to_postfix(put_dot(keywords[i])))

    # for punctuation dont doo shit
    for i in range(len(punctuation)):
        # print(punctuation[i])
        # postfix_punctuation.append(punctuation[i])
        postfix_punctuation.append(infix_to_postfix((put_dot(punctuation[i]))))

        # print(postfix_punctuation[i])

    # removed regdef_simplifid
    return (
        regex,
        postfix_regex,
        keywords,
        postfix_keywords,
        punctuation,
        postfix_punctuation,
        ref_dict,
    )


def generate_nfa(fname):
    (
        _,
        postfix_regex,
        keywords,
        postfix_keywords,
        punctuation,
        postfix_punctuation,
        id_lexeme,
    ) = generate_rules(fname)

    lexeme_id = {v: k for k, v in id_lexeme.items()}

    nfa_list = []

    # print(id_lexeme)
    # print(lexeme_id)

    for i in range(len(postfix_keywords)):
        id = lexeme_id[keywords[i]]
        nfa = NFA(postfix=postfix_keywords[i])
        nfa.final_states = {next(iter(nfa.final_states)): id}
        nfa_list.append(nfa)
        pass

    for i in range(len(postfix_punctuation)):
        id = lexeme_id[punctuation[i]]
        nfa = NFA(postfix=postfix_punctuation[i])
        nfa.final_states = {next(iter(nfa.final_states)): id}
        nfa_list.append(nfa)
        pass

    for key in postfix_regex:
        id = lexeme_id[key]
        nfa = NFA(postfix=postfix_regex[key])
        nfa.final_states = {next(iter(nfa.final_states)): id}
        nfa_list.append(nfa)
        pass

    initial_state, final_states, alphabet, tt = combine_nfa(nfa_list)
    return NFA(initial_state, final_states, alphabet, tt), id_lexeme
