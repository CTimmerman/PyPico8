"""Loading bar ported from https://twitter.com/heymatthias_/status/1357435447224459266
"""
from pypico8 import (  # noqa
    Table,
    cls,
    fillp,
    flr,
    rectfill,
    pico8_to_python,
    print,
    printh,
    tostr,
    run,
)


printh(
    pico8_to_python(
        r"""
t={0,16705,23130,0xbebe,0xffff}f=fillp
r=rectfill
function d(p)f(t[5-flr(p*5)])end
cls()x=3w=122print('loading...',48,12,7)
::_::
if(x<w)x+=1p=x/w
d(p)r(x,56,x,72,9)f(0)rect(x+1,55,x+1,73,7)line(4,55,4,73,7)r(0,76,127,127,0)pr=tostr(flr(p*100))..'%'print(pr,x-9,76,7)flip()
goto _
        """
    )
)


def _init():
    global t, f, r, x, w, p
    t = Table([0, 16705, 23130, 0xBEBE, 0xFFFF])
    f = fillp
    r = rectfill
    cls()
    x = 3
    w = 122
    fillp(16705)
    print("loading...", 48, 12, 7)
    p = 0


def d(p):
    f(t[5 - flr(p * 5)])


def _update():
    pass


def _draw():
    global x, p
    if x < w:
        x += 1
        p = x / w
    d(p)
    r(x, 56, x, 72, 9)  # patterned bar
    f(0)
    r(x + 1, 55, x + 1, 73, 7)  # right border # FIXME: rect x1 = x + 2 is as far and one pixel ahead of "50%". x1 = x + 1 now is x-4 to x+4, only with _border > 0 !
    r(4, 55, 4, 73, 7)  # left border
    r(0, 76, 127, 127, 0)  # bottom
    pr = tostr(flr(p * 100)) + "%"
    print(pr, x - 9, 76, 7)


run(_init, _update, _draw)