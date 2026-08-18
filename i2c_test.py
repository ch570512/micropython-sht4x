# I2C read test for SHT4x on CYD - run this file (not a REPL paste)
import time

from machine import I2C, Pin

ADDR = 0x44

# 1) 400 kHz (the default), plain write + read
i2c = I2C(0, sda=Pin(27), scl=Pin(22))
try:
    i2c.writeto(ADDR, b"\xFD")
    time.sleep(0.2)
    b = bytearray(6)
    i2c.readfrom_into(ADDR, b)
    print("400k  stop=True  OK :", b.hex())
except OSError as e:
    print("400k  stop=True  FAIL:", e)

# 2) 100 kHz, plain write + read
i2c = I2C(0, sda=Pin(27), scl=Pin(22), freq=100_000)
try:
    i2c.writeto(ADDR, b"\xFD")
    time.sleep(0.2)
    b = bytearray(6)
    i2c.readfrom_into(ADDR, b)
    print("100k  stop=True  OK :", b.hex())
except OSError as e:
    print("100k  stop=True  FAIL:", e)

# 3) 100 kHz, no-stop write (driver style, stop=False)
i2c = I2C(0, sda=Pin(27), scl=Pin(22), freq=100_000)
try:
    i2c.writeto(ADDR, b"\xFD", False)
    time.sleep(0.2)
    b = bytearray(6)
    i2c.readfrom_into(ADDR, b)
    print("100k  stop=False OK :", b.hex())
except OSError as e:
    print("100k  stop=False FAIL:", e)
