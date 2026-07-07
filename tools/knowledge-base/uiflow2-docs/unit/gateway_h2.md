# GatewayH2 Unit

<!-- .. sku: U195 -->

<!-- .. include:: ../refs/unit.gateway_h2.ref -->

This library is the driver for Unit Gateway H2, and the unit communicates via UART.

Support the following products:

    |Unit Gateway H2|

<!-- .. note:: When using this unit, you need to flash the NCP firmware to the unit. For details, refer to the `ESP Zigbee NCP <https://docs.m5stack.com/en/esp_idf/zigbee/unit_gateway_h2/zigbee_ncp>`_ documentation. -->

## UiFlow2 Example

#### Switch Control

<!-- .. note:: To use this example, you need to flash this program onto an ESP32C6 or similar unit as a light node device. For details, refer to `HA_on_off_light <https://github.com/espressif/esp-zigbee-sdk/tree/main/examples/esp_zigbee_HA_sample/HA_on_off_light>`_ -->

Open the |cores3_switch_endpoint_example.m5f2| project in UiFlow2.

The example demonstrates group control and targeted device operation for light nodes through SwitchEndpoint of Gateway H2 unit.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Switch Control

The example demonstrates group control and targeted device operation for light nodes through SwitchEndpoint of Gateway H2 unit.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import GatewayH2Unit

title0 = None
label0 = None
label1 = None
label2 = None
label_addr = None
gateway_h2_0 = None
gateway_h2_0_ep = None
device_addr = None
device_count = None
device_list = None

def first_index(my_list, elem):
    try:
        index = my_list.index(elem) + 1
    except:
        index = 0
    return index

def gateway_h2_0_ep_bind_event(addr):
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        gateway_h2_0, \
        gateway_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list
    device_addr = addr
    print(device_addr)
    if first_index(device_list, device_addr) == 0:
        device_list.append(device_addr)
        device_count = device_count + 1
        label_addr.setText(str((str("new device addr: ") + str(device_addr))))
        gateway_h2_0_ep.off(device_addr)

def btnPWR_wasClicked_event(state):
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        gateway_h2_0, \
        gateway_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list
    if not not len(device_list):
        gateway_h2_0_ep.toggle()

def setup():
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        gateway_h2_0, \
        gateway_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("GatewayH2Unit Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "if has device connect", 2, 26, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "press the power button toggle", 2, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label(
        "connect device: ", 2, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_addr = Widgets.Label("None", 5, 115, 1.0, 0x00FF00, 0x222222, Widgets.FONTS.DejaVu18)

    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btnPWR_wasClicked_event)

    gateway_h2_0 = GatewayH2Unit(1, port=(1, 2))
    gateway_h2_0_ep = gateway_h2_0.create_switch_ep()
    gateway_h2_0_ep.set_bind_callback(gateway_h2_0_ep_bind_event)
    device_count = 0
    device_list = []

def loop():
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        gateway_h2_0, \
        gateway_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list
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

    None

## **API**

#### GatewayH2Unit

<!-- .. class:: unit.gateway_h2.GatewayH2Unit -->

    Create an GatewayH2Unit object.

    :param int id: The UART ID for communication with the GatewayH2 Unit. It can be 1, 2.
    :param port: A list or tuple containing the TX and RX pins for UART communication.

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from unit import GatewayH2Unit

            gateway_h2_unit = GatewayH2Unit(2, port=(1, 2))

<!-- .. method:: create_switch_endpoint() -->

        Create Switch Endpoint.

        :returns SwitchEndpoint: zigbee switch endpoint object.
        :return type: SwitchEndpoint

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                h2_switch_endpoint = gateway_h2_unit.create_switch_endpoint()

Refer to :ref:`switchendpoint` for more details about SwitchEndpoint.
