"""Pico8 string functions."""
# pylint:disable = import-outside-toplevel, multiple-imports, redefined-builtin, wrong-import-position
import builtins, os, pathlib, sys  # noqa: E401

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pypico8.math import flr
from pypico8.table import Table


BTN_X = "❎"
BTN_O = "🅾️"
BTN_LEFT = "⬅️"
BTN_RIGHT = "➡️"
BTN_UP = "⬆️"
BTN_DOWN = "⬇️"
PROBLEMATIC_MULTI_CHAR_CHARS = (BTN_O, BTN_X, BTN_LEFT, BTN_RIGHT, BTN_UP, BTN_DOWN)


def printh(s, filename=None, overwrite=False, save_to_desktop=False):
    """
    >>> filename = "pico8_printh_test.txt"
    >>> printh('pico8 printh test', filename, overwrite=True, save_to_desktop=True)
    >>> open(os.path.join(os.environ["HOMEPATH"], "Desktop", os.path.split(filename)[1])).read()
    'pico8 printh test'
    >>> printh('naughty',  '../../../../../../../../../../important')  # doctest:+ELLIPSIS
    Traceback (most recent call last):
    OSError: path ...
    """
    if save_to_desktop:
        filename = os.path.join(
            os.environ["HOMEPATH"], "Desktop", os.path.split(filename)[1]
        )
    else:
        p = pathlib.Path(filename).resolve()
        p2 = pathlib.Path(sys.argv and sys.argv[0] or sys.executable).parent.resolve()
        if not str(p).startswith(str(p2)):
            raise IOError(f"path {p} not in {p2}")
    if filename:
        with open(filename, "w" if overwrite else "a", encoding="UTF8") as fp:
            fp.write(s)
    else:
        builtins.print(s)


def pico8_to_python(s):
    r"""Hackily translates PICO-8 to Python.
    >>> pico8_to_python('for i=0,30 do ?"웃"')
    'def _init():\n    global \nfor i in range(0, 30+1): print("웃")\nrun(_init, _update, _draw)'
    """
    import re  # noqa

    s = s.replace("local", "")
    s = re.sub(r"#([a-zA-Z0-9]+)", r"len(\1)", s)
    # Lua table
    s = s.replace("{[0]=", "([").replace("}", "])")  # 0-based
    s = s.replace("{", "Table([")  # 1-based
    # logic
    s = re.sub(r"\s*then", ":", s)
    s = s.replace("elseif", "elif")
    s = s.replace("else", "else:")
    s = re.sub(
        r"function\b\s*([^)]+)\)", r"def \1):\n    ", s
    )  # Note: Extra parameters are default None.
    s = s.replace("end", "# }")
    # operators
    s = s.replace("...", "*argv")
    s = s.replace("..", "+")
    s = s.replace("^", "**")
    s = s.replace("/", "|div|")
    s = s.replace("\\", "|divi|")
    s = s.replace(">>", "|shr|")
    s = re.sub(r"//\s*1\b", "#int()", s)
    s = s.replace("~=", "!=")
    s = re.sub(r",%([a-zA-Z0-9]+)", r",peek2(\1)", s)
    # comments
    s = re.sub(r"--\[\[(.*?)\]\]", r"'''\1'''", s, flags=re.DOTALL)
    s = re.sub(r"\[\[(.*?)\]\]", r'"""\1"""', s, flags=re.DOTALL)
    s = s.replace("--", "#")
    # loops, whose variable is local to the loop (TODO). https://www.lexaloffle.com/bbs/?pid=51130#p
    s = re.sub(r"([0-9)\] ])\s*do\b", r"\1:", s)
    s = re.sub(
        r"for (.*?)=(.+?),(.+?),(.+?):",
        r'''\1 = \2\nwhile 1:
if \1 == \3: break; \1 += \4  # TODO, move to end of loop & maybe use \1 = round(\1 + \4, 4)
''',
        s,
    )
    s = re.sub(
        r"for (.*?)=([^,]+),(.*?):",
        r"for \1 in range(\2, \3+1):",
        s,
    )
    # print
    # s = (
    #     s.replace(BTN_X, "P0_X")
    #     .replace(BTN_O, "P0_O")
    #     .replace(BTN_LEFT, "P0_LEFT")
    #     .replace(BTN_RIGHT, "P0_RIGHT")
    #     .replace(BTN_UP, "P0_UP")
    #     .replace(BTN_DOWN, "P0_DOWN")
    # )
    s = re.sub(r"print\(?(\b[^\)]+?)\)?", r"print(\1)", s)
    s = re.sub(r"\?\s*(.*)", r"print(\1)", s)

    s = re.sub(r"\bdel\b", "delete", s)
    # separate statements
    s = re.sub(r"([\])0-9])([a-zA-Z])", r"\1\n\2", s)
    # hooks
    s = "def _init():\n    global \n" + s
    s = re.sub(r"\n{3,}", r"\n\n", s)
    s = s.replace("::_::", "\n\n\ndef _update(): pass\n\n\ndef _draw():\n    global \n")
    s = s.replace("goto _", "return")
    s = s.replace("def update():\n", "def update():\n    global ")
    if "_update60" in s:
        s += "\nrun(_init, _update60, _draw)"
    else:
        s += "\nrun(_init, _update, _draw)"
    return s


def tostr(val, use_hex=False) -> str:
    """Value to string or hex string.
    >>> tostr(244)
    '244'
    >>> tostr(244, 1)
    '0X00F4.0000'
    """
    if use_hex:
        return f"0X{hex(val).upper()[2:]:>04}.0000"
    return str(val)


def tonum(s) -> int:
    """Converts a string representation of a decimal, hexadecimal,
    or binary number to a number value or None."""
    if type(s) in (int, float):
        return s

    if s is None:
        return 0

    base = 10
    if isinstance(s, str):
        if "x" in s:
            base = 16
        elif "b" in s:
            base = 2

    try:
        return int(s, base)
    except ValueError:
        return 0


def chr(index) -> str:  # noqa
    "Number string to char."
    return builtins.chr(flr(tonum(index) % 256))


def ord(s, index=1) -> int:  # noqa
    """
    >>> ord("@")
    64
    >>> ord("123", 2)   # returns 50 (the second character: "2")
    50
    """
    c = s[index - 1]
    return builtins.ord(c)


def sub(s: str, pos0: int, pos1: int | None=None) -> str:
    """
    Grab a substring from string str, from pos0 up to and including pos1.
    When pos1 is not specified, the remainer of the string is returned.

    >>> s = "the quick brown fox"
    >>> sub(s, 5, 9)
    'quick'
    >>> sub(s, -2.1, -.1)
    'fox'
    >>> sub(s, -2.1, -2)
    'fo'
    """
    pos0 = flr(pos0) - (1 if pos0 >= 1 else 0)
    if pos1 is not None:
        pos1 = flr(pos1)
        if pos1 < 0:
            pos1 += 1
            if pos1 >= 0:
                pos1 = None
    return s[pos0 : pos1]


def split(s: str, separator=",", convert_numbers=True) -> Table:
    """
    Split a string into a table of elements delimited by the given separator (defaults to ",").
    When convert_numbers is true, numerical tokens are stored as numbers (defaults to true).
    Empty elements are stored as empty strings.
    When the separator is "", every character is split into a separate element.

    >>> split("1,2,3")
    {1: 1, 2: 2, 3: 3}
    >>> split("one:two:3",":",False)
    {1: 'one', 2: 'two', 3: '3'}
    >>> split("1,,2,")
    {1: 1, 2: '', 3: 2, 4: ''}
    """
    result = []
    items = s.split(separator)
    for item in items:
        if convert_numbers:
            try:
                if item == "":
                    result.append("")
                else:
                    result.append(tonum(item))  # type: ignore
            except ValueError:
                result.append(item)
        else:
            result.append(item)
    return Table(result)
