"""Based on https://code.activestate.com/recipes/384122-infix-operators/ but clear about precedence."""


class InfixDiv:
    """Infix operator with div precedence.
    >>> 1 + 1 / 2
    1.5
    >>> div = InfixDiv(lambda x,y: x / y)
    >>> 1 + 1 /div/ 2
    1.5
    """

    def __init__(self, function):
        self.function = function

    def __rtruediv__(self, other):
        return InfixDiv(lambda x, self=self, other=other: self.function(other, x))

    def __truediv__(self, other):
        return self.function(other)

    def __call__(self, value1, value2):
        return self.function(value1, value2)


class InfixShift:
    """Infix operator with shift precedence.
    >>> 1 + 1 << 1
    4
    >>> shl = InfixShift(lambda x,y: x << y)
    >>> 1 + 1 <<shl>> 1
    4
    """

    def __init__(self, function):
        self.function = function

    def __rlshift__(self, other):
        return InfixShift(lambda x, self=self, other=other: self.function(other, x))

    def __rshift__(self, other):
        return self.function(other)

    def __call__(self, value1, value2):
        return self.function(value1, value2)
