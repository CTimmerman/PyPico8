"""Dancing Rectangles ported from https://twitter.com/picoter8/status/1334310272509620224 #pico8 #tweetcart #tweetjam

-- dancing rects #pico8 #tweetcart #tweetjam
::_::cls()camera(-64,-64)
for k=18,96,18do
c=k/18
for i=0,1,.1/c do
b=i-t()/24*c
x=k*cos(b)y=k*sin(b)
o=0p=0
for j=0,1,.25do
a=64/k+i*c+j-t()/4*c
n=8*cos(a)m=8*sin(a)
if(o!=p)line(x+n,y+m,x+o,y+p,7)
o=n p=m
end
end
end
flip()goto _

>>> run(_init, _update, _draw)
"""

from pypico8 import camera, cls, cos, line, run, sin, t


def _init() -> None:
    camera(-64, -64)


def _update() -> None:
    pass


def _draw() -> None:
    cls()
    for k in range(18, 97, 18):
        c = k / 18
        i = 0.0
        while i <= 1:
            b = i - t() / 24 * c
            x = k * cos(b)
            y = k * sin(b)
            o = 0.0
            p = 0.0
            j = 0.0
            while j <= 1:
                a = 64 / k + i * c + j - t() / 4 * c
                n = 8 * cos(a)
                m = 8 * sin(a)
                if o != p:
                    line(x + n, y + m, x + o, y + p, 7)
                o = n
                p = m
                j += 0.25
            i += 0.1 / c


if __name__ == "__main__":
    run(_init, _update, _draw)
