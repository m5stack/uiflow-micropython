# PPS Module

The `PPS` class controls a Programmable Power Supply (PPS), capable of providing
an output up to 30V and 5A. It allows for precise control over the output
voltage and current, with features to read back the actual output values and the
module's status.

Support the following products:

    PPSModule

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from module import PPSModule
import time

label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
pps_0 = None

def setup():
    global label0, label1, label2, label3, label4, label5, pps_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label(
        "Output Voltage:", 20, 40, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Output Current:", 20, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("Mode:", 22, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 180, 40, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("label4", 180, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 180, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    pps_0 = PPSModule(address=0x35)
    pps_0.set_output_voltage(5.5)
    pps_0.set_output_current(1)
    pps_0.enable_output()

def loop():
    global label0, label1, label2, label3, label4, label5, pps_0
    M5.update()
    label3.setText(str(pps_0.read_output_voltage()))
    label4.setText(str(pps_0.read_output_current()))
    label5.setText(str(pps_0.read_psu_running_mode()))
    time.sleep_ms(100)

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

## class PPSModule

## Constructors

### `class PPSModule(addr=0x35)`

    Creates a PPS object to interact with the programmable power supply.

    - `addr`: I2C address of the PPS device (default is `0x35`).

## Methods

### `PPSModule.set_output(enable: bool)`

    Enable or disable the PPS output.

    - `enable`: True to enable, False to disable.

### `PPSModule.enable_output()`

    Enable the PPS output.

### `PPSModule.disable_output()`

    Disable the PPS output.

### `PPSModule.set_output_voltage(voltage: float)`

    Set the output voltage of the PPS.

    - `voltage`: Desired output voltage from 0.0 to 30.0 volts.

### `PPSModule.set_output_current(current: float)`

    Set the output current of the PPS.

    - `current`: Desired output current from 0.0A to 5.0A.

### `PPSModule.read_psu_running_mode() -> int`

    Read the PSU running mode.

### `PPSModule.read_output_current() -> float`

    Read the current output current.

### `PPSModule.read_output_voltage() -> float`

    Read the current output voltage.

### `PPSModule.read_input_voltage() -> float`

    Read the input voltage.

### `PPSModule.read_data_update_flag() -> int`

    Read the data update flag.

### `PPSModule.read_mcu_temperature() -> float`

    Read the MCU temperature.

### `PPSModule.read_module_id() -> int`

    Read the module ID.

### `PPSModule.read_uid() -> bytearray`

    Read the unique identifier (UID).

### `PPSModule.get_i2c_address() -> int`

    Get the current I2C address of the device.

### `PPSModule.set_i2c_address(new_address: int)`

    Set a new I2C address for the device.

    - `new_address`: The new I2C address to set.
