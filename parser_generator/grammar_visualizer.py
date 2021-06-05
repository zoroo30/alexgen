from pyvis.network import Network
import os
import webbrowser


class GrammarVisualizer:
    def __init__(self, grammar=False):
        self.grammar = grammar
        return

    def __str__(self):
        return str(self.grammar)

    def set_grammar(self, grammar):
        self.grammar = grammar

    def draw_transition_diagrams(
        self, physics=True, output_file="transition_diagrams.html"
    ):
        if not self.grammar:
            return
        g = Network(height="100%", width="100%", directed=True)
        g.set_edge_smooth("continuous")
        g.toggle_physics(physics)
        state_counter = -1
        for non_terminal in self.grammar:
            border_width = 1
            border_width_selected = 2
            color = "#dedede"
            state_counter += 1
            title = str(state_counter)

            start_state = title

            g.add_node(
                title,
                label=non_terminal,
                title=non_terminal,
                shape="diamond",
                color="#6492ee",
                borderWidth=border_width,
                borderWidthSelected=border_width_selected,
            )

            end_state = -1
            for production in self.grammar[non_terminal]:
                from_state = start_state
                for i, p in enumerate(production):
                    if i == len(production) - 1:
                        if end_state == -1:
                            color = "#b0ee64"
                            state_counter += 1
                            end_state = state_counter
                        title = str(end_state)
                    else:
                        color = "#dedede"
                        state_counter += 1
                        title = str(state_counter)

                    g.add_node(
                        title,
                        label=title,
                        title=title,
                        shape="circle",
                        color=color,
                        borderWidth=border_width,
                        borderWidthSelected=border_width_selected,
                    )
                    g.add_edge(
                        from_state,
                        title,
                        label=p,
                        arrowStrikethrough=False,
                    )
                    from_state = title

        output_file = (
            os.environ.get("PARSER_OUTPUT_FOLDER") + "visualization/" + output_file
        )
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        g.write_html(output_file)
        webbrowser.open("file://" + os.path.realpath(output_file))
