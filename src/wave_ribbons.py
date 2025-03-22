"""Wave Ribbons ported from https://twitter.com/Andy_Makes/status/1375075441929752584

printh(
    pico8_to_python(
        r'''
t=0
pal({1,2,8,9,10,11},1)
::Water wave::
cls(1)t+=.008
for k=1,5 do
for c=-20,150 do
y=-30+sin(t*(k+1)+c*.01)*10+sin(k*.3-c*.00003*c)*6+k*26+sin(t+k*.3)*5line(c,y,c,y+128,k+1)
if(c%2==0)line(c,y,c-20,y+20,k)
end
end
flip()goto Water wave
        '''
    )
)

>>> run(_init, _update, _draw)
"""

from pypico8 import *


def _init() -> None:
    global t2
    t2 = 0.0
    pal(Table([1, 2, 8, 9, 10, 11]), 1)


def _update() -> None:
    pass


def _draw() -> None:
    global t2
    cls(1)
    t2 += 0.008
    for k in range(1, 6):
        for c in range(-20, 151):
            y = (
                -30
                + sin(t2 * (k + 1) + c * 0.01) * 10
                + sin(k * 0.3 - c * 0.00003 * c) * 6
                + k * 26
                + sin(t2 + k * 0.3) * 5
            )
            line(c, y, c, y + 128, k + 1)
            if c % 2 == 0:
                line(c, y, c - 20, y + 20, k)


if __name__ == "__main__":
    run(_init, _update, _draw)
