"""Cistercian numerals ported from https://twitter.com/lexaloffle/status/1357029681703178241
Each character can represent 1 to 9999. https://en.wikipedia.org/wiki/Cistercian_numerals
"""

from pypico8 import (
    Table,
    cls,
    line,
    pico8_to_python,
    printh,
    run,
    t,
)


printh(
    pico8_to_python(
        r"""
p,l={2,7,3,6,98,11,178,183,2930},line
::_::
cls()
for b=0,8do
    for a=0,9do
        q,x,y=a+b*t()\.2,8+a*12,3+b*14
        l(x,y,x,y+9)
        for j=0,3do
            z=(j&2)*5
            l()
            n,u,v=p[q%10]or 0,3*(j&1)*2-3,3*(j&2)-3
            for i=0,2do
                l(x-u*(n&8)/8,y-v*(n&4)/4+z,x-u*(n&2)/2,y-v*(n&1)+z)n>>=4
            end
            q\=10
        end
    end
end
flip()goto _
        """
    )
)


def _init():
    global p, L
    p, L = Table([2, 7, 3, 6, 98, 11, 178, 183, 2930]), line


def _update():
    pass


def _draw():
    global a
    cls()
    for b in range(0, 8 + 1):
        for a in range(0, 9 + 1):
            q, x, y = a + b * t() // 0.2, 8 + a * 12, 3 + b * 14
            L(x, y, x, y + 9)
            for j in range(0, 3 + 1):
                z = (j & 2) * 5
                # L()
                n, u, v = p[q % 10] or 0, 3 * (j & 1) * 2 - 3, 3 * (j & 2) - 3
                for _ in range(0, 2 + 1):
                    L(
                        x - u * (n & 8) / 8,
                        y - v * (n & 4) / 4 + z,
                        x - u * (n & 2) / 2,
                        y - v * (n & 1) + z,
                    )
                    n >>= 4
                # }
                q //= 10
            # }
        # }
    # }


run(_init, _update, _draw)
