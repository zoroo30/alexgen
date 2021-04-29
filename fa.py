from pyvis.network import Network


class FA:
    def __init__(self):
        self.alphabet = {}
        self.initial_state = None
        self.final_states = {}
        self.transition_table = {}

    def visualize(self, output_file):
        g = Network(height="100%", width="100%", directed=True)

        g.set_edge_smooth("dynamic")
        for state in self.transition_table:
            border_width = 1
            color = "#dedede"

            if state in self.final_states:
                border_width = 5

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

        g.show(output_file)