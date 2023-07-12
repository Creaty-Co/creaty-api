class UndefinableVariable(str):
    def __mod__(self, variable):
        from jinja2 import UndefinedError

        raise UndefinedError(variable)
