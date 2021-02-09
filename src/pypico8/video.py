# pylint:disable = multiple-imports, too-many-function-args, redefined-builtin, too-many-arguments
import base64, io
import pygame
from .multiple_dispatch import multimethod
from .audio import threads
from .math import flr
from .strings import PROBLEMATIC_MULTI_CHAR_CHARS, printh, tonum
from .table import Table


SCREEN_SIZE = (128, 128)
screen = None
clock = None
fps = 30
frame_count = 0

# Pointers
CLIP_X1_PT = 24352
CLIP_Y1_PT = 24353
CLIP_X2_PT = 24354
CLIP_Y2_PT = 24355

surf = None
pen_x = 0
pen_y = 0

characters = []
font_img = None
spritesheet = None
sprite_flags = []


def _init_video() -> None:
    global characters, clock, frame_count, font_img, pen_color, screen, spritesheet, sprite_flags, surf
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED | pygame.RESIZABLE)
    surf = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

    pen_color = 6
    cls()  # set cursor
    camera()  # set camera offset
    clock = pygame.time.Clock()
    frame_count = 0

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
    sprite_flags = [0] * 256

    characters = [get_char_img(i) for i in range(256)]


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
    global SCREEN_SIZE, memory
    if addr == 0x5F2C and val == 3:
        SCREEN_SIZE = (64, 64)
    elif addr == 24365:
        pass  # devkit_mode = val  # 1 allows stat for mouse and keyboard
    elif addr == 24367:
        for thread in threads:
            if val == 1:
                thread.do_work.clear()
            elif val == 0:
                thread.do_work.set()

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


def flip():
    """
    Flip the back buffer to screen and wait for next frame
    Don't normally need to do this -- _draw() calls it for you.
    """
    global frame_count
    frame_count += 1
    screen.fill(0)
    # area = (peek(CLIP_X1_PT), peek(CLIP_Y1_PT), peek(CLIP_X2_PT), peek(CLIP_Y2_PT))
    screen.blit(surf, (0, 0))
    pygame.display.flip()
    clock.tick(fps)


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
    """
    >>> fset(2, 1+2+8)  # sets bits 0,1 and 3
    >>> fset(2, 4, True)  # sets bit 4
    >>> printh(fget(2))  # (1+2+8+16)
    27
    """
    global sprite_flags
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
    """
    global cursor_x, cursor_y, pen_x, pen_y, surf
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


def reset():
    """Reset the draw state, including palette, camera position, TODO: clipping and fill pattern."""
    global palette, pen_color
    pen_color = 6
    palette = PALETTE.copy()
    camera(0, 0)