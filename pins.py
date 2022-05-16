import machine
from pyb import Pin
import time


# screen
screenVolt = Pin('B6', Pin.OUT)
screenVolt.value(1)
time.sleep(0.05)

screenSda = machine.Pin('A8',)
screenScl = machine.Pin('A9')


# pins spo2
spoVolt = Pin('B8', Pin.OUT)
spoGround = Pin('B9', Pin.IN, Pin.PULL_DOWN)

sensorVolt = Pin('A0', Pin.OUT)
sensorVolt.value(1)
time.sleep(0.05)
sensorInput = Pin('A2', Pin.IN, Pin.PULL_DOWN)


# buttons
button1 = Pin('A7', Pin.IN, Pin.PULL_UP)
button2 = Pin('A6', Pin.IN, Pin.PULL_UP)
button3 = Pin('A5', Pin.IN, Pin.PULL_UP)