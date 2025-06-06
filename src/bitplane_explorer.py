r"""Bitplane Explorer ported from https://www.lexaloffle.com/bbs/?tid=54214

printh(
    pico8_to_python(
        r'''
-- bitplane explorer
--  BY PANCELOR

-- bitplane config
col=15
read=15
write=4

-- circle
x=64
y=64
r0=32
r=r0

function _draw()
 cls()

 -- draw palette
 for i=0,15 do
  u,v=i%4*32,i\4*32
  rectfill(u,v,u+31,v+31,i)
 end

 -- handle buttons
 if btn(5) then
  dx,dy=axis(btnp())
  read+=dx
  write-=dy
  maskem="\#0\^i"
  maskex=" ⬅️➡️⬆️⬇️"
 else
  maskem=""
  maskex=" ❎"
 end
 if btn(4) then
  dx,dy=axis(btnp())
  r0+=dx*16
  r0=mid(16,96,r0)
  col-=dy
  col&=0xf
  colem="\#0\^i"
  colex=" ⬅️➡️⬆️⬇️"
 else
  colem=""
  colex=" 🅾️"
 end

 -- move
 if not btn(4) and not btn(5) then
  dx,dy=axis(btn())
  x+=4*dx
  y+=4*dy
  btnex="⬅️➡️⬆️⬇️"
 else
  btnex=""
 end

 -- animate radius
 rgoal=r0
 rgoal*=1+sin(time()/2)/12
 r=approach(r,rgoal,8)

 -- this is the bitplane part.
 -- very short! even shorter
 -- if you hardcode val
 val=(read&0xf)<<4 | write&0xf
 poke(0x5f5e,val)
 circfill(x,y,r,col)
 poke(0x5f5e,-1) --reset

 -- outline
 circ(x,y,r,0)

 -- explainer text
 cursor(0,0)
 color(7)
 if btn(5) then
  ?"            \#00xrw"
 else
  ?""
 end
 ?btnex,0,0
 ?qf("poke(0x5f5e,%%)%",maskem,tobyte(val),maskex)
 ?qf("circfill(x,y,%%,%)%",colem,r0,col,colex)
end

-->8
--helpers
function axis(b)
 return b\2%2-b%2,b\8%2-b\4%2
end
function tobyte(num)
 return "0x"..sub(tostr(num,1),5,6)
end
function approach(x,x1, dx)
 dx=dx or 1
 return x<x1 and min(x+dx,x1) or max(x-dx,x1)
end
function qf(fmt,...)
 local parts=split(fmt,"%")
 local str=deli(parts,1)
 for ix,pt in ipairs(parts) do
  local arg=select(ix,...)
  str..=tostr(arg)..pt
 end
 return str
end
        '''
    )
)

>>> run(_init, _update, _draw)
"""

# pylint: disable=redefined-builtin
from pypico8 import (
    btn,
    btnp,
    circ,
    circfill,
    cls,
    color,
    cursor,
    deli,
    ipairs,
    mid,
    poke,
    print,
    rectfill,
    select,
    sin,
    split,
    sub,
    run,
    time,
    tostr,
)


col: int = 0
read: int = 0
write: int = 0
x: int = 0
y: int = 0
r: int = 0
r0: int = 0


def _init() -> None:
    global col, read, write, x, y, r0
    global r

    # bitplane explorer
    #  BY PANCELOR

    # bitplane config
    col = 15
    read = 15
    write = 4

    # circle
    x = 64
    y = 64
    r0 = 32
    r = r0


def _draw() -> None:
    global col, r, r0, read, write, x, y

    cls()

    # draw palette
    for i in range(0, 15 + 1):
        u, v = i % 4 * 32, i // 4 * 32
        rectfill(u, v, u + 31, v + 31, i)

    # handle buttons
    if btn(5):
        dx, dy = axis(btnp())
        read += dx
        write -= dy
        maskem = r"\#0\^i"  # bg color 0 and invert bg and fg color.
        maskex = " ⬅️➡️⬆️⬇️"
    else:
        maskem = ""
        maskex = " ❎"
        # maskex = " 5"
    if btn(4):
        dx, dy = axis(btnp())
        r0 += dx * 16
        r0 = int(mid(16, 96, r0))
        col -= dy
        col &= 0xF
        colem = r"\#0\^i"
        colex = " ⬅️➡️⬆️⬇️"
    else:
        colem = ""
        colex = " 🅾️"

    # move
    if not btn(4) and not btn(5):
        dx, dy = axis(btn())
        x += 4 * dx
        y += 4 * dy
        btnex = "⬅️➡️⬆️⬇️"
    else:
        btnex = ""

    # animate radius
    rgoal = float(r0)
    rgoal *= 1 + sin(time() / 2) / 12
    r = approach(r, rgoal, 8)

    # this is the bitplane part.
    # very short! even shorter
    # if you hardcode val
    val = (read & 0xF) << 4 | write & 0xF
    poke(0x5F5E, val)
    circfill(x, y, r, col)
    poke(0x5F5E, -1)  # reset

    # outline
    circ(x, y, r, 0)

    # explainer text
    cursor(0, 0)
    color(7)
    if btn(5):
        print("            \\#00xrw")
    else:
        print("")

    print(btnex, 0, 0)
    print(qf("poke(0x5f5e,%%)%", maskem, tobyte(val), maskex))
    print(qf("circfill(x,y,%%,%)%", colem, r0, col, colex))


# >8
# helpers
def axis(b):
    "Arrow button to direction."
    return b // 2 % 2 - b % 2, b // 8 % 2 - b // 4 % 2


def tobyte(num: int) -> str:
    """
    >>> tobyte(244)
    '0xF4'
    """
    return "0x" + sub(tostr(num, 1), 5, 6)


def approach(xv, x1, dx):
    "Return increment that doesn't exceed target value."
    dx = dx or 1
    return xv < x1 and min(xv + dx, x1) or max(xv - dx, x1)


def qf(fmt: str, *argv) -> str:
    """Format string.
    >>> qf("aaa%bbb", "ccc", "ddd")
    'aaacccbbb'
    """
    parts = split(fmt, "%", False)
    s = deli(parts, 1)  # type: ignore  # s = "aaa"
    for ix, pt in ipairs(parts):
        arg = select(ix, *argv)
        s += tostr(arg) + pt

    return str(s)


def _update() -> None:
    pass


if __name__ == "__main__":
    run(_init, _update, _draw)
