class TestingTokens:
    testing_tokens = [
        "id",
        ";",
        "var",
        "id",
        ",",
        "id",
        ":",
        "integer",
        ";",
        "begin",
        "id",
        "assign",
        "num",
        ";",
        "while",
        "id",
        "relop",
        "num",
        "do",
        "begin",
        "id",
        "assign",
        "id",
        "addop",
        "num",
        ";",
        "read",
        "(",
        "id",
        ")",
        ";",
        "if",
        "id",
        "num",
        "then",
        "id",
        "assign",
        "id",
        "addop",
        "num",
        "else",
        "id",
        "assign",
        "id",
        "addop",
        "id",
        "end",
        ";",
        "write",
        "(",
        "id",
        ",",
        "id",
        ")",
        "end",
        "."
    ]

    current_testing_token_index = 0

    @staticmethod
    def get_next_testing_token():
        if TestingTokens.current_testing_token_index > len(
            TestingTokens.testing_tokens
        ):
            return None
        if TestingTokens.current_testing_token_index == len(
            TestingTokens.testing_tokens
        ):
            TestingTokens.current_testing_token_index += 1
            return "$"

        curr = TestingTokens.current_testing_token_index
        TestingTokens.current_testing_token_index += 1

        return TestingTokens.testing_tokens[curr]
