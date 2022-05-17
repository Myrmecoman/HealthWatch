import pins
import ssd1306
import machine
import time
from pyb import Pin
from pyb import ADC


# setup screen
i2c = machine.SoftI2C(scl=pins.screenScl, sda=pins.screenSda)
screen = ssd1306.SSD1306_I2C(128, 64, i2c)

# setup clock
now = (2020, 1, 21, 2, 10, 32, 36, 0)
rtc = machine.RTC()
rtc.datetime(now)
lastCall = rtc.datetime()

# buttons codes
def rtcToMs(rtcTime):
    return rtcTime[3] * 86400000 + rtcTime[4] * 3600000 + rtcTime[5] * 60000 + rtcTime[6] * 1000 + rtcTime[7] // 1000

def callback1(p):
    global lastCall
    currentTime = rtcToMs(rtc.datetime())
    if (currentTime - rtcToMs(lastCall) > 200):
        lastCall = rtc.datetime()
        print('button 1 pushed')

def callback2(p):
    global lastCall
    currentTime = rtcToMs(rtc.datetime())
    if (currentTime - rtcToMs(lastCall) > 200):
        lastCall = rtc.datetime()
        print('button 2 pushed')

def callback3(p):
    global lastCall
    currentTime = rtcToMs(rtc.datetime())
    if (currentTime - rtcToMs(lastCall) > 200):
        lastCall = rtc.datetime()
        print('button 3 pushed')

def initButtonCallback():
    p1 = pins.button1
    p2 = pins.button2
    p3 = pins.button3
    p1.irq(trigger=Pin.IRQ_FALLING, handler=callback1)
    p2.irq(trigger=Pin.IRQ_FALLING, handler=callback2)
    p3.irq(trigger=Pin.IRQ_FALLING, handler=callback3)

initButtonCallback()

# graph utility code ---------------
values = []

def AddValue(val):
    val = -val + 4095
    if len(values) > 2:
        val = (val + values[len(values) - 1] + values[len(values) - 2])/3
        values.append(val)
    else:
        values.append(val)
    if len(values) > 120:
        del values[0]

def DisplayValues():
    screen.fill(0)
    min = 1000000
    max = 0

    for i in range(len(values)):
        if values[i] > max:
            max = values[i]
        if values[i] < min:
            min = values[i]

    maxSpread = max - min
    if maxSpread == 0:
        return

    x = 60 - len(values)/2
    for i in range(len(values) - 1):
        y0 = ((values[i] - min)/maxSpread) * 60
        y1 = ((values[i + 1] - min)/maxSpread) * 60
        x = x + 1
        screen.line(int(x), int(y0), int(x) + 1, int(y1), 1)
    
    screen.show()
# end of graph utility code ---------------


loopBeforeDisplay = 3
loopNb = 0
pins.spoVolt.value(1)
time.sleep(0.05)
while True:
    AddValue(ADC('A2').read())
    if loopNb >= loopBeforeDisplay - 1:
        DisplayValues()
    loopNb += 1
    loopNb = loopNb % loopBeforeDisplay
