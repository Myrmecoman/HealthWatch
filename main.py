import ssd1306
import machine
import pins


i2c = machine.SoftI2C(scl=pins.screenScl, sda=pins.screenSda)
screen = ssd1306.SSD1306_I2C(128, 64, i2c)

screen.fill(1)