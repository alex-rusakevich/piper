import re
from typing import Any, List, Tuple

from piper.exception import PiperSyntaxError

LEX_TYPES = {
    "piper": r"->",
    "arg-separator": r"\,",
    "string-literal": r"\"[^\"]*\"",
    "float-literal": r"\d*\.\d+",
    "integer-literal": r"\d+",
    "function-name": r"[\w\-][\w\-]*",
    "variable-name": r"\$[\w\-][\w\-]*",
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

                if k in "space":
                    break

                if lex[0] == "arg-separator" and (
                    len(lex_sequence) < 1
                    or not lex_sequence[-1][0].endswith("-literal")
                ):
                    raise PiperSyntaxError(
                        "Unneeded comma separator", command_str, moving_pointer
                    )

                if (
                    len(lex_sequence) >= 1 and lex_sequence[-1][0].endswith("-literal")
                ) and lex[0] not in ("piper", "arg-separator", "command-end"):
                    print(lex)
                    print(lex_sequence)
                    raise PiperSyntaxError(
                        "Piper enumerations must use comma", command_str, moving_pointer
                    )

                lex_sequence.append(lex)
                break

        if not matched_smth:
            raise PiperSyntaxError("Unknown syntax", command_str, moving_pointer)

    if len(lex_sequence) == 0 or lex_sequence[-1][0] != "command-end":
        lex_sequence.append(("command-end", ";"))

    return lex_sequence
