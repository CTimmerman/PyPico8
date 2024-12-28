"""GvR's function overloading emulation by multiple dispatch decorator."""
registry: dict = {}


class MultiMethod:
    """Overloaded function dictionary."""
    def __init__(self, name):
        self.name = name
        self.typemap = {}

    def __call__(self, *args):
        types = tuple(arg.__class__ for arg in args)  # a generator expression!
        function = self.typemap.get(types)
        if function is None:
            raise TypeError(f"no match for {self.name}{types}")
        return function(*args)

    def register(self, types, function):
        """Registers a function name including its types."""
        if types in self.typemap:
            # raise TypeError("duplicate registration")
            # print()
            # print(types, "already in")
            # for o in self.typemap:
            #     print(o)
            pass
        self.typemap[types] = function


def multimethod(*types):
    """Decorator to add types to function name to support overloads."""
    def register(function):
        name = function.__name__
        mm = registry.get(name)
        if mm is None:
            mm = registry[name] = MultiMethod(name)
        mm.register(types, function)
        return mm

    return register
