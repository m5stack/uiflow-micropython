# DAC Unit

The `Dac2` class interfaces with a GP8413 15-bit Digital to Analog Converter (DAC), capable of converting digital signals into two channels of analog voltage output, ranging from 0-5V and 0-10V.

Support the following products:

    DACUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import DACUnit

label0 = None
label1 = None
label2 = None
label3 = None
i2c0 = None
dac_0 = None

v = None

def btnA_wasClicked_event(state):  # noqa: N802
    global label0, label1, label2, label3, i2c0, dac_0, v
    if v >= 0.1:
        v = v - 0.1
    dac_0.set_voltage(v)

def btnB_wasClicked_event(state):  # noqa: N802
    global label0, label1, label2, label3, i2c0, dac_0, v
    if v < 3.3:
        v = v + 0.1
    dac_0.set_voltage(v)

def btnC_wasClicked_event(state):  # noqa: N802
    global label0, label1, label2, label3, i2c0, dac_0, v
    v = 0
    dac_0.set_voltage(v)

def setup():
    global label0, label1, label2, label3, i2c0, dac_0, v

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 133, 110, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("-", 60, 210, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label2 = Widgets.Label("+", 143, 210, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label3 = Widgets.Label("reset", 214, 210, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnB_wasClicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnC_wasClicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    dac_0 = DACUnit(i2c0)
    v = 0

def loop():
    global label0, label1, label2, label3, i2c0, dac_0, v
    M5.update()
    label0.setText(str(dac_0.get_voltage()))

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

## class DACUnit

## Constructors

### `class DACUnit(i2c: I2C, address: int = 0x60, vdd: float = 5.0, vout: float = 3.3)`

    Create an DACUnit object.

    - Parameter `i2c`: I2C object
    - Parameter `address`: I2C address
    - Parameter `vdd`: Supply voltage
    - Parameter `vout`: Output voltage

## Methods

### `DACUnit.get_value() -> int`

    Get the current value of the DAC.

    - Returns: The DAC value as a 16-bit unsigned value.

### `DACUnit.get_voltage() -> float`

    Get the current voltage of the DAC.

    - Returns: The DAC voltage as a float.

### `DACUnit.set_value(value: int) -> None`

    Set the value of the DAC.

    - Parameter `value`: The DAC value as a 16-bit unsigned value.

### `DACUnit.set_voltage(voltage: float) -> None`

    Set the voltage of the DAC.

    - Parameter `voltage`: The DAC voltage as a float. The voltage must be between 0 and 3.3V.

### `DACUnit.get_raw_value() -> int`

    Get the raw value of the DAC.

    - Returns: The raw DAC value as a 12-bit unsigned value.

### `DACUnit.set_raw_value(value: int) -> None`

    Set the raw value of the DAC.

    - Parameter `value`: The raw DAC value as a 12-bit unsigned value.

### `DACUnit.get_normalized_value() -> float`

    Get the normalized value of the DAC.

    - Returns: The normalized DAC value as a float.

### `DACUnit.set_normalized_value(value: float) -> None`

    Set the normalized value of the DAC.

    - Parameter `value`: The normalized DAC value as a float.

### `DACUnit.save_to_eeprom() -> None`

    Save the current DAC value to EEPROM.
