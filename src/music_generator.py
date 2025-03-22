"""Music Generator ported from https://www.youtube.com/watch?v=1EWR6gVyPh4

printh(
    pico8_to_python(
        r'''
q=poke
r=0x3200
s={0x2d2c,3,65,16,67,32}
t={0,2,3,5,7}
for i=1,#s,2 do
    q(r+s[i],s[i+1])
end
sfx(0)
cls()
::_::
    flip()
    l=stat(20)
    pset(2*l,44,15)
    if l==31 then
        cls()
        for x=0,31 do
            y=r+x*2
            n=12+t[flr(rnd(#t)+1)]
            q(y,n)
            q(y+1,94-x%8*2)
            line(2*x,42,2*x,42-n,1.7*(7-x%8))
        end
    end
goto _'''
    )
)

>>> import pygame
>>> pygame.mixer.init()
>>> run(_init, _update, _draw)
"""

# fmt: off
from pypico8 import cls, flip, flr, line, poke, pset, sfx, stat, Table, rnd, run
# fmt: on


def _init() -> None:
    global r, s, t
    r = 0x3200  # 12800 - audio pointer
    s = Table(
        [0x2D2C, 3, 65, 16, 67, 32]
    )  # 11564? TODO: https://pico-8.fandom.com/wiki/Memory#Sound_effects
    t = Table([0, 2, 3, 5, 7])
    for i in range(1, len(s) + 1, 2):
        poke(int(r) + (s[i] or 0), s[i + 1] or 0)  # write notes

    sfx(0)
    cls()


def _update() -> None:
    pass


def _draw() -> None:
    global r, t

    flip()
    note = stat(20)
    pset(2 * note, 44, 15)
    if note == 31:
        cls()
        for x in range(0, 31 + 1):
            y = r + x * 2
            n = 12 + t[flr(rnd(len(t)) + 1)]
            poke(y, n)
            poke(y + 1, 94 - x % 8 * 2)
            line(2 * x, 42, 2 * x, 42 - n, 1.7 * (7 - x % 8))


if __name__ == "__main__":
    run(_init, _update, _draw)
