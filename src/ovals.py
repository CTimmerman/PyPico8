"""Ovals ported from https://www.lexaloffle.com/bbs/?tid=38665
TODO: Fix character patterns.
"""
# flake8:noqa
from pypico8 import *


printh(
    pico8_to_python(
        r"""
pattern={[0]=
…,∧,░,⧗,▤,✽,★,✽,
ˇ,░,▤,♪,░,✽,★,☉,
░,▤,♪,░,✽,★,☉,…,
∧,░,⧗,▤,✽,★,✽,★
}

function _draw()
 cls(1)
 for i=0,31/32,1/32 do
  local x=64+cos(i+t()/8)*48
  local y=64+sin(i+t()/8)*44
  local w=8+cos(i*2+t()/2)*6
  local h=8+sin(i*3+t()/2)*6

  fillp(pattern[i*32])
  ovalfill(x-w,y-h,x+w,y+h,
   (i*32)%8+8)

 end
 print("pico-8 0.2.1",40,62,13)
end
        """
    )
)


def _init():
    global pattern
    # fmt: off
    pattern = [
            "…","∧","░","⧗","▤","✽","★","✽",
            "ˇ","░","▤","♪","░","✽","★","☉",
            "░","▤","♪","░","✽","★","☉","…",
            "∧","░","⧗","▤","✽","★","✽","★",
        ]
    # fmt: on


def _update():
    pass


def _draw():
    cls(1)
    i = 0
    while i <= 31 / 32:
        x = 64 + cos(i + t() / 8) * 48
        y = 64 + sin(i + t() / 8) * 44
        w = 8 + cos(i * 2 + t() / 2) * 6
        h = 8 + sin(i * 3 + t() / 2) * 6

        fillp(pattern[int(i * 32)])
        ovalfill(x - w, y - h, x + w, y + h, (i * 32) % 8 + 8)
        i += 1 / 32

    print("PICO-8 0.2.1", 40, 62, 13)


run(_init, _update, _draw)