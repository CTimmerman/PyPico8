"""Blink Frame ported from https://pico-8.fandom.com/wiki/Pal
Move code ported from https://www.lexaloffle.com/pico8_manual.txt#:~:text=interactive
"""
from pypico8 import btn, circfill, cls, pal, run


def _init():
    global blink_frame, t, x, y
    blink_frame = False
    t = 0
    x = y = 64


def _update():
    global blink_frame, t, x, y
    # every 8th frame is a "blink frame"
    t = (t + 1) % 8
    blink_frame = t == 0

    if btn(0):
        x = x - 1
    if btn(1):
        x = x + 1
    if btn(2):
        y = y - 1
    if btn(3):
        y = y + 1


def _draw():
    cls()

    # reset the palette
    pal()

    if blink_frame:
        # replace dark grey with red
        pal(5, 8)

    # draw the blinking light sprite
    # spr(16, 56, 72)
    circfill(x, y, 5, 5)


run(_init, _update, _draw)