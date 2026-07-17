# Atomic QRCode2 Base

This library is the driver for Atomic QRCode2 Base, and the module communicates via UART.

Support the following products:

    Atomic QRCode2 Base

## MicroPython Example:

#### QRCode Scan in Key Mode

In **Key Mode**, the module starts decoding when the button is pressed and stops decoding when the button is released. After a successful decoding, it stops decoding. To continue decoding, the button must be released and pressed again.

```python
import os, sys, io
import M5
from M5 import *
from base import AtomicQRCode2Base

title0 = None
label_data = None
label_status = None
base_qrcode2 = None
is_scanning = None
status = None
data = None

def setup():
    global title0, label_data, label_status, base_qrcode2, is_scanning, status, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "stop scan", 5, 25, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    base_qrcode2 = AtomicQRCode2Base(2, 5, 6, 7)
    base_qrcode2.set_trigger_mode(base_qrcode2.TRIGGER_MODE_KEY)
    is_scanning = False
    status = is_scanning

def loop():
    global title0, label_data, label_status, base_qrcode2, is_scanning, status, data
    M5.update()
    if BtnA.isPressed():
        base_qrcode2.set_trig(0)
        is_scanning = True
    else:
        base_qrcode2.set_trig(1)
        is_scanning = False
    if status != is_scanning:
        status = is_scanning
        if status:
            label_status.setColor(0x00FF00, 0x000000)
            label_status.setText(str("scanning"))
        else:
            label_status.setColor(0xFFFFFF, 0x000000)
            label_status.setText(str("stop scan"))
    data = base_qrcode2.read()
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

#### QRCode Scan in Continuous Mode

In **Continuous Mode**, pressing the button once starts decoding, and pressing the button again stops decoding.

```python
import os, sys, io
import M5
from M5 import *
from base import AtomicQRCode2Base

title0 = None
label_data = None
label_status = None
base_qrcode2 = None
is_scanning = None
data = None

def btna_was_clicked_event(state):
    global title0, label_data, label_status, base_qrcode2, is_scanning, data
    if is_scanning:
        base_qrcode2.stop_decode()
        label_status.setText(str("stop scan"))
        label_status.setColor(0xFFFFFF, 0x000000)
    else:
        base_qrcode2.start_decode()
        label_status.setText(str("scanning"))
        label_status.setColor(0x00FF00, 0x000000)
    is_scanning = not is_scanning

def setup():
    global title0, label_data, label_status, base_qrcode2, is_scanning, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "stop scan", 5, 25, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    base_qrcode2 = AtomicQRCode2Base(2, 5, 6, 7)
    base_qrcode2.set_trigger_mode(base_qrcode2.TRIGGER_MODE_CONTINUOUS)
    base_qrcode2.set_startup_tone(1)
    base_qrcode2.set_decode_success_beep(2)
    base_qrcode2.stop_decode()
    is_scanning = False

def loop():
    global title0, label_data, label_status, base_qrcode2, is_scanning, data
    M5.update()
    data = base_qrcode2.read()
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

#### QRCode Scan in Auto Mode

In **Auto Mode**, the module starts decoding when powered on and cannot be stopped.

```python
import os, sys, io
import M5
from M5 import *
from base import AtomicQRCode2Base

title0 = None
label_data = None
label_status = None
base_qrcode2 = None
data = None

def setup():
    global title0, label_data, label_status, base_qrcode2, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "scanning", 5, 25, 1.0, 0x00FF00, 0x000000, Widgets.FONTS.DejaVu18
    )
    base_qrcode2 = AtomicQRCode2Base(2, 5, 6, 7)
    base_qrcode2.set_trigger_mode(base_qrcode2.TRIGGER_MODE_AUTO)

def loop():
    global title0, label_data, label_status, base_qrcode2, data
    M5.update()
    data = base_qrcode2.read()
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
from base import AtomicQRCode2Base
import time

title0 = None
label_data = None
label_status = None
base_qrcode2 = None
data = None

def btna_was_clicked_event(state):
    global title0, label_data, label_status, base_qrcode2, data
    base_qrcode2.set_trig(0)
    time.sleep_ms(20)
    base_qrcode2.set_trig(1)
    label_status.setText(str("scanning"))
    label_status.setColor(0x00FF00, 0x000000)

def setup():
    global title0, label_data, label_status, base_qrcode2, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "stop scan", 5, 25, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    base_qrcode2 = AtomicQRCode2Base(2, 5, 6, 7)
    base_qrcode2.set_trigger_mode(base_qrcode2.TRIGGER_MODE_PULSE)

def loop():
    global title0, label_data, label_status, base_qrcode2, data
    M5.update()
    data = base_qrcode2.read()
    if data:
        label_data.setText(str(data.decode()))
        label_status.setText(str("stop scan"))
        label_status.setColor(0xFFFFFF, 0x000000)

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
from base import AtomicQRCode2Base

title0 = None
label_data = None
label_status = None
base_qrcode2 = None
data = None

def setup():
    global title0, label_data, label_status, base_qrcode2, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "detecting", 5, 25, 1.0, 0x00FF00, 0x000000, Widgets.FONTS.DejaVu18
    )
    base_qrcode2 = AtomicQRCode2Base(2, 5, 6, 7)
    base_qrcode2.set_trigger_mode(base_qrcode2.TRIGGER_MODE_MOTION_SENSING)
    base_qrcode2.set_motion_sensitivity(1)

def loop():
    global title0, label_data, label_status, base_qrcode2, data
    M5.update()
    data = base_qrcode2.read()
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

#### AtomicQRCode2Base

### `class base.qrcode2.AtomicQRCode2Base`

    Create an AtomicQRCode2Base object.

    - Parameter `id` (`int`): UART id.
    - Parameter `tx` (`int`): the UART TX pin.
    - Parameter `rx` (`int`): the UART RX pin.
    - Parameter `trig` (`int`): the trigger pin.

```python
from base import AtomicQRCode2Base

base_qrcode2 = AtomicQRCode2Base(id = 1, tx = 6, rx = 5, trig = 7)
```
### `set_trig(value)`

        Set trigger pin value.

        - Parameter `value` (`int`):

            - `0` : low level.
            - `1` : high level.

```python
base_qrcode2.set_trig(value)
```
### `start_decode()`

        Start decode.

```python
base_qrcode2.start_decode()
```
### `stop_decode()`

        Stop decode.

```python
base_qrcode2.stop_decode()
```
### `read()`

        Read qrcode data.

        - Returns: qrcode data.
        - Return type: None | bytes

        If no data is received, return None.

```python
base_qrcode2.read()
```
### `set_trigger_mode(mode)`

        Set trigger mode.

        - Parameter `mode` (`int`): The trigger mode. Available options:

            - `TRIGGER_MODE_KEY`: Key Mode, Decoding starts when the trigger pin is low and stops when the trigger pin is high.
            - `TRIGGER_MODE_CONTINUOUS`: Call start_decode() to start decoding and stop_decode() to stop decoding.
            - `TRIGGER_MODE_AUTO`: Auto Mode, Performs continuous decoding upon power-up and cannot be stopped.
            - `TRIGGER_MODE_PULSE`: Pulse Mode, A 20ms low-level pulse on the trigger pin initiates a single decoding operation.
            - `TRIGGER_MODE_MOTION_SENSING`: Motion Sensing Mode, Uses image recognition; decoding starts when a scene change is detected.

```python
base_qrcode2.set_trigger_mode(mode)
```
### `set_decode_delay(delay_ms)`

        Set decode delay.

        - Parameter `delay_ms` (`int`): decode delay time(ms), 0 means continuous decoding until success.

```python
base_qrcode2.set_decode_delay(delay_ms)
```
### `set_trigger_timeout(timeout_ms)`

        Set trigger timeout.

        - Parameter `timeout_ms`: trigger timeout time(ms), Decoding will automatically stop when the duration exceeds this value.

```python
base_qrcode2.set_trigger_timeout(timeout_ms)
```
### `set_motion_sensitivity(level)`

        Set motion detection sensitivity. (in Motion Sensing Mode)

        - Parameter `level` (`int`): sensitivity level. Range: 1~5. The higher the level, the more sensitive it is to scene changes.

```python
base_qrcode2.set_motion_sensitivity(level)
```
### `set_continuous_decode_delay(delay_ms)`

        Set continuous decode delay. (in Motion Sensing Mode)

        - Parameter `delay_ms` (`int`): delay time(unit: 100ms), 0 means continuous decoding until timeout.

```python
base_qrcode2.set_continuous_decode_delay(delay_ms)
```
### `set_trigger_decode_delay(delay_ms):`

        Set trigger decode delay. (in Motion Sensing Mode)

        Sets the trigger decoding delay time. This is the delay between re-entering the scene change detection phase and starting recognition again after detecting a change.

        - Parameter `delay_ms` (`int`): Trigger decode delay time(unit: ms).

```python
base_qrcode2.set_trigger_decode_delay(delay_ms)
```
### `set_same_code_interval(interval_ms)`

        Set same code interval.

        - Parameter `interval_ms` (`int`): The interval time for repeated recognition of the same code (unit: ms).

```python
base_qrcode2.set_same_code_interval(interval_ms)
```
### `set_diff_code_interval(interval_ms)`

        Set difference code interval.

        - Parameter `interval_ms` (`int`): The interval time for repeated recognition of the difference code (unit: ms).

```python
base_qrcode2.set_diff_code_interval(interval_ms)
```
### `set_same_code_no_delay(enable)`

        Set same code no delay.

        - Parameter `enable` (`bool`): Whether to enable non-delay output for the same code. True means enabled, False means disabled.

```python
base_qrcode2.set_same_code_no_delay(enable)
```
### `set_fill_light_mode(mode)`

        Set fill light mode.

        - Parameter `mode` (`int`): The fill light mode. Available options:

            - `FILL_LIGHT_OFF`: Light off.
            - `FILL_LIGHT_ON`: Light on.
            - `FILL_LIGHT_ON_DECODE`: Light on during decoding.

```python
base_qrcode2.set_fill_light_mode(mode)
```
### `set_fill_light_brightness(brightness)`

        Set fill light brightness.

        - Parameter `brightness` (`int`): The fill light brightness. Range: 0~100.

```python
base_qrcode2.set_fill_light_brightness(brightness)
```
### `set_pos_light_mode(mode)`

        Set positioning light mode.

        - Parameter `mode` (`int`): The positioning light mode. Available options:

        - `POS_LIGHT_OFF`: Light off.
        - `POS_LIGHT_ON_DECODE`: Light on during decoding.
        - `POS_LIGHT_FLASH_ON_DECODE`: Light flash during decoding.

```python
base_qrcode2.set_pos_light_mode(mode)
```
### `set_startup_tone(mode)`

        Set startup tone.

        - Parameter `mode` (`int`):

            - `0`: Disable startup tone.
            - `1`: Play 4 beeps.
            - `2`: Play 2 beeps.

```python
base_qrcode2.set_startup_tone(mode)
```
### `set_decode_success_beep(count)`

        Set decode success beep.

        - Parameter `count` (`int`):

            - `0`: No prompt sound.
            - `1`: Play prompt sound once.
            - `2`: Play prompt sound twice.

```python
base_qrcode2.set_decode_success_beep(count)
```
### `set_case_conversion(mode)`

        Set case conversion.

        - Parameter `mode` (`int`):

            - `0`: Off (Original data).
            - `1`: Convert to uppercase.
            - `2`: Convert to lowercase.

```python
base_qrcode2.set_case_conversion(mode)
```
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
base_qrcode2.set_protocol_format(mode)
```
