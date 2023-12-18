import re
from typing import Any, List, Tuple

from piper.exception import PiperSyntaxError
from piper.utils import get_line_by_char_pos

LEX_TYPES = {
    "string-literal": r"\".*\"",
    "function-name": r"[a-zA-Z_]\w*",
    "variable-name": r"\$[a-zA-Z_]\w*",
    "piper": r"->",
    "command-end": r"[;\n]",
    "space": r"\s+",
}


def lex(command_str: str) -> List[Tuple[str, Any]]:
    command = command_str
    lex_sequence = []
    moving_pointer = 0

    while command != "":
        matched_smth = False

        for k, v in LEX_TYPES.items():
            if match_obj := re.match(v, command):
                matched_smth = True

                command = command[match_obj.end() :]
                moving_pointer += match_obj.end() - 1

                lex = (k, match_obj.group(0))

                if k == "space":
                    break

                lex_sequence.append(lex)
                break

        if not matched_smth:
            mistake_str, line_pos, char_pos = get_line_by_char_pos(
                command_str, moving_pointer
            )
            mistake_str += (
                "\n" + "~" * (char_pos - 1) + "^" * (len(mistake_str) - char_pos + 1)
            )

            raise PiperSyntaxError(
                "Unknown syntax (line {}, char {}):\n{}".format(
                    line_pos, char_pos, mistake_str
                )
            )

    if len(lex_sequence) == 0 or lex_sequence[-1][0] != "command-end":
        lex_sequence.append(("command-end", ";"))

    return lex_sequence
