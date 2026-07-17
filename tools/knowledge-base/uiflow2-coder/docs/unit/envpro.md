
# ENVPRO Unit

ENV Pro Unit is an environmental sensor that utilizes the BME688 sensor solution, supporting the measurement of various environmental parameters such as volatile organic compounds (VOCs), indoor air quality (IAQ), temperature, humidity, and atmospheric pressure. It features a compact size, wide operating range, simple communication interface (I2C), excellent performance, and low power consumption, making it suitable for weather stations, indoor environmental monitoring, and air quality detection applications.

Support the following products:

ENVPROUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ENVPROUnit
import time

title0 = None
label0 = None
label1 = None
label2 = None
i2c0 = None
envpro_0 = None
co2_0 = None

def setup():
    global title0, label0, label1, label2, i2c0, envpro_0, co2_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ENVProUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 0, 58, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 0, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 0, 160, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    envpro_0 = ENVPROUnit(i2c0)

def loop():
    global title0, label0, label1, label2, i2c0, envpro_0, co2_0
    M5.update()
    label0.setText(str((str("Pressure:") + str((envpro_0.get_pressure())))))
    label1.setText(str((str("Humidity:") + str((envpro_0.get_humidity())))))
    label2.setText(str((str("Temperature:") + str((envpro_0.get_temperature())))))
    time.sleep(1)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## class ENVPROUnit

## Constructors

### `class ENVPROUnit(i2c, address)`

    Initialize the ENVPROUnit with an I2C object and an optional address.

    - Parameter `i2c`: The I2C interface or PAHUBUnit instance to communicate with the ENV PRO sensor.
    - Parameter `address` (`int`): The I2C address of the ENV PRO sensor. Defaults to 0x77.

## Methods

### `ENVPROUnit.get_over_sampling_rate(env)`

    Retrieve the oversampling rate for the specified environment parameter.

    - Parameter `env`: The environment parameter (TEMPERATURE, PRESSURE, HUMIDITY).

### `ENVPROUnit.set_over_sampling_rate(env, rate)`

    Set the oversampling rate for the specified environment parameter.

    - Parameter `env`: The environment parameter (TEMPERATURE, PRESSURE, HUMIDITY).
    - Parameter `rate`: The oversampling rate to be set.

### `ENVPROUnit.get_iir_filter_coefficient()`

    Retrieve the IIR filter coefficient.

### `ENVPROUnit.set_iir_filter_coefficient(value)`

    Set the IIR filter coefficient.

    - Parameter `value`: The IIR filter coefficient to be set.

### `ENVPROUnit.get_temperature()`

    Retrieve the measured temperature.

### `ENVPROUnit.get_humidity()`

    Retrieve the measured humidity.

### `ENVPROUnit.get_pressure()`

    Retrieve the measured pressure.

### `ENVPROUnit.get_gas_resistance()`

    Retrieve the measured gas resistance.

### `ENVPROUnit.get_altitude()`

    Retrieve the calculated altitude based on pressure readings.

    `Note`: Altitude is calculated based on the difference between barometric pressure and sea level pressure

## Constants

### `ENVPROUnit.TEMPERATURE`
### `ENVPROUnit.PRESSURE`
### `ENVPROUnit.HUMIDITY`
