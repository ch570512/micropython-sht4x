# SHT4X API Reference

Complete reference for `sht4x.py`, a MicroPython driver for the Sensirion
**SHT40, SHT41 and SHT45** temperature and humidity sensors, connected over
I2C.

It is a drop-in driver for use with any `machine.I2C` bus; no other changes
are required. The driver:

- communicates with the sensor at the default I2C address `0x44`,
- reads temperature and relative humidity in a single I2C transaction,
- validates each reading against the sensor's **CRC8 checksum** and raises
  `RuntimeError` if either byte fails the check,
- exposes selectable **measurement precision** and an integrated **heater**
  (three power levels × two on-times) for condensation and self-test use.

The sensor is read through the single `measurements` property, which also
handles the extra wait time required after a heater command.

---

## Module Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `HIGH_PRECISION` | `0` | Measurement command `0xFD` (highest resolution) |
| `MEDIUM_PRECISION` | `1` | Measurement command `0xF6` |
| `LOW_PRECISION` | `2` | Measurement command `0xE0` (fastest) |
| `HEATER200mW` | `0` | Heater power 200 mW |
| `HEATER110mW` | `1` | Heater power 110 mW |
| `HEATER20mW` | `2` | Heater power 20 mW |
| `TEMP_1` | `0` | Heater on-time 1 s (long) |
| `TEMP_0_1` | `1` | Heater on-time 0.1 s (short) |

The precision and heater constants are passed to the corresponding properties
below; you never need to reference the raw command bytes directly.

---

## Class `SHT4X`

### `__init__(i2c, address=0x44)`

Create the driver for a sensor on the given I2C bus.

| Arg | Type | Default | Description |
|-----|------|---------|-------------|
| `i2c` | `machine.I2C` | — | The I2C bus the SHT4X is connected to |
| `address` | int | `0x44` | The I2C device address of the sensor |

```python
from machine import Pin, I2C
import sht4x

# CYD (ESP32-2432S028R): sensor wired to GPIO 27 (SDA) / GPIO 22 (SCL)
i2c = I2C(0, sda=Pin(27), scl=Pin(22), freq=100_000)
sht = sht4x.SHT4X(i2c)

temperature, relative_humidity = sht.measurements
print(f"Temperature: {temperature:.2f}°C")
print(f"Relative Humidity: {relative_humidity:.2f}%")
```

The constructor only stores the bus and address; the sensor is first contacted
when a measurement is taken.

---

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `temperature` | float | Current temperature in °C (performs a measurement) |
| `relative_humidity` | float | Current relative humidity in % rH (performs a measurement) |
| `measurements` | `(float, float)` | Temperature and humidity read in one transaction |
| `temperature_precision` | str (get) / int (set) | Measurement precision mode |
| `heater_power` | str (get) / int (set) | Heater power level |
| `heat_time` | str (get) / int (set) | Heater on-time duration |

#### `temperature` → float

The current temperature in degrees Celsius.

```python
print(f"{sht.temperature:.2f} °C")
```

#### `relative_humidity` → float

The current relative humidity in `% rH`. Values are cropped to the physical
range `0…100 %rH` (the raw sensor reading may otherwise fall slightly outside
this range near the boundaries).

```python
print(f"{sht.relative_humidity:.2f} %")
```

#### `measurements` → `(temperature, relative_humidity)`

Perform one measurement and return temperature and relative humidity together.
This is the most efficient way to read the sensor, since both values come from
a single I2C transaction.

The read is blocking: it sleeps ~0.2 s for the measurement to complete, or
~1.2 s when a 1 s heater command has been issued. Each value is validated
against its CRC8 checksum, and `RuntimeError` is raised if either check fails.

```python
temperature, relative_humidity = sht.measurements
```

#### `temperature_precision` — getter / setter

Select the measurement precision.

| Value | Command | Notes |
|-------|---------|-------|
| `sht4x.HIGH_PRECISION` | `0xFD` | Default; highest resolution |
| `sht4x.MEDIUM_PRECISION` | `0xF6` | Medium resolution |
| `sht4x.LOW_PRECISION` | `0xE0` | Lowest resolution, fastest |

The getter returns a name string such as `"HIGH_PRECISION"`. The setter
accepts one of the precision constants and raises `ValueError` for anything
else.

```python
sht.temperature_precision = sht4x.HIGH_PRECISION
```

#### `heater_power` — getter / setter

Select the heater power level (used together with `heat_time`).

| Value | Power |
|-------|-------|
| `sht4x.HEATER200mW` | 200 mW |
| `sht4x.HEATER110mW` | 110 mW |
| `sht4x.HEATER20mW` | 20 mW (default) |

When a heater command is used, the next `measurements` call enables the
heater, waits for the configured on-time, then performs the measurement; the
heater is switched off automatically afterwards. The maximum on-time is one
second to prevent overheating.

The getter returns a name string such as `"HEATER20mW"`. The setter accepts
one of the heater-power constants and raises `ValueError` for anything else.

```python
sht.heater_power = sht4x.HEATER110mW
```

#### `heat_time` — getter / setter

Select the heater on-time duration (used together with `heater_power`).

| Value | On-time |
|-------|---------|
| `sht4x.TEMP_1` | 1 s (long) |
| `sht4x.TEMP_0_1` | 0.1 s (short, default) |

The getter returns a name string such as `"TEMP_0_1"`. The setter accepts one
of the heat-time constants and raises `ValueError` for anything else.

```python
sht.heat_time = sht4x.TEMP_1
```

---

### Methods

#### `reset()`

Send the soft-reset command (`0x94`) to the sensor and wait 0.1 s for it to
restart. The sensor returns to its default settings (high precision, heater
off).

```python
sht.reset()
```

#### `_crc(buffer)` — static, internal

Compute the CRC8 checksum of a data buffer using the SHT4x polynomial
(`0x31`). Used internally by `measurements` to validate the raw temperature
and humidity bytes; there is normally no need to call it directly.

| Arg | Type | Description |
|-----|------|-------------|
| `buffer` | iterable of int | Byte sequence to checksum |
| **returns** | int | 8-bit CRC value |
