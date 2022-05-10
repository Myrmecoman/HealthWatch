from pyb import Pin


screenSda = Pin('A8')
screenScl = Pin('A9')
screenVoltage = Pin('B7', Pin.OUT)
screenVoltage.value(1)                          # send current
screenGround = Pin('B6', Pin.IN, Pin.PULL_DOWN) # pull current