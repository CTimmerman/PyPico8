"""https://code.activestate.com/recipes/384122-infix-operators/
Definition of an Infix operator class.
This recipe also works in Jython.
Calling sequence for the infix is either:
  x |op| y
or:
  x <<op>> y

Examples

simple multiplication
>>> x=Infix(lambda x,y: x*y)
>>> print(2 |x| 4)
8

# class checking
>>> isa=Infix(lambda x,y: x.__class__==y.__class__)
>>> print([1,2,3] |isa| [])
True
>>> print([1,2,3] <<isa>> [])
True

# inclusion checking
>>> is_in=Infix(lambda x,y: x in y)
>>> print(1 |is_in| {1:'one'})
True
>>> print(1 <<is_in>> {1:'one'})
True

# an infix div operator
>>> import operator
>>> div=Infix(operator.floordiv)
>>> print(10 |div| (4 |div| 2))
5
"""


class Infix:
    "Infix operator."

    def __init__(self, function):
        self.function = function

    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __or__(self, other):
        return self.function(other)

    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __rshift__(self, other):
        return self.function(other)

    def __call__(self, value1, value2):
        return self.function(value1, value2)
