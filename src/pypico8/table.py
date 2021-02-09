class Table(dict):
    """
    In Lua, tables are a collection of key-value pairs where the key and value types can both be mixed.
    They can be used as arrays by indexing them with integers.
    >>> a=Table()  # create an empty table
    >>> a[1] = "blah"
    >>> a[2] = 42
    >>> a["foo"] = Table([1,2,3])

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
    """

    def __init__(self, stuff=None, **kwargs):
        if stuff is not None:
            for index, item in enumerate(stuff):
                dict.__setitem__(self, index + 1, item)
        else:
            stuff = kwargs

        if isinstance(stuff, dict):
            for key in stuff:
                self[key] = stuff[key]

    def __iter__(self):
        for index in dict.__iter__(self.copy()):
            yield dict.__getitem__(self, index)

    def __getitem__(self, index):
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
        return super().__setitem__(name, value)


def add(t: dict, v, index=None):
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
    >>> printh(foo[2])
    22
    """
    if index is None:
        index = len(t) + 1
    t[index] = v
    return v


# pylint:disable=redefined-builtin
def all(t: Table):
    """
    Used in FOR loops to iterate over all items in a Table (that have a 1-based integer index),
    in the order they were added.

    >>> T = Table([11,12,13])
    >>> add(T,14)
    14
    >>> add(T,"HI")
    'HI'
    >>> for v in T: printh(v)
    11
    12
    13
    14
    HI
    >>> printh(len(T))
    5
    """
    return list(t.values())


def foreach(t: Table, fun: type):
    list(map(fun, t))


def delete(t: dict, v=None):
    """
    del  t [v]

    Delete the first instance of value v in Table t
    The remaining entries are shifted left one index to avoid holes. XXX: What about string keys?!
    Note that v is the value of the item to be deleted, not the index into the Table.
    To remove an item at a particular index, use deli.
    When v is not given, the last element in the Table is removed.
    del returns the deleted item, or returns no value when nothing was deleted.

    >>> A = Table([1,10,2,11,3,12])
    >>> for item in A.copy():
    ...   if item < 10: delete(A, item)
    ...
    >>> foreach(A, printh)
    10
    11
    12
    >>> import time; time.sleep(5)  # Give VS Code debugger time to attach to doctest process.
    >>> printh(A[3])
    12
    """
    if v is None:
        try:
            return t.pop(list(t.keys())[-1])
        except IndexError:
            return None

    done = False
    for k in list(t.keys()):
        if done:
            t[k - 1] = t[k]
        elif t[k] == v:
            del t[k]
            done = True
            break

    return None


def pairs(d: dict):
    return d.items()