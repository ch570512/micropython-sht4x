# I2C scan helper for the CYD (ESP32-2432S028R)
# Run this on the board with MicroPico (Upload & Run)
from machine import I2C, Pin

# (i2c_id, sda_pin, scl_pin) — candidate pairs on the CYD
# GPIO 21/22 is the standard CYD I2C. Avoid 25/26/32/33 (touch),
# 34/35/36/39 (input-only), 23/18/5/2/4 (display).
pairs = [
    (0, 27, 22),
    (0, 21, 22),
    (0, 22, 21),
    (0, 16, 17),
    (0, 27, 14),
    (0, 13, 15),
]

for i2c_id, sda_pin, scl_pin in pairs:
    try:
        i2c = I2C(i2c_id, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=100_000)
        devices = i2c.scan()
        if devices:
            print(f"I2C{i2c_id} SDA=GP{sda_pin} SCL=GP{scl_pin} -> {[hex(d) for d in devices]}")
        else:
            print(f"I2C{i2c_id} SDA=GP{sda_pin} SCL=GP{scl_pin} -> nothing found")
    except (OSError, ValueError) as e:
        print(f"I2C{i2c_id} SDA=GP{sda_pin} SCL=GP{scl_pin} -> error: {e}")
