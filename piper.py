#!/usr/bin/env python3
import re

from piper import __author__, __version_str__
from piper.vm import exec_ast


def repl():
    command = input("[Command]: ")

    # region Lexing
    LEX_TYPES = {
        "string-literal": r"\".*\"",
        "function-name": r"[a-zA-Z_]\w*",
        "variable-name": r"\$[a-zA-Z_]\w*",
        "piper": r"->",
        "space": r"\s+",
        "command-end": r"[;\n]",
    }

    lex_sequence = []
    moving_pointer = 0

    while command != "":
        lex = ()

        for k, v in LEX_TYPES.items():
            if match_obj := re.match(v, command):
                command = command[match_obj.end() :]
                moving_pointer += match_obj.end() - 1

                lex = (k, match_obj.group(0))

                if k == "space":
                    break

                lex_sequence.append(lex)
                break

        if lex == ():
            raise SyntaxError("Unknown syntax at position " + str(moving_pointer))

    if len(lex_sequence) == 0 or lex_sequence[-1][0] != "command-end":
        lex_sequence.append(("command-end", ";"))
    # endregion

    # region Parsing
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
    # endregion

    exec_ast(ast)


def main():
    print(f"piper v{__version_str__}, created by {__author__}\n")

    while True:
        repl()


if __name__ == "__main__":
    main()
