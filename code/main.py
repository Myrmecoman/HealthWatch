from init import *
from watch import *
from heartbeat import *
from flappy import *
from notifs import *


App = [watch, heartbeat, notifs, flappy]
App_L = [WATCH, HEART, NOTIFS, FLAPPY]
index = 0
swap_val = 0
push = 0

settime()

# Reset screen
oled.fill(0)
oled.show()

while True:
    oled.fill(0)

    now = utime.gmtime()
    t = ("", "0")[now[3] < 10] + str(now[3]) + ":" + ("", "0")[now[4] < 10] + str(now[4])
    date = DAY[now[6]] + " " + str(now[2]) + " " + MONTH[now[1]] + " " + str(now[0])
    write(5, 5, t, CC, 118, 16, 1, 2)
    write(5, 20, date, CC, 118, 16, 1, 1)

    swap_val = (getVrY(), swap_val)[swap_val != 0]
    if swap_val != 0 and getVrY() == 0:
        index += swap_val
        index %= len(App_L)
        swap_val = 0

    push = (getBMid(), push)[push != 0]
    if push != 0 and getBMid() == 0:
        App[index]()
        push = 0

    for i in range(len(App_L)):
        logo = App_L[i]
        invert = index == i

        for y, row in enumerate(logo):
            for x, c in enumerate(row):
                if invert:
                    c = int(not c)
                oled.pixel(36 + x + i * 15, 42 + y, c)
    oled.show()

uart.close()