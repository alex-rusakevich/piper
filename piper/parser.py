def parse(lex_sequence: list) -> list:
    ast = []

    while len(lex_sequence) > 0:
        pipeline = []
        lex_count = 0

        for lex in lex_sequence:
            (lex_type, lex_val) = lex
            lex_count += 1

            if lex_type == "command-end":
                break
            elif lex_type == "piper":
                continue
            elif lex_type == "string-literal":
                lex_val = lex_val[1:-1]
            elif lex_type == "variable-name":
                lex_val = lex_val[1:]

            pipeline.append((lex_type, lex_val))

        lex_sequence = lex_sequence[lex_count:]
        ast.append(pipeline)

    return ast
