from functools import wraps


class Statics:
    class Current:
        class Value:
            def __init__(self, name):
                self.name = name

        def __init__(self, statics):
            self.__statics = statics

        def __getattr__(self, name):
            if hasattr(self.__statics, name):
                return self.Value(name)
            else:
                return None

    def __init__(self):
        self.current = self.Current(self)

    def __setattr__(self, name, value):
        if isinstance(value, self.Current.Value):
            assert value.name == name, \
                f"static.current.{value.name} can only be use to assign to " \
                f"static.{value.name}, not to static.{name}"
        else:
            super(Statics, self).__setattr__(name, value)


def with_statics(f):
    """Add static variables to a function.
    
    A function decorated with @with_statics must accept a "static variables"
    or "statics" object as its very first argument; the recommended name for
    this parameter is 'static'. This "statics" object is used access the
    function's static variables.
    
    A static variable is initialised with a value the first time control flow
    reaches its initialisation, and retains its value after that, even across
    several calls to the function. To initialise a static variable, use the
    following syntax: `static.x = static.current.x or expression`. When
    executing this statement for the first time, `expression` will be
    evaluated and stored in `static.x`. On all subsequent executions of this
    statement (even on subsequent calls to the containing function), the
    statement does nothing and `expression` is guaranteed to *not* be
    evaluated.
    
    Here's an example of using statics to implement a call counter:
    
    >>> @with_statics
    ... def counter(static):
    ...     static.val = static.current.val or 0
    ...     val = static.val
    ...     static.val += 1
    ...     return val
    >>> (counter(), counter(), counter())
    (0, 1, 2)
    
    The initialisation expression is guaranteed to only execute once:
    >>> def get_string():
    ...     print("Getting string")
    ...     return ""
    ... 
    >>> @with_statics
    ... def record(static, text):
    ...     static.recorded = static.current.recorded or get_string()
    ...     static.recorded += text
    ...     return static.recorded
    ... 
    >>> record("Hello")
    Getting string
    'Hello'
    >>> record(", world!")
    'Hello, world!'
    
    Notice the absence of "Getting string" after the second call.
    """
    statics = Statics()
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(statics, *args, **kwargs)
    return wrapper
