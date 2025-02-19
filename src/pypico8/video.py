"""Graphical functions.
>>> _init_video()
"""

# pylint:disable = function-redefined, global-statement, invalid-name, line-too-long, multiple-imports, no-member, pointless-string-statement, redefined-builtin, too-many-function-args, too-many-lines, unused-import, wrong-import-position
import base64, builtins, decimal, io, math, os, re, sys  # noqa: E401

from emoji.tokenizer import tokenize

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pypico8.audio import threads
from pypico8.math import ceil, flr, rnd, shl, shr
from pypico8.strings import (
    PROBLEMATIC_MULTI_CHAR_CHARS,
    chr,
    ord,
    printh,  # noqa:E401,F401  # printh is for doctest.
    tonum,
)

from pypico8.table import Table

DEBUG = False

decimal.getcontext().prec = 4

SCREEN_SIZE = (128, 128)
screen: pygame.Surface
clock: pygame.time.Clock
fps: int = 30
frame_count: int = 0

# Pointers https://pico-8.fandom.com/wiki/Memory
SPRITE_SHEET_PT = 0
SPRITE_FLAGS_PT = 0x3000  # 12288
USER_DATA_PT = 0x4300  # up to, not including 0x5e00 (24064)
CHAR_WIDTH_LO_PT = 0x5600  # 22016
CHAR_WIDTH_HI_PT = 0x5601  # 22017
CHAR_HEIGHT_PT = 0x5602  # 22018
CHAR_LEFT_PT = 0x5603  # 22019
CHAR_TOP_PT = 0x5604  # 22020
CUSTOM_FONT_PT = 0x5600  # Bytes 0 to 15 are used as defined above!
DRAW_PALETTE_PT = 0x5F00  # 24320
SCREEN_PALETTE_PT = 0x5F10  # 24336
CLIP_X1_PT = 0x5F20  # 24352
CLIP_Y1_PT = 0x5F21  # 24353
CLIP_X2_PT = 0x5F22  # 24354
CLIP_Y2_PT = 0x5F23  # 24355
DRAW_COLOR_PT = 0x5F25  # 24357
CURSOR_X_PT = 0x5F26  # 24358
CURSOR_Y_PT = 0x5F27  # 24359
CAMERA_X_PT = 0x5F28  # 24360
CAMERA_Y_PT = 0x5F29  # 24362
VIDEO_MODE_PT = 0x5F2C  # 24364
PERSIST_PT = 0x5F2E  # 24366
PAUSE_AUDIO_PT = 0x5F2F  # 24367
PAUSE_MENU_PT = 0x5F30  # 24368
FILL_PATTERN_PT = 0x5F31  # 24369
COLOR_AS_FLOAT_PT = 0x5F34  # 24372
PEN_RESET_PT = 0x5F35  # 24373
PEN_X_PT = 0x5F3C  # 24380
PEN_Y_PT = 0x5F3E  # 24382
AUDIO_FX_PT = 0x5F40  # 24384
PRINT_PT = 0x5F58  # 24408
BITPLANE_PT = 0x5F5E  # 24414
HIGH_COLOR_PT = 0x5F5F  # 24415
FILL_PALETTE_PT = 0x5F60  # 24416
SCREEN_DATA_PT = 0x6000  # 24576
GENERAL_USE_PT = 0x8000  # 32768. Pico8 0.2.4+


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


off_color_visible: bool = True
# palette: dict = {}
surf: pygame.Surface

characters: list[pygame.Surface] = []
font_img: pygame.Surface
spritesheet: pygame.Surface


def debug(s):
    if DEBUG:
        printh(s)


def _init_video() -> None:
    global characters, clock, frame_count, font_img, screen, spritesheet, surf

    mem[VIDEO_MODE_PT] = 0

    pygame.display.set_caption("PyPico8")
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED | pygame.RESIZABLE)
    surf = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

    reset()
    cls()
    color(6)
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

    spritesheet = surf.copy()
    # for i in range(0x3100):
    #     mem[i] = 0

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

mem = [0] * 65535  # 16 bit (15 until Pico8 0.2.4)
mem[BITPLANE_PT] = 255  # bitplane mode disabled


def camera(x_offset: int = 0, y_offset: int = 0) -> int:
    """
    Set a screen offset of -x, -y for all drawing operations
        camera() to reset
    """
    color(0)  # Undocumented.
    mem[CAMERA_X_PT] = -x_offset
    mem[CAMERA_Y_PT] = -y_offset
    return 0


def clip(
    x: int = 0,
    y: int = 0,
    w: int = SCREEN_SIZE[0],
    h: int = SCREEN_SIZE[1],
    clip_previous=False,
) -> tuple:
    """
    When the draw state has a clipping rectangle set, all draw operations will not affect any pixels in the
    graphics buffer outside of this rectangle. This is useful for reserving parts of the screen

    When called without arguments, the function resets the clipping region to be the entire screen and returns
    the previous state as 4 return values x, y, w, h (since PICO-8 0.2.0d).

    When CLIP_PREVIOUS is true, clip the new clipping region by the old one.

    camera(), cursor(), color(), pal(), palt(), fillp(), clip() return their previous state.

    >>> peek4(24352)  # Pico8 hides trailing zeroes.
    -32640.0
    >>> clip(10, 20, 30, 40)
    (0, 0, 128, 128)
    >>> clip(0, 0, 64, 64, 1)
    (10, 20, 40, 60)
    >>> peek4(24352)
    15400.0783
    """
    prev_state = (
        peek(CLIP_X1_PT),
        peek(CLIP_Y1_PT),
        peek(CLIP_X2_PT),
        peek(CLIP_Y2_PT),
    )
    if clip_previous:
        ox, oy, ow, oh = prev_state
        x = max(x, ox)
        y = max(y, oy)
        w = min(w, ow - ox)
        h = min(h, oh - oy)

    poke(CLIP_X1_PT, x)
    poke(CLIP_Y1_PT, y)
    poke(CLIP_X2_PT, x + w)
    poke(CLIP_Y2_PT, y + h)
    surf.set_clip((x, y, w, h))
    return prev_state


def cls(col: int | float | str = 0) -> None:
    """
    Clear the screen and reset the clipping rectangle. col defaults to 0 (black)
    cls() also sets the text cursor in the draw state to (0, 0).

    >>> cls(2)
    >>> pget(0, 0)
    2
    >>> cls()
    """
    clip()
    cursor()
    _cls(col)


def _cls(col: int | float | str = 0) -> None:
    r"""Only clear the screen with color.
    >>> print(r"\^c3Like this.")
    40
    >>> cls()
    """
    col = flr(tonum(col))
    for i in range(128 * 64):
        mem[SCREEN_DATA_PT + i] = col + col * 16


def color(col: int | float | str | None = None) -> int:
    """https://www.lexaloffle.com/pico-8.php?page=manual
    Set the current color to be used by drawing functions

    "Many graphics functions accept an optional color argument.
    When this argument is omitted, the current color of the draw state is used by default."
    - https://pico-8.fandom.com/wiki/Color

    0  black   1  dark_blue   2  dark_purple   3  dark_green
    4  brown   5  dark_gray   6  light_gray    7  white
    8  red     9  orange      10  yellow       11  green
    12  blue   13  indigo     14  pink         15  peach

    Returns previous color byte (primary + secondary*16).

    POKE(0x5F34, 1) -- sets integrated fillpattern + colour mode
    CIRCFILL(64,64,20, 0x114E.ABCD) -- sets fill pattern to ABCD

    -- bit  0x1000.0000 means the non-colour bits should be observed
    -- bit  0x0100.0000 transparency bit
    -- bits 0x00FF.0000 are the usual colour bits
    -- bits 0x0000.FFFF are interpreted as the fill pattern:

        .-----------------------.
        |32768|16384| 8192| 4096|
        |-----|-----|-----|-----|
        | 2048| 1024| 512 | 256 |
        |-----|-----|-----|-----|
        | 128 |  64 |  32 |  16 |
        |-----|-----|-----|-----|
        |  8  |  4  |  2  |  1  |
        '-----------------------'

    >>> color()
    6
    >>> color(2.5)
    6
    >>> color(-2.5)
    2
    >>> color()
    253
    >>> poke(0x5F34, 1)
    0
    >>> color(4 * 16 + 13 + shr(0xAA00, 16))  # pcol1 + pcol0 + p
    6
    >>> rect(0, 0, 4, 1)
    0
    >>> [pget(i, 0) for i in range(5)]
    [4, 13, 4, 13, 4]
    >>> _ == [pget(i, 1) for i in range(5)]
    True
    >>> poke(0x5F34, 0)
    0
    """
    global off_color_visible
    old_col = mem[DRAW_COLOR_PT] & 0xFF

    if col is None:
        col = 6
    else:
        col = tonum(col)  # amorphous_form.py

    if mem[COLOR_AS_FLOAT_PT]:
        debug(f"Setting float color to {col}.")
        pattern, col = math.modf(col)  # type: ignore[arg-type]
        pattern = int(shl(pattern, 16))
        fillp(pattern)
        mem[DRAW_COLOR_PT] = int(col) & 0xFF
    else:
        debug(
            f"Setting color to {flr(col) % 256:02x} from {sys._getframe().f_back.f_code.co_name}"  # type: ignore[union-attr]
        )
        mem[DRAW_COLOR_PT] = flr(col) % 256

    # 64 fixes test_pset rectfill and center circle.
    # 32 only the center circle.
    # 16 breaks pattern
    # != 16 works. Still leaves pixel cursor changing color.
    off_color_visible = True  # int(col) & 16 != 16
    debug(
        f"color set off_color_visible to {off_color_visible} from col bin {flr(col):08b}"
    )

    return old_col


def cursor(x: int = 0, y: int = 0, col=None) -> int:
    """
    Set the cursor position and carriage return margin
    If col is specified, also set the current color.
    """
    mem[CURSOR_X_PT] = x
    mem[CURSOR_Y_PT] = y
    if col is not None:
        color(col)
    return 0


def draw_pattern(
    cel: pygame.Surface | None = None,
    area: pygame.Rect | None = None,
):
    """Draw area with 4x4 fill pattern in 16 bits at 0x5F31 with transparency option at 0x5F33. Pattern 0 is draw color 0x0F; 1 is 0xF0."""

    if cel is None:
        cel = surf
    if area is None:
        area = cel.get_bounding_rect()
    xr = range(area.left, area.right)
    yr = range(area.top, area.bottom)
    # debug(f"draw_pattern {mem[FILL_PATTERN_PT + 1]:02x} {mem[FILL_PATTERN_PT]:02x} area {area} from {sys._getframe().f_back.f_code.co_name}")
    for y in yr:
        for x in xr:
            if cel.get_at((x, y))[3] != 0:
                _pset(x, y)


def fillp(p: int | float | str = 0) -> float:
    """
    The PICO-8 fill pattern is a 4x4 2-colour tiled pattern observed by:
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

    This can be more neatly expressed in 16-bit binary: FILLP(0b0011001111001100)
    The default fill pattern is 0, which means a single solid colour is drawn.

    Alternatively, you can set the pattern to make the on bits transparent (showing what is drawn underneath). To do this, add 0b0.1, or 0x0.8 if using hex, to the pattern value. Data is stored at [0x5F31 - 0x5F33].


    https://x.com/lexaloffle/status/1359600870799806464
    A new bit for fillp in #pico8 0.2.2: 0x0.4
    e.g. fillp(♥ | 0.25)

    When it's set, pixel values in spr/sspr/map/tline are mapped to 8-bit colour pairs starting at 0x5f60, and the fill pattern is observed when the high & low nibbles differ.

    >>> reset()
    >>> see = lambda: [mem[FILL_PATTERN_PT + i] for i in range(3)]
    >>> x = -1.0
    >>> while x <= 1: _ = fillp(x); printh(f"{x}: {see()}"); x += 0.25
    -1.0: [255, 255, 0]
    -0.75: [255, 255, 2]
    -0.5: [255, 255, 1]
    -0.25: [255, 255, 3]
    0.0: [0, 0, 0]
    0.25: [0, 0, 2]
    0.5: [0, 0, 1]
    0.75: [0, 0, 3]
    1.0: [1, 0, 0]
    >>> fillp(-3855); see()
    1.0
    [241, 240, 0]
    >>> fillp(-3855.5); see()
    -3855.0
    [240, 240, 1]
    >>> fillp(32768); see()
    -3855.5
    [0, 128, 0]
    >>> _ = fillp()  # Clear pattern to not mess up other tests.
    """
    global off_color_visible

    if isinstance(p, str):  # ovals.py
        index = ord(p)
        character = characters[index].copy()
        # r = character.get_rect()
        p = 0
        for hi in range(4):
            for wi in range(4):
                clr_at = character.get_at((wi, hi))
                if clr_at[:3] != (0, 0, 0):
                    p = (p << 1) + 0
                else:
                    p = (p << 1) + 1
        # off_color_visible = False
    else:
        p = tonum(p)  # type: ignore

    # 65535 = full off color 16-bit pattern.
    # p = int(p) & 0b1111111111111111  # type: ignore

    # pygame.image.save(peek2(FILL_PATTERN_PT), "fill_pattern.png")
    # debug(f"fillp {p}:")
    # s = f"{bin(p)[2:]:0>16}"
    # for i in range(0, 16, 4):
    #     debug(s[i : i + 4])
    # https://pico-8.fandom.com/wiki/Fillp

    b = peek(FILL_PATTERN_PT + 2)
    d = 0.0
    if b & 1:
        d += 0.5
    if b & 2:
        d += 0.25
    prev_state = peek2(FILL_PATTERN_PT) + d

    part, whole = math.modf(p)
    if p < 0 and part:
        whole -= 1
    poke2(FILL_PATTERN_PT, whole)

    n = flr(part * 8)
    n = ((n & 1) << 2) | (n & 2) | ((n & 4) >> 2)
    poke(FILL_PATTERN_PT + 2, n)
    return prev_state


def rgb(col: int) -> tuple:
    col = uint8(col)
    if col >= 128:
        col = 128 + (col % 16)
    else:
        col %= 16
    return PALETTE[col]


def flip() -> None:
    """
    Flip the back buffer to screen and wait for next frame
    Don't normally need to do this -- _draw() calls it for you.

    Screen data

    This 8,192-byte (8 KiB) region contains the graphics buffer. This is what is modified by the built-in drawing functions, and is what is copied to the actual display at the end of the game loop or by a call to flip().

    0x6000..0x7fff / 24576..32767

    pget(i % 64 * 2, row) + (pget(i % 64 * 2 + 1, row) << 4)

    24336 is screen palette start.
    """
    global frame_count
    frame_count += 1
    screen.fill(0)
    # area = (peek(CLIP_X1_PT), peek(CLIP_Y1_PT), peek(CLIP_X2_PT), peek(CLIP_Y2_PT))

    x = 0
    y = 0
    for addr in range(SCREEN_DATA_PT, 0x8000):  # 24576-32767
        """
        All 128 rows of the screen, top to bottom. Each row contains 128 pixels in 64 bytes.
        Each byte contains two adjacent pixels, with the lo 4 bits being the left/even pixel
        and the hi 4 bits being the right/odd pixel.
        """
        pixels = mem[addr]
        # pixels = addr % 16 + 32 # OK
        col1 = pixels & 0b1111
        col2 = (pixels >> 4) & 0b1111
        # col1 = (addr + y) % 16
        # col2 = (addr + y) % 16
        # debug(f"x {x}, y {y}, pixels {pixels} so {col1} and {col2}")
        if addr > SCREEN_DATA_PT and addr % 64 == 0:
            y += 1
        surf.set_at((x, y), rgb(mem[SCREEN_PALETTE_PT + col1]))
        surf.set_at((x + 1, y), rgb(mem[SCREEN_PALETTE_PT + col2]))
        x = (x + 2) % 128

    # https://www.reddit.com/r/pico8/comments/s4o8l6/comment/hstbjcf/
    video_mode = mem[VIDEO_MODE_PT]
    if video_mode == 1:
        # horizontal stretch, 64x128 screen, left half of normal screen
        topleft = surf.subsurface(0, 0, 64, 128)
        screen.blit(pygame.transform.scale(topleft, (128, 128)), (0, 0))
    elif video_mode == 2:
        # vertical stretch, 128x64 screen, top half of normal screen
        topleft = surf.subsurface((0, 0, 128, 64))
        screen.blit(pygame.transform.scale(topleft, (128, 128)), (0, 0))
    elif video_mode == 3:
        # both stretch, 64x64 screen, top left quarter of normal screen
        topleft = surf.subsurface((0, 0, 64, 64))
        screen.blit(pygame.transform.scale(topleft, (128, 128)), (0, 0))
    elif video_mode == 5:
        # horizontal mirroring, left half copied and flipped to right half
        topleft = surf.subsurface((0, 0, 64, 128))
        screen.blit(topleft, (0, 0))
        screen.blit(pygame.transform.flip(topleft, 1, 0), (64, 0))
    elif video_mode == 6:
        # vertical mirroring, top half copied and flipped to bottom half
        topleft = surf.subsurface((0, 0, 128, 64))
        screen.blit(topleft, (0, 0))
        screen.blit(pygame.transform.flip(topleft, 0, 1), (0, 64))
    elif video_mode == 7:
        # both mirroring, top left quarter copied and flipped to other quarters
        topleft = surf.subsurface((0, 0, 64, 64))
        screen.blit(pygame.transform.flip(topleft, 0, 0), (0, 0))
        screen.blit(pygame.transform.flip(topleft, 1, 0), (64, 0))
        screen.blit(pygame.transform.flip(topleft, 0, 1), (0, 64))
        screen.blit(pygame.transform.flip(topleft, 1, 1), (64, 64))
    elif video_mode == 129:
        # horizontal flip
        screen.blit(pygame.transform.flip(surf, 1, 0), (0, 0))
    elif video_mode == 130:
        # vertical flip
        screen.blit(pygame.transform.flip(surf, 0, 1), (0, 0))
    elif video_mode == 131:
        # both flip
        screen.blit(pygame.transform.flip(surf, 1, 1), (0, 0))
    elif video_mode == 133:
        # clockwise 90 degree rotation
        screen.blit(pygame.transform.rotate(surf, -90), (0, 0))
    elif video_mode == 134:
        # 180 degree rotation (effectively equivalent to 131)
        screen.blit(pygame.transform.rotate(surf, 180), (0, 0))
    elif video_mode == 135:
        # counterclockwise 90 degree rotation
        screen.blit(pygame.transform.rotate(surf, 90), (0, 0))
    else:
        screen.blit(surf, (0, 0))

    pygame.display.flip()
    clock.tick(fps)


def memcpy(dest_addr: int, source_addr: int, length: int) -> None:
    """
    Copy len bytes of base ram from source to dest
    Sections can be overlapping

    >>> for i in range(100): mem[i] = flr(rnd(256))
    >>> memcpy(100, 0, 100)
    >>> mem[0:100] == mem[100:200]
    True
    >>> for i in range(200): mem[i] = 0
    """
    vals = []
    for i in range(length):
        vals.append(peek(source_addr + i))
    for i, val in enumerate(vals):
        poke(dest_addr + i, val)


# ---------- Map ---------- #
"""
The PICO-8 map is a 128x32 grid of 8-bit cells, or 128x64 when using the shared memory. When 
using the map editor, the meaning of each cell is taken to be an index into the spritesheet 
(0..255). However, it can instead be used as a general block of data.
"""
map_sprites = [0] * 128 * 64


def map(
    cell_x: int,
    cell_y: int,
    sx: int,
    sy: int,
    cell_w: int = 128,
    cell_h: int = 32,
    layers: int | None = None,
) -> None:
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
            if layers is not None and (fget(v) & layers):
                spr(map_sprites[xi + yi * 128], sx, sy)


def mget(x: int, y: int) -> int:
    """Get map value (v) at x,y"""
    return map_sprites[(x % 128) + (y % 64) * 128]


def mset(x: int, y: int, v: int) -> None:
    """Set map value (v) at x,y"""
    map_sprites[x + y * 128] = v


def peek(addr: int) -> int:
    """
    Read one byte from an address in base ram.
    Reading out of 0..2**16 range returns 0.

    >>> peek(-1)
    0
    >>> peek(2**16)
    0
    """
    try:
        return mem[int(addr)]  # & 0xFF
    except IndexError:
        return 0
    except TypeError as ex:
        raise TypeError(
            f"Mem addr {addr} is type {type(mem[addr])}: {mem[addr]} instead of int!"
        ) from ex


def peek2(addr: int, _: int = 1) -> int:
    """Reads one or more signed 16-bit values from contiguous groups of two consecutive memory locations.
    More not implemented in Pico8 0.2.2c
    >>> poke(GENERAL_USE_PT, 1)
    0
    >>> peek2(GENERAL_USE_PT)
    1
    >>> poke(GENERAL_USE_PT + 1, 1)
    0
    >>> peek2(GENERAL_USE_PT)
    257
    >>> poke(GENERAL_USE_PT + 1, 255)
    0
    >>> peek2(GENERAL_USE_PT)
    -255
    """
    n = peek(addr) + shl(peek(addr + 1), 8)
    # Convert to two's complement signed
    if n >= (1 << 15):  # If n is outside the signed range
        n -= 1 << 16  # Apply two's complement adjustment for negative value

    return n


def peek4(addr: int) -> float:
    """Read a 32-bit float.
    >>> a = 0x5000
    >>> poke4(a, -(1/512 + 1/4 + 42 + 256)); peek4(a)
    0
    -298.252
    >>> v = 2**15; poke4(a, v); peek4(a)
    0
    -32768.0
    >>> v = 2**15-1; poke4(a, v); peek4(a)
    0
    32767.0
    >>> v = 2**15+1; poke4(a, v); peek4(a)
    0
    -32767.0
    >>> v = 2**16+1234567; poke4(a, v); peek4(a)
    0
    -10617.0
    >>> poke4(a, 1.1); peek4(a)
    0
    1.1
    >>> poke4(a, -1.1); peek4(a)
    0
    -1.1
    """
    rv = (
        shr(peek(addr), 16)
        + shr(peek(addr + 1), 8)
        + peek(addr + 2)
        + shl(peek(addr + 3), 8)
    )
    if int(rv) & 2**15:
        rv = -0xFFFF + rv - 1
    return round(rv, 4)


def poke(addr: int, val: int = 0, *more) -> int:
    """
    Write one byte to an address in base ram.
    Legal addresses are 0x0..0x7fff
    Writing out of range causes a runtime error.
    """
    for val in (val, *more):
        # if val == 9 and addr >= 0 and addr < 200:
        #     printh(f"POKED {addr} {val} from {sys._getframe().f_back.f_code.co_name}:")  # type: ignore[union-attr]
        # if addr >= 0x5F60 and addr < 0x5F60 + 16:
        #     printh(f"POKED FILL PALETTE {addr} {val} from {sys._getframe().f_back.f_code.co_name}:")  # type: ignore[union-attr]

        if 0 <= addr <= 0x1FFF:  # Spritesheet
            # x = addr % 64 * 2
            # y = addr // 64
            # spritesheet.set_at((x, y), PALETTE[val & 0b1111])
            # spritesheet.set_at((x + 1, y), PALETTE[val >> 4 & 0b1111])
            # if addr % 10 == 0:
            #     printh(f"spritesheet @ {x},{y}=>{addr} to {val}")
            pass
        elif 0x2000 <= addr <= 0x2FFF:
            # https://pico-8.fandom.com/wiki/Memory#Memory_map
            pass
        elif 0x3000 <= addr <= 0x30FF:
            # https://pico-8.fandom.com/wiki/Memory#Sprite_flags
            pass
        elif 0x3100 <= addr <= 0x31FF:
            # https://pico-8.fandom.com/wiki/Memory#Music
            pass
        elif 0x3200 <= addr <= 0x42FF:
            # https://pico-8.fandom.com/wiki/Memory#Sound_effects
            pass
        elif 0x4300 <= addr <= 0x55FF:
            # General use
            pass
        elif CHAR_WIDTH_LO_PT <= addr <= 0x5DFF:
            # General use / custom font (Pico8 0.2.2+)
            pass
        elif 0x5E00 <= addr <= 0x5EFF:
            # Persistent cart data (64 numbers = 256 bytes)
            pass
        elif DRAW_PALETTE_PT <= addr <= 0x5F3F:  # 24320 24383
            # https://pico-8.fandom.com/wiki/Memory#Draw_state
            if addr == 24367:
                # pause. val 2 keeps music (TODO)
                if val and mem[PAUSE_MENU_PT] == 1:
                    mem[PAUSE_MENU_PT] = 0
                    return 0
                for thread in threads:
                    if val == 1:
                        thread.do_work.clear()
                    elif val == 0:
                        thread.do_work.set()
        elif AUDIO_FX_PT <= addr <= 0x5F7F:  # 24384 24447
            # https://pico-8.fandom.com/wiki/Memory#Hardware_state
            if (
                addr == BITPLANE_PT
            ):  # 0x5F5E  # bitplane read (hi nibble) and write (lo nibble) masks.
                # debug(f"bitplane poke {val}")
                pass

        mem[addr] = flr(val) & 0xFF
        addr += 1
    return 0


def poke2(addr: int, val: int | float) -> int:
    """Write 16 bits.
    >>> poke2(0x5f00, 32768)
    0
    >>> peek(0x5f00)
    0
    >>> peek(0x5f00 + 1)
    128
    >>> peek2(0x5f00)
    -32768
    >>> poke2(0x5f00, 2.5)
    0
    >>> peek2(0x5f00)
    2
    """
    poke(addr + 1, (flr(val) >> 8) & 0xFF)
    poke(addr, flr(val) & 0xFF)
    return 0


def poke4(addr: int, val: int) -> int:
    """Write 32-bit float.
    >>> def p(v): poke4(0x5000, v); exec("for i in range(4): i8 = peek(0x5000 + i); printh(i8)")
    >>> p(1/512 + 1/4 + 42 + 256)
    128
    64
    42
    1
    >>> p(-(1/512 + 1/4 + 42 + 256))
    128
    191
    213
    254
    >>> p(1)
    0
    0
    1
    0
    >>> p(-1)
    0
    0
    255
    255
    >>> p(-1.5)
    0
    128
    254
    255
    >>> p(.75)
    0
    192
    0
    0
    """
    whole = int(val)
    part = int(shl(val, 16))
    if val < 0 and val % 1:
        print("-")
        whole -= 1
    poke(addr, part & 0xFF)
    poke(addr + 1, part >> 8 & 0xFF)
    poke(addr + 2, whole & 0xFF)
    poke(addr + 3, whole >> 8 & 0xFF)
    return 0


def circ(
    x: int, y: int, radius: int = 4, col: int | None = None, _border: bool = True
) -> None:
    """
    Draw a circle at x,y with radius r.
    If r is negative, the circle is not drawn.
    """
    if radius < 0:
        return
    if radius == 0:
        pset(x, y, col)
        return
    if col is not None:
        color(col)

    cel = surf.copy()
    cel.fill((0, 0, 0, 0))
    area = pygame.draw.ellipse(
        cel,
        (255, 255, 255, 255),
        (pos(x - radius, y - radius), (2 * radius + 1, 2 * radius + 1)),
        _border,
    )
    # x = 0
    # y = 10
    # for radius in range(0, 10):
    #     x += radius * 2
    #     pygame.draw.circle(cel, col2rgb(col + radius), pos(x, y), ceil(radius), _border)
    #     pygame.draw.ellipse(cel, col2rgb(col + radius), (pos(x, y + 20), (2 * radius + 1, 2 * radius + 1)), _border)
    #     with open("debug.png", "wb") as fp:
    #         pygame.image.save(cel, fp, "png")
    # raise Exception("DEBUG")

    draw_pattern(cel, area)


def circfill(x: int, y: int, r: int = 4, col: int | None = None) -> None:
    """
    Draw a circle at x,y with radius r
    If r is negative, the circle is not drawn
    """
    circ(x, y, r, col, False)


def line(
    x0: int,
    y0: int,
    x1: int | None = None,
    y1: int | None = None,
    col: int | None = None,
) -> None:
    """Draw line.
    If x1,y1 are not given, the end of the last drawn line is used.
    """

    if x1 is None:
        x1 = peek2(PEN_X_PT)
        # See globe.py
        poke2(PEN_X_PT, x0)
    else:
        poke2(PEN_X_PT, x1)

    if y1 is None:
        y1 = peek2(PEN_Y_PT)
        poke2(PEN_Y_PT, y0)
    else:
        poke2(PEN_Y_PT, y1)

    if col is not None:
        color(col)

    cel = surf.copy()
    cel.fill((0, 0, 0, 0))
    # debug(f"line {pos(x0, y0)} to {pos(x1, y1)}")
    draw_pattern(
        cel, pygame.draw.line(cel, (255, 255, 255, 255), pos(x0, y0), pos(x1, y1))
    )


def oval(
    x0: int, y0: int, x1: int, y1: int, col: int | None = None, _border: bool = True
) -> None:
    """Draw an oval that is symmetrical in x and y (an ellipse), with the given bounding rectangle."""
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0
    if col is not None:
        color(col)
    cel = surf.copy()
    cel.fill((0, 0, 0, 0))
    area = pygame.draw.ellipse(
        cel, (255, 255, 255, 255), (pos(x0, y0), (x1 - x0 + 1, y1 - y0 + 1)), _border
    )
    draw_pattern(cel, area)


def ovalfill(x0: int, y0: int, x1: int, y1: int, col: int | None = None) -> None:
    """Draw an oval that is symmetrical in x and y (an ellipse), with the given bounding rectangle."""
    oval(x0, y0, x1, y1, col, False)


def rect(*args, _border_only=True) -> int:
    """Draw a rectangle. x0: int, y0: int, x1: int, y1: int, col: int | None = None, _border_only=True
    Col None => 0 but No col => draw color!!!"""
    x0, y0 = pos(args[0], args[1])
    x1, y1 = pos(args[2], args[3])
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0

    debug(f"rect called with {len(args)} args: {args}")

    if len(args) > 4:
        col = args[4]
        # moving_checkers.py
        if isinstance(col, (float, int)):
            color(col)
        else:
            col = 0
    else:
        debug("Col from draw col")
        col = None

    debug(f"rect({x0},{y0} {x1},{y1} {col} {_border_only})")
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not _border_only or y == y0 or y == y1 or x == x0 or x == x1:
                _pset(x, y, col)

    return 0


def rectfill(*args) -> int:
    """Draw a filled rectangle."""
    return rect(*args, _border_only=False)


def pal(*args) -> int | None:
    """pal(old_col, new_col, p) changes the draw state so all instances of a given color are replaced with a new color. p: palette (0 for draw, 1 for display, 2 for secondary)

    pal() resets draw palette and screen palette to system defaults (including transparency values and fill pattern)

    pal(0, 9, 1)
    for a=0,2^15-1,1 do if peek(a) == 9 or a >= 24300 and a <= 24351 then print(a..": "..peek(a)) end end

    Doctests for all pal functions here because it only finds the last multimethod one:
    >>> def seek(x):
    ...   for a in range(0, 2**15-1):
    ...     if mem[a] == x:
    ...       printh(hex(a))
    ...
    >>> pal()
    0
    >>> peek(DRAW_PALETTE_PT) # 24320
    16
    >>> pal(0, 9)
    0
    >>> seek(9)
    0x5f00
    0x5f09
    0x5f19
    >>> pal(0, 9, 1)
    0
    >>> seek(9)
    0x5f00
    0x5f09
    0x5f10
    0x5f19
    >>> [pal(1, 340.5, 1) for _ in range(2)]
    [1, 84]
    >>> pal(0, 9, 0)
    9
    >>> pal()
    0
    """

    if len(args) == 0:
        """pal() resets first 2 palettes to defaults."""
        mem[PERSIST_PT] = 0
        fillp()
        pal(0)
        pal(1)
        return 0
    if len(args) == 1:
        p = args[0]
        """Reset draw (0), display (1), or secondary palette (2)."""
        if p == 0:
            poke(
                DRAW_PALETTE_PT,
                16,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
            )
        elif p == 1:
            poke(
                SCREEN_PALETTE_PT,
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
            )
        elif p == 2:
            poke(
                FILL_PALETTE_PT,
                0,
                1,
                18,
                19,
                36,
                21,
                214,
                103,
                72,
                73,
                154,
                59,
                220,
                93,
                142,
                239,
            )
        return 0
    if len(args) == 2:
        a = args[0]
        b = args[1]
        if isinstance(a, (float, int)):
            return pal(a, b, 0)
        if isinstance(a, list):
            # @multimethod(list, int)  # type: ignore
            # def pal(tbl: list, remap_screen: int = 0) -> None:  # noqa: F811
            """0-based palette replacement."""
            for i, col in enumerate(a):
                pal(i + 1, col, b)
            return None
        if isinstance(a, Table):
            # @multimethod(Table, int)  # type: ignore
            # def pal(tbl: Table, remap_screen: int = 0) -> None:  # noqa: F811
            """
            When the first parameter of pal is a table, colours are assigned (not swapped!) for each entry.
            For example, to re-map colour 12 and 14 to red:

            PAL({12: 9, 14: 8})

            Or to re-colour the whole screen shades of gray (including everything that is already drawn):

            PAL({1,1,5,5,5,6,7,13,6,7,7,6,13,6,7}, 1)
            """
            for i, col in enumerate(a):
                pal((i + 1 % 16), col, b)
            return None

    p = args[2]
    if p < 0 or p > 2:
        return 0

    old_col = uint4(args[0])
    new_col = args[1]

    pt = DRAW_PALETTE_PT
    if p == 1:
        pt = SCREEN_PALETTE_PT
    elif p == 2:
        pt = FILL_PALETTE_PT
    else:
        new_col = uint4(new_col)
    rv = mem[pt + old_col]
    if p == 0:
        rv = uint4(rv)
    mem[pt + old_col] = uint8(new_col)
    return rv


def palt(coli: int | None = None, transparent: bool | None = None) -> int | bool:
    """PALT(C, [T]) Set transparency for colour index to T (boolean)
    Transparency is observed by SPR(), SSPR(), MAP() AND TLINE()

    When C is the only parameter, it is treated as a bitfield used to set all 16 values. For example: to set colours 0 and 1 as transparent:
    PALT(0B1100000000000000)

    PALT() resets to default: all colours opaque except colour 0
    >>> palt()
    -32768
    >>> palt(0, 0)
    True
    >>> palt(0, False)
    True
    >>> palt(0, False)
    False
    >>> palt()
    0
    >>> palt(1, True)
    False
    >>> palt()
    -16384
    """
    prev_state = 0

    if coli is None and transparent is None:
        # palt() to make all but 0 transparent.
        for i in range(0, 16):
            prev_state += (1 << (15 - i)) if (mem[DRAW_PALETTE_PT + i] & 16) else 0
            mem[DRAW_PALETTE_PT + i] &= 0x0F
        mem[DRAW_PALETTE_PT] |= 0x1F
        prev_state = twos_complement_to_signed(prev_state)
    elif coli is not None and transparent is None:
        # palt(0) to make all transparent.
        for i in range(16):
            prev_state += mem[DRAW_PALETTE_PT] & (1 << i)
            if coli & (i << (16 - i)):
                mem[DRAW_PALETTE_PT + i] |= 0x1F
            else:
                mem[DRAW_PALETTE_PT + i] &= 0x0F
    else:
        # pal(0, True) to make color 0 transparent.
        if not coli:
            coli = 0
        a = DRAW_PALETTE_PT + coli
        prev_state = mem[a] & 16 == 16
        if transparent is True:
            mem[a] |= 16
        elif transparent is False:
            mem[a] &= 15
    return prev_state


def pos(x: int | float, y: int | float) -> tuple[int, int]:
    """Returns floored and camera-offset x,y tuple.
    Setting out of bounds is possible, but getting is not; mod in callers for get_at.
    """
    return (flr(mem[CAMERA_X_PT] + x), flr(mem[CAMERA_Y_PT] + y))


def pget(x: int, y: int) -> int:
    """Get the palette color of a pixel at x, y.
    >>> pget(-1, -1)
    0
    >>> pget(128, 128)
    0
    >>> pset(0, 0, 13)
    0
    >>> pget(0, 0)
    13
    >>> pset(127, 127, 14)
    0
    >>> pget(127, 127)
    14
    >>> fillp(1)
    0.0
    >>> rectfill(0, 0, 10, 10); pget(0, 0); pget(7, 7)
    0
    14
    0
    >>> fillp()
    1.0
    """
    x, y = pos(x, y)
    if x < 0 or y < 0 or x > 127 or y > 127:
        return 0
    B = mem[SCREEN_DATA_PT + y * 64 + x // 2]
    if x % 2:
        return (B & 0xF0) >> 4
    return B & 0x0F


def pset(x: int, y: int, col: int | None = None) -> int:
    """Set the color and pixel at x, y plus camera offset.
    >>> reset()
    >>> pset(-1, 0, 10); pset(0, 0, 11); pset(1, 0, 12)
    0
    0
    0
    >>> pget(0, 0)
    11
    >>> pget(1, 0)
    12
    """
    x, y = pos(x, y)  # See neon_jellyfish.py
    if col:
        color(col)

    _pset(x, y, col)
    return 0


def _pset(x: int, y: int, col: int | None = None, use_pattern=True) -> None:
    """Set the color of a pixel at x, y in memory.
    Each byte contains two adjacent pixels,
    with the lo 4 bits being the left/even pixel
    and the hi 4 bits being the right/odd pixel.
    """
    if x < 0 or y < 0 or x > 127 or y > 127:
        return

    if col is None:
        col = mem[DRAW_COLOR_PT]
    col = flr(col)

    # off_color_visible = col & 16  # fractus good. ovals not.
    # off_color_visible = mem[FILL_PATTERN_PT] & 16

    # nice_tutorial.py
    on_col = mem[DRAW_PALETTE_PT + (col & 0x0F)]
    debug(f"col {col} => on_col {col}")

    if use_pattern:
        if peek2(FILL_PATTERN_PT) >> (15 - ((x % 4) + 4 * (y % 4))) & 1:
            if off_color_visible:
                off_col = (col & 0xF0) >> 4
                col = off_col
        else:
            bitplane_mode = mem[BITPLANE_PT]  # 0x5F5 / 24414
            if bitplane_mode != 255:
                read_mask = (bitplane_mode & 0xF0) >> 4
                write_mask = bitplane_mode & 0x0F
                # https://www.lexaloffle.com/bbs/?tid=54215#:~:text=%3E%200x5f5e%20/-,24414,-%3E%20Allows%20PICO%2D8
                dst_color = pget(x, y)
                on_col = (dst_color & ~write_mask) | (on_col & write_mask & read_mask)
            col = on_col

    ax, hi = divmod(x, 2)
    addr = int(SCREEN_DATA_PT + y * 64 + ax)
    if hi:
        mem[addr] = (mem[addr] & 0x0F) | ((col & 0x0F) << 4)
    else:
        mem[addr] = (mem[addr] & 0xF0) | (col & 0x0F)

    debug(f"pset {x},{y} @ {addr} to 0x{mem[addr]:02x}, vis {off_color_visible}")


def fget(n: int, flag_index: int | None = None) -> int:
    """Get sprite n flag_index (0..7; not 1-based like Table) value, or combined flags value."""
    if n < 0 or n > 255:
        return 0
    if flag_index is None:
        return mem[SPRITE_FLAGS_PT + n]
    return mem[SPRITE_FLAGS_PT + n] & (1 << flag_index)


def fset(n: int, f: int = 0, v: bool | None = None) -> None:
    """Set sprite n flag bit value.
    >>> fset(2, 1+2+8)  # sets bits 0,1 and 3
    >>> fset(2, 4, True)  # sets bit 4
    >>> printh(fget(2))  # (1+2+8+16)
    27
    """
    if n < 0 or n > 255:
        return
    if v is None:
        mem[SPRITE_FLAGS_PT + n] = f % 256
    if v:
        mem[SPRITE_FLAGS_PT + n] |= 1 << f
    else:
        mem[SPRITE_FLAGS_PT + n] &= ~(1 << f)


def get_char_img(n: int) -> pygame.Surface:
    """Return Surface with character N image."""
    x = n % 16 * 8
    y = n // 16 * 8
    area = (x, y, 8, 5)
    image = pygame.Surface((9, 7), pygame.SRCALPHA).convert_alpha()
    image.blit(font_img, (1, 1), area)
    return image


def print(
    s: str | None = None,
    x: int | None = None,
    y: int | None = None,
    col: int | None = None,
) -> int | None:
    r"""Prints to screen, supporting control codes at https://www.lexaloffle.com/dl/docs/pico-8_manual.html#Appendix_A__P8SCII_Control_Codes
    For example, to print with a blue background ("\#c") and dark gray foreground ("\f5"): PRINT("\#C\F5 BLUE ")

    Returns width of string.

    >>> print()
    >>> print("")
    0
    >>> print("foo", 5)
    12
    >>> print("O")
    4
    >>> print("🅾️")
    8
    >>> mem[DRAW_COLOR_PT] & 0x0F
    5
    >>> # offset each word by +4 pixels vertically ("j" = 20, 20 - 16 = +4)
    >>> print("my \|jawesome \|jgame")
    60
    >>> print("abc\0def")
    12
    """
    if s is None:
        return None

    do_scroll = y is None

    if x is not None and y is not None:
        x, y = pos(x, y)  # archery.py
        mem[CURSOR_X_PT] = x
        mem[CURSOR_Y_PT] = y
    elif x is not None and y is None:
        col = x
        x = None

    if x is None:
        x = mem[CURSOR_X_PT]
    if y is None:
        y = mem[CURSOR_Y_PT]

    s = str(s)
    if s.startswith("\\^@"):
        addr = int(s[3:7], 16)
        n = int(s[7:11], 16)
        for i in range(n):
            poke(addr + i, ord(s[11 + i]))
        return None
    # spark.py uses 0x5f11 aka 24337 to set the palette.
    if s.startswith("\\^!"):
        addr = int(s[3:7], 16)
        for i, c in enumerate(s[7:]):
            poke(addr + i, ord(c))
        return None

    if col is not None:
        color(col)

    bg = mem[DRAW_COLOR_PT] & 0xF0
    fg = mem[DRAW_COLOR_PT] & 0x0F
    bg_rgb = None
    char_pause = 0
    for ln in re.split(r"(?<!\\)\\n|\n", s):
        x = mem[CURSOR_X_PT]

        if do_scroll and y > 128 - 7:
            scroll(-7)
            y -= 7

        debug(f"printing {repr(ln)} @ {x}, {y}")

        tokens = list(c for c, _ in tokenize(ln, True))
        i = 0
        invert = False
        custom_font = False
        char_width = 4
        char_width_hi = 8
        char_height = 6
        while i < len(tokens):
            c = tokens[i]
            c2 = "".join(tokens[i : i + 2])
            c3 = "".join(tokens[i : i + 3])
            c4 = "".join(tokens[i : i + 4])
            # printh(f"i {i} tokens {''.join(tokens[i:])}")
            if c == "\b" or c2 == r"\b":
                x -= char_width
                i += 2 if c == "\\" else 1
                continue
            if c == "\r" or c2 == r"\r":
                x = mem[CURSOR_X_PT]
                i += 2 if c == "\\" else 1
                continue
            if c == "\t" or c2 == r"\t":
                x = (x & 0xF0) + (16 if x % 16 else 0)
                i += 2 if c == "\\" else 1
                continue
            if c == "\0":
                mem[CURSOR_X_PT] = x
                return x

            if c in "abcdefghijklmnopqrstuvwxyz":
                c = c.upper()
            elif c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                c = c.lower()

            if c == "\\" and i + 1 < len(tokens):
                if tokens[i + 1] == "-":
                    # a to z = -16 to +19
                    x += ord(tokens[i + 2]) - 74 + 20 - 16
                    i += 3
                    continue
                if tokens[i + 1] == "|":
                    y += ord(tokens[i + 2]) - 74 + 20 - 16
                    i += 3
                    continue
                if tokens[i + 1] == "+":
                    x += ord(tokens[i + 2]) - 74 + 20 - 16
                    y += ord(tokens[i + 3]) - 74 + 20 - 16
                    i += 4
                    continue
                if tokens[i + 1] == "#":
                    # Set background color for this print call only.
                    bg = int(tokens[i + 2], 16)
                    mem[DRAW_COLOR_PT] = (bg << 4) | fg
                    bg_rgb = PALETTE[bg]
                    i += 3
                    continue
                if tokens[i + 1] == "f":
                    # Set foreground color.
                    fg = int(tokens[i + 2], 16)
                    mem[DRAW_COLOR_PT] = (bg << 4) | fg
                    i += 3
                    continue
                if "".join(tokens[i : i + 3]) == r"\^i":
                    invert = True
                    i += 3
                    continue
                if i + 3 < len(tokens) and c4 == r"\^-i":
                    invert = False
                    i += 4
                    continue
                if i + 3 < len(tokens) and c4 == r"\014":
                    debug("custom font on")
                    custom_font = True
                    char_width = mem[CHAR_WIDTH_LO_PT]
                    char_width_hi = mem[CHAR_WIDTH_HI_PT]
                    char_height = mem[CHAR_HEIGHT_PT]
                    i += 4
                    continue
                if i + 3 < len(tokens) and c4 == r"\015":
                    debug("custom font off")
                    custom_font = False
                    char_width = 4
                    char_width_hi = 8
                    char_height = 6
                    i += 4
                    continue
                if i + 2 < len(tokens) and c3 == r"\^:":
                    # https://pico-8.fandom.com/wiki/P8SCII_Control_Codes#Drawing_one-off_characters
                    ccn = int("".join(tokens[i + 3 : i + 3 + 16]), 16)
                    for ccy in range(8):
                        for ccx in range(8):
                            if ccn & (1 << (ccy * 8 + ccx)):
                                pset(x + ccx, y + 7 - ccy)
                    x += 9
                    i += 3 + 16
                    continue
                if i + 2 < len(tokens) and c3 == r"\^.":
                    # https://pico-8.fandom.com/wiki/P8SCII_Control_Codes#Drawing_one-off_characters
                    ccn = 0
                    for raw_byte in tokens[i + 3 : i + 3 + 8]:
                        ccn = (ccn << 8) + ord(raw_byte)
                    for ccy in range(8):
                        for ccx in range(8):
                            if ccn & (1 << (ccy * 8 + ccx)):
                                pset(x + ccx, y + 7 - ccy)
                    x += 9
                    i += 3 + 16
                    continue
                if i + 3 < len(tokens) and c3 == r"\^c":
                    _cls(tokens[i + 3])
                    x = y = 0
                    i += 4
                    continue
                if i + 2 < len(tokens) and c3 == r"\^g":
                    x = mem[CURSOR_X_PT]
                    y = mem[CURSOR_Y_PT]
                    i += 3
                    continue
                # \^h updates the home position to be the cursor's current position.
                if i + 2 < len(tokens) and c3 == r"\^h":
                    mem[CURSOR_X_PT] = x
                    mem[CURSOR_Y_PT] = y
                    i += 3
                    continue
                # \^j P0 P1 sets the cursor to an absolute (x, y) pixel position. Each parameter value is multiplied by 4.
                if i + 4 < len(tokens) and c3 == r"\^j":
                    x = int(tokens[i + 3], 16) * 4
                    y = int(tokens[i + 4], 16) * 4
                    i += 5
                    continue
                if i + 3 < len(tokens) and c3 == r"\^d":
                    # Wait for n frames between characters.
                    char_pause = ord(tokens[i + 3]) * 2
                    i += 4
                    continue
                if i + 2 < len(tokens) and c2 == r"\^":
                    # Wait for n frames.
                    flip()
                    pygame.time.wait(ord(tokens[i + 2]) * 20)
                    i += 3
                    continue
                if i + 4 <= len(tokens) and c2 == r"\*":
                    tokens = [tokens[i + 3]] * int(tokens[i + 2]) + tokens[4:]
                    continue
                if i + 1 < len(tokens) and c2 == r"\0":
                    try:
                        c = chr(int("".join(tokens[i + 2 : i + 4])))
                        debug(f"i {i} custom char {c}")
                        i += 3
                    except ValueError:
                        """Handles r"\0"."""
                        mem[CURSOR_X_PT] = x
                        return x

            if char_pause:
                flip()
                pygame.time.wait(char_pause)

            o = ord(c)
            if custom_font:
                debug(f"rendering char {c} ord {o}")
                CHAR_PT = CUSTOM_FONT_PT + o * 8
                w = char_width if o < 128 else char_width_hi
                ccn = 0
                for ibyte in range(8):
                    ccn = (ccn << 8) + mem[CHAR_PT + ibyte]
                for ccy in range(char_height):
                    for ccx in range(w):
                        if ccn & (1 << (ccy * 8 + ccx)):
                            pset(x + ccx, y + 7 - ccy)
                debug(f"x {x}, y {y}")
                x += w
                i += 1
                continue

            character = characters[o].copy()
            r = character.get_rect()

            for hi in range(r.h):
                for wi in range(r.w):
                    clr_at = character.get_at((wi, hi))
                    if clr_at[:3] != (0, 0, 0):
                        _pset(
                            x - 1 + wi,
                            y - 1 + hi,
                            bg if invert else fg,
                            False,
                        )
                    elif bg_rgb is not None:
                        _pset(
                            x - 1 + wi,
                            y - 1 + hi,
                            fg if invert else bg,
                            False,
                        )

            x += char_width if o < 128 else char_width_hi
            i += 1

        y += char_height

    mem[CURSOR_Y_PT] = y
    return x


def scroll(dy: int) -> None:
    """Shift surface pixels by offset dy."""
    scroll_addr = SCREEN_DATA_PT + 64 * abs(dy)
    memcpy(SCREEN_DATA_PT, scroll_addr, 64 * 128)


def uint4(col: int | float | None = None) -> int:
    """Take number and return palette index.
    >>> uint4(-1)
    15
    >>> uint4(-1.5)
    14
    """
    return flr(col) % 16


def uint8(col: int | float | None = None) -> int:
    """Take number and return palette index.
    >>> uint8(-1)
    255
    >>> uint8(-1.5)
    254
    """
    return flr(col) % 256
    # (0x8F if mem[PERSIST_PT] else 0x0F) # https://youtu.be/AsVzk6kCAJY?t=434


def set_debug(b: bool = True):
    global DEBUG
    DEBUG = b


def replace_color(
    surface: pygame.Surface, old_color: tuple, new_color: tuple
) -> pygame.Surface:
    """Replace single color in surface."""
    r = surface.get_rect()
    for hi in range(r.h):
        for wi in range(r.w):
            if surface.get_at((wi, hi)) == old_color:
                surface.set_at((wi, hi), new_color)

    return surface


def sget(x: int | float = 0, y: int | float = 0) -> int:
    """Get the color of a spritesheet pixel.
    >>> sset(0, 0, 13)
    >>> sget()
    13
    >>> sset(0, 0, 0)
    """
    x = flr(x)
    y = flr(y)
    if x < 0 or y < 0 or x > 127 or y > 127:
        return 0

    # return rgb2col(spritesheet.get_at(p)[:3])
    mx, hi = divmod(x, 2)
    return 0x0F & (mem[SPRITE_SHEET_PT + y * 64 + mx] >> int(4 * hi))


def sset(x: int = 0, y: int = 0, col=None) -> None:
    """Set the color of a spritesheet pixel.
    Each 64-byte row contains 128 pixels. Each byte contains two adjacent
    pixels, with the low 4 bits being the left/even pixel and the high 4
    bits being the right/odd pixel."""

    if col is None:
        col = mem[DRAW_COLOR_PT] & 0x0F

    mx, hi = divmod(x, 2)
    addr = SPRITE_SHEET_PT + flr(y) * 64 + flr(mx)
    if hi:
        mem[addr] = (mem[addr] & 0x0F) | ((col & 0x0F) << 4)
    else:
        mem[addr] = (mem[addr] & 0xF0) | (col & 0x0F)


def sprite_get(x: int = 0, y: int = 0, w: int = 16, h: int = 16) -> pygame.Surface:
    sprite = pygame.Surface((w, h))
    x = flr(x)
    y = flr(y)
    for dh in range(h):
        for dw in range(w):
            sprite.set_at((dw, dh), PALETTE[sget(x + dw, y + dh)])

    return sprite


def spr(
    n: int,
    x: int = 0,
    y: int = 0,
    w: int = 1,  # w and h only work in pairs in Pico8 0.2.2c
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
    for dy in range(8 * h):
        for dx in range(8 * w):
            if flip_x:
                tdx = 8 - dx
            else:
                tdx = dx
            if flip_y:
                tdy = 8 - dy
            else:
                tdy = dy
            # printh(
            #     f"_pset({x} + {tdx}, {y} + {tdy}, sget({sx} + {dx}, {sy} + {dy}) => {sget(sx + dx, sy + dy)})"
            # )
            _pset(x + tdx, y + tdy, sget(sx + dx, sy + dy), False)


def show_surf(s: pygame.Surface):
    builtins.print(f"show_surf {s} from {sys._getframe().f_back.f_code.co_name}:")  # type: ignore[union-attr]
    for y in range(s.get_height()):
        for x in range(s.get_width()):
            builtins.print(f"{','.join(f'{n:02x}' for n in s.get_at((x, y)))}", end=" ")
        builtins.print()
    builtins.print()
    # 1 / 0


def sspr(
    sx: int,
    sy: int,
    sw: int,
    sh: int,
    dx: int,
    dy: int,
    dw: int | float | None = None,
    dh: int | float | None = None,
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
    if dx is None:
        dx = 0
    if dy is None:
        dy = 0

    if dw < 0:
        dw = abs(dw)
        flip_x = not flip_x
    if dh < 0:
        dh = abs(dh)
        flip_y = not flip_y

    if flr(sw) == 0 or flr(sh) == 0 or flr(dw) == 0 or flr(dh) == 0:
        return

    # printh(
    #     f"sspr(sx {sx:.2f}, sy {sy:.2f}, sw {sw}, sh {sh}, dx {dx:.2f}, dy {dy:.2f}, dw {dw:.2f}, dh {dh:.2f}, {flip_x}, {flip_y})"
    # )

    dh = abs(flr(dh))
    dw = abs(flr(dw))

    rw = sw / dw
    rh = sh / dh

    # sprite = pygame.transform.flip(sprite_get(sx, sy, sw, sh), flip_x, flip_y)
    # sprite = pygame.transform.scale(sprite, (dw, dh))
    # sprite.set_at((0, 0), (255, 0, 0, 100))
    # sprite.set_colorkey((0, 0, 0))

    # OK
    # pygame.image.save(sprite, f"debug_sspr{sx},{sy},{sw},{sh}, d {dx},{dy},{dw},{dh}, f {flip_x},{flip_y}.png")
    # pygame.image.save(spritesheet, f"debug_spritesheet.png")
    # 1/0
    # show_surf(sprite)
    # surf.blit(sprite, (dx, dy))

    # for y in range(sh):
    #     for x in range(sx):
    #         c = sget(x, y)
    #         builtins.print(f"{c if c else ' '}", end="")
    #     builtins.print()
    # return

    fg = mem[DRAW_COLOR_PT] & 0x0F
    bg = (mem[DRAW_COLOR_PT] & 0xF0) >> 4
    for y in range(dh):
        for x in range(dw):
            tx = (dw - 1 - x) if flip_x else x
            ty = (dh - 1 - y) if flip_y else y
            col = sget(sx + tx * rw, sy + ty * rh)
            col2 = mem[DRAW_PALETTE_PT + col]
            # col = mem[DRAW_PALETTE_PT + sget(sx + tx * rw, sy + ty * rh)]
            # builtins.print(f"({x * rw: 2.0f},{y * rh:2.0f}c{col:2})", end="")
            # builtins.print(f"{col:2} ", end="")
            # rgba = sprite.get_at((x, y))
            # printh(rgba)
            # v = sum(rgba) % 16
            if mem[FILL_PALETTE_PT] and fg != bg:
                # builtins.print(f"f{fg:02}b{bg:02} ", end="")
                _pset(flr(dx + tx), flr(dy + ty), bg if (col2 & 16) else fg)
            else:
                # builtins.print(
                #     f"0v{v:02} {col} ", end=""
                # )
                # Draw if not transparent.
                if not col2 & 16:
                    _pset(flr(dx + tx), flr(dy + ty), col)  # v)
        # builtins.print()


def twos_complement_to_signed(value: int, bits: int = 16) -> int:
    """
    >>> twos_complement_to_signed(49152)
    -16384
    >>> twos_complement_to_signed(0xFFFF, 16)
    -1
    >>> twos_complement_to_signed(0b01111111, 8)
    127
    """
    # If the sign bit is set (i.e., value is negative)
    if value & (1 << (bits - 1)):
        # Subtract 2^bits to get the negative value
        value -= 1 << bits
    return value


def complement(n: int, bits: int = 8, signed: bool = True, twos: bool = False) -> int:
    """
    Computes the one's or two's complement of n within a given bit width.

    Args:
        n (int): The number to compute the complement of. 3-bit range is 0 to 7 or -4 to 3 (signed).
        bits (int, optional): The bit width. Defaults to 8.
        signed (bool, optional): If True, interpret result as signed; otherwise, keep it unsigned.
        twos (bool, optional): If True, computes the two’s complement; otherwise, one's complement.

    Returns:
        int: The complement result, signed or unsigned based on input.

    Raises:
        ValueError: If n is out of range for the given bit width.

    Doctests:
    >>> complement(3, 3, signed=True)   # One's complement of 3 (3-bit signed)
    -4
    >>> complement(3, 3, signed=False)  # One's complement of 3 (3-bit unsigned)
    4
    >>> complement(-3, 3, signed=True)  # One's complement of -3 (3-bit signed)
    2
    >>> complement(6, 3, signed=False)  # One's complement of 6 (3-bit unsigned)
    1
    >>> complement(-6)  # One's complement of -6 in default 8-bit signed
    5
    >>> complement(-4, 3, signed=True)  #  Edge case: smallest valid one's complement of -4 (3-bit signed)
    3
    >>> complement(-5, 3, signed=True)   # Invalid input (out of range)
    Traceback (most recent call last):
    ValueError: Number -5 is out of range for signed 3-bit representation.
    >>> complement(-5, 3, signed=False) # Invalid (negative in unsigned mode)
    Traceback (most recent call last):
    ValueError: Negative numbers are not allowed in unsigned mode.
    >>> complement(-3, 3, signed=True, twos=True)  # Two's complement of -3 (3-bit signed)
    3
    >>> complement(3, 3, signed=True, twos=True)  # Two's complement of 3 (3-bit signed)
    -3
    >>> complement(6, 3, signed=False, twos=True)  # Two's complement of 6 (3-bit unsigned)
    2
    >>> bin(complement(5, signed=False, twos=True))   # Expected: 0b11111011 (251, -5 in two's complement)
    '0b11111011'
    """

    if signed:
        min_val = -(1 << (bits - 1))
        max_val = (1 << (bits - 1)) - 1
    else:
        if n < 0:
            raise ValueError("Negative numbers are not allowed in unsigned mode.")
        min_val = 0
        max_val = (1 << bits) - 1
    if n < min_val or n > max_val:
        raise ValueError(
            f"Number {n} is out of range for {'signed' if signed else 'unsigned'} {bits}-bit representation."
        )

    # Convert negative number to its unsigned equivalent before applying one's complement
    if n < 0:
        n = (1 << bits) + n

    # Apply one's complement and mask it to fit within the bit width
    mask = (1 << bits) - 1
    result = ~n & mask

    # If two’s complement is requested, add 1
    if twos:
        result = (result + 1) & mask

    # If signed output is requested, convert result to signed representation
    # The one’s complement of 3 (011 in 3-bit) should be:
    # ~011 = 100 (binary) = -4 in signed 3-bit representation
    if signed and (result & (1 << (bits - 1))):  # Check if the sign bit is set
        result -= 1 << bits

    return result


def reset() -> None:
    """Reset the draw state, including 3 palettes, camera position, clipping, and fill pattern."""
    mem[DRAW_COLOR_PT] = 0
    # https://pico-8.fandom.com/wiki/Memory#Draw_state
    flags = mem[PERSIST_PT]
    if not flags & 1:
        pal()
        pal(2)
    if not flags & 2:
        poke(HIGH_COLOR_PT, 0)
    if not flags & 4:
        poke(AUDIO_FX_PT, 0, 0, 0)
    if not flags & 8:
        poke(BITPLANE_PT, 255)
    if not flags & 16:
        poke(PRINT_PT, 0, 0, 0, 0)
    if not flags & 32:
        fillp()
    camera()
    clip()


def get_fps():
    return fps


def get_frame_count():
    return frame_count


def _set_fps(n: int = 30):
    global fps
    fps = n


if __name__ == "__main__":
    import doctest

    doctest.testmod()
