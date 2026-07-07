# NB-IoT2 Unit

<!-- .. sku: U111-B -->

<!-- .. include:: ../refs/unit.nbiot2.ref -->

The ``NB-IOT2 Unit`` is a wireless communication module suitable for global Cat-NB frequency bands. It features an integrated SIM7028 communication module, utilizing serial communication (controlled via AT commands).

Support the following products:

    |NB-IOT2Unit|

<!-- .. note:: -->

    Please ensure that the device supports the NB-IoT frequency bands in your area before use.

<!-- .. note:: -->

    Please ensure that the firmware version of SIM7028 is greater than or equal to **2110B07SIM7028**.

     can be used to check the firmware version.

## UiFlow2 Example

#### NBIoT HTTP Example

Open the |cores3_unit_nbiot2_http_example.m5f2| project in UiFlow2.

This example shows how to send HTTP request using the NBIoT2 Unit.

click **Send** button to send HTTP request. Response data will be printed in the textarea.

UiFlow2 Code Block:

Example output:

    Output of received NBIoT message data on screen.

#### MQTT Example

Open the |cores3_unit_nbiot2_mqtt_example.m5f2| project in UiFlow2.

This example shows how to send MQTT message using the NBIoT2 Unit.

UiFlow2 Code Block:

Example output:

    Output of received NBIoT message data on screen.

## MicroPython Example

#### NBIoT HTTP Example

This example shows how to send HTTP request using the NBIoT2 Unit.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import NBIOT2Unit

page0 = None
label0 = None
label1 = None
button0 = None
textarea0 = None
textarea1 = None
nbiot2_0_http_req = None
nbiot2_0 = None

def button0_short_clicked_event(event_struct):
    global page0, label0, label1, button0, textarea0, textarea1, nbiot2_0_http_req, nbiot2_0
    nbiot2_0_http_req = nbiot2_0.post(
        "http://httpbin.org/post",
        json={"message": "Hello from M5Stack!", "status": "active"},
        headers={
            "Content-Type": "application/json",
            "Custom-Header": "MyHeaderValue",
        },
    )
    textarea1.set_text(str(nbiot2_0_http_req.text))

def button0_event_handler(event_struct):
    global page0, label0, label1, button0, textarea0, textarea1, nbiot2_0_http_req, nbiot2_0
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return

def setup():
    global page0, label0, label1, button0, textarea0, textarea1, nbiot2_0_http_req, nbiot2_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="http://httpbin.org/post",
        placeholder="Placeholder...",
        x=46,
        y=10,
        w=195,
        h=21,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    textarea1 = m5ui.M5TextArea(
        text="textarea1",
        placeholder="Placeholder...",
        x=10,
        y=68,
        w=300,
        h=162,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "url:",
        x=10,
        y=10,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "Response",
        x=10,
        y=44,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="Send",
        x=251,
        y=10,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    nbiot2_0 = NBIOT2Unit(1, port=(18, 17), verbose=False)
    page0.screen_load()
    nbiot2_0.connect(apn="cmnbiot")
    while not (nbiot2_0.isconnected()):
        pass
    textarea0.set_one_line(True)

def loop():
    global page0, label0, label1, button0, textarea0, textarea1, nbiot2_0_http_req, nbiot2_0
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    Output of received NBIoT message data on screen.

#### MQTT Example

This example shows how to send MQTT message using the NBIoT2 Unit.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import NBIOT2Unit

page0 = None
label0 = None
nbiot2_0_mqtt = None
nbiot2_0 = None

def nbiot2_0__testtopic_a_event(data):
    global page0, label0, nbiot2_0_mqtt, nbiot2_0
    label0.set_text(str(data[1]))

def setup():
    global page0, label0, nbiot2_0_mqtt, nbiot2_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "label0",
        x=130,
        y=105,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    nbiot2_0 = NBIOT2Unit(1, port=(18, 17), verbose=False)
    page0.screen_load()
    nbiot2_0.connect(apn="cmnbiot")
    while not (nbiot2_0.isconnected()):
        pass
    nbiot2_0_mqtt = nbiot2_0.MQTTClient(
        "uiflow2-client", "mqtt.m5stack.com", port=1883, user="", password="", keepalive=0
    )
    nbiot2_0_mqtt.connect(clean_session=False)
    nbiot2_0_mqtt.subscribe("testtopic/a", nbiot2_0__testtopic_a_event, qos=0)

def loop():
    global page0, label0, nbiot2_0_mqtt, nbiot2_0
    M5.update()
    nbiot2_0_mqtt.check_msg()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    Output of received NBIoT message data on screen.

## **API**

#### NBIOT2Unit

## NBIOT2Unit
Create an NBIOT2Unit object.

:param int id: The UART ID.
:param port: A list or tuple containing the RX and TX pin numbers.
:type port: list | tuple
:param bool verbose: Whether to print debug information.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import NBIOT2Unit

        # Using UART ID 1 and pins (rx=16, tx=17)
        nbiot2 = NBIOT2Unit(1, port=(16, 17))

<!-- .. note:: -->

        See :class:`NBIOTUnit <unit.nbiot.NBIOTUnit>` for more details.
