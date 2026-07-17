# QRCode Module

This library is the driver for Module13.2 QRCode, and the module communicates via UART.

Support the following products:

    Module13.2 QRCode

## MicroPython Example:

#### QRCode Scan in Continuous Mode

In **Continuous Mode**, pressing the button once starts decoding, and pressing the button again stops decoding.

```python
import os, sys, io
import M5
from M5 import *
from module import QRCodeModule

title0 = None
label_status = None
label_data = None
module_qrcode_0 = None
is_scanning = None
data = None

def btn_pwr_was_clicked_event(state):
    global title0, label_status, label_data, module_qrcode_0, is_scanning, data
    if is_scanning:
        module_qrcode_0.stop_decode()
        label_status.setColor(0xFFFFFF, 0x222222)
        label_status.setText(str("stop scan"))
    else:
        module_qrcode_0.start_decode()
        label_status.setColor(0x00FF00, 0x222222)
        label_status.setText(str("scanning"))
    is_scanning = not is_scanning

def setup():
    global title0, label_status, label_data, module_qrcode_0, is_scanning, data
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_status = Widgets.Label(
        "stop scan", 5, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    label_data = Widgets.Label("data", 4, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btn_pwr_was_clicked_event)
    module_qrcode_0 = QRCodeModule(1, tx=17, rx=18)
    module_qrcode_0.set_trigger_mode(QRCodeModule.TRIGGER_MODE_CONTINUOUS)
    module_qrcode_0.stop_decode()
    is_scanning = False

def loop():
    global title0, label_status, label_data, module_qrcode_0, is_scanning, data
    M5.update()
    data = module_qrcode_0.read()
    if data:
        label_data.setText(str(data.decode()))
        print(data.decode())

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

#### QRCode Scan in Auto Mode

In **Auto Mode**, the module starts decoding when powered on and cannot be stopped.

```python
import os, sys, io
import M5
from M5 import *
from module import QRCodeModule

title0 = None
label_status = None
label_data = None
module_qrcode_0 = None
data = None

def setup():
    global title0, label_status, label_data, module_qrcode_0, data
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_status = Widgets.Label(
        "scanning", 5, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    label_data = Widgets.Label("data", 5, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    module_qrcode_0 = QRCodeModule(2, tx=17, rx=18)
    module_qrcode_0.set_trigger_mode(QRCodeModule.TRIGGER_MODE_AUTO)

def loop():
    global title0, label_status, label_data, module_qrcode_0, data
    M5.update()
    data = module_qrcode_0.read()
    if data:
        label_data.setText(str(data.decode()))

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

#### QRCode Scan in Pulse Mode

In **Pulse Mode**, set the TRIG pin to hold a low level for more than 20ms to trigger decoding once.

```python
import os, sys, io
import M5
from M5 import *
from module import QRCodeModule
import time

title0 = None
label_status = None
label_data = None
module_qrcode_0 = None
data = None

def btn_pwr_was_clicked_event(state):
    global title0, label_status, label_data, module_qrcode_0, data
    module_qrcode_0.set_trig(0)
    time.sleep_ms(20)
    module_qrcode_0.set_trig(1)
    label_status.setColor(0x00FF00, 0x222222)
    label_status.setText(str("scanning"))

def setup():
    global title0, label_status, label_data, module_qrcode_0, data
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_status = Widgets.Label(
        "scanning", 5, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    label_data = Widgets.Label("data", 5, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btn_pwr_was_clicked_event)
    module_qrcode_0 = QRCodeModule(2, tx=17, rx=18)
    module_qrcode_0.set_trigger_mode(QRCodeModule.TRIGGER_MODE_PULSE)

def loop():
    global title0, label_status, label_data, module_qrcode_0, data
    M5.update()
    data = module_qrcode_0.read()
    if data:
        label_data.setText(str(data.decode()))
        label_status.setColor(0xFFFFFF, 0x222222)
        label_status.setText(str("stop scan"))

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

#### QRCode Scan in Motion Sensing Mode

In **Motion Sensing Mode**, the module automatically triggers decoding when it detects a change in the scene based on visual recognition information.

```python
import os, sys, io
import M5
from M5 import *
from module import QRCodeModule

title0 = None
label_status = None
label_data = None
module_qrcode_0 = None
data = None

def setup():
    global title0, label_status, label_data, module_qrcode_0, data
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_status = Widgets.Label(
        "detecting", 5, 50, 1.0, 0x00FF00, 0x222222, Widgets.FONTS.DejaVu24
    )
    label_data = Widgets.Label("data", 5, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    module_qrcode_0 = QRCodeModule(2, tx=17, rx=18)
    module_qrcode_0.set_trigger_mode(QRCodeModule.TRIGGER_MODE_MOTION_SENSING)
    module_qrcode_0.set_motion_sensitivity(1)

def loop():
    global title0, label_status, label_data, module_qrcode_0, data
    M5.update()
    data = module_qrcode_0.read()
    if data:
        label_data.setText(str(data.decode()))

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

#### QRCodeModule

### `class module.qrcode.QRCodeModule`

    Create an QRCodeModule object.

    - Parameter `id` (`int`): UART id.
    - Parameter `tx` (`int`): the UART TX pin.
    - Parameter `rx` (`int`): the UART RX pin.

```python
from module import ModuleQRCode

module_qrcode = ModuleQRCode(id = 1, tx = 17, rx = 18)
```
### `set_power(enable)`

        Set power.

        - Parameter `enable` (`bool`):

            - `True` : power on.
            - `False` : power off.

```python
module_qrcode.set_power(enable)
```
### `set_trig(value)`

        Set trigger pin value.

        - Parameter `value` (`int`):

            - `0` : low level.
            - `1` : high level.

```python
module_qrcode.set_trig(value)
```
### `start_decode()`

        Start decode.

```python
module_qrcode.start_decode()
```
### `stop_decode()`

        Stop decode.

```python
module_qrcode.stop_decode()
```
### `read()`

        Read decode data.

        - Returns: qrcode data.
        - Return type: None | bytes

        If no data is received, return None.

```python
module_qrcode.read()
```
### `set_trigger_mode(mode)`

        Set trigger mode.

        - Parameter `mode` (`int`): The trigger mode. Available options:

            - `TRIGGER_MODE_KEY`: Key Mode, Triggers a single decode; decoding stops after a successful read.
            - `TRIGGER_MODE_CONTINUOUS`: Continuous Mode, Triggers continuous decoding; decoding continues even after a successful read and stops only when triggered again.
            - `TRIGGER_MODE_AUTO`: Auto Mode, Performs continuous decoding upon power-up and cannot be stopped.
            - `TRIGGER_MODE_PULSE`: Pulse Mode, The Trig pin's low-level signal triggers decoding, which stops after a successful read or when the single read time limit is reached.
            - `TRIGGER_MODE_MOTION_SENSING`: Motion Sensing Mode, Uses image recognition; decoding starts when a scene change is detected.

```python
module_qrcode.set_trigger_mode(mode)
```
### `set_decode_delay(delay_ms)`

        Set decode delay.

        - Parameter `delay_ms` (`int`): decode delay time(ms), 0 means continuous decoding until success.

```python
module_qrcode.set_decode_delay(delay_ms)
```
### `set_trigger_timeout(timeout_ms)`

        Set trigger timeout.

        - Parameter `timeout_ms`: trigger timeout time(ms), Decoding will automatically stop when the duration exceeds this value.

```python
module_qrcode.set_trigger_timeout(timeout_ms)
```
### `set_motion_sensitivity(level)`

        Set motion detection sensitivity. (in Motion Sensing Mode)

        - Parameter `level` (`int`): sensitivity level. Range: 1~5. The higher the level, the more sensitive it is to scene changes.

```python
module_qrcode.set_motion_sensitivity(level)
```
### `set_continuous_decode_delay(delay_100ms)`

        Set continuous decode delay. (in Motion Sensing Mode)

        - Parameter `delay_ms` (`int`): delay time(unit: 100ms), 0 means continuous decoding until timeout.

```python
module_qrcode.set_continuous_decode_delay(delay_ms)
```
### `set_trigger_decode_delay(delay_ms):`

        Set trigger decode delay. (in Motion Sensing Mode)

        Sets the trigger decoding delay time. This is the delay between re-entering the scene change detection phase and starting recognition again after detecting a change.

        - Parameter `delay_ms` (`int`): Trigger decode delay time(unit: ms).

```python
module_qrcode.set_trigger_decode_delay(delay_ms)
```
### `set_same_code_interval(interval_ms)`

        Set same code interval.

        - Parameter `interval_ms` (`int`): The interval time for repeated recognition of the same code (unit: ms).

```python
module_qrcode.set_same_code_interval(interval_ms)
```
### `set_diff_code_interval(interval_ms)`

        Set difference code interval.

        - Parameter `interval_ms` (`int`): The interval time for repeated recognition of the difference code (unit: ms).

```python
module_qrcode.set_diff_code_interval(interval_ms)
```
### `set_same_code_no_delay(enable)`

        Set same code no delay.

        - Parameter `enable` (`bool`): Whether to enable non-delay output for the same code. True means enabled, False means disabled.

```python
module_qrcode.set_same_code_no_delay(enable)
```
### `set_fill_light_mode(mode)`

        Set fill light mode.

        - Parameter `mode` (`int`): The fill light mode. Available options:

            - `FILL_LIGHT_OFF`: Light off.
            - `FILL_LIGHT_ON`: Light on.
            - `FILL_LIGHT_ON_DECODE`: Light on during decoding.

```python
module_qrcode.set_fill_light_mode(mode)
```
### `set_fill_light_brightness(brightness)`

        Set fill light brightness.

        - Parameter `brightness` (`int`): The fill light brightness. Range: 0~100.

```python
module_qrcode.set_fill_light_brightness(brightness)
```
### `set_pos_light_mode(mode)`

        Set positioning light mode.

        - Parameter `mode` (`int`): The positioning light mode. Available options:

            - `POS_LIGHT_OFF`: Light off.
            - `POS_LIGHT_ON_DECODE`: Light on during decoding.
            - `POS_LIGHT_FLASH_ON_DECODE`: Light flash during decoding.

```python
module_qrcode.set_pos_light_mode(mode)
```
### `set_startup_tone(mode)`

        Set startup tone.

        - Parameter `mode` (`int`):

            - `0`: Disable startup tone.
            - `1`: Play 4 beeps.
            - `2`: Play 2 beeps.

```python
module_qrcode.set_startup_tone(mode)
```
### `set_decode_success_beep(count)`

        Set decode success beep.

        - Parameter `count` (`int`):

            - `0`: No prompt sound.
            - `1`: Play prompt sound once.
            - `2`: Play prompt sound twice.

```python
module_qrcode.set_decode_success_beep(count)
```
### `set_case_conversion(mode)`

        Set case conversion.

        - Parameter `mode` (`int`):

            - `0`: Off (Original data).
            - `1`: Convert to uppercase.
            - `2`: Convert to lowercase.

```python
module_qrcode.set_case_conversion(mode)
```
### `set_protocol_format(mode):`

### `set_protocol_format(mode)`

        - Parameter `mode` (`int`):

            - `0`: No protocol
            - `1`: Format 1: [0x03] + Data Length (2 bytes) + Data
            - `2`: Format 2: [0x03] + Data Length + Number of Barcodes + Code 1 Data Length + Code 1 Data + ... + CRC
            - `3`: Format 3: [0x03] + Data Length + Number of Barcodes + Code 1 ID + Code 1 Data Length + Code 1 Data + ... + CRC

        CRC generate reference program.

```python
def crc16_calc(data: bytes) -> int:
    ca_crc = 0
    for byte in data:
        for i in range(7, -1, -1):
            if ca_crc & 0x8000:
                ca_crc = (ca_crc << 1) ^ 0x18005
            else:
                ca_crc <<= 1
            if (byte & (1 << i)) != 0:
                ca_crc ^= 0x18005
    return ca_crc & 0xFFFF
```

```python
module_qrcode.set_protocol_format(mode)
```
