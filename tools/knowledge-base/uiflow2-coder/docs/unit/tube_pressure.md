# Tube Pressure Unit

This is the driver library of Tube Pressure Unit, which is used to control the pressure sensor.

Support the following products:

    Tube Pressure

## MicroPython Example

#### get pressure value

The example shows the pressure value of the tube pressure unit.

```python
import os, sys, io
import M5
from M5 import *
from unit import TubePressureUnit

title0 = None
label2 = None
label0 = None
label1 = None
tubepressure_0 = None

def setup():
    global title0, label2, label0, label1, tubepressure_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "TubePressureUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("label2", 1, 159, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("label0", 1, 73, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 1, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    tubepressure_0 = TubePressureUnit((36, 26))

def loop():
    global title0, label2, label0, label1, tubepressure_0
    M5.update()
    label0.setText(str((str("Pressure:") + str((tubepressure_0.get_pressure())))))
    label1.setText(str((str("ADC 12Bits Value:") + str((tubepressure_0.get_analog_value(12))))))
    label2.setText(str((str("Voltage:") + str((tubepressure_0.get_voltage())))))

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

## **API**

#### TubePressureUnit

## `TubePressureUnit`
Create an TubePressureUnit object.

- Parameter `port` (`tuple`): The port of the tube pressure.

```python
from unit import TubePressureUnit

tube_pressure_0 = TubePressureUnit((32, 26))
```

### `get_pressure`
Getting the pressure value of the tube pressure.

- Returns: pressure value.
- Return type: float

```python
tube_pressure_0.get_pressure()
```

### `get_voltage`
Getting the voltage value of the tube pressure.

- Returns: voltage value.
- Return type: float

```python
tube_pressure_0.get_voltage()
```

### `get_analog_value`
Getting the analog value of the tube pressure.

- Parameter `bits` (`int`): The bits of the analog value.
- Returns: analog value.
- Return type: int

```python
tube_pressure_0.get_analog_value()
```
