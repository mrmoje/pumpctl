from machine import I2C, Pin, Timer
import sh1106_i2c
from utils import tank


# Pindefs
SDA = Pin(5)
SCL = Pin(4)

PUMP = Pin(10, Pin.OUT)
TRIG = Pin(16, Pin.OUT)

top_tank = tank(Pin(0, Pin.OUT), Pin(14, Pin.IN, Pin.PULL_UP), PUMP, TRIG)
bot_tank = tank(Pin(2, Pin.OUT), Pin(12, Pin.IN, Pin.PULL_UP), PUMP, TRIG)

# Function buttons
f1 = Pin(13, Pin.IN, Pin.PULL_UP)
f2 = Pin(15, Pin.IN, Pin.PULL_UP)
f3 = Pin(9, Pin.IN, Pin.PULL_UP)


# Some inits
OLED = sh1106_i2c.Display(
    I2C(-1, sda=SDA, scl=SCL, freq=400000)
)

display_timer = Timer(1)
