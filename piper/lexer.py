import re
from typing import Any, List, Tuple

from piper.exception import PiperSyntaxError

LEX_TYPES = {
    "string-literal": r"\".*\"",
    "function-name": r"[a-zA-Z_]\w*",
    "variable-name": r"\$[a-zA-Z_]\w*",
    "piper": r"->",
    "space": r"\s+",
    "command-end": r"[;\n]",
}


def lex(command_str: str) -> List[Tuple[str, Any]]:
    command = command_str
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
            raise PiperSyntaxError("Unknown syntax at position " + str(moving_pointer))

    if len(lex_sequence) == 0 or lex_sequence[-1][0] != "command-end":
        lex_sequence.append(("command-end", ";"))

    return lex_sequence
