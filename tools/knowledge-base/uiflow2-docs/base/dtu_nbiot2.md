# Atom DTU NBIoT2

<!-- .. sku: K059-B -->

<!-- .. include:: ../refs/base.dtu_nbiot2.ref -->

This is the driver library for the ATOM DTU NBIoT2 to accept and send data from the DTU NBIoT.

Support the following products:

    |Atom DTU NBIoT2|

<!-- .. note:: -->

    Please ensure that the device supports the NB-IoT frequency bands in your area before use.

<!-- .. note:: -->

    Please ensure that the firmware version of SIM7028 is greater than or equal to **2110B07SIM7028**.

     can be used to check the firmware version.

## UiFlow2 Example

#### NBIoT HTTP Example

Open the |atoms3_base_nbiot2_http_example.m5f2| project in UiFlow2.

This example shows how to send HTTP request using the Atom DTU NBIoT2.

UiFlow2 Code Block:

Example output:

    Output of received NBIoT message data via serial port.

#### MQTT Example

Open the |atoms3_base_nbiot2_mqtt_example.m5f2| project in UiFlow2.

This example shows how to send MQTT message using the Atom DTU NBIoT2.

UiFlow2 Code Block:

Example output:

    Output of received NBIoT message data on screen.

## MicroPython Example

#### NBIoT HTTP Example

This example shows how to send HTTP request using the Atom DTU NBIoT2.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import UART
from base import AtomRS485
from base import AtomDTUNBIoT2

label0 = None
uart2 = None
base_rs485 = None
base_nbiot2 = None
base_nbiot2_http_req = None

def setup():
    global label0, uart2, base_rs485, base_nbiot2, base_nbiot2_http_req

    M5.begin()
    Widgets.fillScreen(0x000000)
    label0 = Widgets.Label("label0", 8, 7, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    uart2 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=5, rx=6)
    base_rs485 = AtomRS485(
        1,
        baudrate=115200,
        bits=8,
        parity=None,
        stop=1,
        tx=7,
        rx=8,
        txbuf=256,
        rxbuf=256,
        timeout=0,
        timeout_char=0,
        invert=0,
        flow=0,
    )
    base_nbiot2 = AtomDTUNBIoT2(uart2, verbose=False)
    base_nbiot2.connect(apn="cmnbiot")
    while not (base_nbiot2.isconnected()):
        pass
    base_nbiot2_http_req = base_nbiot2.post(
        "http://httpbin.org/post",
        json={"message": "Hello from M5Stack!", "status": "active"},
        headers={
            "Content-Type": "application/json",
            "Custom-Header": "MyHeaderValue",
        },
    )
    print((str("status code: ") + str((base_nbiot2_http_req.status_code))))
    print((str("content: ") + str((base_nbiot2_http_req.content))))

def loop():
    global label0, uart2, base_rs485, base_nbiot2, base_nbiot2_http_req
    M5.update()

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

    Output of received NBIoT message data via serial port.

#### MQTT Example

This example shows how to send MQTT message using the Atom DTU NBIoT2.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import UART
from base import AtomRS485
from base import AtomDTUNBIoT2

label0 = None
base_nbiot2 = None
uart2 = None
base_rs485 = None
base_nbiot2_mqtt = None

def base_nbiot2_testtopic_a_event(data):
    global label0, base_nbiot2, uart2, base_rs485, base_nbiot2_mqtt
    label0.setText(str(data[1]))

def setup():
    global label0, base_nbiot2, uart2, base_rs485, base_nbiot2_mqtt

    M5.begin()
    Widgets.fillScreen(0x000000)
    label0 = Widgets.Label("label0", 8, 7, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    uart2 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=5, rx=6)
    base_rs485 = AtomRS485(
        1,
        baudrate=115200,
        bits=8,
        parity=None,
        stop=1,
        tx=7,
        rx=8,
        txbuf=256,
        rxbuf=256,
        timeout=0,
        timeout_char=0,
        invert=0,
        flow=0,
    )
    base_nbiot2 = AtomDTUNBIoT2(uart2, verbose=False)
    base_nbiot2.connect(apn="cmnbiot")
    while not (base_nbiot2.isconnected()):
        pass
    base_nbiot2_mqtt = base_nbiot2.MQTTClient(
        "uiflow2-client", "mqtt.m5stack.com", port=1883, user="", password="", keepalive=0
    )
    base_nbiot2_mqtt.connect(clean_session=False)
    base_nbiot2_mqtt.subscribe("testtopic/a", base_nbiot2_testtopic_a_event, qos=0)

def loop():
    global label0, base_nbiot2, uart2, base_rs485, base_nbiot2_mqtt
    M5.update()
    base_nbiot2_mqtt.check_msg()

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

    Output of received NBIoT message data on screen.

## **API**

#### AtomDTUNBIoT2

## AtomDTUNBIoT2
Create an AtomDTUNBIoT2 object.

:param machine.UART uart: The UART object to use.
:param bool verbose: Whether to print debug information.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from base import AtomDTUNBIoT2
        from hardware import UART

        uart2 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=22, rx=19)
        base_nbiot2 = AtomDTUNBIoT2(uart2, verbose=False)

<!-- .. note:: -->

        See :class:`NBIOT2Unit <unit.nbiot2.NBIOT2Unit>` for more details.

#### AtomRS485

<!-- .. note:: -->

    See :class:`AtomRS485 <base.rs232.AtomRS232>` for more details.
