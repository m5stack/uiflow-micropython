# SHT4X

SHT4X measures temperature and relative humidity.

Supported controllers:

     Controller         SHT4X           |
     M5PaperColor       S             |

## MicroPython Example

#### get temperature and humidity

This example reads temperature and relative humidity from the onboard SHT4X
sensor on M5PaperColor.

```python
import os, sys, io
import M5
from M5 import *
from hardware import SHT4X
import time

sht4x = None

def setup():
    global sht4x

    M5.begin({"clear_display": False})
    Widgets.setRotation(1)

    M5.Lcd.setEpdMode(M5.Lcd.EPDMode.EPD_FASTEST)
    sht4x = SHT4X()

def loop():
    global sht4x
    M5.update()
    print((str("hum:") + str((sht4x.get_humidity()))))
    print((str("temp:") + str((sht4x.get_temperature()))))
    time.sleep(1)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            print(e)
        except ImportError:
            print("please update to latest firmware")
```

## **API**

#### SHT4X

## `SHT4X`
Create an onboard SHT4X sensor object.

```python
from hardware import SHT4X

sht4x = SHT4X()
```

## `SHT4x`
Create an SHT4x temperature and humidity sensor object.

- Parameter `i2c` (`I2C`): The I2C bus object connected to the sensor.
- Parameter `address` (`int`): The I2C address of the sensor. Default is `0x44`.

```python
from hardware import I2C, Pin
from driver.sht4x import SHT4x

i2c0 = I2C(0, scl=Pin(2), sda=Pin(3), freq=100000)
sht4x = SHT4x(i2c0)
```

### `serial_number`
The unique 32-bit serial number of the sensor.

- Returns: The sensor serial number.
- Return type: int

```python
sht4x.serial_number
```

### `reset`
Perform a soft reset of the sensor.

```python
sht4x.reset()
```

### `mode`
The current sensor reading mode.

The mode selects both heater behavior and measurement precision. Use
one of the values from `Mode`, such as
`Mode.NOHEAT_HIGHPRECISION` or `Mode.HIGHHEAT_100MS`.

- Returns: The current measurement mode command.
- Return type: int

```python
from driver.sht4x import Mode

sht4x.mode = Mode.NOHEAT_HIGHPRECISION
sht4x.mode
```

### `mode`
Set the sensor reading mode.

- Parameter `new_mode` (`int`): A mode value from `Mode`.

### `relative_humidity`
The current relative humidity in percent RH.

- Returns: The relative humidity, constrained to `0` through `100`.
- Return type: float

```python
sht4x.relative_humidity
```

### `get_humidity`
Get the current relative humidity in percent RH.

- Returns: The relative humidity, constrained to `0` through `100`.
- Return type: float

```python
sht4x.get_humidity()
```

### `temperature`
The current temperature in degrees Celsius.

- Returns: The temperature in degrees Celsius.
- Return type: float

```python
sht4x.temperature
```

### `get_temperature`
Get the current temperature in degrees Celsius.

- Returns: The temperature in degrees Celsius.
- Return type: float

```python
sht4x.get_temperature()
```

### `measure`
Measure temperature and relative humidity simultaneously.

- Returns: A tuple containing `(temperature, relative_humidity)`.
- Return type: tuple[float, float]

```python
temperature, humidity = sht4x.measure()
```
