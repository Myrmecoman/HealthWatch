from init import *
from var import *
import random

RISE_THRESHOLD = 4
MAX_READS = 4

beatval = [0, 1, 2, 1, 0, 0, -1, 10, -3, 0, 0, 0, 1, 2, 0, 1, 0]

def refresh(i):
    oled.scroll(-1, 0)
    oled.scroll(-1, 0)

    # Reset top screen
    oled.fill_rect(0, 0, 128, 16, 0) 
    
    # Draw heart on beat
    if i >= 7 and i <= 10:
        for y, row in enumerate(HEART):
            for x, c in enumerate(row):
                oled.pixel(x, y, c)

    # Show bpm
    oled.text("%d bpm" % 56, 14, 1)
    oled.line(124, 48 - 2 * beatval[i - 1], 126, 48 - 2 * beatval[i], 1)

    oled.show()


def heartbeat():
    # Reset screen
    oled.fill(0)
    oled.show()

    # On
    spoVolt.value(1)
    sensorVolt.value(1)
    time.sleep(0.05)

    # Init default values
    swap = 0
    i = 0
    y = 0

    # main looop
    while True:
        swap = (getVrY(), swap)[swap != 0]
        if swap != 0 and getVrY() == 0:
            # Off
            spoVolt.value(0)
            sensorVolt.value(0)
            time.sleep(0.05)
            return swap

        refresh(i)
        i = (i + 1) % len(beatval)

        time.sleep(0.02)
