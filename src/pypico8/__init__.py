"""Pico8 functions in Python
2021-01-03 v1.0 by Cees Timmerman
2021-01-04 v1.0.1 fixed palette in line()
2021-01-04 v1.1 added color, circle, mid, oval, and rect functions.
2021-01-07 v1.2 added pget, pset, palette swap, PICO-8/Lua to Python translator.
2021-01-09 v1.3 added reset, stop, fget, fset, div, sub, split, argv, btn, printh
2021-01-11 v1.4 added spr, sspr, sget, sset, screen mode 3 (64x64); fixed rect size.
2021-01-18 v1.5 added ^, ^=, for with float step, tonum, ceil, atan2, stat.
2021-01-19 v1.5.1 fixed print color, atan2.
2021-01-25 v1.5.2 fixed print, sget.
2021-01-27 v1.5.3 fixed cls, most Prospector problems, print.
2021-01-29 v1.5.4 fixed fps.
2021-02-08 v1.6 added sfx, music, clip, sgn.
2021-02-09 v1.7 added pack, unpack. Fixed min, max, rnd, chr. Refactored.
2021-02-14 v1.8 prt -> print, fillp.
"""
# pylint:disable=import-outside-toplevel,multiple-imports,pointless-string-statement,redefined-builtin,too-many-arguments,unused-import,unidiomatic-typecheck,wrong-import-position,too-many-nested-blocks
import builtins, os, sys, time as py_time

# fmt:off
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame, pygame.freetype

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pypico8.math import atan2, ceil, cos, div, flr, max, mid, min, rnd, shl, shr, sgn, sin, sqrt, srand  # noqa; unused here but maybe not elsewhere.
from pypico8.table import Table, add, all, delete, foreach, pairs, pack, unpack  # noqa
from pypico8.audio import audio_channel_notes, music, sfx, threads  # noqa
from pypico8.strings import chr, ord, pico8_to_python, printh, split, sub, tonum, tostr  # noqa
from pypico8.video import  _init_video, camera, circ, circfill, clip, cls, color, cursor, fget, fillp, flip, frame_count, fset, get_char_img, line, map, memcpy, mget, mset, multimethod, oval, ovalfill, pal, palt, peek, peek2, peek4, pget, poke, poke2, poke4, pos, print, pset, rect, rectfill, replace_color, reset, sget, spr, sset, sspr, to_col  # noqa
# fmt:on
false = False
true = True

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
    global btnp_state, btnp_frame
    current_state = btn(i, p)
    if current_state != btnp_state:
        btnp_state = current_state
        btnp_frame = frame_count
        printh(f"frame: {btnp_frame}")
        return current_state

    return False


# ---------- Control flow ---------- #
def init(_init=lambda: True):
    _init_video()
    _init()
    flip()


running = False


def run(_init=lambda: True, _update=lambda: True, _draw=lambda: True):
    """Run from the start of the program. Can be called from inside a program to reset program."""
    global begin, fps, running, btnp_state, stopped

    begin = py_time.time()
    if _update.__name__ == "_update60":
        fps = 60
    else:
        fps = 30

    try:
        init(_init)
        if running:
            return

        stopped = False
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

            if not stopped:
                btnp_state = 0
                _update()
                _draw()
                flip()
    except ZeroDivisionError:
        builtins.print("Use div(a, b) instead.", file=sys.stderr)
        raise

    pygame.quit()


def stop(message=None):
    """Stop the cart and optionally print a message."""
    global stopped
    if message:
        builtins.print(message)

    stopped = True


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
    exec(
        open(
            os.path.join(os.path.dirname(__file__), "../fake_sprite.py"),
            encoding="utf8",
        ).read()
    )
