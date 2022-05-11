import machine
from pyb import Pin


# screen
screenSda = machine.Pin('A14',)
screenScl = machine.Pin('B3')

# buttons
button1 = Pin('A7', Pin.IN, Pin.PULL_UP)
button2 = Pin('A6', Pin.IN, Pin.PULL_UP)
button3 = Pin('A5', Pin.IN, Pin.PULL_UP)