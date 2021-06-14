import os
import pandas as pd


class Parser:
    def __init__(self, parsing_table, start_symbol):
        self.parsing_table = parsing_table
        self.start_symbol = start_symbol

    def set_input_src(self, get_next_token):
        self.get_next_token = get_next_token

    def parse(self):
        if not hasattr(self, "get_next_token"):
            raise Exception("no input source")

        print("parsing")
        stack = list()
        output = list()
        errors = list()
        stack.append("'$'")
        stack.append(self.start_symbol)
        next_token = self.get_next_token()
        while len(stack) != 0 and next_token != None:
            # print(next_token)
            # print(stack[-1], str(stack))
            if stack[-1] in self.parsing_table:  # top of stack is non terminal
                # terminal has entry with non terminal
                if next_token in self.parsing_table[stack[-1]]:
                    table_element = self.parsing_table[stack[-1]][next_token]
                    temp = stack.pop()
                    if table_element == "sync":
                        errors.append("sync")
                        output.append(("", "sync", ""))
                        continue
                    else:
                        symbol_list = table_element
                        for symbol in symbol_list[::-1]:  # reverse
                            stack.append(symbol)
                        output.append((temp, "--->", symbol_list))
                else:
                    errors.append(
                        f"Error : terminal {next_token} has no entry with nonterminal {stack[-1]} in table"
                    )
                    output.append(
                        (
                            "",
                            f"Error : terminal {next_token} has no entry with nonterminal {stack[-1]} in table",
                            "",
                        )
                    )
                    next_token = self.get_next_token()
                    # print("Terminal: " + next_token)
                    # print("Top of stack: " + stack[-1])
                    # print("Table row: " + str(self.parsing_table[stack[-1]]))
                    # print(output)
                    # return -1  # check later
            else:  # top of stack is a terminal
                if stack[-1] == "\L":
                    stack.pop()

                elif stack[-1] == "'" + next_token + "'":
                    stack.pop()
                    output.append(("", "Matched " + next_token, ""))
                    next_token = self.get_next_token()

                else:
                    errors.append(f"Error 2 : missing terminal {stack[-1]} in stack")
                    output.append(
                        ("", f"Error 2 : missing terminal {stack[-1]} in stack", "")
                    )
                    stack.pop()
                    # print("Terminal: " + next_token)
                    # print("stack: " + str(stack))
                    # print(output)
                    # print("Table row: " + str(self.parsing_table[stack[-1]]))
            # next_token = self.get_next_token()

        self.df = pd.DataFrame(output, columns=[" ", " ", " "])
        self.errors = errors

    def _writeOutput(self, file_path, output):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, "w") as f:
                if isinstance(output, str):
                    f.write(output)
                else:
                    for line in output:
                        f.write(line + "\n")
        except:
            print("An error occured opening the file!")

    def writeOutput(self, parser_file_path="parser.txt", errors_file_path="errors.txt"):
        self._writeOutput(
            os.environ.get("PARSER_OUTPUT_FOLDER") + parser_file_path,
            self.df.to_string(header=False, index=False),
        )
        self._writeOutput(
            os.environ.get("PARSER_OUTPUT_FOLDER") + errors_file_path,
            self.errors,
        )
