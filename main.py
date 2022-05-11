import pins
import ssd1306
import machine
from pyb import Pin

# setup clock
now = (2020, 1, 21, 2, 10, 32, 36, 0)
rtc = machine.RTC()
rtc.datetime(now)
lastCall = rtc.datetime()

# setup screen
i2c = machine.SoftI2C(scl=pins.screenScl, sda=pins.screenSda)
screen = ssd1306.SSD1306_I2C(128, 64, i2c)

screen.fill(1)
screen.show()

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

