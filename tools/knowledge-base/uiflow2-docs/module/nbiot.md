# NB-IoT Module

<!-- .. include:: ../refs/module.nbiot.ref -->

The ``NB-IoT Module`` is a wireless communication module suitable for global Cat-NB frequency bands. It features an integrated SIM7020G communication module and communicates via serial port (AT commands).

Support the following products:

    |NB-IoT Module|

<!-- .. note:: -->

    Please ensure that the device supports the NB-IoT frequency bands in your area before use.

<!-- .. note:: -->

    Please ensure that the firmware version of SIM7020 is greater than or equal to **1752B12SIM7020C**.

     can be used to check the firmware version.

## UiFlow2 Example

#### NBIoT HTTP Example

Open the |cores3_module_nbiot_http_example.m5f2| project in UiFlow2.

This example shows how to send HTTP request using the NBIoT Module.

UiFlow2 Code Block:

Example output:

    Output of received NBIoT message data on screen.

#### MQTT Example

Open the |cores3_module_nbiot_mqtt_example.m5f2| project in UiFlow2.

This example shows how to send MQTT message using the NBIoT Module.

UiFlow2 Code Block:

Example output:

    Output of received NBIoT message data on screen.

## MicroPython Example

#### NBIoT HTTP Example

This example shows how to send HTTP request using the NBIoT Module.

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
from module import NBIOTModule

page0 = None
label0 = None
label1 = None
button0 = None
textarea0 = None
textarea1 = None
nbiotmodule_0_http_req = None
nbiotmodule_0 = None

def button0_short_clicked_event(event_struct):
    global \
        page0, \
        label0, \
        label1, \
        button0, \
        textarea0, \
        textarea1, \
        nbiotmodule_0_http_req, \
        nbiotmodule_0
    nbiotmodule_0_http_req = nbiotmodule_0.post(
        "http://httpbin.org/post",
        json={"message": "Hello from M5Stack!", "status": "active"},
        headers={
            "Content-Type": "application/json",
            "Custom-Header": "MyHeaderValue",
        },
    )
    textarea1.set_text(str(nbiotmodule_0_http_req.text))

def button0_event_handler(event_struct):
    global \
        page0, \
        label0, \
        label1, \
        button0, \
        textarea0, \
        textarea1, \
        nbiotmodule_0_http_req, \
        nbiotmodule_0
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return

def setup():
    global \
        page0, \
        label0, \
        label1, \
        button0, \
        textarea0, \
        textarea1, \
        nbiotmodule_0_http_req, \
        nbiotmodule_0

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

    textarea0.set_one_line(True)
    page0.screen_load()
    nbiotmodule_0 = NBIOTModule(2, 17, 18)
    nbiotmodule_0.connect(apn="cmnbiot")
    while not (nbiotmodule_0.isconnected()):
        pass

def loop():
    global \
        page0, \
        label0, \
        label1, \
        button0, \
        textarea0, \
        textarea1, \
        nbiotmodule_0_http_req, \
        nbiotmodule_0
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

This example shows how to send MQTT message using the NBIoT Module.

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
from module import NBIOTModule

page0 = None
label0 = None
nbiotmodule_0 = None
nbiotmodule_0_mqtt = None

def nbiotmodule_0__testtopic_a_event(data):
    global page0, label0, nbiotmodule_0, nbiotmodule_0_mqtt
    label0.set_text(str(data[1]))

def setup():
    global page0, label0, nbiotmodule_0, nbiotmodule_0_mqtt

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

    page0.screen_load()
    nbiotmodule_0 = NBIOTModule(2, 17, 18)
    nbiotmodule_0.connect(apn="cmnbiot")
    while not (nbiotmodule_0.isconnected()):
        pass
    nbiotmodule_0_mqtt = nbiotmodule_0.MQTTClient(
        "uiflow2-client", "mqtt.m5stack.com", port=1883, user="", password="", keepalive=0
    )
    nbiotmodule_0_mqtt.connect(clean_session=False)
    nbiotmodule_0_mqtt.subscribe("testtopic/a", nbiotmodule_0__testtopic_a_event, qos=0)

def loop():
    global page0, label0, nbiotmodule_0, nbiotmodule_0_mqtt
    M5.update()
    nbiotmodule_0_mqtt.check_msg()

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

## NBIOTModule
Create an NBIOTModule object.

:param uart_or_id: The UART object or UART ID.
:type uart_or_id: machine.UART | int
:param int tx: The UART TX pin. Required if uart_or_id is an ID.
:param int rx: The UART RX pin. Required if uart_or_id is an ID.
:param bool verbose: Whether to print debug information.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from module import NBIOTModule
        import machine

        # Using UART ID and pins (rx, tx)
        nbiot = NBIOTModule(1, tx=17, rx=16)

        # Or using UART object
        uart = machine.UART(1, tx=17, rx=16)
        nbiot = NBIOTModule(uart)

<!-- .. note:: -->

        See :class:`NBIOTUnit <unit.nbiot.NBIOTUnit>` for more details.
