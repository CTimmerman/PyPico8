"""Curvy Lines ported from https://twitter.com/picoter8/status/1344334600479404034

-- curvy lines #pico8 #tweetcart #tweetjam
s=64
::_::
cls()
camera(-s,-s)
n=-s m=-s
for j=-80,s,6do
for i=-s,s,4do
p=40*t()%6
y=j+p
w=sqrt(i*i+y*y)/s
v=y+4*sin(w*2+t())
if(i!=-s)line(n,m,i,v,7)
n=i
m=v
end
end
flip()
goto _

>>> run(_init, _update, _draw)
"""

from pypico8 import camera, cls, line, run, sin, sqrt, t


def _init() -> None:
    global s
    s = 64
    camera(-s, -s)


def _update() -> None:
    pass


def _draw() -> None:
    cls()
    n = -s
    m = -s
    for j in range(-80, s + 1, 6):
        for i in range(-s, s + 1, 4):
            p = 40 * t() % 6
            y = j + p
            w = sqrt(i * i + y * y) / s
            v = y + 4 * sin(w * 2 + t())
            if i != -s:
                line(n, m, i, v, 7)
            n = i
            m = v


if __name__ == "__main__":
    run(_init, _update, _draw)
