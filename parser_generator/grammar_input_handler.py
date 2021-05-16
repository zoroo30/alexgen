import re
import os


class GrammarInputHandler:
    def __init__(self, input_file_path):
        input_file_path = os.environ["PARSER_INPUT_FOLDER"] + input_file_path
        self.grammar, self.terminals, self.non_terminals = self.generate_rules(
            input_file_path
        )
        return

    def __str__(self):
        return str(self.grammar)

    def generate_rules(self, fname):
        try:
            with open(fname, "r") as f:
                grammar = {}
                terminals = set()
                non_terminals = set()
                rules = f.read()
                rules = rules.split("#")
                for rule in rules:
                    if not rule:
                        continue
                    test = re.match(
                        r"[\s]*(\w+)[\s]*=(([\s]*(\w+|'[^']*'|\\L)[\s]*|\|[\s]*(\w+|'[^']*'|\\L)[\s]*)+)$",
                        rule,
                        flags=re.MULTILINE,
                    )

                    if not test:
                        raise Exception("wrong format", rule)

                    grammar[test.group(1)] = [
                        re.findall(r"\w+|'[^']*'|\\L", r)
                        for r in [r for r in test.group(2).split("|")]
                    ]

                    for t in grammar[test.group(1)]:
                        for s in t:
                            ss = re.match(
                                r"(?P<non_terminal>\w+)|'(?P<terminal>[^']*)'|(\\L)",
                                s,
                            )
                            if ss.group("terminal"):
                                terminals.add(ss.group("terminal"))
                            elif ss.group("non_terminal"):
                                non_terminals.add(ss.group("non_terminal"))
                            else:
                                terminals.add("\L")

                for non_terminal in non_terminals:
                    if not non_terminal in grammar:
                        raise Exception("non terminal do not exist", non_terminal)

                return grammar, terminals, non_terminals

        except Exception as e:
            print(e)