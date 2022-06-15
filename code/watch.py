from init import *
from var import *

def printTime(now, last):
    oled.fill(0)
    h = ("", "0")[now[3] < 10] + str(now[3])
    sep = (":", " ")[last[5] != now[5]]
    m = ("", "0")[now[4] < 10] + str(now[4])
    s = ("", "0")[now[5] < 10] + str(now[5])
    date = DAY[now[6]] + " " + str(now[2]) + " " + MONTH[now[1]] + " " + str(now[0])

    write(5, 5, h, CC, 48, 32, 1, 4)
    write(53, 5, sep, CC, 9, 32, 1, 3)
    write(62, 5, m, CC, 48, 32, 1, 4)
    write(110, 5, s, CC, 13, 32, 1, 1)
    write(0, 37, date, CC, 128, 32, 1, 1)
    
def fh(val):
    if val < 0:
        return 23
    elif val >= 24:
        return 0
    return val

def fms(val):
    if val < 0:
        return 59
    elif val >= 60:
        return 0
    return val

def fd(val):
    if val < 0:
        return 6
    elif val >= 7:
        return 0
    return val

def fdn(val):
    if val < 1:
        return 31
    elif val >= 32:
        return 1
    return val

def fm(val):
    if val < 1:
        return 12
    elif val >= 13:
        return 1
    return val

def fy(val):
    if val < 0:
        return 0
    return val

def settime():
    now = utime.gmtime()
    printTime(now, now)
    oled.show()

    val = [now[3], now[4], now[5], now[6], now[2], now[1], now[0]]
    format_val = [fh, fms, fms, fd, fdn, fm, fy]
    index = 0

    swap_val = 0
    swap = 0

    while index < 7:
        swap_val = (getBMid(), swap_val)[swap_val != 0]
        if swap_val != 0 and getBMid() == 0:
            index += 1
            swap_val = 0

        swap = (getVrY(), swap)[swap != 0]
        if swap != 0 and getVrY() == 0:
            val[index] = format_val[index](val[index] + swap)
            swap = 0

        new = (val[6], val[5], val[4], val[0], val[1], val[2], val[3], 0)
        machine.RTC().datetime((new[0], new[1], new[2], new[6] + 1, new[3], new[4], new[5], 0))
        printTime(new, new)
        oled.show()

def watch():    
    last = utime.gmtime()
    swap = 0
    push = 0

    # main looop
    while True:
        swap = (getVrY(), swap)[swap != 0]
        if swap != 0 and getVrY() == 0:
            return swap
        
        push = (getBMid(), push)[push != 0]
        if push != 0 and getBMid() == 0:
            settime()
            push = 0

        now = utime.gmtime()
        printTime(now, last)

        oled.show()
        last = now

