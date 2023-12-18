import inspect
import re

from piper.exception import *

GLOBAL_VARS = {"backslash": "\\"}
FUNCTIONS = {
    "out": lambda input: print(input, end=""),
    "in": lambda: input(),
    "reverse": lambda input: input[::-1],
    "lower": lambda input: input.lower(),
    "upper": lambda input: input.upper(),
    "strip": lambda input: input.strip(),
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
    str_in = str_in.replace("\\n", "\n")

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


def exec_ast(ast):
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
                else:  # Set variable
                    GLOBAL_VARS[cmd_val] = stored_result
            elif cmd_type.endswith("-literal"):
                if cmd_type == "string-literal":
                    cmd_val = unwrap_str(cmd_val)

                stored_result = cmd_val
