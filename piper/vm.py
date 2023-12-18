import inspect
import re
import sys

from piper.exception import *
from piper.lexer import *
from piper.parser import *


# region Functions definitions
def piper_fn__out(input):
    print(input, end="")


def piper_fn__in():
    return sys.stdin.read()


# endregion


GLOBAL_VARS = {"backslash": "\\"}
FUNCTIONS = {
    "out": piper_fn__out,
    "enter": lambda: input(),
    "in": piper_fn__in,
    "reverse": lambda input: input[::-1],
    "lower": lambda input: input.lower(),
    "upper": lambda input: input.upper(),
    "strip": lambda input: input.strip(),
    "exit": lambda: sys.exit(0),
    "die": lambda: sys.exit(1),
}


def call_fn(fn_name, input=None):
    fn = FUNCTIONS.get(fn_name, None)

    if fn is None:
        raise FunctionDoesNotExistError(f"Function does not exist: {fn_name}")

    fn_args = inspect.signature(fn).parameters

    if len(fn_args) == 0 and input is not None:
        raise ArgumentError(f"Function {fn_name} takes no arguments")

    if len(fn_args) == 0 and input is None:
        return fn()
    else:
        return fn(input)


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
            cmd_type, cmd_val = cmd

            if cmd_type == "function-name":
                stored_result = call_fn(cmd_val, stored_result)
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
