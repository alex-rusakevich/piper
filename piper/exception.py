from piper.utils import get_line_by_char_pos


class PiperError(BaseException):
    ...


class PiperSyntaxError(PiperError):
    def __init__(self, message, text, abs_char_pos):
        mistake_str, line_pos, char_pos = get_line_by_char_pos(text, abs_char_pos)
        mistake_str += (
            "\n" + "~" * (char_pos - 1) + "^" * (len(mistake_str) - char_pos + 1)
        )

        msg = ("{} (line {}, char {}):\n{}").format(
            message, line_pos, char_pos, mistake_str
        )

        super().__init__(msg)


class VarNotSetError(PiperError):
    ...


class FunctionDoesNotExistError(PiperError):
    ...


class ArgumentError(PiperError):
    ...


class NotReadyYet(PiperError):
    ...
