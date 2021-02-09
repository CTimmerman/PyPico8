"""Pico8 functions in Python
2021-01-03 v1.0 by Cees Timmerman
2021-01-04 v1.0.1 fixed palette in line()
2021-01-04 v1.1 added color, circle, mid, oval, and rect functions.
2021-01-07 v1.2 added pget, pset, palette swap, PICO-8/Lua to Python translator.
2021-01-09 v1.3 added reset, stop, fget, fset, div, sub, split, argv, btn, printh
2021-01-11 v1.4 added spr, sspr, sget, sset, screen mode 3 (64x64); fixed rect size.
2021-01-18 v1.5 added ^, ^=, for with float step, tonum, ceil, atan2, stat.
2021-01-19 v1.5.1 fixed prt color, atan2.
2021-01-25 v1.5.2 fixed prt, sget.
2021-01-27 v1.5.3 fixed cls, most Prospector problems, prt.
2021-01-29 v1.5.4 fixed fps.
2021-02-08 v1.6 Added sfx, music, clip, sgn.
"""
# pylint:disable=import-outside-toplevel,multiple-imports,pointless-string-statement,redefined-builtin,too-many-arguments,too-many-function-args,unused-import,unidiomatic-typecheck,wrong-import-position,protected-access
import builtins, base64, io, math, os, random, sys, threading
from math import ceil, floor as flr, sqrt  # noqa; unused here but maybe not elsewhere.
import time as py_time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame, pygame.freetype

# Pointers
CLIP_X1_PT = 24352
CLIP_Y1_PT = 24353
CLIP_X2_PT = 24354
CLIP_Y2_PT = 24355

false = False
true = True
BTN_X = "❎"
BTN_O = "🅾️"
BTN_LEFT = "⬅️"
BTN_RIGHT = "➡️"
BTN_UP = "⬆️"
BTN_DOWN = "⬇️"
PROBLEMATIC_MULTI_CHAR_CHARS = (BTN_O, BTN_X, BTN_LEFT, BTN_RIGHT, BTN_UP, BTN_DOWN)

# ---------- GvR's function overloading emulation by multiple dispatch decorator ---------- #
registry = {}


class MultiMethod:
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
        if types in self.typemap:
            raise TypeError("duplicate registration")
        self.typemap[types] = function


def multimethod(*types):
    def register(function):
        name = function.__name__
        mm = registry.get(name)
        if mm is None:
            mm = registry[name] = MultiMethod(name)
        mm.register(types, function)
        return mm

    return register


# ---------- Tables ---------- #
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
    list(builtins.map(fun, t))


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


# ---------- Input ---------- #
P0_LEFT = 0
P0_RIGHT = 1
P0_UP = 2
P0_DOWN = 3
P0_O = 4
P0_X = 5
P0_PAUSE = 7


def btn(i=None, p=0):
    """
    get button i state for player p (default 0)
    i: 0..5: left right up down button_o button_x
    p: player index 0..7

    If no parameters supplied, returns a bitfield of all 12 button states for player 0 & 1
    // P0: bits 0..5  P1: bits 8..13

    Default keyboard mappings to player buttons:

        player 0: [DPAD]: cursors, [O]: Z C N   [X]: X V M
        player 1: [DPAD]: SFED,    [O]: LSHIFT  [X]: TAB W Q A

    ** Note for cart authors: when
        Using a physical gamepad, certain combinations of buttons can be awkward
        (UP to jump/accelerate instead of [X] or [O]) or even impossible (LEFT + RIGHT)
    """
    player_keymaps = (
        {
            80: 0,  # left
            79: 1,  # right
            82: 2,  # up
            81: 3,  # down
            29: 4,  # z
            6: 4,  # c
            17: 4,  # n
            27: 5,  # x
            25: 5,  # v
            16: 5,  # m
        },
        {
            22: 0,  # s
            9: 1,  # f
            8: 2,  # e
            7: 3,  # d
            225: 4,  # Lshift
            43: 5,  # tab
            26: 5,  # w
            20: 5,  # q
            4: 5,  # a
        },
    )
    pressed = list(nr for nr, isdown in enumerate(pygame.key.get_pressed()) if isdown)
    if i is None:
        player_keymap = player_keymaps[0]
        player_keymap.update(player_keymaps[1])
        bitfield = 1 if 80 in pressed else 0
        bitfield += 2 if 79 in pressed else 0
        bitfield += 4 if 82 in pressed else 0
        bitfield += 8 if 81 in pressed else 0
        bitfield += 16 if 29 in pressed or 6 in pressed or 17 in pressed else 0
        bitfield += 32 if 27 in pressed or 25 in pressed or 16 in pressed else 0

        bitfield += 64 if 22 in pressed else 0
        bitfield += 128 if 9 in pressed else 0
        bitfield += 256 if 8 in pressed else 0
        bitfield += 512 if 7 in pressed else 0

        bitfield += 1024 if 225 in pressed else 0
        bitfield += (
            2048
            if 43 in pressed or 26 in pressed or 20 in pressed or 4 in pressed
            else 0
        )

        return bitfield

    player_keymap = player_keymaps[p]

    button_pressed = False
    for key in pressed:
        if key in player_keymap:
            if player_keymap[key] == i:
                button_pressed = True

    return button_pressed


def btnp(i=None, p=0):
    """btnp is short for "Button Pressed"; Instead of being true when a button is held down,
    btnp returns true when a button is down AND it was not down the last frame. It also
    repeats after 15 frames, returning true every 4 frames after that (at 30fps -- double
    that at 60fps). This can be used for things like menu navigation or grid-wise player
    movement.

    The state of btnp is reset at the start of each call to _update or _update60, so it
    is preferable to use btnp from inside one of those functions.

    Custom delays (in frames @ 30fps) can be set by poking the following memory addresses:

    POKE(0x5F5C, DELAY) -- set the initial delay before repeating. 255 means never repeat.
    POKE(0x5F5D, DELAY) -- set the repeating delay.

    In both cases, 0 can be used for the default behaviour (delays 15 and 4)"""
    global btnp_state, btnp_frame, clock, fps
    current_state = btn(i, p)
    if current_state != btnp_state:
        btnp_state = current_state
        btnp_frame = clock
        return current_state

    return False


# ---------- Audio ---------- #


def sfx(n, channel=-1, offset=0, length=1):
    """
    play sfx n on channel (0..3) from note offset (0..31) for length notes
    n -1 to stop sound on that channel
    n -2 to release sound on that channel from looping
    Any music playing on the channel will be halted
    offset in number of notes (0..31)

    channel -1 (default) to automatically choose a channel that is not being used
    channel -2 to stop the sound from playing on any channel
    """
    if channel == -1:
        chan = pygame.mixer.find_channel()
    else:
        chan = pygame.mixer.Channel(channel)
    note_list = sfx_list[n]
    for note in note_list[offset : offset + length]:
        if chan:
            # chan.play(note)
            # Play note for half a second.
            reps = int(0.1 / note.get_length())
            note.play(reps)
            py_time.sleep(note.get_length() * reps)


# https://gist.github.com/ohsqueezy/6540433
from array import array
from pygame.mixer import Sound, get_init, pre_init

pre_init(44100, -16, 1, 1024)
pygame.init()


class Note(Sound):
    def __init__(self, frequency, volume=0.1):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in range(period):
            # square wave
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples


sfx_list = []
for sfx_i in range(64):
    sfx_notes = []
    for note_i in range(32):
        sfx_notes.append(Note(50 + sfx_i * 4 + note_i * 40))

    sfx_list.append(sfx_notes)


def music(n=0, fade_len=0, channel_mask=0):
    """
    play music starting from pattern n (0..63)
    n -1 to stop music
    fade_len in ms (default: 0)
    channel_mask specifies which channels to reserve for music only
        e.g. to play on channels 0..2: 1+2+4 = 7

    Reserved channels can still be used to play sound effects on, but only when that
    channel index is explicitly requested by sfx().
    """
    global threads
    if n == -1:
        for thread in threads:
            thread.stop = True
            thread.join()
        return

    def music_worker():
        thread = threading.currentThread()
        pattern = sfx_list[n]
        while True:
            for note in pattern:
                reps = int(0.1 / note.get_length())
                note.play(reps)
                py_time.sleep(note.get_length() * reps)
                if getattr(thread, "stop", False):
                    return

    thread = threading.Thread(target=music_worker)
    threads.append(thread)
    thread.start()


# ---------- Map ---------- #
"""
The PICO-8 map is a 128x32 grid of 8-bit cells, or 128x64 when using the shared memory. When 
using the map editor, the meaning of each cell is taken to be an index into the spritesheet 
(0..255). However, it can instead be used as a general block of data.
"""
map_sprites = [0] * 128 * 64


def mget(x: int, y: int) -> int:
    """Get map value (v) at x,y"""
    return map_sprites[(x % 128) + (y % 64) * 128]


def mset(x: int, y: int, v: int) -> None:
    """Set map value (v) at x,y"""
    global map_sprites
    map_sprites[x + y * 128] = v


def map(cell_x, cell_y, sx, sy, cell_w=128, cell_h=32, layers=None):
    """
    Draw section of map (starting from cell_x, cell_y) at screen position sx, sy (pixels)

    MAP(0, 0, 20, 20, 4, 2) -- draws a 4x2 blocks of cells starting from 0,0 in the map, to the screen at 20,20

    If cell_w and cell_h are not specified, defaults to 128,32 (the top half of the map)
    To draw the whole map (including the bottom half shared with the spritesheet), use:

    MAP(0, 0, 0, 0, 128,64)

    Layers is an 8-bit bitfield. When it is specified, only sprites with matching flags are drawn.
    For example, when layers is 0x5, only sprites with flag 0 and 2 are drawn.

    Sprite 0 is always taken to mean empty, and is never drawn.
    """
    yi = cell_y
    xi = cell_x
    yi_end = yi + cell_h
    xi_end = xi + cell_w
    while yi < yi_end:
        yi += 1
        xi = 0
        while xi < xi_end:
            xi += 1
            v = map_sprites[xi + yi * 128]
            if v == 0:
                continue
            if layers is not None:
                if fget(v) & layers:
                    spr(map_sprites[xi + yi * 128], sx, sy)


# ---------- Memory ---------- #
"""
:: Base ram memory layout

0x0    gfx
0x1000 (4096) gfx2/map2 (shared)
0x2000 (8192) map
0x3000 (12288) gfx flags
0x3100 (12544) song
0x3200 (12800) sfx
0x4300 (17152) user data
0x5e00 (24064) persistent cart data (256 bytes)
0x5f00 (24320) draw state
0x5f40 (24384) hardware state
0x5f80 (24448) gpio pins (128 bytes)
0x6000 (24576) screen (8k)

User data has no particular meaning and can be used for anything via memcpy(), peek() & poke().
Persistent cart data is mapped to 0x5e00..0x5eff but only stored if cartdata() has been called.
Colour format (gfx/screen) is 2 pixels per byte: low bits encode the left pixel of each pair.
Map format is one byte per cel, where each byte normally encodes a sprite index.
"""

memory = [0] * 2 ** 15


def peek(addr: int):
    """
    Read one byte from an address in base ram.
    Legal addresses are 0x0..0x7fff
    Reading out of range returns 0
    """
    try:
        return memory[addr]
    except IndexError:
        return 0


def peek2(addr):
    return peek(addr)


def peek4(addr):
    return peek(addr)


def poke(addr, val):
    """
    Write one byte to an address in base ram.
    Legal addresses are 0x0..0x7fff
    Writing out of range causes a runtime error
    """
    global SCREEN_SIZE, memory, threads
    if addr == 0x5F2C and val == 3:
        SCREEN_SIZE = (64, 64)
    elif addr == 24365:
        pass  # devkit_mode = val  # 1 allows stat for mouse and keyboard
    elif addr == 24367:
        for thread in threads:
            if val == 1:
                thread.__flag = threading.Event()
            elif val == 0:
                thread.__flag.clear()

    memory[addr] = val


def poke2(addr, val):
    return poke(addr, val)


def poke4(addr, val):
    return poke(addr, val)


def memcpy(dest_addr, source_addr, length):
    """
    Copy len bytes of base ram from source to dest
    Sections can be overlapping
    """
    global memory, spritesheet
    memory[dest_addr : dest_addr + length] = memory[source_addr : source_addr + length]
    if dest_addr == 0 and source_addr == 0x6000:
        # copy drawing surface to spritesheet
        spritesheet = surf.copy()


# ---------- Math ---------- #
"""
>>> flr(4.1)
4
>>> ceil(4.1)
5
>>> flr(-2.3)
-3
>>> ceil(-2.3)
-2
"""


def mid(x, y, z):
    """Returns the middle value of parameters
    >>> mid(7,5,10)
    7
    """
    a = [x, y, z]
    a.remove(min(a))
    a.remove(max(a))
    return a[0]


def cos(x):
    return math.cos(x * (math.pi * 2))


def sin(x):
    return -math.sin(x * (math.pi * 2))


def atan2(dx, dy):
    """
    Converts dx, dy into an angle from 0..1
    As with cos/sin, angle is taken to run anticlockwise in screenspace

    Longer vector uses the ratio:
    >>> atan2(99, 99)
    0.875

    Special case:
    >>> atan2(0, 0)
    0.25

    >>> [(x,y, atan2(x,y)) for x in range(-1,2) for y in range(-1,2)]
    [(-1, -1, -0.375), (-1, 0, 0.5), (-1, 1, 0.625), (0, -1, -0.25), (0, 0, 0.25), (0, 1, 0.75), (1, -1, 0.125), (1, 0, 0.0), (1, 1, 0.875)]
    """
    newangle = math.atan2(dy, -dx)
    normalizedangle = (newangle / math.pi + 1) / 2
    return normalizedangle


def rnd(x=1):
    if isinstance(x, dict):
        return random.choice(x)
    return random.random() * x


def srand(x=0):
    random.seed(x)


def sgn(x):
    return math.copysign(1, x)


def div(a, b):
    """Dividing by zero evaluates to 0x7fff.ffff if positive, or -0x7fff.ffff if negative. (-32768.0 to 32767.99999)"""
    if not b:
        return (-32768.0, 32767.99999)[bool(math.copysign(1, b) + 1)]
    return a / b


# ---------- Strings ---------- #


def pico8_to_python(s):
    r"""Hackily translates PICO-8 to Python.
    >>> pico8_to_python('for i=0,30 do ?"웃"')
    'def _init():\n    global \nfor i in range(0, 30+1): print("웃")\nrun(_init, _update, _draw)'
    """
    import re

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
    s = s.replace("\\", "//")
    s = s.replace("~=", "!=")
    # comments
    s = re.sub(r"--\[\[(.*?)\]\]", r"'''\1'''", s, flags=re.DOTALL)
    s = re.sub(r"\[\[(.*?)\]\]", r'"""\1"""', s, flags=re.DOTALL)
    s = s.replace("--", "#")
    # loops
    s = re.sub(r"([0-9)\] ])\s*do\b", r"\1:", s)
    s = re.sub(
        r"for (.*?)=(.+?),(.+?),(.+?):", r"\1 = \2\nwhile \1 <= \3:\n    \1 += \4\n", s
    )
    s = re.sub(
        r"for (.*?)=([^,]+),(.*?):",
        r"for \1 in range(\2, \3+1):",
        s,
    )
    # print
    s = (
        s.replace(BTN_X, "P0_X")
        .replace(BTN_O, "P0_O")
        .replace(BTN_LEFT, "P0_LEFT")
        .replace(BTN_RIGHT, "P0_RIGHT")
        .replace(BTN_UP, "P0_UP")
        .replace(BTN_DOWN, "P0_DOWN")
    )
    s = re.sub(r"print\(?(\b[^\)]+?)\)?", r"print(\1)", s)
    s = re.sub(r"\?\s*(.*)", r"print(\1)", s)

    s = re.sub(r"\bdel\b", "delete", s)
    # separate statements
    s = re.sub(r"([\])])([a-zA-Z])", r"\1\n\2", s)
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


def tostr(val, use_hex=False):
    if use_hex:
        return hex(val)
    return str(val)


def tostring(val, use_hex=False):
    return tostr(val, use_hex=False)


def tonum(s):
    """Converts a string representation of a decimal, hexadecimal, or binary number to a number value or None."""
    if type(s) in (int, float):
        return s

    if s is None:
        return None

    base = 10
    if type(s) is str:
        if "x" in s:
            base = 16
        elif "b" in s:
            base = 2

    try:
        return int(s, base)
    except ValueError:
        return None


def ord(s, index=1):
    """
    >>> ord("@")
    64
    >>> ord("123", 2)   # returns 50 (the second character: "2")
    50
    """
    c = s[index - 1]
    return builtins.ord(c)


def sub(s, pos0, pos1=None):
    """
    Grab a substring from string str, from pos0 up to and including pos1.
    When pos1 is not specified, the remainer of the string is returned.

    >>> s = "the quick brown fox"
    >>> sub(s,5,9)
    'quick'
    >>> sub(s,5)
    'quick brown fox'
    """
    return s[flr(pos0) - 1 : flr(pos1) if pos1 else None]


def split(s, separator=",", convert_numbers=True):
    """
    Split a string into a table of elements delimited by the given separator (defaults to ",").
    When convert_numbers is true, numerical tokens are stored as numbers (defaults to true).
    Empty elements are stored as empty strings.
    When the separator is "", every character is split into a separate element.

    >>> split("1,2,3")
    {1: 1, 2: 2, 3: 3}
    >>> split("one:two:3",":",false)
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
                    result.append(tonum(item))
            except ValueError:
                result.append(item)
        else:
            result.append(item)
    return Table(result)


# ---------- Graphics ---------- #
SCREEN_SIZE = (128, 128)


def camera(x_offset=0, y_offset=0):
    """
    Set a screen offset of -x, -y for all drawing operations
        camera() to reset
    """
    global xo, yo
    xo = -x_offset
    yo = -y_offset


def clip(x=0, y=0, w=SCREEN_SIZE[0], h=SCREEN_SIZE[1]) -> tuple:
    """
    When the draw state has a clipping rectangle set, all draw operations will not affect any pixels in the
    graphics buffer outside of this rectangle. This is useful for reserving parts of the screen

    When called without arguments, the function resets the clipping region to be the entire screen and returns
    the previous state as 4 return values x, y, w, h (since PICO-8 0.2.0d).
    """
    poke(CLIP_X1_PT, x)
    poke(CLIP_Y1_PT, y)
    poke(CLIP_X2_PT, x + w)
    poke(CLIP_Y2_PT, y + h)
    surf.set_clip(x, y, x + w, y + h)
    return (x, y, w, h)


def circ(x, y, r=4, col: int = None):
    """
    Draw a circle at x,y with radius r
    If r is negative, the circle is not drawn
    """
    if r > 0:
        pygame.draw.circle(surf, color(col), pos(x, y), r, 1)


def circfill(x, y, r=4, col: int = None):
    """
    Draw a circle at x,y with radius r
    If r is negative, the circle is not drawn
    """
    if r > 0:
        pygame.draw.circle(surf, color(col), pos(x, y), r)


def oval(x0, y0, x1, y1, col: int = None):
    """Draw an oval that is symmetrical in x and y (an ellipse), with the given bounding rectangle."""
    pygame.draw.ellipse(surf, color(col), (pos(x0, y0), (x1 - x0 + 1, y1 - y0 + 1)), 1)


def ovalfill(x0, y0, x1, y1, col: int = None):
    """Draw an oval that is symmetrical in x and y (an ellipse), with the given bounding rectangle."""
    pygame.draw.ellipse(surf, color(col), (pos(x0, y0), (x1 - x0 + 1, y1 - y0 + 1)))


def line(x0, y0, x1=None, y1=None, col: int = None):
    """Draw line. If x1,y1 are not given the end of the last drawn line is used"""
    global pen_x, pen_y
    if x1 is None:
        x1 = pen_x
    if y1 is None:
        y1 = pen_y
    pygame.draw.line(surf, color(col), pos(x0, y0), pos(x1, y1))
    pen_x = x0
    pen_y = y0


def rect(x0, y0, x1, y1, col: int = None):
    """Draw a rectangle."""
    pygame.draw.rect(surf, color(col), (pos(x0, y0), (x1 - x0 + 1, y1 - y0 + 1)), 1)


def rectfill(x0, y0, x1, y1, col: int = None):
    """Draw a filled rectangle."""
    pygame.draw.rect(surf, color(col), (pos(x0, y0), (x1 - x0 + 1, y1 - y0 + 1)))


@multimethod(int, int, int)
def pal(old_col: int, new_col: int, remap_screen: int = 0):
    """pal() swaps old_col for new_col for one of two (TODO) palette re-mappings"""
    old_col = to_col(old_col)
    new_col = to_col(new_col)
    if remap_screen:
        img_copy = surf.copy()
        cls(new_col)
        img_copy.set_colorkey(color(old_col))
        surf.blit(img_copy, (0, 0))

    palette[old_col] = palette[new_col]


@multimethod(int, int)
def pal(old_col: int, new_col: int):  # noqa: F811
    """pal() swaps colour c0 for c1 for one of two palette re-mappings"""
    pal(old_col, new_col, 0)


@multimethod(int, float)
def pal(old_col: int, new_col: int):  # noqa: F811
    """pal() swaps colour c0 for c1 for one of two palette re-mappings"""
    pal(old_col, flr(new_col), 0)


@multimethod(Table, int)
def pal(tbl: Table, remap_screen: int = 0):  # noqa: F811
    """
    When the first parameter of pal is a table, colours are assigned for each entry.
    For example, to re-map colour 12 and 14 to red:

    PAL({12: 9, 14: 8})

    Or to re-colour the whole screen shades of gray (including everything that is already drawn):

    PAL({1,1,5,5,5,6,7,13,6,7,7,6,13,6,7}, 1)
    """
    for i, col in enumerate(tbl):
        pal(i + 1, col, remap_screen)


@multimethod(list, int)
def pal(tbl: list, remap_screen: int = 0):  # noqa: F811
    """
    0-based palette replacement.
    """
    for i, col in enumerate(tbl):
        pal(i, col, remap_screen)


@multimethod()
def pal():  # noqa: F811
    """Resets to system defaults (including transparency values and fill pattern)"""
    global palette, fill_pattern
    palette = PALETTE.copy()
    fill_pattern = 0


def palt(col: int = None, transparent: bool = None):
    if col is None and transparent is None:
        for col in palette:  # noqa
            r, g, b, *_ = palette[col]
            palette[col] = (r, g, b, 255)
    else:
        r, g, b, *_ = palette[col]
        palette[col] = (r, g, b, 0 if transparent else 255)


def pos(x, y):
    """Returns floored and camera-offset x,y tuple.
    Setting out of bounds is possible, but getting is not; mod in callers for get_at.
    """
    return (flr(xo + x), flr(yo + y))


def pget(x, y) -> int:
    """Get the color of a pixel at x, y."""
    p = pos(x, y)
    clr = surf.get_at((p[0] % SCREEN_SIZE[0], p[1] % SCREEN_SIZE[1]))
    col = 0
    for k, v in palette.items():
        if v == clr:
            col = k
    return col


def pset(x: int, y: int, col: int = None):
    """Set the color of a pixel at x, y."""
    surf.set_at(pos(x, y), color(col))


def sget(x, y) -> int:
    """Get the color of a spritesheet pixel."""
    p = pos(x, y)
    clr = spritesheet.get_at((p[0] % SCREEN_SIZE[0], p[1] % SCREEN_SIZE[1]))
    col = 0
    for k, v in PALETTE.items():
        if v[:3] == clr[:3]:
            col = k

    return col


def sset(x, y, col=None):
    """Set the color of a spritesheet pixel."""
    spritesheet.set_at(pos(x, y), color(col))


def fget(n: int, flag_index: int = None):
    """Get sprite n flag_index (0..7; not 1-based like Table) value, or combined flags value."""
    if flag_index is None:
        return sprite_flags[n]
    return sprite_flags[n] & (1 << flag_index)


def fset(n: int, f: int = None, v: bool = None):
    global sprite_flags
    """
    >>> fset(2, 1+2+8)  # sets bits 0,1 and 3
    >>> fset(2, 4, True)  # sets bit 4
    >>> printh(fget(2))  # (1+2+8+16)
    27
    """
    if v is None:  # f not provided. No function overloading in Python.
        sprite_flags[n] = f
    if v:
        sprite_flags[n] |= 1 << f
    else:
        sprite_flags[n] &= ~(1 << f)


def get_char_img(n: int):
    x = n % 16 * 8
    y = n // 16 * 8
    rect = (x, y, 8, 8)
    image = pygame.Surface((8, 8), pygame.SRCALPHA).convert_alpha()
    image.blit(font_img, (0, 0), rect)
    return image


def ascii_to_pico8(s):
    # Pause Black formatter to not mess this up.
    # fmt: off
    ocr = [
        '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?',
        '▌', '⯀','⚬', '×', '∷', '⏸', '⏴','⏵', '⌜','⌟', '¥', '⬝', '⹁', '․', '"', '˚',
        ' ', '!', '"', '#', '$', '%', '&', '´', '(', ')', '*', '+', ',', '-', '.', '/',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
        '@', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '[', '\\',']', '^', '_',
        '`', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
        'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '{', '|', '}', '?', '⚬',
        '█', '▒','😈','⬇️','░', '✦','⚈', '♥', '⟐','웃','🏠','⬅️','☻', '♪','🅾️','♦',
        '᠁','➡️','★','⌛','⬆️','~','〜','❎','≡', '⦀','あ', 'い','う','え','お','か',
        'ぎ','く','け','こ','さ','し','す','せ', 'そ','た','ち','つ','て','と','な','に',
        'ぬ','ね','の','は','ひ','ふ','へ','ほ', 'ま','み','む','め','も','や','ゆ','よ',
        'ら','り','る','れ','ろ','わ','を','ん', 'ゔ','っ','ぇ','ょ','ア','イ','ウ','エ',
        'オ','カ','キ','ク','ケ','コ','サ','シ', 'ス','セ','ソ','タ','チ','ツ','テ','ト',
        'ナ','ニ','ヌ','ネ','ノ','ハ','ヒ','フ', 'ヘ','ホ','マ','ミ','ム','メ','モ','ヤ',
        'ユ','ヨ','ラ','リ','ル','レ','ロ','ワ', 'ヲ','ン','ッ','ャ','ュ','?', 'ᨀ','⺀',
    ]
    # fmt: on
    ps = ""
    if s in PROBLEMATIC_MULTI_CHAR_CHARS:
        s = [s]  # Else Python takes multiple characters from it!
    for c in s:
        if c == "?":
            i = 63
        else:
            try:
                i = ocr.index(c)
            except ValueError:
                printh(f"Char not found: {repr(c)} of {repr(s)}.")
                i = -1
            if i < 0:
                i = ord(c)
            if i > 255:
                i = 70
        ps += chr(i)
    return ps


def prt(s, x=None, y=None, col=None):
    return print(s, x, y, col)


def print(s, x=None, y=None, col=None):
    global cursor_x, cursor_y, yo
    if x is not None:
        cursor_x = x
    if y is not None:
        cursor_y = y

    """
    if y >= 128:
        # Scroll up.
        # surf_old = surf.copy()
        # surf_old.fill(color(1))
        screen.fill(color(0))
        # surf.blit(surf_old, (0, -16))
        surf.scroll(0, -8)
        y = 112
    """
    """
    font = pygame.font.SysFont("System", 15)
    text = font.render(s, True, color(col))
    surf.blit(text, (x, y))
    """
    """
    font2 = pygame.freetype.Font(
        "PICO-8 wide.ttf", 8
    )  # Download from https://www.lexaloffle.com/bbs/?tid=3760
    font2.render_to(surf, pos(x, y), s, color(col))
    """
    for s in str(s).split("\n"):  # noqa
        clr = color(col)
        for c in ascii_to_pico8(s):
            character = characters[ord(c)].copy()
            r = character.get_rect()

            for hi in range(r.h):
                for wi in range(r.w):
                    clr_at = character.get_at((wi, hi))
                    if clr_at[:3] != (0, 0, 0):
                        character.set_at((wi, hi), clr)

            # character.fill(color(col), special_flags=pygame.BLEND_MULT)  # uses 254? so nonzero color band values are 1 short!

            surf.blit(character, (xo + cursor_x, yo + cursor_y))
            cursor_x += 4 if ord(c) < 128 else 8
            if cursor_y > 128:
                # TODO: scroll up.
                # yo += 8
                pass

        cursor_x = 0
        cursor_y += 6


def cursor(x, y, col=None):
    """
    Set the cursor position and carriage return margin
    If col is specified, also set the current color.
    """
    global cursor_x, cursor_y, pen_color
    cursor_x = x
    cursor_y = y
    if col is not None:
        pen_color = col


PALETTE = {
    0: (0, 0, 0),
    1: (29, 43, 83),
    2: (126, 37, 83),
    3: (0, 135, 81),
    4: (171, 82, 54),
    5: (95, 87, 79),
    6: (194, 195, 199),
    7: (255, 241, 232),
    8: (255, 0, 77),
    9: (255, 163, 0),
    10: (255, 236, 39),
    11: (0, 228, 54),
    12: (41, 173, 255),
    13: (131, 118, 156),
    14: (255, 119, 168),
    15: (255, 204, 170),
    128: (41, 24, 20),
    129: (17, 29, 53),
    130: (66, 33, 54),
    131: (18, 83, 89),
    132: (116, 47, 41),
    133: (73, 51, 59),
    134: (162, 136, 121),
    135: (243, 239, 125),
    136: (190, 18, 80),
    137: (255, 108, 36),
    138: (168, 231, 46),
    139: (0, 181, 67),
    140: (6, 90, 181),
    141: (117, 70, 101),
    142: (255, 110, 89),
    143: (255, 157, 129),
}
palette = PALETTE.copy()


def to_col(col=None):
    global pen_color

    col = tonum(col)

    if col is None:
        if "pen_color" not in globals():
            pen_color = 6
        col = pen_color
    if col is None:
        col = 6

    if col not in palette:  # Sleight of Hand uses color 48?!
        col %= 16

    return flr(col)


def color(col=None):
    """https://www.lexaloffle.com/pico-8.php?page=manual
    Set the current color to be used by drawing functions
    If col is not specified, the current color is set to 6?

    "Many graphics functions accept an optional color argument.
    When this argument is omitted, the current color of the draw state is used by default."
    - https://pico-8.fandom.com/wiki/Color

    0  black   1  dark_blue   2  dark_purple   3  dark_green
    4  brown   5  dark_gray   6  light_gray    7  white
    8  red     9  orange      10  yellow       11  green
    12  blue   13  indigo     14  pink         15  peach
    """
    global pen_color
    pen_color = to_col(col)
    return palette[pen_color]


def cls(col=0):
    """
    Clear the screen and reset the clipping rectangle. col defaults to 0 (black)
    cls() also sets the text cursor in the draw state to (0, 0). TODO: cursor pos is last line pos?

    # https://pico-8.fandom.com/wiki/Cls says:
    "This ignores the alternate palette set by pal() for the purposes of using color 0.
    (pal(0, 7) cls() does not fill the screen with white.)
    To fill the screen with a specific color, use rectfill."
    """
    global cursor_x, cursor_y, pen_x, pen_y
    if col == 0:
        surf.fill((0, 0, 0, 255))
    else:
        if col not in palette:
            col %= 16
        surf.fill(palette[col])
    cursor_x = 0
    cursor_y = 0
    pen_x = 0
    pen_y = 0


def adjust_color(surface: pygame.Surface) -> pygame.Surface:
    r = surface.get_rect()

    old_new = [
        (old_color, palette[key])
        for key, old_color in PALETTE.items()
        if old_color != palette[key]
    ]

    for hi in range(r.h):
        for wi in range(r.w):
            clr_at = surface.get_at((wi, hi))[:3]
            for old_color, new_color in old_new:
                if clr_at == old_color:
                    surface.set_at((wi, hi), new_color)

    return surface


def replace_color(
    surface: pygame.Surface, old_color: tuple, new_color: tuple
) -> pygame.Surface:
    r = surface.get_rect()
    for hi in range(r.h):
        for wi in range(r.w):
            if surface.get_at((wi, hi)) == old_color:
                surface.set_at((wi, hi), new_color)

    return surface


def spr(
    n: int,
    x: int,
    y: int,
    w: int = 1,
    h: int = 1,
    flip_x: bool = False,
    flip_y: bool = False,
) -> None:
    """
    draw sprite n (0..255) at position x,y
        width and height are 1,1 by default and specify how many sprites wide to blit.
    """
    sx = (n % 16) * 8
    sy = (n // 16) * 8
    area = (sx, sy, 8 * w, 8 * h)
    sprite = pygame.transform.flip(spritesheet.subsurface(area), flip_x, flip_y)
    surf.blit(sprite, (x, y))


def sspr(
    sx: int,
    sy: int,
    sw: int,
    sh: int,
    dx: int,
    dy: int,
    dw=None,
    dh=None,
    flip_x=False,
    flip_y=False,
) -> None:
    """
    Stretch rectangle from sprite sheet (sx, sy, sw, sh) // given in pixels
    and draw in rectangle (dx, dy, dw, dh)
    Colour 0 drawn as transparent by default (see palt())
    dw, dh defaults to sw, sh
    """
    if dw is None:
        dw = sw
    if dh is None:
        dh = sh
    sprite = pygame.transform.flip(
        spritesheet.subsurface((sx, sy, sw, sh)), flip_x, flip_y
    )
    sprite = adjust_color(pygame.transform.scale(sprite, (flr(dw), flr(dh))))
    sprite.set_colorkey((0, 0, 0))
    surf.blit(sprite, (dx, dy))


def fillp(p=0):
    """
    TODO: The PICO-8 fill pattern is a 4x4 2-colour tiled pattern observed by:
        circ() circfill() rect() rectfill() oval() ovalfill() pset() line()

    p is a bitfield in reading order starting from the highest bit. To calculate the value
    of p for a desired pattern, add the bit values together:

        .-----------------------.
        |32768|16384| 8192| 4096|
        |-----|-----|-----|-----|
        | 2048| 1024| 512 | 256 |
        |-----|-----|-----|-----|
        | 128 |  64 |  32 |  16 |
        |-----|-----|-----|-----|
        |  8  |  4  |  2  |  1  |
        '-----------------------'

    For example, FILLP(4+8+64+128+  256+512+4096+8192) would create a checkerboard pattern.

    This can be more neatly expressed in binary: FILLP(0b0011001111001100)
    The default fill pattern is 0, which means a single solid colour is drawn.
    """
    global fill_pattern
    fill_pattern = p


def printh(s, filename=None, overwrite=False, save_to_desktop=False):
    """
    >>> filename = "pico8_printh_test.txt"
    >>> printh('pico8 printh test', filename, overwrite=True, save_to_desktop=True)
    >>> open(os.path.join(os.environ["HOMEPATH"], "Desktop", os.path.split(filename)[1])).read()
    'pico8 printh test'
    """
    if save_to_desktop:
        filename = os.path.join(
            os.environ["HOMEPATH"], "Desktop", os.path.split(filename)[1]
        )
    if filename:
        with open(filename, "w" if overwrite else "a") as fp:
            fp.write(s)
    else:
        builtins.print(s)


def reset():
    """Reset the draw state, including palette, camera position, TODO: clipping and fill pattern."""
    global palette, pen_color
    pen_color = 6
    palette = PALETTE.copy()
    camera(0, 0)


# ---------- /Graphics ---------- #


def flip():
    """
    Flip the back buffer to screen and wait for next frame
    Don't normally need to do this -- _draw() calls it for you.
    """
    global clock, fps
    screen.fill(0)
    # area = (peek(CLIP_X1_PT), peek(CLIP_Y1_PT), peek(CLIP_X2_PT), peek(CLIP_Y2_PT))
    screen.blit(surf, (0, 0))
    pygame.display.flip()
    clock.tick(fps)


# ---------- Control flow ---------- #
def init(_init=lambda: True):
    global clock, pen_color, screen, SCREEN_SIZE, surf, threads
    global characters, font_img, spritesheet, sprite_flags
    global audio_channel_notes
    audio_channel_notes = [0, 0, 0]
    sprite_flags = [0] * 256
    threads = []

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED | pygame.RESIZABLE)
    surf = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

    pen_color = 6
    cls()  # set cursor
    camera()  # set camera offset

    # CC-0 licenced font https://www.lexaloffle.com/gfx/pico-8_font_020.png
    FONT_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAIAAAACAAQMAAAD58POIAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAGUExURQAAAP///6XZn90AAAAJcEhZcwAADsQAAA7EAZUrDhsAAAN+SURBVEjHzVUxiBtHFP2IwUwhzC+OIIIwg1iOI4SgwsUUixjEciyHOI5DhTGHWQ4RQrhiOVIs4SMGc4UIKYIrFymGkMKoCiaYcLhYglGZ4grXU7k8XBoTRN5KZydO502T0WoFf9/8//57f0f0f1lxczc+UsBvcBRjDCEUtTfNoxAQQDTE6I1zgHyI8PU/clB05OqWRFwIMdTOuYYHmSYQa1P792VxhQLpUTaipNuwjz5Qg3DvENhFTQ5PzrehEWt0Fz16bEg0sjhjAliEgCrRGQRigccNC1QxBQLeAIPPBtGw2jw2EQlwuVZy/DsAwQtwK+BE8LFG2VD7UOPrXO3hCMgGD6Yhon8PhwhYbEI41qEAnP7bqn0BVrCgaPyHXd6Z0IxI8DAPshgEqJGwNrABWvltwBcwtnCwF44WN+Pykcuh9Q/ahyFNt037CKBb1N3oERs9mvZpiwjhnR6YYji31SO21CM27m/bb4bx7/bDxn6D1wNtbvVw6DrClzps9AjQxzmMw3s94k2OFmu9fCgLY8+stbLuC9N6ul4N0m/kzMqrS15ZIC5XCytyLevVml8KEJfXg0qwZ/rqYblBiCy0Zbt3IusSOdosYRHc18vSWz7PiP6w9josXtLSLKgyb2mJ6quD6fV6WV0AnAMhdqUGQPz6s0p+QkCymxwz17s3O2pDw3azUhznqTGp8P4DkuEDzU5El3/+rvuvx2RdRiUQ889th02Go2qYOZ8NHbuuYvfjEXLkaQU5bh9WPZ1+etiGxw+TNH8xpOe2SI6q5IRJro5P9mm4kOQ8NfOv+3R1+ijPOH/Oc3O/2j1gerZ6dJJNLx5Xs9PTAXcr+nJ/dt8+7Ty7q9Nun3nWhge71KSTcnOMSJctuUyf6avdko6MU43Zko3ujk5tXr55Xe6xYlLJ4Wz8Yuc7fe+JM6yZrO7udvM737P55TfHQ2nDQ+NoNJKwmGxkj62huVTpSM1zNU8GfIyDvpdwlqvE6EQdiBJLX2WitVK3ekbfAo2EehNmFm1nfdZmaEwrPTCoSjsZsqTckS9IrBKVTFQuiswOnwOxo3RSqgvek0TPEwS6b3nsdGfKtP8JMxnsLsbpkJ7q6tvidqv35U5lkz03F9n8OyFpRxMC40y5J45Ko0mJNAEFEd6U1WpFCmJ8NhlrxZwzFKBR1etNyjn3YmGqkj+eB9FfyJq4mv/1Y4UAAAAASUVORK5CYII="  # noqa
    font_file = io.BytesIO(base64.b64decode(FONT_BASE64))
    """
    with open("font_file.png", "wb") as fp:
        fp.write(font_file.read())
    font_file.seek(0)
    """
    font_img = pygame.image.load(font_file).convert_alpha()
    replace_color(font_img, (255, 255, 255, 255), (194, 195, 199, 255))
    font_img.set_colorkey((0, 0, 0))

    spritesheet = font_img.copy()

    characters = [get_char_img(i) for i in range(256)]

    _init()
    flip()


running = False


def run(_init=lambda: True, _update=lambda: True, _draw=lambda: True):
    """Run from the start of the program. Can be called from inside a program to reset program."""
    global begin, fps, running, btnp_state
    if running:
        raise StopIteration("reset")

    begin = py_time.time()
    if _update.__name__ == "_update60":
        fps = 60
    else:
        fps = 30

    init()

    stopped = False
    while not stopped:
        try:
            _init()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        global threads
                        for thread in threads:
                            thread.stop = True
                        for thread in threads:
                            thread.join()
                        running = False
                        stopped = True

                btnp_state = 0
                _update()
                _draw()
                flip()
        except StopIteration as ex:
            if ex.value != "reset":
                stopped = True
        except ZeroDivisionError:
            import sys

            builtins.print("Use div(a, b) instead.", file=sys.stderr)
            raise

    pygame.quit()


def stop(message=None):
    """Stop the cart and optionally print a message."""
    if message:
        builtins.print(message)
    raise StopIteration


def t():
    """Or time(). Returns the number of seconds elasped since the cartridge was run."""
    global begin
    return py_time.time() - begin


def time():
    return t()


def stat(x):
    """
    Get system status where x is:

    0  Memory usage (0..2048)
    1  CPU used since last flip (1.0 == 100% CPU at 30fps)
    4  Clipboard contents (after user has pressed CTRL-V)
    6  Parameter string
    7  Current framerate

    16..19  Index of currently playing SFX on channels 0..3
    20..23  Note number (0..31) on channel 0..3
    24      Currently playing pattern index
    25      Total patterns played
    26      Ticks played on current pattern

    From inside a cart, "devkit mode" can be enabled for platforms that have mouse and keyboard attached:

    poke(0x5f2d, 1)

    stat(30) -> true if a keypress is in stat(31), false otherwise
    stat(31) -> the key being pressed, as a string
    stat(32) -> mouse X coord
    stat(33) -> mouse Y coord
    stat(34) -> mouse button bitmask (1=primary, 2=secondary, 3=primary AND secondary 4=middle)
    stat(35) -> (unknown, returns 0 in testing)
    stat(36) -> mouse wheel delta since previous update
    When the user presses one or more keys, PICO-8 sets stat(30) to true, and then sets stat(31) to the next keypress to be read.
    When the application sees stat(30) is true and reads the keypress via stat(31), PICO-8 will then refresh the value of both stats,
    based on whether or not there are more keypresses remaining to be reported. This can be checked multiple times per frame to fully
    read all keys pressed since last frame.

    80..85  UTC time: year, month, day, hour, minute, second
    90..95  Local time

    100     Current breadcrumb label, or nil
    110     Returns true when in frame-by-frame mode
    """
    global audio_channel_notes, fps
    if x == 7:
        return fps
    if x == 30:
        return btn() > 0
    if x == 31:
        return str(btn())
    if x == 32:
        return pygame.mouse.get_pos()[0]
    if x == 33:
        return pygame.mouse.get_pos()[1]
    if x == 34:
        primary, middle, secondary = pygame.mouse.get_pressed()
        return 1 * primary + 2 * secondary + 4 * middle

    if x in range(16, 20):
        x += 4
    if x in range(20, 24):
        note = (audio_channel_notes[x - 20] + 1) % 32
        audio_channel_notes[x - 20] = note

        sfx(peek(12800 + note * 2))  # TODO: loop in different thread.
        return note

    return 0


if __name__ == "__main__":
    sys.modules["pypico8"] = sys.modules[__name__]
    exec(
        open(
            os.path.join(os.path.dirname(__file__), "../fake_sprite.py"),
            encoding="utf8",
        ).read()
    )
