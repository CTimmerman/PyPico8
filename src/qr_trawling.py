"""QR Trawling ported from https://twitter.com/MunroHoberman/status/1359165139258335238
"""

from pypico8 import (  # noqa
    camera,
    cls,
    fillp,
    flip,
    line,
    pico8_to_python,
    printh,
    pset,
    rect,
    rnd,
    run,
)


printh(
    pico8_to_python(
        r"""
function q(x,y)
    for i=1,n do
        rect(x-i,y-i,x+i,y+i,(i+k)%2*7)
    end
end
cls(7)
f=fillp
::_::
for h=0,3do
    for u=0,3do
        camera(-u*33,-h*33)
        for x=0,28do
            for y=0,28do
                pset(x,y,rnd(2)\1*7)
            end
        end
        f(23130)
        line(6,25,6,6,7)
        line(25,6)
        f()
        n=4
        k=1
        q(3,3)
        q(25,3)
        q(3,25)
        n=2
        k=0
        q(22,22)
    end
    flip()
end
goto _
        """
    )
)


def _init():
    global f
    cls(7)
    f = fillp


def q(x, y):
    for i in range(1, n + 1):
        rect(x - i, y - i, x + i, y + i, (i + k) % 2 * 7)


def _update():
    pass


def _draw():
    global n, k

    for h in range(0, 3 + 1):
        for u in range(0, 3 + 1):
            camera(-u * 33, -h * 33)
            for x in range(0, 28 + 1):
                for y in range(0, 28 + 1):
                    pset(x, y, rnd(2) // 1 * 7)

            f(23130)
            line(6, 25, 6, 6, 7)
            line(25, 6)
            f()
            n = 4
            k = 1
            q(3, 3)
            q(25, 3)
            q(3, 25)
            n = 2
            k = 0
            q(22, 22)

        flip()


if __name__ == "__main__":
    run(_init, _update, _draw)
