class PiperError(BaseException):
    ...


class VarNotSetError(PiperError):
    ...


class FunctionDoesNotExistError(PiperError):
    ...


class ArgumentError(PiperError):
    ...
