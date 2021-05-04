from pyvis.network import Network


class FA:
    def __init__(self):
        self.alphabet = {}
        self.initial_state = None
        self.final_states = {}
        self.transition_table = {}
        self.dead_states = set()

    def visualize(self, output_file, labels, physics=True):
        g = Network(height="100%", width="100%", directed=True)

        g.set_edge_smooth("continuous")
        g.toggle_physics(physics)
        for state in self.transition_table:
            border_width = 1
            border_width_selected = 2
            color = "#dedede"
            title = str(state)

            if state in self.final_states:
                color = "#b0ee64"
                border_width = 5
                border_width_selected = 7
                title = labels[self.final_states[state]]

            if state == self.initial_state:
                color = "#6492ee"

            if self.dead_states and state in self.dead_states:
                color = "#ee6464"

            state = str(state)

            g.add_node(
                state,
                label=state,
                title=title,
                shape="circle",
                color=color,
                borderWidth=border_width,
                borderWidthSelected=border_width_selected,
            )

        for state in self.transition_table:
            from_state = str(state)
            for ch in self.transition_table[state]:
                if type(self).__name__ == "NFA":
                    for s in self.transition_table[state][ch]:
                        to_state = str(s)
                        g.add_edge(
                            from_state,
                            to_state,
                            label=ch,
                            arrowStrikethrough=False,
                        )
                else:
                    to_state = str(self.transition_table[state][ch])
                    g.add_edge(
                        from_state,
                        to_state,
                        label=ch,
                        arrowStrikethrough=False,
                    )

        g.show(output_file)