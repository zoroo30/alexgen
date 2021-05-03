class Lexer:
    def __init__(self, input_file, dfa):
        self.input_file = input_file
        self.dfa = dfa
        self.lines = self._preprocess()

    def _preprocess(self):
        # read input test program
        try:
            with open("program.txt", "r") as f:
                program = f.readlines()
        except:
            print("An error occured opening the file!")

        # Remove whitespace characters(\t,\n)
        program = list(map(str.strip, program))

        # split each line by space
        program = list(map(str.split, program))

        return program

    def _scanner(self):
        tokens = []
        errors = []
        for line_num, words in enumerate(self.lines):
            for word in words:
                _tokens, _errors = self._analyze(word, line_num)
                tokens.append(_tokens)
                errors.append(_errors)

        return tokens, errors

    def _analyze(self, word, line_number):
        errors = []
        tokens = []
        acceptance_state = None

        i = 0
        while i < len(word):
            try:
                result = self.dfa.apply(word[i])
                acceptance_state = result
            except:
                if acceptance_state == None:
                    error = {
                        "line_number": line_number,
                        "word": word,
                        "ch": word[i],
                        "char_index": i,
                    }
                    errors.append(error)
                else:
                    tokens.append(acceptance_state)
                    acceptance_state = None
                    i -= 1

            i += 1

        if acceptance_state != None:
            tokens.append(acceptance_state)

        return tokens, errors
