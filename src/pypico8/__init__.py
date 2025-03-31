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
2025-01-04 v1.9 added deli, ipairs, select.
2025-02-10 v1.9.1 fixed display memory, print, tonum.
2025-03-01 v1.10 CLI.
2025-03-17 v2.0 delete -> delv

>>> _init_video()
"""

# pylint:disable = global-statement, import-outside-toplevel, invalid-name, line-too-long, multiple-imports, no-member, pointless-string-statement, redefined-builtin, too-many-arguments,unused-import, unidiomatic-typecheck, wrong-import-position, too-many-nested-blocks
import builtins, os, queue, sys, threading, time as py_time  # noqa: E401
from typing import Callable
from unittest.mock import Mock

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
try:
    import pygame
    from pygame.event import Event

    # fmt:off
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from pypico8.maths import atan2, ceil, cos, div, divi, flr, max, mid, min, round4, rnd, shl, shr, sgn, sin, sqrt, srand  # type: ignore  # noqa  # unused here but maybe not elsewhere.
    from pypico8.table import Table, add, all, delv, deli, foreach, ipairs, pairs, pack, select, unpack  # noqa
    from pypico8.audio import audio_channel_notes, music, sfx, threads  # noqa
    from pypico8.strings import chr, ord, pico8_to_python, printh, split, sub, tonum, tostr  # noqa
    from pypico8.video import _init_video, camera, circ, circfill, clip, cls, color, cursor, debug, fget, fillp, flip, fset, get_char_img, get_fps, get_frame_count, line, map, memcpy, mget, mset, oval, ovalfill, pal, palt, peek, peek2, peek4, pget, poke, poke2, poke4, pos, print, pset, rect, rectfill, replace_color, reset, set_debug, _set_fps, scroll, sget, spr, sset, sspr  # noqa
    # fmt:on
except ModuleNotFoundError as ex:
    builtins.print(ex)
    # So my PyGLet implementation can import this from the old folder next to the src folder.


FUN0 = Callable[[], None]

false = False
true = True
DEVKIT_PT = 0x5F2D  # 24365
P0_LEFT = 0
P0_RIGHT = 1
P0_UP = 2
P0_DOWN = 3
P0_O = 4
P0_X = 5
P0_PAUSE = 7
# scancode to p8 button
PLAYER_KEYMAPS = (
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

begin = py_time.time()
btnp_state = 0
btnp_frame = 0
clock = pygame.time.Clock()
command = ""
command_history: list[str] = []
command_mode = False
command_y = 0
cursor_x = 0
flipper: threading.Thread | None = None
stopped = False
running = False
tick = 0
buttons_pressed_since = [0] * 2 * 6  # 2 players * 6 buttons
single_frame_mode = 0


class Flipper(threading.Thread):
    """Async rendering for busy demos like assembled_horizon."""

    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.queue: queue.Queue[str] = queue.Queue(
            maxsize=10
        )  # To talk to this thread.
        self.daemon = True  # Die with main thread.

    def run(self) -> None:
        t_running = True
        while t_running:
            if self.queue.empty():
                flip()
                # clock tick in flip should already keep it responsive, but it doesn't with assembled_horizon!
                pygame.time.wait(1)
            else:
                data = self.queue.get()
                if data == "exit":
                    t_running = False


def cli_start() -> None:
    global command_mode
    stop()
    command_mode = True


def cli_stop() -> None:
    global command_mode
    command_mode = False


def btn(button: int | None = None, player: int = 0) -> int | bool:
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

    >>> btn()
    0
    >>> real_pressed = pygame.key.get_pressed
    >>> pygame.key.get_pressed = mock_pressed
    >>> btn(0)
    True
    >>> pygame.key.get_pressed = real_pressed
    """

    pressed = list(nr for nr, isdown in enumerate(pygame.key.get_pressed()) if isdown)

    if button is None:
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

    player_keymap = PLAYER_KEYMAPS[player]
    # printh(f"keymap {player_keymap}\npressed {pressed}\nname >>>{pygame.key.name(122)}<<<")
    button_pressed = False
    for key in pressed:
        if key in player_keymap and player_keymap[key] == button:
            button_pressed = True

    return button_pressed


def btnp(button: int | None = None, player: int = 0) -> bool | int:
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

    In both cases, 0 can be used for the default behaviour (delays 15 and 4)

    >>> tick_up(10)
    >>> btnp(0)
    False
    >>> real_pressed = pygame.key.get_pressed
    >>> pygame.key.get_pressed = mock_pressed
    >>> btn(0, 0)
    True
    >>> btnp(0)
    True
    >>> buttons_pressed_since
    [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> tick_up(14)
    >>> btnp(0)
    False
    >>> buttons_pressed_since
    [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> tick_up(1)
    >>> btnp(0)
    True
    >>> buttons_pressed_since
    [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> tick_up(1)
    >>> btnp(0)
    False
    >>> tick_up(3)
    >>> btnp(0)
    True
    >>> pygame.key.get_pressed = real_pressed
    """
    # printh(f"btn addr: {btn}")
    pressed = btn(button, player)
    # printh("pressed?" + str(pressed))
    if button is None:
        return pressed
    last_pressed_at = buttons_pressed_since[player * 5 + button]
    if not pressed:
        if last_pressed_at:
            buttons_pressed_since[player * 5 + button] = 0
        return False

    d = tick - last_pressed_at

    initial_delay = peek(0x5F5C) or 15
    repeating_delay = peek(0x5F5D) or 4
    fps = get_fps()
    if fps == 60:
        initial_delay *= 2
        repeating_delay *= 2
    if fps == 15:
        initial_delay >>= 1
        repeating_delay >>= 1

    if last_pressed_at == 0:
        # printh(f"First at tick {tick} frame {get_frame_count()}")
        buttons_pressed_since[player * 5 + button] = tick
        return True

    if d == initial_delay or (
        d > initial_delay and d != 255 and ((d - initial_delay) % repeating_delay) == 0
    ):
        # Delay seems to be in ticks instead of frames in Pico8 0.2.2c. TODO
        # At 15 FPS, True on 0, 7, 9, 11...
        # At 30 FPS, True on 0, 15, 19, 23...
        # At 60 FPS, True on 0, 30, 38, 46...
        # printh(f"Repeat at tick {tick} frame {get_frame_count()}")
        return True
    return False


def erase_command() -> None:
    s = r"\#0\f0" + (" " * (len(command) + 3))
    print(s, 0, command_y, _wrap=True)


def escape_command() -> str:
    r"""Return printable command.
    >>> escape_command() in ('\\#0 \\#0', '\\#8 \\#0')
    True
    """
    return (
        command[:cursor_x].replace("\\", "\\\\")
        + rf"\#{8 if (t() * 10 % 8) < 4 else 0}{command[cursor_x:cursor_x+1] or ' '}\#0"
        + (command[cursor_x + 1 :].replace("\\", "\\\\"))
        + ""
    )


def init(_init: FUN0 = lambda: None) -> None:
    """Initialize."""
    _init_video()
    _init()
    flip()


def mock_pressed() -> list[bool]:
    """Pretend to press button 0 (left)."""
    mock_rv = [False] * 512
    mock_rv[80] = True
    return mock_rv


def pause() -> None:
    """Pause execution."""
    global pause_start, stopped
    stopped = True
    pause_start = time()


def resume() -> None:
    """Resume execution."""
    global begin, pause_start, stopped
    begin += time() - pause_start
    stopped = False


def run(
    _init: FUN0 = lambda: None, _update: FUN0 = lambda: None, _draw: FUN0 = lambda: None
) -> None:
    """Run from the start of the program. Can be called from inside a program to reset program.

    >>> pygame.event.get = Mock(return_value=[
    ...     Event(pygame.KEYDOWN, key=pygame.K_BREAK, unicode=''),
    ...     Event(pygame.KEYDOWN, key=pygame.K_BREAK, unicode=''),
    ...     Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, unicode=''),
    ...     Event(pygame.KEYDOWN, key=pygame.K_z, unicode='z'),
    ...     Event(pygame.KEYDOWN, key=pygame.K_RETURN, unicode=''),
    ...     Event(pygame.KEYDOWN, key=pygame.K_UP, unicode=''),
    ...     Event(pygame.KEYDOWN, key=pygame.K_DOWN, unicode=''),
    ...     Event(pygame.QUIT),
    ... ])
    >>> run()
    >>> cli_stop()
    """
    global begin, btnp_state, command, command_mode, command_y, cursor_x, flipper, pause_start, running, single_frame_mode, stopped, tick
    begin = py_time.time()
    command_mode = False
    fps = 60 if _update.__name__ == "_update60" else 30
    _set_fps(fps)

    try:
        init(_init)
        caption = pygame.display.get_caption()[0]
        pygame.display.set_caption(
            caption + " " + os.path.split(str(sys.modules["__main__"].__file__))[-1]
        )

        if running:
            return

        stopped = False
        running = True
        pause_start = 0.0

        if not flipper:
            flipper = Flipper()
            flipper.start()

        while running:
            # clock.tick(15)
            if command_mode:
                erase_command()
                # printh(f"{escaped_command} curx: {cursor_x} peekx: {peek(0x5F26)}")
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        debug(
                            f"KEYDOWN {event}"
                        )  # eg <Event(768-KeyDown {'unicode': '', 'key': 1073741904, 'mod': 32768, 'scancode': 80, 'window': None})>
                        if (
                            event.key == pygame.K_HOME
                            or event.key == pygame.K_KP7
                            and event.unicode == ""
                        ):
                            cursor_x = 0
                        if (
                            event.key == pygame.K_END
                            or event.key == pygame.K_KP1
                            and event.unicode == ""
                        ):
                            cursor_x = len(command)
                        elif event.key == pygame.K_LEFT:
                            cursor_x = int(max(cursor_x - 1, 0))
                        elif event.key == pygame.K_RIGHT:
                            cursor_x = int(min(cursor_x + 1, len(command)))
                        elif event.key == pygame.K_UP:
                            if not command and command_history:
                                command = command_history[-1]
                            elif command not in command_history:
                                command_history.append(command)
                            else:
                                command = command_history[
                                    int(max(command_history.index(command) - 1, -1))
                                ]
                            cursor_x = len(command)
                        elif event.key == pygame.K_DOWN:
                            try:
                                ci = int(
                                    min(
                                        command_history.index(command) + 1,
                                        len(command_history) - 1,
                                    )
                                )
                                command = command_history[ci]
                                cursor_x = len(command)
                            except ValueError:
                                pass
                        elif event.key == pygame.K_RETURN:
                            if command and command not in command_history:
                                command_history.append(command)

                            escaped_command = escape_command().replace(r"\#8", "")
                            print(
                                rf"\#0\f7> {escaped_command}", 0, command_y, _wrap=True
                            )
                            try:
                                if command == ".":
                                    single_frame_mode = 1
                                    _update()
                                    tick += 1
                                    _draw()
                                    flip()
                                    single_frame_mode = 0
                                    reset()
                                elif command.startswith("?"):
                                    print(eval(command[1:]))
                                else:
                                    debug(f"EXEC {command}")
                                    exec(command)
                            except Exception as ex:
                                print(rf"\#0\fe{ex}", _wrap=True)
                            command = ""
                            command_y = peek(0x5F27)
                            if command_y > 120:
                                scroll(6)
                                command_y -= 6
                            continue
                        elif event.key == pygame.K_BACKSPACE:
                            command = command[: cursor_x - 1] + command[cursor_x:]
                            cursor_x -= 1
                        elif event.key == pygame.K_DELETE:
                            command = command[:cursor_x] + command[cursor_x + 1 :]
                        elif event.key == pygame.K_ESCAPE:
                            command = ""
                            cursor_x = 0
                        elif event.unicode:
                            command = (
                                command[:cursor_x] + event.unicode + command[cursor_x:]
                            )
                            cursor_x += 1
                    elif event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.VIDEORESIZE:
                        pygame.display.flip()

                escaped_command = escape_command()
                print(rf"\#0\f7> {escaped_command}", 0, command_y, _wrap=True)
                command_y -= scroll()
                # rect(cursor_x * 4, command_y,cursor_x * 4 + 4, command_y + 7, 0)
                flip()
                pygame.time.wait(200)
                continue

            # FIXME: demos like assembled_horizon don't return fast enough to be responsive.
            # check_events()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_BREAK, pygame.K_p, pygame.K_RETURN):
                        caption = pygame.display.get_caption()[0]
                        if stopped and not caption.endswith("PAUSED"):
                            # Cart stopped by itself.
                            continue
                        stopped = not stopped
                        debug(f"STOPPED {stopped}")
                        if stopped:
                            pause_start = time()
                            pygame.display.set_caption(caption + " PAUSED")
                        else:
                            begin += time() - pause_start
                            if caption.endswith("PAUSED"):
                                pygame.display.set_caption(caption[: -len(" PAUSED")])
                    elif event.key == pygame.K_ESCAPE:
                        cli_start()
                        break
                elif event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.flip()

            if not stopped:
                _update()
                tick += 1
                _draw()
                # flip()  # Assembled_horizon prefers async flipping, but we do need to pause here.
                pygame.time.wait(10)
                # printh(f"stat7 {stat(7)} stat8 {stat(8)}")

            # Doctest doesn't need user input.
            if (
                not command_mode
                and _init.__name__ == _update.__name__ == _draw.__name__ == "<lambda>"
            ):
                debug("END RUN")
                running = False

    except ZeroDivisionError:
        builtins.print("Use div(a, b) instead.", file=sys.stderr)
        raise

    # audio threads
    for thread in threads:
        thread.stop = True  # type: ignore[attr-defined]
    for thread in threads:
        thread.join()

    # video threads
    flipper.queue.put("exit")
    flipper.join()

    pygame.quit()


def stat(x: int) -> int | bool | str:
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

    >>> _init_video()
    >>> stat(7)
    0
    >>> stat(8)
    30
    >>> poke(DEVKIT_PT, 1)
    0
    >>> for i in range(30, 111): _ = stat(i)
    """
    if x == 6 and "-p" in sys.argv:
        return " ".join(sys.argv[sys.argv.index("-p") :])  # Unable to verify.
    if x == 7:
        return get_fps() if command_mode else int(get_frame_count() / time())
    if x == 8:
        return 0 if command_mode else get_fps()

    if x in range(16, 20):
        x += 4
    if x in range(20, 24):
        note = (audio_channel_notes[x - 20] + 1) % 32
        audio_channel_notes[x - 20] = note

        sfx(peek(12800 + note * 2))  # TODO: loop in different thread.
        return note

    if x == 30:
        return btn() > 0
    if x == 31:
        return str(btn())
    if peek(DEVKIT_PT) == 1:
        if x == 32:
            return pygame.mouse.get_pos()[0]
        if x == 33:
            return pygame.mouse.get_pos()[1]
        if x == 34:
            primary, middle, secondary = pygame.mouse.get_pressed()
            return 1 * primary + 2 * secondary + 4 * middle

    utc_time = py_time.gmtime()
    if x == 80:
        return utc_time.tm_year
    if x == 81:
        return utc_time.tm_mon
    if x == 82:
        return utc_time.tm_mday
    if x == 83:
        return utc_time.tm_hour
    if x == 84:
        return utc_time.tm_min
    if x == 85:
        return utc_time.tm_sec

    local_time = py_time.localtime()
    if x == 90:
        return local_time.tm_year
    if x == 91:
        return local_time.tm_mon
    if x == 92:
        return local_time.tm_mday
    if x == 93:
        return local_time.tm_hour
    if x == 94:
        return local_time.tm_min
    if x == 95:
        return local_time.tm_sec

    if x == 110:
        return single_frame_mode

    return 0


def stop(message: str | None = None) -> None:
    """Stop the cart and optionally print a message.
    >>> stop("doctest")
    doctest
    """
    global stopped
    if message:
        builtins.print(message)
    reset()
    stopped = True


def t() -> float:
    """Return seconds since cart start."""
    return py_time.time() - begin


def tick_up(delta: int = 1) -> None:
    # """
    # >>> tick_up(0)
    # """
    global tick
    tick += delta


def time() -> float:
    """Return seconds since cart start.
    >>> _ = time()
    """
    return t()
