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

# Pause Black formatter to not mess this up.
# fmt: off
CHARS = [
    '?', '¹', '²', '³', '⁴', '⁵', '⁶', '?', '?', '?', '?', '?', '?', '?', '?', '?',  # 16
    '▌', '⯀','⚬', '×', '∷', '⏸', '⏴','⏵', '⌜','⌟', '¥', '⬝', '⹁', '․', '"', '˚',  # 32
    ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',  # 48
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',  # 64
    '@', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',  # 80
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '[', '\\',']', '^', '_',  # 96
    '`', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',  # 112
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '{', '|', '}', '?', '○',  # 128
    '█', '▒','🐱','⬇️','░', '✽','⚈', '♥', '⟐','웃','🏠','⬅️','😐', '♪','🅾️','♦',  # 144
    '…','➡️','★','⧗','⬆️','ˇ','∧','❎','▤', '⦀','あ', 'い','う','え','お','か',  # 160
    'ぎ','く','け','こ','さ','し','す','せ', 'そ','た','ち','つ','て','と','な','に',  # 176
    'ぬ','ね','の','は','ひ','ふ','へ','ほ', 'ま','み','む','め','も','や','ゆ','よ',  # 192
    'ら','り','る','れ','ろ','わ','を','ん', 'ゔ','っ','ぇ','ょ','ア','イ','ウ','エ',  # 208
    'オ','カ','キ','ク','ケ','コ','サ','シ', 'ス','セ','ソ','タ','チ','ツ','テ','ト',  # 224
    'ナ','ニ','ヌ','ネ','ノ','ハ','ヒ','フ', 'ヘ','ホ','マ','ミ','ム','メ','モ','ヤ',  # 240
    'ユ','ヨ','ラ','リ','ル','レ','ロ','ワ', 'ヲ','ン','ッ','ャ','ュ','?', 'ᨀ','⺀',  # 256
]
# fmt: on


def printh(
    s: str, filename: str = "", overwrite: bool = False, save_to_desktop: bool = False
) -> None:
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
    elif filename:
        p = pathlib.Path(filename).resolve()
        p2 = pathlib.Path(sys.argv and sys.argv[0] or sys.executable).parent.resolve()
        if not str(p).startswith(str(p2)):
            raise IOError(f"path {p} not in {p2}")
    if filename:
        with open(filename, "w" if overwrite else "a", encoding="UTF8") as fp:
            fp.write(s)
    else:
        builtins.print(s)


def pico8_to_python(s: str) -> str:
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
    # comments
    s = re.sub(r"--\[\[(.*?)\]\]", r"'''\1'''", s, flags=re.DOTALL)
    s = re.sub(r"\[\[(.*?)\]\]", r'"""\1"""', s, flags=re.DOTALL)
    s = s.replace("--", "#")
    # operators
    s = s.replace("...", "*argv")
    s = s.replace("..", "+")
    s = re.sub(r"//\s*1\b", "#int()", s)
    s = s.replace("~=", "!=")
    s = s.replace(">>", "|shr|")
    s = s.replace("/", "|div|")
    s = re.sub(r"\\([^n])", r"|divi|\1", s)
    s = s.replace("^", "**")
    s = re.sub(r",%([a-zA-Z0-9]+)", r",peek2(\1)", s)
    # loops, whose variable is local to the loop (TODO). https://www.lexaloffle.com/bbs/?pid=51130#p
    s = re.sub(r"([0-9)\] ])\s*do\b", r"\1:", s)
    s = re.sub(
        r"for (.*?)=(.+?),(.+?),(.+?):",
        r"""\1 = \2\nwhile 1:
if \1 == \3: break; \1 += \4  # TODO, move to end of loop & maybe use \1 = round(\1 + \4, 4)
""",
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


def hex_fraction(decimal_number: float, precision: int = 4) -> str:
    """Converts a decimal fraction to a string with a given precision.
    >>> hex_fraction(0.5)
    '8000'
    >>> hex_fraction(255.5)
    'FF8000'
    """
    hex_result = ""
    fraction = decimal_number

    for _ in range(precision):
        fraction *= 16
        digit = int(fraction)
        hex_result += hex(digit)[2:].upper()
        fraction -= digit

    return hex_result


def tostr(val: int | float | str, use_hex: bool = False) -> str:
    """Value to string or hex string.
    >>> tostr(244)
    '244'
    >>> tostr(244, 1)
    '0X00F4.0000'
    >>> tostr(1.8, 1)
    '0X0001.CCCC'
    >>> tostr(1.5, 1)
    '0X0001.8000'
    """
    if use_hex:
        whole, part = divmod(float(val), 1)
        whole = int(whole)
        if part:
            return f"0X{hex(whole).upper()[2:]:>04}.{hex_fraction(part)}"
        return f"0X{hex(whole).upper()[2:]:>04}.0000"
    return str(val)


def tonum(s: str | int | float) -> int | float | None:
    """Converts a string representation of a decimal, hexadecimal,
    or binary number to a number value or None.

    >>> tonum("65.6")
    65.6
    >>> tonum("0x11")
    17
    >>> tonum("0b11")
    3
    >>> tonum("0b11.1")
    3.5
    >>> tonum("0.5555555555555")
    0.5556
    """
    if type(s) in (int, float):
        return s  # type: ignore

    if s is None:
        return 0

    base = 10
    if isinstance(s, str):
        if "x" in s:
            base = 16
        elif "b" in s:
            base = 2
        a = s.split(".")
        if len(a) > 1:
            if base == 10:
                return round(float(s), 4)
            whole, part = a
            return round(int(whole, base) + int(part, base) / base ** len(part), 4)  # type: ignore
    try:
        return int(s, base)  # type: ignore
    except TypeError as ex:
        # "TypeError: int() can't convert non-string with explicit base" is too vague.
        raise TypeError(f"to_num got type {type(s)}") from ex
    except ValueError:
        return None


def chr(*index: int | float | str) -> str:  # noqa
    """Number to p8nsi char.
    >>> chr("65.6")
    'a'
    >>> chr(104,101,108,108,111)
    'HELLO'
    """
    s = ""
    for i in index:
        s += CHARS[flr(tonum(i)) % 256]  # type: ignore[arg-type]
    return s


def ord(s: str, index: int = 1) -> int:  # noqa
    """Match source code char to Pico8 char in docs/pico-8_font_020.png.
    >>> ord('a')
    65
    """
    # printh(f"Ord got s {s}, index {index} from {sys._getframe().f_back.f_code.co_name}")
    c = s[index - 1]
    if c == "?":
        return 63
    if c == "☉" or s == "🅾️":
        return 142
    n = builtins.ord(c)
    if 120354 <= n <= 120379:
        # Mathematical Sans-Serif Italic Small A-Z.
        return n - 120354 + 65  # Lowercase p8nsi A-Z.
    return CHARS.index(c)


def sub(s: str, pos0: int, pos1: int | None = None) -> str:
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
    >>> sub("hello", 3)
    'llo'
    """
    pos0 = flr(pos0) - (1 if pos0 >= 1 else 0)
    if pos1 is not None:
        pos1 = flr(pos1)
        if pos1 < 0:  # type: ignore
            pos1 += 1  # type: ignore
            if pos1 >= 0:
                pos1 = None
    return s[pos0:pos1]


def split(s: str, separator: str = ",", convert_numbers: bool = True) -> Table:
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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
