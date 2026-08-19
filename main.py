# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time

from machine import I2C, Pin

import sht4x

# CYD (ESP32-2432S028R): sensor wired to GPIO 27 (SDA) / GPIO 22 (SCL)
i2c = I2C(0, sda=Pin(27), scl=Pin(22), freq=100_000)
sht = sht4x.SHT4X(i2c)

while True:
    temperature, relative_humidity = sht.measurements
    print(f"Temperature: {temperature:.2f}°C")
    print(f"Relative Humidity: {relative_humidity:.2f}%")
    print()
    time.sleep(0.5)
