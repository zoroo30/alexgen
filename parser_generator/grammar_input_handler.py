import re
import os


class GrammarInputHandler:
    def __init__(self, input_file_path):
        input_file_path = os.environ["PARSER_INPUT_FOLDER"] + input_file_path
        self.grammar, self.terminals, self.non_terminals = self.generate_rules(
            input_file_path
        )
        self.left_recursion_elimination()
        self.update_nonTerminals()
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
                        raise Exception(
                            "non terminal do not exist", non_terminal)

                return grammar, terminals, non_terminals

        except Exception as e:
            print(e)

    def update_nonTerminals(self):
        for thing in self.grammar:
            if thing not in self.non_terminals:
                self.non_terminals.add(thing)
                self.terminals.add('\\L')

    def eliminate_immediate(self, derivations):
        new_derivations = {}
        for non_trmnl in derivations:
            A = []
            B = []
            for production in derivations[non_trmnl]:
                if production[0] == non_trmnl:
                    A.append(production[1:])
                else:
                    B.append(production)
            if len(A) > 0:
                new_derivations[non_trmnl] = [b + [non_trmnl+'_'] for b in B]
                new_derivations[non_trmnl+'_'] = [a +
                                                  [non_trmnl+'_'] for a in A]
                new_derivations[non_trmnl+'_'].append(["'\\L'"])
            else:
                new_derivations = derivations
        # print(new_derivations)
        return new_derivations

    def left_recursion_elimination(self):
        for i, derivation in enumerate(self.grammar):
            new_derivations = {}
            for j in range(i):
                Aj = list(self.grammar)[j]
                for production in self.grammar[derivation]:
                    if production[0] == Aj:
                        # replace
                        Y = production[1:]
                        self.grammar[derivation].remove(production)
                        for aj_prod in self.grammar[Aj]:
                            copy = aj_prod.copy()
                            copy.append(Y)
                            self.grammar[derivation].append(copy)

            self.eliminate_immediate(new_derivations)
            if len(new_derivations) > 0:
                del self.grammar[derivation]
                self.grammar.update(new_derivations)
        new = {}
        for derivation in self.grammar:
            dictrow = {}
            dictrow[derivation] = self.grammar[derivation]
            derivations = self.eliminate_immediate(dictrow)
            new.update(derivations)
        self.grammar.update(new)
