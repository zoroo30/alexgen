# nfa example
# transition_table = {0: {"0": [0], "1": [0, 1]}, 1: {"0": [2], "1": [2]}, 2: {"0": [], "1": []}}
# nfa = NFA(0, {2}, ["0", "1"], tt)
from pyvis.network import Network
import random

OPERATORS_1 = set(['+', '*',])  # set of operators
OPERATORS_2 = set(['-', '.','|'])

class NFA:
    def __init__(self, initial_state=0, final_states={}, inputs=[], transition_table={}, postfix=None):

        if postfix == None:
            self.inputs = frozenset(inputs)
            self.initial_state = initial_state
            self.final_states = final_states
            self.transition_table = transition_table
            self.alphabet =  frozenset(inputs)
        else:
            # TODO BASEM
            #print(postfix)

            stack = []

            for i in range(len(postfix)):
                if postfix[i] in OPERATORS_1:
                    operand_1 = stack.pop()
                elif postfix[i] in OPERATORS_2:
                    operand_2_1 = stack.pop()
                    operand_2_2 = stack.pop()
                #add if thing is /
                
                # this is a character that i need to transform to NFA then push on stack
                # but i realized i cant do that bec of the '-' operations as its takes input 2 char
                # 2 options ; 1- change in the range to accept nfa
                else:

                    tt_temp = {0: { postfix[i]: [1]}, 1: {}}
                    nfa_temp = NFA(0, {1}, postfix[i], tt_temp)

                    stack.append(nfa_temp)

                    pass 
                    #


            print("HI BASEM")
            pass


    def isFinal(self, state):
        return state in self.final_states

    def __str__(self):
        x = "<NFA initial_state:%s final_states:%s inputs:%s \n transition_table:%s \n" % (
            self.initial_state,
            self.final_states,
            self.inputs,
            self.transition_table,
        )

        for state in self.transition_table:
            x+="state:[%s] " %(state)
            for inp in self.transition_table[state]:
                if inp == "":
                    x+="%s->%s , "% ("EPS",self.transition_table[state][inp])
                else:
                    x+="%s->%s , "% (inp,self.transition_table[state][inp])
            x+="\n"

        return x

    def visualize(self):
        g = Network(height="100%", width="100%", directed=True)


        g.set_edge_smooth("dynamic")
        for state in self.transition_table:
            border_width = 1
            color = "#dedede"

            if state in self.final_states:
                border_width = 5
                color = "red"


            if state == self.initial_state:
                color = "#6492ee"

            g.add_node(
                state,
                label=state,
                shape="circle",
                color=color,
                borderWidth=border_width,
            )

        for state in self.transition_table:
            for ch in self.transition_table[state]:
                if type(self).__name__ == "NFA":
                    for s in self.transition_table[state][ch]:
                        g.add_edge(
                            state,
                            s,
                            label=ch,
                            arrowStrikethrough=False,
                        )
                else:
                    g.add_edge(
                        state,
                        self.transition_table[state][ch],
                        label=ch,
                        arrowStrikethrough=False,
                    )

        n = random.random() 
        g.show("out"+str(n)+".html")