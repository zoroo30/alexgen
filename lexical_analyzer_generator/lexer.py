import os


class Lexer:
    def __init__(self, dfa, input_file_path=None):
        self.dfa = dfa
        if input_file_path:
            self.analyze_file(input_file_path)

    def analyze_file(self, input_file_path):
        self.input_file_path = os.environ["LEXER_INPUT_FOLDER"] + input_file_path
        self.lines = self._preprocess()

    def _preprocess(self):
        # read input test program
        try:
            with open(self.input_file_path, "r") as f:
                program = f.readlines()
                # Remove whitespace characters(\t,\n)
                program = list(map(str.strip, program))

                # split each line by space
                program = list(map(str.split, program))

                return program
        except:
            print("An error occured opening the file!")

    def _generateError(self, line_number, word_num, char_index, word, ch):
        return {
            "line_number": line_number,
            "word_index": word_num,
            "char_index": char_index,
            "word": word,
            "ch": ch,
        }

    def _analyze(self, word, line_number, word_num):
        errors = []
        tokens = []
        acceptance_state = None

        i = 0
        while i < len(word):
            try:
                result = self.dfa.apply(word[i])
                acceptance_state = result
                if result == None and i == len(word) - 1:
                    error = self._generateError(line_number, word_num, i, word, word[i])
                    errors.append(error)
            except:
                if acceptance_state == None:
                    error = self._generateError(line_number, word_num, i, word, word[i])
                    errors.append(error)
                else:
                    tokens.append(acceptance_state)
                    acceptance_state = None
                    i -= 1

            i += 1

        if acceptance_state != None:
            tokens.append(acceptance_state)
            self.dfa.reset()

        return tokens, errors

    def analyze(self):
        tokens = []
        errors = []
        for line_num, words in enumerate(self.lines):
            for word_num, word in enumerate(words):
                _tokens, _errors = self._analyze(word, line_num, word_num)
                tokens.append(_tokens)
                errors.append(_errors)

        self.tokens = [item for sublist in tokens for item in sublist]
        self.errors = [item for sublist in errors for item in sublist]

        return tokens, errors

    def _writeOutput(self, file_path, words):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, "w") as f:
                for word in words:
                    f.write(str(word) + "\n")
        except:
            print("An error occured opening the file!")

    def writeOutput(self, tokens_file_path="tokens.txt", errors_file_path="errors.txt"):
        self._writeOutput(
            os.environ.get("LEXER_OUTPUT_FOLDER") + tokens_file_path, self.tokens
        )
        self._writeOutput(
            os.environ.get("LEXER_OUTPUT_FOLDER") + errors_file_path, self.errors
        )

    def reset_current_token(self):
        self.current_token_index = 0

    def get_next_token(self):
        if not hasattr(self, "tokens"):
            return

        if not hasattr(self, "current_token_index"):
            self.current_token_index = 0

        if self.current_token_index == len(self.tokens):
            self.reset_current_token()
            return "$"

        current_token_index = self.current_token_index
        self.current_token_index += 1

        return self.tokens[current_token_index]