"""Bitplane Explorer ported from https://www.lexaloffle.com/bbs/?tid=54214
TODO: FIXME
"""

from pypico8 import (  # noqa
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
    pico8_to_python,
    poke,
    print,
    printh,
    rectfill,
    select,
    sin,
    split,
    sub,
    run,
    time,
    tostr
)


printh(
    pico8_to_python(
        r"""
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
        """
    )
)


def _init():
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


def _draw():
    global col, r, r0, read, write, x, y
    cls()

    # draw palette
    for i in range(0, 15 + 1):
        u, v = i % 4 * 32, i // 4 * 32
        rectfill(u, v, u + 31, v + 31, i)
    # }

    # handle buttons
    if btn(5):
        dx, dy = axis(btnp())
        read += dx
        write -= dy
        maskem = "\#0\^i"  # TODO: \# P0 : background color
        maskex = " ⬅️➡️⬆️⬇️"
    else:
        maskem = ""
        maskex=" ❎"
        #maskex = " 5"
    # }
    if btn(4):
        dx, dy = axis(btnp())
        r0 += dx * 16
        r0 = mid(16, 96, r0)
        col -= dy
        col &= 0xF
        colem = "\#0\^i"
        colex = " ⬅️➡️⬆️⬇️"
    else:
        colem = ""
        colex = " 🅾️"
    # }

    # move
    if not btn(4) and not btn(5):
        dx, dy = axis(btn())
        x += 4 * dx
        y += 4 * dy
        btnex = "⬅️➡️⬆️⬇️"
    else:
        btnex = ""
    # }

    # animate radius
    rgoal = r0
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
        print("            \#00xrw")
    else:
        print("")
    # }
    print(btnex, 0, 0)
    print(qf("poke(0x5f5e,%%)%", maskem, tobyte(val), maskex))
    print(qf("circfill(x,y,%%,%)%", colem, r0, col, colex))
# }


# >8
# helpers
def axis(b):
    return b // 2 % 2 - b % 2, b // 8 % 2 - b // 4 % 2
# }
def tobyte(num):
    return "0x" + sub(tostr(num, 1), 5, 6)
# }
def approach(x, x1, dx):
    dx = dx or 1
    return x < x1 and min(x + dx, x1) or max(x - dx, x1)
# }


def qf(fmt, *argv):
    parts = split(fmt, "%", False)
    s = deli(parts, 1)
    # printh(f"fmt\"{fmt}\" argv{argv} parts{parts}")
    for ix, pt in ipairs(parts):
        arg = select(ix, *argv)[1]
        s += tostr(arg) + pt
    # }
    return s
# }


def _update():
    pass


run(_init, _update, _draw)
