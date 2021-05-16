from parser_generator.parser import Parser


class ParserGenerator:
    def __init__(self, grammar):
        self.grammar = grammar

    def first_sets(self):
        return "calc first sets for grammar"

    def follow_sets(self):
        return "calc follow sets for grammar"

    def generate_parsing_table(self):
        first_sets = self.first_sets()
        follow_sets = self.follow_sets()

        self.parsing_table = None

        return self.parsing_table

    def generate(self):
        self.generate_parsing_table()
        self.parser = Parser(self.parsing_table)
        return self.parser
