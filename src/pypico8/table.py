"""Table object functions."""

from typing import Any


class Table(dict):
    """
    In Lua, tables are a collection of key-value pairs where the key and value
    types can both be mixed. They can be used as arrays by indexing them with integers.
    >>> a=Table()  # create an empty table
    >>> a[1] = "blah"
    >>> a[2] = 42
    >>> a["foo"] = Table([1,2,3])
    >>> a
    {1: 'blah', 2: 42, 'foo': {1: 1, 2: 2, 3: 3}}

    Arrays use 1-based indexing by default:
    >>> a = Table([11,12,13,14])
    >>> a[2]
    12

    The size of a table indexed with sequential 1-based integers:
    >>> len(a)
    4

    Indexes that are strings can be written using dot notation:
    >>> player = Table()
    >>> player.x = 2  # is equivalent to player["x"]
    >>> player.y = 3
    >>> player.y
    3
    >>> foo = Table({'bar': 'baz'})
    >>> foo.bar
    'baz'

    Keyword arguments are passed as dict.
    >>> foo = Table(x=10, y=20, z=30)
    >>> foo
    {'x': 10, 'y': 20, 'z': 30}
    >>> foo.x
    10
    """

    def __init__(self, stuff=None, **kwargs):
        if stuff is not None:
            if isinstance(stuff, dict):
                for index, item in enumerate(stuff):
                    dict.__setitem__(self, "key" + str(index + 1), item)
            else:
                for index, item in enumerate(stuff):
                    dict.__setitem__(self, index + 1, item)
        else:
            stuff = kwargs

        if isinstance(stuff, dict):
            for key in stuff:
                self[key] = stuff[key]

    def __iter__(self):
        """
        >>> t = Table([10, 20, 30])
        >>> for v in t:
        ...    print(v)
        10
        20
        30
        >>> A = Table([1,10,2,11,3,12])
        >>> for k in list(A.keys()):
        ...   if A[k] < 10:
        ...     delete(A, A[k])
        ...
        1
        2
        3
        >>> foreach(A, print)
        10
        11
        12
        """
        for index in dict.__iter__(self.copy()):
            yield dict.__getitem__(self, index)

    def __getitem__(self, index):
        """
        >>> t = Table()
        >>> t[10] = "ten"
        >>> t[10]
        'ten'
        """
        if index in dict.__iter__(self):
            return dict.__getitem__(self, index)

        for i, k in enumerate(dict.__iter__(self)):
            if i + 1 == index:
                return dict.__getitem__(self, k)

        return None

    def __getattribute__(self, name: str):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self.__getitem__(name)

    def __setattr__(self, name: str, value) -> None:
        return self.__setitem__(name, value)


def add(t: Table, v: Any, index: int | None = None) -> Any:  # NOSONAR
    """https://www.lexaloffle.com/pico-8.php?page=manual#:~:text=add%20t
    add t v [index]

    Add value v to the end of Table t.
    Equivalent to t[#t+1] = v
    If index is given then the element is inserted at that position

    >>> foo = Table()
    >>> add(foo, 11)
    11
    >>> add(foo, 22)
    22
    >>> print(foo[2])
    22
    >>> bar = Table(x=0.0, y=99.0)
    >>> add(foo, bar)
    {'x': 0.0, 'y': 99.0}
    >>> foo
    {1: 11, 2: 22, 3: {'x': 0.0, 'y': 99.0}}
    """
    if index is None:
        index = len(t) + 1
    t[index] = v
    return v


# pylint:disable=redefined-builtin
def all(t: Table):
    """
    Returns an iterator for all non-nil items in a sequence in a table, for use with for...in.
    >>> t = Table([11, None, 13])
    >>> for v in all(t): print(v)
    11
    13
    >>> print(len(t))
    3
    >>> t = Table({10: "ten"})
    >>> t
    {'key1': 10, 10: 'ten'}
    >>> for v in all(t): print(v)
    >>> t[1] = "one"
    >>> for v in all(t): print(v)
    one
    """
    k = 0
    while 1:
        k += 1
        if k not in t:
            break
        if t[k] is None:
            continue
        yield t[k]


def foreach(t: Table, fun: type) -> None:
    "Apply function fun to table t."
    list(map(fun, t))


def delete(t: dict, v=None) -> Any | None:
    """
    del  t [v]

    Delete the first instance of value v in Table t
    The remaining entries are shifted left one index to avoid holes. XXX: What about string keys?!
    Note that v is the value of the item to be deleted, not the index into the Table.
    To remove an item at a particular index, use deli.
    When v is not given, the last element in the Table is removed.
    del returns the deleted item, or returns no value when nothing was deleted.

    >>> A = Table([1,10,2,11,3,12])
    >>> for k in list(A.keys()):
    ...   if A[k] < 10:
    ...     delete(A, A[k])
    ...
    1
    2
    3
    >>> foreach(A, print)
    10
    11
    12
    >>> import time; time.sleep(5)  # Give VS Code debugger time to attach to doctest process.
    >>> print(A[3])
    12
    """
    if v is None:
        try:
            return t.pop(list(t.keys())[-1])
        except IndexError:
            return None

    for k in list(t.keys()):
        if t[k] == v:
            rv = t[k]
            del t[k]
            return rv

    return None


# del is a Python keyword.
# def del():


def deli(t: Table, i: int | None = None) -> Any | None:
    """Like del(), but remove the item from table t at index i.
    >>> A = Table([1,10,2,11,3,12])
    >>> deli(A, 1)
    1
    >>> A
    {1: 10, 2: 2, 3: 11, 4: 3, 5: 12}
    >>> deli(A, 2)
    2
    >>> A
    {1: 10, 2: 11, 3: 3, 4: 12}
    >>> for v in all(A): print(v)
    10
    11
    3
    12
    """
    if i is None:
        try:
            return t.pop(list(t.keys())[-1])
        except IndexError:
            return None

    rv = None
    reindex = False
    for j, k in enumerate(list(t.keys())):
        if j + 1 == i:
            rv = t[k]
            if j + 1 == len(t):
                del t[k]
            else:
                # Don't delete; k reinsertion gets appended.
                reindex = True
        elif reindex:
            t[j] = t[k]
            if j + 1 == len(t):
                del t[k]
    return rv


def pairs(d: dict):
    """Return dict key-value pairs.
    >>> pairs({'foo': 'bar'})
    dict_items([('foo', 'bar')])
    """
    return d.items()


def ipairs(d: dict):
    """Return dict key > 1 -value pairs.
    >>> ipairs({-1: 'a', 0: 'b', 1: "c", 2: "d"})
    [(1, 'c'), (2, 'd')]
    """
    return [(k, v) for k, v in d.items() if isinstance(k, int) and k > 0]


def pack(*args) -> Table:
    """
    >>> pack('hello', 64, 64, 14)
    {1: 'hello', 2: 64, 3: 64, 4: 14}
    """
    return Table(args)


def unpack(tbl, start=1, stop=None) -> list:
    """
    >>> t = Table(["hello", 64, 64, 14])
    >>> unpack(t)
    ['hello', 64, 64, 14]
    >>> unpack(t, 2)
    [64, 64, 14]
    >>> unpack(t, 2, 3)
    [64, 64]
    """
    if stop is None:
        stop = len(tbl)
    rv = []
    for i in range(start, stop + 1):
        rv.append(tbl[i])
    return rv


def select(start, *array):
    """Lua select from array.
    >>> select(1, "a", "b", "c")
    ('a', 'b', 'c')
    >>> select(2, "a", "b", "c")
    ('b', 'c')
    >>> select("#")
    0
    >>> print(select("#", {1,2,3}, 4, 5, {6,7,8}))
    4
    """
    if start == "#":
        return len(array)
    return Table(array[start - 1 :])
