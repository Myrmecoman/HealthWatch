from var import *
from bt import *

import machine, ssd1306, pyb
from pyb import ADC, Pin, Timer
import time, utime

nom = 'hwatch'
UUID_UART = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
UUID_TX = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
UUID_RX = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'

uart = Bleuart(nom, UUID_UART, UUID_TX, UUID_RX)

# LED
r_led = pyb.LED(1)
g_led = pyb.LED(2)
b_led = pyb.LED(3)

# Display
screenVolt = Pin('B3', Pin.OUT)
screenVolt.value(1)
time.sleep(0.05)

i2c = machine.SoftI2C(scl=machine.Pin('A14'), sda=machine.Pin('A13'))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# HeartBeat sensor
spoVolt = Pin('B8', Pin.OUT)
spoGround = Pin('B9', Pin.IN, Pin.PULL_DOWN)
sensorVolt = Pin('A2', Pin.OUT)
sensorInput = Pin('A0', Pin.IN)
HBS = ADC("A0")

# Joystick
Pin(Pin.cpu.A5, mode=Pin.IN)
BUp = ADC("A5")
Pin(Pin.cpu.A6, mode=Pin.IN)
BMid = ADC("A6")
Pin(Pin.cpu.A7, mode=Pin.IN)
BDown = ADC("A7")

base_BUp = BUp.read()
base_BMid  = BMid.read()
base_BDown = BDown.read()


def getBUp():
    val = BUp.read()

    if base_BUp * 0.1 >= val:
        return 1
    else:
        return 0

def getBMid():
    val = BMid.read()

    if base_BMid * 0.1 >= val:
        return 1
    else:
        return 0

def getBDown():
    val = BDown.read()

    if base_BDown * 0.1 >= val:
        return 1
    else:
        return 0

def getVrY():
    if getBUp():
        return 1
    elif getBDown():
        return -1
    else:
        return 0

def write(x, y, text, justify = LT, w = 0, h = 0, margin = 1, scale = 1):
    chars = {
        "0" : b'\x57\x10\x31\x01\x15\x41\x15\x16\x31',
        "1" : b'\x57\x20\x16\x11\x11\x16\x31',
        "2" : b'\x57\x10\x31\x01\x11\x41\x12\x33\x11\x24\x11\x15\x11\x06\x51',
        "3" : b'\x57\x10\x31\x01\x11\x41\x12\x23\x21\x44\x12\x05\x11\x16\x31',
        "4" : b'\x57\x30\x17\x21\x11\x12\x11\x03\x11\x04\x51',
        "5" : b'\x57\x00\x51\x01\x12\x12\x31\x43\x13\x05\x11\x16\x31',
        "6" : b'\x57\x30\x11\x21\x11\x12\x11\x03\x41\x04\x12\x44\x12\x16\x31',
        "7" : b'\x57\x00\x51\x41\x12\x33\x11\x24\x11\x15\x11\x06\x11',
        "8" : b'\x57\x10\x31\x01\x12\x41\x12\x13\x31\x04\x12\x44\x12\x16\x31',
        "9" : b'\x57\x10\x31\x01\x12\x41\x12\x13\x41\x34\x11\x25\x11\x16\x11',
        ":" : b'\x17\x02\x11\x05\x11',
        " " : b'\x47\x00\x00',
        "a" : b'\x47\x12\x21\x33\x14\x14\x21\05\x11\x16\x21',
        "b" : b'\x47\x00\x17\x12\x21\x33\x13\x16\x21',
        "c" : b'\x47\x12\x21\x03\x13\x16\x21\x33\x11\x35\x11',
        "d" : b'\x47\x30\x17\x12\x21\x03\x13\x16\x21',
        "e" : b'\x47\x12\x21\x03\x13\x33\x11\x14\x21\x16\x21',
        "g" : b'\x49\x03\x12\x12\x21\x33\x15\x15\x21\x07\x11\x18\x21',
        "h" : b'\x47\x00\x17\x12\x21\x33\x14',
        "i" : b'\x17\x01\x11\x03\x14',
        "l" : b'\x27\x00\x16\x16\x11',
        "n" : b'\x47\x02\x15\x12\x21\x33\x14',
        "o" : b'\x47\x12\x21\x03\x13\x33\x13\x16\x21',
        "p" : b'\x49\x02\x17\x12\x21\x33\x13\x16\x21',
        "r" : b'\x47\x02\x15\x13\x11\x22\x21',
        "t" : b'\x37\x00\x16\x12\x21\x16\x21',
        "u" : b'\x47\x02\x14\x16\x31\x32\x14',
        "v" : b'\x47\x02\x13\x32\x13\x15\x22',
        "y" : b'\x49\x02\x13\x32\x16\x15\x21\x07\x11\x18\x21',
        "A" : b'\x57\x20\x11\x11\x11\x31\x11\x02\x15\x42\x15\x14\x31',
        "B" : b'\x57\x00\x17\x10\x31\x13\x31\x16\x31\x41\x12\x44\x12',
        "D" : b'\x57\x00\x17\x10\x31\x41\x15\x16\x31',
        "F" : b'\x57\x00\x17\x10\x41\x13\x31',
        "J" : b'\x57\x00\x51\x31\x15\x05\x11\x16\x21',
        "M" : b'\x57\x00\x17\x40\x17\x11\x11\x31\x11\x22\x12',
        "N" : b'\x57\x00\x17\x40\x17\x11\x12\x22\x13\x34\x12',
        "O" : b'\x57\x10\x31\x01\x15\x41\x15\x16\x31',
        "P" : b'\x57\x00\x17\x10\x31\x13\x31\x41\x12',
        "S" : b'\x57\x10\x31\x01\x12\x13\x31\x44\x12\x16\x31',
        "T" : b'\x57\x00\x51\x21\x16',
        "W" : b'\x57\x00\x16\x40\x16\x23\x13\x16\x11\x36\x11'
        }
    tw = 0 #text width
    th = 0 #text height
    ww = w #window width
    wh = h #window height
    xc = x #start x for next character
    yc = y
    for c in text:
        tw += (chars[c][0] >> 4) + margin
        ch = (chars[c][0] & 0x0f) * scale
        if ch > th:
            th = ch
    tw = (tw - margin) * scale
    if tw > ww:
        ww = tw
    if th > wh:
        wh = th
    if justify >> 4 == 0x01:
        xc = x + (ww - tw) // 2
    if justify & 0x0f == 0x01:
        yc = y + (wh - th) // 2
    oled.fill_rect(x, y, ww, wh, 0)
    for c in text:
        cb = memoryview(chars[c])  #char bytearray 
        w = (cb[0] >> 4) * scale   #width
        h = (cb[0] & 0x0f) * scale   #height
        for i in range(1, len(cb), 2):
            px = xc + (cb[i] >> 4) * scale
            py = yc + (cb[i] & 0x0f) * scale
            pw = (cb[i + 1] >> 4) * scale
            ph = (cb[i + 1] & 0x0f) * scale
            oled.fill_rect(px, py, pw, ph, 1)
        xc += w + (margin * scale)
