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
    total = (ord(last_char) - ord(first_char) + 1) * 2 + 1
    final_states = {total}

    tt[total] = {}

    tt[0] = {}
    tt[0][""] = []

    for i in range(ord(first_char), ord(last_char) + 1):
        tt[0][""].append(counter)
        alphabet.append(chr(i))
        tt[total][chr(i)] = []

        tt[counter] = {}

        tt[counter][chr(i)] = [counter + 1]
        tt[counter + 1] = {}
        tt[counter + 1][""] = [total]
        counter += 2

    return 0, final_states, alphabet, tt
