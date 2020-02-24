from functools import wraps


class Statics:
    class AlreadyDeclared:
        def __bool__(self):
            return False

    class Init:
        def __init__(self, statics):
            object.__setattr__(self, '_Init__statics', statics)

        def __setattr__(self, name, value):
            if not isinstance(value, Statics.AlreadyDeclared):
                setattr(self.__statics, name, value)

    class Declare:
        def __init__(self, statics):
            self.__statics = statics

        def __getattr__(self, name):
            if hasattr(self.__statics, name):
                return Statics.AlreadyDeclared()
            else:
                return True

    def __init__(self):
        self.init = Statics.Init(self)
        self.declare = Statics.Declare(self)


def with_statics(f):
    statics = Statics()
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(statics, *args, **kwargs)
    return wrapper
