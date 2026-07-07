# Atomic QRCode Base

<!-- .. sku: A133 -->

<!-- .. include:: ../refs/base.qrcode.ref -->

This library is the driver for Atomic QRCode Base, and the module communicates via UART.

Support the following products:

    |Atomic QRCode Base|

## UiFlow2 Example:

#### QRCode Scan in Key Mode

Open the |atoms3_qrcode_key_mode_example.m5f2| project in UiFlow2.

In **Key Mode**, the module starts decoding when the button is pressed and stops decoding when the button is released. After a successful decoding, it stops decoding. To continue decoding, the button must be released and pressed again.

UiFlow2 Code Block:

Example output:

    None

#### QRCode Scan in Host Mode

Open the |atoms3_qrcode_host_mode_example.m5f2| project in UiFlow2.

In **Host Mode**, pressing the button once starts decoding, and pressing the button again stops decoding.

UiFlow2 Code Block:

Example output:

    None

#### QRCode Scan in Auto Mode

Open the |atoms3_qrcode_auto_mode_example.m5f2| project in UiFlow2.

In **Auto Mode**, the module starts decoding when powered on and cannot be stopped.

UiFlow2 Code Block:

Example output:

    None

#### QRCode Scan in Pulse Mode

Open the |atoms3_qrcode_pulse_mode_example.m5f2| project in UiFlow2.

In **Pulse Mode**, set the TRIG pin to hold a low level for more than 20ms to trigger decoding once.

UiFlow2 Code Block:

Example output:

    None

#### QRCode Scan in Motion Sensing Mode

Open the |atoms3_qrcode_motion_sensing_mode_example.m5f2| project in UiFlow2.

In **Motion Sensing Mode**, the module automatically triggers decoding when it detects a change in the scene based on visual recognition information.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example:

#### QRCode Scan in Key Mode

In **Key Mode**, the module starts decoding when the button is pressed and stops decoding when the button is released. After a successful decoding, it stops decoding. To continue decoding, the button must be released and pressed again.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicQRCodeBase

title0 = None
label_data = None
label_status = None
base_qrcode = None
is_scanning = None
status = None
data = None

def setup():
    global title0, label_data, label_status, base_qrcode, is_scanning, status, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "stop scan", 5, 25, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    base_qrcode = AtomicQRCodeBase(2, 5, 6, 7, 8)
    base_qrcode.set_trigger_mode(base_qrcode.TRIGGER_MODE_KEY)
    is_scanning = False
    status = is_scanning

def loop():
    global title0, label_data, label_status, base_qrcode, is_scanning, status, data
    M5.update()
    if BtnA.isPressed():
        base_qrcode.set_trig(0)
        is_scanning = True
    else:
        base_qrcode.set_trig(1)
        is_scanning = False
    if status != is_scanning:
        status = is_scanning
        if status:
            label_status.setColor(0x00FF00, 0x000000)
            label_status.setText(str("scanning"))
        else:
            label_status.setColor(0xFFFFFF, 0x000000)
            label_status.setText(str("stop scan"))
    data = base_qrcode.read()
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

Example output:

    None

#### QRCode Scan in Host Mode

In **Host Mode**, pressing the button once starts decoding, and pressing the button again stops decoding.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicQRCodeBase

title0 = None
label_data = None
label_status = None
base_qrcode = None
is_scanning = None
data = None

def btna_was_clicked_event(state):
    global title0, label_data, label_status, base_qrcode, is_scanning, data
    if is_scanning:
        base_qrcode.stop_decode()
        label_status.setText(str("stop scan"))
        label_status.setColor(0xFFFFFF, 0x000000)
    else:
        base_qrcode.start_decode()
        label_status.setText(str("scanning"))
        label_status.setColor(0x00FF00, 0x000000)
    is_scanning = not is_scanning

def setup():
    global title0, label_data, label_status, base_qrcode, is_scanning, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "stop scan", 5, 25, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    base_qrcode = AtomicQRCodeBase(2, 5, 6, 7, 8)
    is_scanning = False
    base_qrcode.set_trigger_mode(base_qrcode.TRIGGER_MODE_HOST)
    base_qrcode.set_pos_light_mode(base_qrcode.POS_LIGHT_ON_DECODE)
    base_qrcode.set_fill_light_mode(base_qrcode.FILL_LIGHT_ON_DECODE)

def loop():
    global title0, label_data, label_status, base_qrcode, is_scanning, data
    M5.update()
    data = base_qrcode.read()
    if data:
        label_data.setText(str(data.decode()))
        print(data.decode())
        base_qrcode.start_decode()

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

Example output:

    None

#### QRCode Scan in Auto Mode

In **Auto Mode**, the module starts decoding when powered on and cannot be stopped.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicQRCodeBase

title0 = None
label_data = None
label_status = None
base_qrcode = None
data = None

def setup():
    global title0, label_data, label_status, base_qrcode, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "scanning", 5, 25, 1.0, 0x00FF00, 0x000000, Widgets.FONTS.DejaVu18
    )
    base_qrcode = AtomicQRCodeBase(2, 5, 6, 7, 8)
    base_qrcode.set_trigger_mode(base_qrcode.TRIGGER_MODE_AUTO)

def loop():
    global title0, label_data, label_status, base_qrcode, data
    M5.update()
    data = base_qrcode.read()
    if data:
        print(data.decode())
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

Example output:

    None

#### QRCode Scan in Pulse Mode

In **Pulse Mode**, set the TRIG pin to hold a low level for more than 20ms to trigger decoding once.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicQRCodeBase
import time

title0 = None
label_data = None
label_status = None
base_qrcode = None
data = None

def btna_was_clicked_event(state):
    global title0, label_data, label_status, base_qrcode, data
    base_qrcode.set_trig(0)
    time.sleep_ms(20)
    base_qrcode.set_trig(1)
    label_status.setText(str("scanning"))
    label_status.setColor(0x00FF00, 0x000000)

def setup():
    global title0, label_data, label_status, base_qrcode, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "stop scan", 5, 25, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    base_qrcode = AtomicQRCodeBase(2, 5, 6, 7, 8)
    base_qrcode.set_trigger_mode(base_qrcode.TRIGGER_MODE_PULSE)

def loop():
    global title0, label_data, label_status, base_qrcode, data
    M5.update()
    data = base_qrcode.read()
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

Example output:

    None

#### QRCode Scan in Motion Sensing Mode

In **Motion Sensing Mode**, the module automatically triggers decoding when it detects a change in the scene based on visual recognition information.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicQRCodeBase

title0 = None
label_data = None
label_status = None
base_qrcode = None
data = None

def setup():
    global title0, label_data, label_status, base_qrcode, data
    M5.begin()
    title0 = Widgets.Title("QRCode", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label(
        "detecting", 5, 25, 1.0, 0x00FF00, 0x000000, Widgets.FONTS.DejaVu18
    )
    base_qrcode = AtomicQRCodeBase(2, 5, 6, 7, 8)
    base_qrcode.set_trigger_mode(base_qrcode.TRIGGER_MODE_MOTION_SENSING)

def loop():
    global title0, label_data, label_status, base_qrcode, data
    M5.update()
    data = base_qrcode.read()
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

Example output:

    None

## **API**

#### AtomicQRCodeBase

## AtomicQRCodeBase
Create an AtomicQRCodeBase object.

:param int id: UART id.
:param int tx: the UART TX pin.
:param int rx: the UART RX pin.
:param int trig: the trigger pin.
:param int done: the receive done pin.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from base import AtomicQRCodeBase

        base_qrcode = AtomicQRCodeBase(id = 1, tx = 6, rx = 5, trig = 7, done = 8)

### `set_trig`
Set trigger value.

:param int value: ``0`` - Low level, ``1`` - High level.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.set_trig(value)

### `start_decode`
Start decode.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.start_decode()

### `stop_decode`
Stop decode.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.stop_decode()

### `read`
Read decode data.

:returns: qrcode data.
:rtype: None | bytes

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.read()

### `set_trigger_mode`
Set trigger mode.

:param int mode: The trigger mode. Available options:

    - ``TRIGGER_MODE_KEY``: Key Mode, Triggers a single decode; decoding stops after a successful read.
    - ``TRIGGER_MODE_HOST``: Host Mode, The command controls the start/stop of decoding. Once triggered, decoding will stop either upon successful decoding or after a timeout of 5 seconds.
    - ``TRIGGER_MODE_AUTO``: Auto Mode, Performs continuous decoding upon power-up and cannot be stopped.
    - ``TRIGGER_MODE_PULSE``: Pulse Mode, The Trig pin's low-level signal triggers decoding, which stops after a successful read or when the single read time limit is reached.
    - ``TRIGGER_MODE_MOTION_SENSING``: Motion Sensing Mode, Uses image recognition; decoding starts when a scene change is detected.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.set_trigger_mode(mode)

### `set_decode_continuous`
Set continuous decode time.

:param int delay_100ms: Continuous scanning time(unit: 100ms). Range: 099, i.e., 025,500 ms (0 means unlimited).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.set_decode_continuous(delay_100ms)

### `set_decode_interval`
Set decode interval.

:param int interval_100ms: Decode interval time(unit: 100ms). Range: 0~99, i.e., 0~9,900 ms.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.set_decode_interval(interval_100ms)

### `set_same_code_interval`
Set same code interval.

:param int interval_100ms: Decode interval for the same code(unit: 100ms). Range: 0~99, i.e., 0~9,900 ms.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.set_same_code_interval(interval_100ms)

### `set_fill_light_mode`
Set fill light mode.

:param int mode: The fill light mode. Available options:
    - ``FILL_LIGHT_OFF``: Light off.
    - ``FILL_LIGHT_ON``: Light on.
    - ``FILL_LIGHT_ON_DECODE``: Light on during decoding.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.set_fill_light_mode(mode)

### `set_pos_light_mode`
Set positioning light mode.

:param int mode: The positioning light mode. Available options:
    - ``POS_LIGHT_OFF``: Light off.
    - ``POS_LIGHT_ON``: Light on.
    - ``POS_LIGHT_ON_DECODE``: Light flash during decoding.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.set_pos_light_mode(mode)

### `set_startup_tone`
Set startup tone.

:param bool enable: True - Enable startup tone, False - Disable startup tone.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.set_startup_tone(enable)

### `set_decode_success_tone`
Set decode success tone.

:param bool enable: True - Enable decode success tone, False - Disable decode success tone.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.set_decode_success_tone(enable)

### `set_config_tone`
Set config tone.

:param bool enable: True - Enable set config tone, False - Disable set config tone.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_qrcode.set_config_tone(enable)
