# Angle Unit

The following products are supported:

    Angle

Micropython Example:
```python
import M5
from M5 import *
from unit import *

M5.begin()

angle_0 = Angle((8,9))

while True:
    print(angle_0.get_voltage())
    print(angle_0.get_value())
```

## class Angle

## Constructors

### `class Angle(port)`

    Create an Angle object.

    parameter is:
        - `port` is the pins number of the port

## Methods

### `Angle.get_value()`

    This method allows reading the Angle's rotation value and returning an integer value. The range is 0-65535.

### `Angle.get_voltage()`

    This method allows reading the voltage value of Angle, and the return value is a floating point value.
