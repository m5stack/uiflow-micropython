# ACSSR Unit

Support the following products:

    ACSSR Unit

Micropython I2C Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ACSSRUnit

label0 = None
rect0 = None
label1 = None
title0 = None
label3 = None
i2c0 = None
acssr_0 = None

touch_x = None
touch_y = None
x = None
y = None
w = None
h = None
state = None
ret = None

# Describe this function...
def is_touch(touch_x, touch_y, x, y, w, h):
    global state, ret, label0, rect0, label1, title0, label3, i2c0, acssr_0
    ret = False
    if touch_x >= x and touch_x <= x + w:
        if touch_y >= y and touch_y <= y + h:
            ret = True
    return ret

# Describe this function...
def display_ui(state):
    global touch_x, touch_y, x, y, w, h, ret, label0, rect0, label1, title0, label3, i2c0, acssr_0
    if state:
        rect0.setColor(color=0x00FF00, fill_c=0x00FF00)
        label3.setColor(0xFFFFFF, 0x00FF00)
        label3.setText(str("On"))
        acssr_0.fill_color(0x00FF00)
    else:
        rect0.setColor(color=0xFF0000, fill_c=0xFF0000)
        label3.setColor(0xFFFFFF, 0xFF0000)
        label3.setText(str("Off"))
        acssr_0.fill_color(0xFF0000)

def setup():
    global \
        label0, \
        rect0, \
        label1, \
        title0, \
        label3, \
        i2c0, \
        acssr_0, \
        ret, \
        state, \
        touch_x, \
        x, \
        w, \
        touch_y, \
        y, \
        h

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 188, 30, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    rect0 = Widgets.Rectangle(130, 105, 60, 30, 0x00FF00, 0x00FF00)
    label1 = Widgets.Label(
        "Firmware Version:", 8, 30, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    title0 = Widgets.Title("ACSSR Unit", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("On", 147, 111, 1.0, 0xFFFFFF, 0x00FF00, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    print(i2c0.scan())
    acssr_0 = ACSSRUnit(i2c0, 0x50)
    label0.setText(str(acssr_0.get_firmware_version()))
    state = acssr_0.value()
    display_ui(state)

def loop():
    global \
        label0, \
        rect0, \
        label1, \
        title0, \
        label3, \
        i2c0, \
        acssr_0, \
        ret, \
        state, \
        touch_x, \
        x, \
        w, \
        touch_y, \
        y, \
        h
    M5.update()
    if M5.Touch.getCount():
        if is_touch(
            (M5.Touch.getTouchPointRaw())[0], (M5.Touch.getTouchPointRaw())[1], 130, 105, 60, 30
        ):
            state = not state
            acssr_0(state)
            display_ui(state)

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

Micropython Modbus Example:

    Connect an ISO485 Unit to CoreS3 Port C (RX=18, TX=17) and configure the
    ACSSR for Modbus mode, 115200 baud, 8N1, device address `0x04`.

```python
import os, sys, io
import M5
from M5 import *
from unit import ACSSRUnit, ISO485Unit
import modbus

label0 = None
rect0 = None
label1 = None
title0 = None
label3 = None
iso485_0 = None
modbusrtumaster_0 = None
acssr_0 = None

touch_x = None
touch_y = None
x = None
y = None
w = None
h = None
state = None
ret = None

# Describe this function...
def is_touch(touch_x, touch_y, x, y, w, h):
    global state, ret, label0, rect0, label1, title0, label3, iso485_0, acssr_0
    ret = False
    if touch_x >= x and touch_x <= x + w:
        if touch_y >= y and touch_y <= y + h:
            ret = True
    return ret

# Describe this function...
def display_ui(state):
    global \
        touch_x, \
        touch_y, \
        x, \
        y, \
        w, \
        h, \
        ret, \
        label0, \
        rect0, \
        label1, \
        title0, \
        label3, \
        iso485_0, \
        acssr_0
    if state:
        rect0.setColor(color=0x00FF00, fill_c=0x00FF00)
        label3.setColor(0xFFFFFF, 0x00FF00)
        label3.setText(str("On"))
        acssr_0.fill_color(0x00FF00)
    else:
        rect0.setColor(color=0xFF0000, fill_c=0xFF0000)
        label3.setColor(0xFFFFFF, 0xFF0000)
        label3.setText(str("Off"))
        acssr_0.fill_color(0xFF0000)

def setup():
    global modbusrtumaster_0
    global \
        label0, \
        rect0, \
        label1, \
        title0, \
        label3, \
        iso485_0, \
        acssr_0, \
        ret, \
        state, \
        touch_x, \
        x, \
        w, \
        touch_y, \
        y, \
        h

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 188, 30, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    rect0 = Widgets.Rectangle(130, 105, 60, 30, 0x00FF00, 0x00FF00)
    label1 = Widgets.Label(
        "Firmware Version:", 8, 30, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    title0 = Widgets.Title("ACSSR Modbus", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("On", 147, 111, 1.0, 0xFFFFFF, 0x00FF00, Widgets.FONTS.DejaVu18)

    # ISO485 Unit on CoreS3 Port C: RX=18, TX=17.
    # Configure the ACSSR hardware for Modbus mode before running.
    iso485_0 = ISO485Unit(2, port=(18, 17))
    iso485_0.init(baudrate=115200, data_bits=8, stop_bits=1, parity=None)
    modbusrtumaster_0 = modbus.ModbusRTUMaster(uart=iso485_0)
    acssr_0 = ACSSRUnit(modbusrtumaster_0, address=0x04)
    label0.setText(str(acssr_0.get_firmware_version()))
    state = acssr_0.value()
    display_ui(state)

def loop():
    global \
        label0, \
        rect0, \
        label1, \
        title0, \
        label3, \
        iso485_0, \
        acssr_0, \
        ret, \
        state, \
        touch_x, \
        x, \
        w, \
        touch_y, \
        y, \
        h
    M5.update()
    if M5.Touch.getCount():
        if is_touch(
            (M5.Touch.getTouchPointRaw())[0], (M5.Touch.getTouchPointRaw())[1], 130, 105, 60, 30
        ):
            state = not state
            acssr_0(state)
            display_ui(state)

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

## class ACSSRUnit

## Constructors

### `class ACSSRUnit(bus, address=0x50)`

    Factory returning the driver selected by the bus object. It does not
    change the ACSSR hardware's communication mode.

    - Parameter `bus`: A `machine.I2C` instance, or a configured Modbus master
        providing `read_coils` and the register/coil operations used below.
    - Parameter `address` (`int`): Device address. The factory default is `0x50` in
        both modes. For a Modbus device at its default address, explicitly
        pass `address=0x04`.
    - Returns: `unit.acssr.ACSSRI2CUnit` for `machine.I2C`;
        `unit.acssr.ACSSRModbusUnit` for a Modbus master.

    The implementation class `ACSSRModbusUnit` has a default address of
    `0x04`, but the factory always forwards its own `address` argument.
    Selecting a bus does not select that implementation default.

```python
from unit import ACSSRUnit, ISO485Unit
from modbus import ModbusRTUMaster

# I2C: use the configured I2C bus.
acssr_i2c = ACSSRUnit(i2c0, address=0x50)

# Modbus: CoreS3 Port C, ISO485 Unit, ACSSR in Modbus mode.
rs485 = ISO485Unit(2, port=(18, 17))
rs485.init(baudrate=115200, data_bits=8, stop_bits=1, parity=None)
master = ModbusRTUMaster(uart=rs485)
acssr_modbus = ACSSRUnit(master, address=0x04)
```
    Use methods on the returned instance, such as `acssr_modbus.value()`.
    The factory class itself does not define the instance methods below.

## Methods

`ACSSRUnit` is a factory: it returns an `ACSSRI2CUnit` for an I2C bus or an
`ACSSRModbusUnit` for a Modbus bus. The methods below belong to the returned
object and are available in both modes.

### `ACSSRUnit.on() -> None`

    Turn on the relay.

### `ACSSRUnit.off() -> None`

    Turn off the relay.

### `ACSSRUnit.__call__([x])`

    Turn on the relay if x is True, otherwise turn off the relay.

    - Parameter `x`: True or False.

### `ACSSRUnit.value([x])`

    Turn on the relay if x is True, otherwise turn off the relay.

    - Parameter `x`: True or False.

### `ACSSRUnit.fill_color(rgb: int = 0) -> None`

    Set the color of the LED.

    - Parameter `rgb`: RGB color value. Default is 0.

### `ACSSRUnit.get_firmware_version() -> int`

    Get the firmware version of the unit.

    - Returns: Firmware version.

### `ACSSRUnit.set_address(new_address: int) -> None`

    Set the I2C address of the unit.

    - Parameter `new_address`: New I2C address. The range is 0x01-0x7f.
