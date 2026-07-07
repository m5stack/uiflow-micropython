# Unit Chain Bus

<!-- .. include:: ../refs/chain.unit_bus.ref -->

BusChainUnit is the helper class for Bus devices on the Chain bus.
It provides methods to configure GPIO pins (input, output, external interrupt), read ADC values, and communicate with I2C devices.
The class supports multiple work modes including GPIO output, GPIO input, external interrupt, ADC, and I2C.

Support the following products:

    |Unit Chain Bus|

## UiFlow2 Example

#### GPIO control

Open the |m5basic_unit_chain_bus_gpio_example.m5f2| project in UiFlow2.

This example demonstrates how to configure and use GPIO pins with the Unit Chain Bus module.
The example configures GPIO1 as input mode with pull-up, and GPIO2 as output mode with push-pull configuration.
It continuously reads GPIO1 input value every 200ms and displays the state (HIGH/LOW) on screen.
GPIO2 output level toggles every 1 second (every 5 cycles) between HIGH and LOW, demonstrating output control functionality.

UiFlow2 Code Block:

Example output:

    None

#### ADC reading

Open the |m5basic_unit_chain_bus_adc_example.m5f2| project in UiFlow2.

This example demonstrates how to read ADC values from the Unit Chain Bus module and use them to control RGB brightness.

UiFlow2 Code Block:

Example output:

    None

#### I2C device communication

Open the |m5basic_unit_chain_bus_i2c_dlight_example.m5f2| project in UiFlow2.

This example demonstrates how to use the Unit Chain Bus module to communicate with I2C devices. The example shows how to configure the bus for I2C mode and use it with I2C devices like the DLight sensor.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### GPIO control

This example demonstrates how to configure and use GPIO pins with the Unit Chain Bus module.
The example configures GPIO1 as input mode with pull-up, and GPIO2 as output mode with push-pull configuration.
It continuously reads GPIO1 input value every 200ms and displays the state (HIGH/LOW) on screen.
GPIO2 output level toggles every 1 second (every 5 cycles) between HIGH and LOW, demonstrating output control functionality.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import BusChainUnit
import time

title = None
label_gpio1 = None
label_tip1 = None
label_tip2 = None
label_gpio2 = None
bus2 = None
unit_chain_bus_0 = None
last_time = None
gpio1_value = None
cnt = None
gpio2_value = None

def setup():
    global \
        title, \
        label_gpio1, \
        label_tip1, \
        label_tip2, \
        label_gpio2, \
        bus2, \
        unit_chain_bus_0, \
        last_time, \
        gpio1_value, \
        cnt, \
        gpio2_value

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title = Widgets.Title(
        "Unit Chain Bus Example: GPIO", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label_gpio1 = Widgets.Label(
        "GPIO1 Value: --", 10, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_tip1 = Widgets.Label(
        "Unit Chain Bus GPIO1: Input", 10, 55, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_tip2 = Widgets.Label(
        "Unit Chain Bus GPIO2: Output", 10, 136, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_gpio2 = Widgets.Label(
        "GPIO2 Value: --", 10, 165, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    bus2 = ChainBus(2, tx=21, rx=22)
    unit_chain_bus_0 = BusChainUnit(bus2, 1)
    unit_chain_bus_0.set_gpio_input(1, BusChainUnit.GPIO_PULL_UP)
    unit_chain_bus_0.set_gpio_output(2, BusChainUnit.GPIO_MODE_PUSHPULL, BusChainUnit.GPIO_PULL_UP)
    if (unit_chain_bus_0.get_work_mode(1)) == (BusChainUnit.WORK_MODE_GPIO_INPUT):
        print("set gpio1 as gpio input success")
    else:
        print("set gpio1 as gpio input failed")
    if (unit_chain_bus_0.get_work_mode(2)) == (BusChainUnit.WORK_MODE_GPIO_OUTPUT):
        print("set gpio2 as gpio output success")
    else:
        print("set gpio2 as gpio output failed")
    unit_chain_bus_0.set_rgb_color(0x000099)

def loop():
    global \
        title, \
        label_gpio1, \
        label_tip1, \
        label_tip2, \
        label_gpio2, \
        bus2, \
        unit_chain_bus_0, \
        last_time, \
        gpio1_value, \
        cnt, \
        gpio2_value
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        gpio1_value = unit_chain_bus_0.get_gpio_input_value(1)
        if gpio1_value:
            label_gpio1.setText(str("GPIO1 Value:  HIGH"))
        else:
            label_gpio1.setText(str("GPIO1 Value:  LOW"))
        cnt = (cnt if isinstance(cnt, (int, float)) else 0) + 1
        if cnt >= 5:
            cnt = 0
            gpio2_value = not gpio2_value
            if gpio2_value:
                unit_chain_bus_0.set_gpio_output_value(2, 1)
                label_gpio2.setText(str("GPIO2 Value:  HIGH"))
            else:
                unit_chain_bus_0.set_gpio_output_value(2, 0)
                label_gpio2.setText(str("GPIO2 Value:  LOW"))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

#### ADC reading

This example demonstrates how to read ADC values from the Unit Chain Bus module and use them to control RGB brightness.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import BusChainUnit
import time
import m5utils

title = None
label_adc = None
label_tip = None
bus2 = None
unit_chain_bus_0 = None
last_time = None
adc_value = None

def setup():
    global title, label_adc, label_tip, bus2, unit_chain_bus_0, last_time, adc_value

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title = Widgets.Title(
        "Unit Chain Bus Example: ADC", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label_adc = Widgets.Label(
        "ADC Value: --", 10, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_tip = Widgets.Label(
        "Unit Chain Bus GPIO1: ADC", 10, 55, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    bus2 = ChainBus(2, tx=21, rx=22)
    unit_chain_bus_0 = BusChainUnit(bus2, 1)
    unit_chain_bus_0.set_adc(1)
    if (unit_chain_bus_0.get_work_mode(1)) == (BusChainUnit.WORK_MODE_ADC):
        print("set gpio1 as adc input success")
    else:
        print("set gpio1 as adc input failed")
    unit_chain_bus_0.set_rgb_color(0x000099)

def loop():
    global title, label_adc, label_tip, bus2, unit_chain_bus_0, last_time, adc_value
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        adc_value = unit_chain_bus_0.get_adc_input(1)
        label_adc.setText(str((str("ADC Value: ") + str(adc_value))))
        print((str("ADC Value: ") + str(adc_value)))
        unit_chain_bus_0.set_rgb_brightness(
            int(m5utils.remap(adc_value, 0, 4096, 0, 100)), save=False
        )

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

#### I2C device communication

This example demonstrates how to use the Unit Chain Bus module to communicate with I2C devices. The example shows how to configure the bus for I2C mode and use it with I2C devices like the DLight sensor.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from chain import ChainBus
from chain import BusChainUnit
import time
from unit import DLightUnit

title = None
label_brightness = None
label_mode = None
i2c0 = None
bus2 = None
dlight_0 = None
unit_chain_bus_0 = None
last_time = None
brightness = None

def setup():
    global \
        title, \
        label_brightness, \
        label_mode, \
        i2c0, \
        bus2, \
        dlight_0, \
        unit_chain_bus_0, \
        last_time, \
        brightness

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title = Widgets.Title(
        "Unit Chain Bus Example: I2C", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label_brightness = Widgets.Label(
        "Brightness: -- lux", 10, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_mode = Widgets.Label(
        "Unit Chain Bus GPIO1&2: I2C", 10, 54, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    bus2 = ChainBus(2, tx=21, rx=22)
    unit_chain_bus_0 = BusChainUnit(bus2, 1)
    unit_chain_bus_0.set_i2c(BusChainUnit.I2C_SPEED_100K)
    dlight_0 = DLightUnit(unit_chain_bus_0)

def loop():
    global \
        title, \
        label_brightness, \
        label_mode, \
        i2c0, \
        bus2, \
        dlight_0, \
        unit_chain_bus_0, \
        last_time, \
        brightness
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 500:
        last_time = time.ticks_ms()
        brightness = int(dlight_0.get_lux())
        label_brightness.setText(str((str("Brightness: ") + str((str(brightness) + str(" lux"))))))
        print((str("Brightness: ") + str((str(brightness) + str(" lux")))))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

## **API**

#### BusChainUnit

## BusChainUnit
Bus Chain Unit class for interacting with Bus devices over Chain bus.

:param ChainBus bus: The Chain bus instance.
:param int device_id: The device ID of the Bus device on the Chain bus.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from chain import ChainBus
        from chain import BusChainUnit

        chainbus_0 = ChainBus(2, 32, 33, verbose=True)
        bus_chain_unit_0 = BusChainUnit(chainbus_0, 1)

### `get_work_mode`
Get the Unit ChainBus work mode.

Returns the work mode of the specified GPIO pin.

Work mode values:
    - :attr:`BusChainUnit.WORK_MODE_UNCONFIGURED`
    - :attr:`BusChainUnit.WORK_MODE_GPIO_OUTPUT`
    - :attr:`BusChainUnit.WORK_MODE_GPIO_INPUT`
    - :attr:`BusChainUnit.WORK_MODE_EXIT`
    - :attr:`BusChainUnit.WORK_MODE_ADC`
    - :attr:`BusChainUnit.WORK_MODE_I2C`

:param int gpio: GPIO number (1 or 2).
:return: Work mode value, or None if failed.
:rtype: int | None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        mode = unit_chain_bus.get_work_mode(1)
        if mode == BusChainUnit.WORK_MODE_GPIO_OUTPUT:
            print("GPIO1 is configured as output")

### `set_gpio_output`
Set pin as output.

:param int gpio: GPIO number (1 or 2).
:param int mode: Output mode. Use :attr:`BusChainUnit.GPIO_MODE_PUSHPULL` (0) or :attr:`BusChainUnit.GPIO_MODE_OPENDRAIN` (1).
:param int pull: Pull-up/down configuration. Use :attr:`BusChainUnit.GPIO_PULL_UP` (0), :attr:`BusChainUnit.GPIO_PULL_DOWN` (1), or :attr:`BusChainUnit.GPIO_PULL_NONE` (2). Default is :attr:`BusChainUnit.GPIO_PULL_NONE` (2).
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = unit_chain_bus.set_gpio_output(1, BusChainUnit.GPIO_MODE_PUSHPULL, BusChainUnit.GPIO_PULL_UP)

### `set_gpio_output_value`
Set GPIO output value.

:param int gpio: GPIO number (1 or 2).
:param int value: Output value. 0 for low level, 1 for high level.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = unit_chain_bus.set_gpio_output_value(1, 1)  # Set GPIO1 to high level

### `set_gpio_input`
Set GPIO input mode configuration.

:param int gpio: GPIO number (1 or 2).
:param int pull: Pull-up/down configuration. Use :attr:`BusChainUnit.GPIO_PULL_UP` (0), :attr:`BusChainUnit.GPIO_PULL_DOWN` (1), or :attr:`BusChainUnit.GPIO_PULL_NONE` (2).
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = unit_chain_bus.set_gpio_input(1, BusChainUnit.GPIO_PULL_UP)

### `get_gpio_input_value`
Get GPIO input value.

:param int gpio: GPIO number (1 or 2).
:return: GPIO value. 0 for low level, 1 for high level. Returns None if failed.
:rtype: int | None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        value = unit_chain_bus.get_gpio_input_value(1)
        if value == 1:
            print("GPIO1 is high")

### `set_gpio_exit`
Set pin as external interrupt input mode.

:param int gpio: GPIO number (1 or 2).
:param int pull: Pull-up/down configuration. Use :attr:`BusChainUnit.GPIO_PULL_UP` (0), :attr:`BusChainUnit.GPIO_PULL_DOWN` (1), or :attr:`BusChainUnit.GPIO_PULL_NONE` (2).
:param int trigger_mode: Trigger mode. Use :attr:`BusChainUnit.GPIO_INTR_RISING` (0), :attr:`BusChainUnit.GPIO_INTR_FALLING` (1), or :attr:`BusChainUnit.GPIO_INTR_ANYEDGE` (2).
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = unit_chain_bus.set_gpio_exit(1, BusChainUnit.GPIO_PULL_UP, BusChainUnit.GPIO_INTR_RISING)

### `set_gpio_exit_callback`
Set GPIO external interrupt callback.

:param int gpio_num: GPIO number (1 or 2).
:param int trigger_mode: Trigger mode. Use :attr:`BusChainUnit.GPIO_INTR_RISING` (0) for rising edge or :attr:`BusChainUnit.GPIO_INTR_FALLING` (1) for falling edge.
:param callback: Callback function.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        def gpio_exit_callback(args):
            print("GPIO external interrupt")

        unit_chain_bus.set_gpio_exit_callback(1, BusChainUnit.GPIO_INTR_RISING, gpio_exit_callback)

### `set_adc`
Set ADC channel.

:param int channel: ADC channel number (1 or 2), corresponding to GPIO1 or GPIO2.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = unit_chain_bus.set_adc(1)

### `get_adc_input`
Read ADC value.

:param int channel: ADC channel number (1 or 2).
:return: ADC value (0-4095), or None if failed.
:rtype: int | None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        value = unit_chain_bus.get_adc_input(1)

### `set_i2c`
Set I2C mode.

:param int speed: I2C speed. Use :attr:`BusChainUnit.I2C_SPEED_100K` (0) or :attr:`BusChainUnit.I2C_SPEED_400K` (1). Default: 0.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = unit_chain_bus.set_i2c(BusChainUnit.I2C_SPEED_400K)

### `readfrom`
Read data from an I2C device.

:param int addr: I2C device address (7-bit).
:param int nbytes: Number of bytes to read (max 64).
:param bool stop: Generate stop condition (ignored, kept for compatibility).
:return: Read data as bytes.
:rtype: bytes

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        data = unit_chain_bus.readfrom(0x48, 4)

### `readfrom_into`
Read data from an I2C device into a buffer.

:param int addr: I2C device address (7-bit).
:param bytearray buf: Buffer to read into.
:param bool stop: Generate stop condition (ignored, kept for compatibility).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        buf = bytearray(4)
        unit_chain_bus.readfrom_into(0x48, buf)

### `writeto`
Write data to an I2C device.

:param int addr: I2C device address (7-bit).
:param bytes|bytearray buf: Data to write.
:param bool stop: Generate stop condition (ignored, kept for compatibility).
:return: Number of bytes written.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        n = unit_chain_bus.writeto(0x48, b"")

### `readfrom_mem`
Read data from an I2C device memory (register).

:param int addr: I2C device address (7-bit).
:param int memaddr: Memory/register address.
:param int nbytes: Number of bytes to read.
:param int addrsize: Register address size in bits (8 or 16). Default: 8.
:return: Read data as bytes.
:rtype: bytes

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        data = unit_chain_bus.readfrom_mem(0x48, 0x00, 4)

### `readfrom_mem_into`
Read data from an I2C device memory (register) into a buffer.

:param int addr: I2C device address (7-bit).
:param int memaddr: Memory/register address.
:param bytearray buf: Buffer to read into.
:param int addrsize: Register address size in bits (8 or 16). Default: 8.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        buf = bytearray(4)
        unit_chain_bus.readfrom_mem_into(0x48, 0x00, buf)

### `writeto_mem`
Write data to an I2C device memory (register).

:param int addr: I2C device address (7-bit).
:param int memaddr: Memory/register address.
:param bytes|bytearray buf: Data to write.
:param int addrsize: Register address size in bits (8 or 16). Default: 8.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_chain_bus.writeto_mem(0x48, 0x00, b"")

### `scan`
Scan for I2C devices.

:return: List of I2C device addresses found, or empty list if failed.
:rtype: list

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        devices = unit_chain_bus.scan()
        for addr in devices:
            print("Found device at 0x{:02X}".format(addr))
