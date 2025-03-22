"""Color Maze ported from https://twitter.com/ValerADHD/status/1331855383045025792

printh(
    pico8_to_python(
        r'''
cls()w=128r=rnd
for i=0,99do
    ?1,r(w),r(w),i|8
end
for i=0,999do
    ?chr(-r(2)),i%22*6,i\22*4,7
end
::_::
    x=r(w)\1*6
    y=r(w)\1*4
    ?"◆",x,y,0
    ?chr(-r(2)),x,y,7
    for i=0,99do
        x=r(w)
        y=r(w)
        k=pget(x,y)
        if k>7then
            for d=0,1,.25do
                a=x+cos(d)b=y+sin(d)
                if(pget(a,b)!=7)pset(a,b,k)
            end
        end
    end
goto _
        '''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import (  # noqa
    chr,
    cls,
    cos,
    print,
    pget,
    pset,
    rnd,
    run,
    sin,
)


def _init() -> None:
    global w, r
    cls()
    w = 128
    r = rnd
    for i in range(0, 99 + 1):
        print(1, r(w), r(w), i | 8)
    for i in range(0, 999 + 1):
        print(chr(-r(2)), i % 22 * 6, i // 22 * 4, 7)


def _update() -> None:
    pass


def _draw() -> None:
    global w, r
    x = r(w) // 1 * 6
    y = r(w) // 1 * 4
    print("◆", x, y, 0)
    print(chr(-r(2)), x, y, 7)
    for _ in range(0, 1000):
        x = r(w)
        y = r(w)
        k = pget(x, y)
        if k > 7:
            d = 0.0
            while d <= 1:
                a = x + cos(d)
                b = y + sin(d)
                if pget(a, b) != 7:
                    pset(a, b, k)
                d += 0.25


if __name__ == "__main__":
    run(_init, _update, _draw)
