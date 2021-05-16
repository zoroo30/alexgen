class Parser:
    def __init__(self, parsing_table):
        self.parsing_table = parsing_table

    def set_input_src(self, get_next_token):
        self.get_next_token = get_next_token

    def parse(self):
        if not hasattr(self, "get_next_token"):
            raise Exception("no input source")

        print("parsing")
        next_token = self.get_next_token()
        while next_token != "$":
            print(next_token)
            next_token = self.get_next_token()

    def write_output(self):
        # print("writing output")
        return
