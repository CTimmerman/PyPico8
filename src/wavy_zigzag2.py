"""Wavy Zigzag 2 ported from https://twitter.com/picoter8/status/1345625478061813761

-- wavy zigzag 2 #pico8 #tweetcart #tweetjam
::_::
cls()
for i=-8,136,8do
for j=-8,136,6do
x=i-64
y=j-64
s=3*sin(y/32+cos(x/180-t()/4)+t()/2)+flr(j/6%2)*10
if(j!=-8)line(i+s,j,n,m,7)
n=i+s
m=j
end
end
flip()
goto _

>>> run(_init, _draw=_draw)
"""

from pypico8 import cls, cos, flr, line, run, sin, t


def _init() -> None:
    global m, n
    m = 0
    n = 0


def _draw() -> None:
    global m, n
    cls()
    for i in range(-8, 136, 8):
        for j in range(-8, 136, 6):
            x = i - 64
            y = j - 64
            s = 3 * sin(y / 32 + cos(x / 180 - t() / 4) + t() / 2) + flr(j / 6 % 2) * 10
            if j != -8:
                line(i + s, j, n, m, 7)
            n = i + s
            m = j


if __name__ == "__main__":
    run(_init, _draw=_draw)
