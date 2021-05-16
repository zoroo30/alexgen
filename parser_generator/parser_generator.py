from parser_generator.parser import Parser


class ParserGenerator:
    def __init__(self, grammarHndlr):
        self.grammarHndlr = grammarHndlr
        self.first = {}
        self.follow = {}
        self.parsing_table = None

    def get_me_start_symbol(self):
        grammar = self.grammarHndlr.grammar
        return next(iter(grammar))

    def compute_First(self, non):
        grammar = self.grammarHndlr.grammar
        self.first[non] = set()
        productions = grammar[non]
        for production in productions:
            if len(production) == 1 and production[0] == '\\L':
                self.first[non].add('\\L')
                continue
            for item in production:
                if item not in self.first:
                    self.compute_First(item)

                set_to_add = self.first[item].copy()
                if '\\L' in set_to_add:
                    if item != production[-1]:
                        set_to_add.discard('\\L')
                    self.first[non].update(set_to_add)
                else:
                    self.first[non].update(set_to_add)
                    break
        return

    def first_sets(self):
        grammar = self.grammarHndlr.grammar
        terminals = self.grammarHndlr.terminals

        for terminal in terminals:
            self.first['\''+terminal+'\''] = {terminal}

        for non in grammar:
            self.compute_First(non)

        # print(self.first)
        return self.first

    def follow_sets(self):
        grammar = self.grammarHndlr.grammar
        non_terminals = self.grammarHndlr.non_terminals

        # for symbol in grammar:
        #     self.follow[symbol] = set()

        # start_symbol = self.get_me_start_symbol()
        # self.follow[start_symbol].add('$')

        waiting = set()
        once = 1
        while len(waiting) + once > 0:
            once = 0
            for symbol in grammar:
                productions = grammar[symbol]
                for production in productions:
                    for index, item in enumerate(production):
                        if item not in non_terminals:
                            continue
                        if item == production[-1]:
                            if symbol not in self.follow:
                                waiting.add(item)
                                continue
                            if item not in self.follow:
                                self.follow[item] = set()
                            if item == self.get_me_start_symbol():
                                self.follow[item].add('$')
                            waiting.discard(item)
                            self.follow[item].update(self.follow[symbol])
                            continue
                        set_to_add = self.first[production[index + 1]].copy()
                        if '\\L' in set_to_add:
                            if symbol not in self.follow:
                                waiting.add(item)
                                continue

                            if item not in self.follow:
                                self.follow[item] = set()
                            if item == self.get_me_start_symbol():
                                self.follow[item].add('$')
                            waiting.discard(item)
                            self.follow[item].update(self.follow[symbol])
                            set_to_add.discard('\\L')
                        if item not in self.follow:
                            self.follow[item] = set()
                        if item == self.get_me_start_symbol():
                            self.follow[item].add('$')
                        self.follow[item].update(set_to_add)

        # print(self.follow)
        return self.follow

    def generate_parsing_table(self):
        grammar = self.grammarHndlr.grammar
        terminals = self.grammarHndlr.terminals
        non_terminals = self.grammarHndlr.non_terminals

        first_sets = self.first_sets()
        follow_sets = self.follow_sets()

        M = {}
        for non in non_terminals:
            M[non] = {}

        for symbol in grammar:
            productions = grammar[symbol]
            for production in productions:
                first_alpha = self.first[production[0]]
                for a in first_alpha:
                    if a in terminals and a != '\\L':
                        M[symbol][a] = production
                    if a == '\\L':
                        follow_A = self.follow[symbol]
                        if '$' in follow_A:
                            M[symbol]['$'] = production
                        for fol_a in follow_A:
                            if fol_a in terminals:
                                M[symbol][fol_a] = production
        self.parsing_table = M
        for key, value in M.items():
            print(key, ' : ', value)
        return self.parsing_table

    def generate(self):
        self.generate_parsing_table()
        self.parser = Parser(self.parsing_table)
        return self.parser
