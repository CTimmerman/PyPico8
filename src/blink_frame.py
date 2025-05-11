"""Blink Frame ported from https://pico-8.fandom.com/wiki/Pal

blink_frame = false
t = 0

function _update()
  -- every 8th frame is a "blink frame"
  t = (t + 1) % 8
  blink_frame = (t == 0)
end

function _draw()
  cls()

  -- reset the palette
  pal()

  if blink_frame then
    -- replace dark grey with red
    pal(5, 8)
  end

  -- draw the blinking light sprite
  spr(16, 56, 72)
end

Move code ported from https://www.lexaloffle.com/pico8_manual.txt#:~:text=interactive

>>> run(_init, _update, _draw)
"""

from pypico8 import *
from pypico8 import _set_fps


def _init() -> None:
    global blink_frame, f, x, y
    blink_frame = False
    f = 0
    x = y = 64


def _update() -> None:
    global blink_frame, f, x, y
    # every 8th frame is a "blink frame"
    f = (f + 1) % 8

    blink_frame = f == 0

    if btn(0):
        x = x - 1
    if btn(1):
        x = x + 1
    if btn(2):
        y = y - 1
    if btn(3):
        y = y + 1
    if btnp(4):
        _set_fps(int(stat(8)) - 15 or 15)
    if btnp(5):
        _set_fps(int(stat(8)) + 15)


def _draw() -> None:
    cls()
    pal()
    if blink_frame:
        # replace dark grey with red
        pal(5, 8)

    # draw the blinking light sprite
    # spr(16, 56, 72)
    circfill(x, y, 5, 5)
    print(stat(8), 10)


if __name__ == "__main__":
    run(_init, _update, _draw)
