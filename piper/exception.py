class PiperError(BaseException):
    ...


class PiperSyntaxError(PiperError):
    ...


class VarNotSetError(PiperError):
    ...


class FunctionDoesNotExistError(PiperError):
    ...


class ArgumentError(PiperError):
    ...
