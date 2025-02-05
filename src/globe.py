"""Globe ported from https://twitter.com/MunroHoberman/status/1335953892685860865
"""

from pypico8 import *


printh(
    pico8_to_python(
        r"""
q={}
for i=0,1,.05do
    for j=0,1,.05do
        c=sin(i)
        add(q,{x=c*cos(j),y=sin(j)*c,z=cos(i)})
    end
end
color(7)
s=.0125
::_::
    cls()
    for i=2,881do
        if(i<442)
            f=q[i*21%#q+i/21\1]
            x=f.x-f.z*s z=f.z+x*s y=f.y-z*s f.z=z+y*s x=x-y*s f.x=x f.y=y+x*s
        else
            f=q[i-441]
        line(f.x*50+63,f.y*50+63)
    end
flip()
goto _
    """
    )
)


def _init():
    global q, s
    q = Table()
    i = 0
    add_count = 0
    while i <= 1:
        j = 0
        while j <= 1:
            c = sin(i)
            wut = Table(x=c * cos(j), y=sin(j) * c, z=cos(i))
            add(q, wut)
            add_count += 1
            j = round(j + 0.05, 4)  # Too soon if not rounded!
        i = round(i + 0.05, 4)
    color(7)
    s = 0.0125


def _update60():
    # for _ in range(4):
    cls()
    for i in range(2, 882):
        if i < 442:
            f = q[(i * 21 % len(q) + i / 21 // 1)]
            x = f.x - f.z * s
            z = f.z + x * s
            y = f.y - z * s
            f.z = z + y * s
            x = x - y * s
            f.x = x
            f.y = y + x * s
        else:
            f = q[(i - 441)]
        line(f.x * 50 + 63, f.y * 50 + 63)


run(_init, _update60)
