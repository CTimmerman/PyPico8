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
        ...   if A[k] and A[k] < 10:
        ...     delv(A, A[k])
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
        >>> t[11]
        >>> t[:1]
        {1: 'ten'}
        >>> t[1]
        """
        if isinstance(index, slice):
            start = index.start or 0
            stop = index.stop or len(self)
            step = index.step or 1
            rv = []
            keys = list(self.keys())
            for i in range(start, stop, step):
                rv.append(self.get(keys[i]))
            return Table(rv)

        if index in dict.__iter__(self):
            return dict.__getitem__(self, index)

        return None

    def __getattribute__(self, name: str):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self.__getitem__(name)

    def len(self):
        """Only counts sequential items! Lua is awful.
        See also https://www.reddit.com/r/pico8/comments/cab542/length_of_tables_containing_nil_values/
        >>> t = Table([10, None, 20])
        >>> t.len()
        3
        >>> t[4] = 30
        >>> t.len()
        4
        >>> t[6] = 40
        >>> t.len()
        4
        """
        rv = 1
        while rv in self:
            rv += 1
        return rv - 1

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
    """Apply function fun to table t."""
    list(map(fun, t))


def delv(*args) -> Any | None:
    """(del is a Python keyword)
    delv  t [v]

    Delete the first instance of value v in Table t.
    The remaining sequential entries are shifted left one index to avoid holes.
    To remove an item at a particular index, use deli.
    delv returns the deleted item or None.

    >>> A = Table([1,10,2,11,3,12])
    >>> for k in list(A.keys()):
    ...   if A[k] and A[k] < 10:
    ...     delv(A, A[k])
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
    >>> print(A[4])
    None
    >>> A
    {1: 10, 2: 11, 3: 12}
    >>> A[2]
    11
    >>> A["foo"] = "bar"
    >>> A.len()
    3
    >>> delv(A, 10)
    10
    >>> delv(A)
    >>> delv(A, 99)
    >>> delv(Table())
    >>> t = Table([10, None, 30])
    >>> t.len()
    3
    """
    if len(args) < 2:
        return None
    t, v = args[:2]
    rv = None
    last_k = None
    for k in list(t.keys()):
        if last_k:
            if last_k + 1 == k:
                t[last_k] = t[k]
                del t[k]
                last_k = k
            else:  # Only sequential keys get reindexed.
                return rv
        elif t[k] == v:
            rv = t[k]
            del t[k]
            last_k = k
    return rv


# del is a Python keyword.
# def del():


def deli(t: Table, i: int | None = None) -> Any | None:
    """Like del(), but remove the item from table t at index i or the end.
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
    >>> deli(A)
    12
    >>> deli(A, 3)
    3
    >>> deli(Table())
    """
    if i is None:
        try:
            return t.pop(list(t.keys())[-1])
        except IndexError:
            return None

    # No pointer to reassign! Python is a toy language.
    # keys = list(t.keys())
    # rv = t.get(keys[i])

    # keys = keys[:i] + keys[i+1:]
    # t2 = []
    # for k in keys:
    #     t2.append(t.get(k))
    # t = Table(t2)

    # return rv

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
    """Lua select from array. https://pico-8.fandom.com/wiki/Select
    Pico8 0.2.2c returns only the index value though, at a messed up location.

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
    return array[start - 1 :]
