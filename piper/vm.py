import re
import string
import sys

from piper import __version_str__
from piper.exception import *
from piper.lexer import *
from piper.parser import *

GLOBAL_VARS = {
    "backslash": "\\",
    "encoding": "utf-8",
    "piper_version": __version_str__,
    "punct": string.punctuation,
}


# region Functions definitions
def piper_fn__out(*args):
    print(*args, end="")


def piper_fn__in():
    return sys.stdin.read()


def piper_fn__read_from(file_path: str):
    return open(file_path, "r", encoding=GLOBAL_VARS["encoding"]).read()


def piper_fn__write_to(file_path: str, data: str):
    open(file_path, "w", encoding=GLOBAL_VARS["encoding"]).write(data)


def piper_fn__replace(text_in, replace_what, replace_with):
    return text_in.replace(replace_what, replace_with)


def piper_fn__split(text_in, delimiter=None):
    return "\n".join(text_in.split(delimiter))


# endregion
FUNCTIONS = {
    "out": piper_fn__out,
    "invite-enter": lambda x="": input(x),
    "in": piper_fn__in,
    "reverse": lambda input: input[::-1],
    "lower": lambda input: input.lower(),
    "upper": lambda input: input.upper(),
    "strip": lambda input: input.strip(),
    "exit": lambda: sys.exit(0),
    "die": lambda: sys.exit(1),
    "read-from": piper_fn__read_from,
    "write-to": piper_fn__write_to,
    "replace": piper_fn__replace,
    "split": piper_fn__split,
}


def call_fn(fn_name, *args):
    fn = FUNCTIONS.get(fn_name, None)

    if fn is None:
        raise FunctionDoesNotExistError(f"Function does not exist: {fn_name}")

    return fn(*args)


def unwrap_str(str_in: str) -> str:
    str_in = str_in.replace("\\\\", "${backslash}")

    replacements = (
        ("\\n", "\n"),
        ("\\r", "\r"),
    )

    for to_be_repl, replacement in replacements:
        str_in = str_in.replace(to_be_repl, replacement)

    # region Paste strings
    while (matches := re.findall(r"\$\{?[a-zA-Z_]\w*\}?", str_in)) != []:
        var = matches[0]
        var_name = re.sub(r"^\${?", "", var)
        var_name = re.sub(r"}?$", "", var_name)

        if not var_name in GLOBAL_VARS:
            raise VarNotSetError(f"Variable not set: {var}")
        else:
            str_in = str_in.replace(var, GLOBAL_VARS[var_name])
    # endregion

    return str_in


def exec_ast(ast: List[List[Tuple[str, Any]]]):
    for pipeline in ast:
        stored_result = None

        for cmd in pipeline:
            cmd_type, cmd_val, args = cmd

            args = list(a[1] for a in args)

            if cmd_type == "function-name":
                if stored_result is not None:
                    args.insert(0, stored_result)

                stored_result = call_fn(cmd_val, *args)
            elif cmd_type == "variable-name":
                if stored_result is None:  # Get variable
                    if cmd_val not in GLOBAL_VARS:
                        raise VarNotSetError(f"Variable not set: {cmd_val}")

                    stored_result = GLOBAL_VARS[cmd_val]
                else:  # Set variable
                    GLOBAL_VARS[cmd_val] = stored_result
            elif cmd_type.endswith("-literal"):
                if cmd_type == "string-literal":
                    cmd_val = unwrap_str(cmd_val)

                stored_result = cmd_val


def piper_exec(str_in: str):
    return exec_ast(parse(lex(str_in)))
