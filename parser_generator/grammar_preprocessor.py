import re
import os


class GrammarPreprocessor:
    def __init__(self, grammar):
        self.grammar, self.terminals, self.non_terminals = (
            grammar.grammar,
            grammar.terminals,
            grammar.non_terminals,
        )
        self.left_recursion_elimination()
        self.update_nonTerminals(1)
        self.left_factoring()
        self.update_nonTerminals(2)
        return

    def __str__(self):
        return str(self.grammar)

    def update_nonTerminals(self, flag):
        for thing in self.grammar:
            if thing not in self.non_terminals:
                self.non_terminals.add(thing)
                if flag == 1:
                    self.terminals.add("\L")
        # if flag == 1:
        #     print("GRAMMAR IS NOT LL(1)! HAD TO PERFORM LEFT RECURSIN ELEMINATION!")
        # if flag == 2:
        #     print("GRAMMAR IS NOT LL(1)! HAD TO PERFORM LEFT FACTORING!")

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
                new_derivations[non_trmnl] = [b + [non_trmnl + "_"] for b in B]
                new_derivations[non_trmnl + "_"] = [a + [non_trmnl + "_"] for a in A]
                new_derivations[non_trmnl + "_"].append(["\L"])
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
        if len(new) > len(self.grammar):
            print("GRAMMAR IS NOT LL(1)! HAD TO PERFORM LEFT RECURSION ELEMINATION!")
        self.grammar.update(new)

    def left_factoring(self):
        new = {}
        for derivation in self.grammar:
            for j, productionA in enumerate(self.grammar[derivation]):
                new_derivations = {}
                indices = list()
                for k, productionB in enumerate(self.grammar[derivation]):
                    if k <= j:
                        continue
                    if productionA[0] == productionB[0]:
                        indices.append(k)
                if len(indices) > 0:
                    new_derivations[derivation] = list()
                    new_derivations[derivation].append(
                        [productionA[0], derivation + "_"]
                    )
                    new_derivations[derivation + "_"] = list()
                    for l, production_curr in enumerate(self.grammar[derivation]):
                        if l in indices or l == j:
                            if len(production_curr) > 1:
                                new_derivations[derivation + "_"].append(
                                    production_curr[1:]
                                )
                            else:
                                new_derivations[derivation + "_"].append(["\L"])

                        else:
                            new_derivations[derivation].append(production_curr)
                    new.update(new_derivations)
        if len(new) > 0:
            print("GRAMMAR IS NOT LL(1)! HAD TO PERFORM LEFT FACTORING!")
        self.grammar.update(new)
