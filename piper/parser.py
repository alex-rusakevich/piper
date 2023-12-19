from typing import Any, List, Tuple


def parse(lex_sequence: List[Tuple[str, Any]]) -> List[List[Tuple[str, Any]]]:
    ast: List[List[Tuple[str, Any]]] = []

    while len(lex_sequence) > 0:
        pipeline: List[Tuple[str, Any]] = []
        args: List[Tuple[str, Any]] = []
        lex_count = 0

        populating_func_args = False

        for lex in lex_sequence:
            (lex_type, lex_val) = lex
            lex_count += 1

            if lex_type == "command-end":
                populating_func_args = False
                args = []
                break
            elif lex_type == "piper":
                populating_func_args = False
                args = []
                continue
            elif lex_type == "string-literal":
                lex_val = lex_val[1:-1]
            elif lex_type == "variable-name":
                lex_val = lex_val[1:]
            elif lex_type == "arg-separator":
                continue

            if not populating_func_args:
                pipeline.append((lex_type, lex_val, args))
            else:
                args.append((lex_type, lex_val))

            if lex_type == "function-name":
                populating_func_args = True

        lex_sequence = lex_sequence[lex_count:]

        if pipeline != []:
            ast.append(pipeline)

    return ast
