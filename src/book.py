"""Book ported from https://x.com/2DArray/status/1109890993543884801
FIXME: Left half glitches sometimes on loop.

printh(
    pico8_to_python(
        r'''::_::cls()
        for k=-1,1,2 do
            for j=8-8*k,8+8*k,k do
                x=59.5
                q=1-mid(2-t()/4%2-j/16,1)^2
                p=1-q
                y=84.5+(16-j)/2*p+q*j/2
                w=q/2
                for i=0,1,.02 do
                    c=6+j%2
                    if(j*i==0or j>15)c=4
                    if(sgn(x-60)==k)line(x,y,x+10,y-40,c)line(x,y,x+10,y-41)
                    x+=cos(w)y+=sin(w)w-=p*.035*q*(1-i)
                end
            end
        end
        flip()
        goto _'''
    )
)

>>> run(_draw=_draw)
"""

from pypico8 import (
    cls,
    cos,
    flip,
    line,
    mid,
    sgn,
    sin,
    round4,
    run,
    t,
)  # noqa


def _draw() -> None:
    cls()
    k = -1
    while k <= 1:
        j = 8 - 8 * k
        while 1:
            x = 59.5
            q = 1 - mid(2 - t() / 4 % 2 - j / 16, 1) ** 2
            p = 1 - q
            y = 84.5 + (16 - j) / 2 * p + q * j / 2
            w = round4(q / 2)
            i = 0.0
            # Pico8's for i=0,1,.02 do doesn't hit 1 but total loops are equal with <=
            while i <= 1:
                c = 6 + j % 2
                if j * i < 0.01 or j > 15:  # last and first page to flip are brown
                    c = 4
                if sgn(x - 60) == k:
                    line(x, y, x + 10, y - 40, c)
                    line(x, y, x + 10, y - 41)
                x = round4(x + cos(w))  # page width
                y = round4(y + sin(w))  # open angle
                w = round4(w - p * 0.035 * q * (1 - i))  # page turn amount
                i = round4(i + 0.02)  # book width
            if j == 8 + 8 * k:
                break
            j += k
        k += 2
    flip()


if __name__ == "__main__":
    run(_draw=_draw)
