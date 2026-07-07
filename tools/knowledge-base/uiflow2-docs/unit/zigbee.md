# Zigbee Unit

<!-- .. include:: ../refs/unit.zigbee.ref -->

Zigbee is a self-organizing network communication module launched by M5Stack.
The module adopts the CC2630F128 solution, integrates the Zigbee protocol stack
internally, and provides an open serial communication interface. It features an
external antenna, with a stable single-node communication distance of up to 1 km
and supports up to 200 levels of router depth. Through MESH networking, it can
significantly extend the range of your IoT applications, offering both ultra-low
power consumption and high sensitivity. The Zigbee network can support hundreds
of nodes and has enhanced security features, providing a complete and
interoperable IoT solution for home and building automation.

Support the following products:

    |ZigbeeUnit|

Micropython TX Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import ZigbeeUnit
import time

label0 = None
zigbee_0 = None

def setup():
    global label0, zigbee_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 67, 43, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    zigbee_0 = ZigbeeUnit(1, port=(18, 17), verbose=True)
    zigbee_0.set_module_param(
        ZigbeeUnit.DEVICE_TYPE_COORDINATOR,
        0x1620,
        11,
        ZigbeeUnit.TRANSFER_MODE_PASS_THROUGH,
        0x6677,
    )
    label0.setText(str("start"))

def loop():
    global label0, zigbee_0
    M5.update()
    zigbee_0.p2p_transmission(0x0066, "p2p")
    time.sleep(3)
    zigbee_0.broadcast("broadcast")
    time.sleep(3)

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

Micropython RX Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import ZigbeeUnit

label0 = None
zigbee_0 = None

zigbee_str_data = None
zigbee_dest_address = None
zigbee_src_address = None

def zigbee_0_receive_event(dest_address, src_address, received_data):
    global label0, zigbee_0, zigbee_str_data, zigbee_dest_address, zigbee_src_address
    zigbee_dest_address = dest_address
    zigbee_src_address = src_address
    try:
        zigbee_str_data = received_data.decode()
    except:
        zigbee_str_data = str(received_data)
    label0.setText(str(zigbee_str_data))

def setup():
    global label0, zigbee_0, zigbee_str_data, zigbee_dest_address, zigbee_src_address

    M5.begin()
    label0 = Widgets.Label("label0", 21, 83, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    zigbee_0 = ZigbeeUnit(1, port=(33, 32), verbose=True)
    zigbee_0.set_module_param(
        ZigbeeUnit.DEVICE_TYPE_ROUTER, 0x1620, 11, ZigbeeUnit.TRANSFER_MODE_PASS_THROUGH, 0x0066
    )
    while not (zigbee_0.isconnected()):
        pass
    label0.setText(str(zigbee_0.get_custom_address()))
    zigbee_0.receive_none_block(zigbee_0_receive_event)

def loop():
    global label0, zigbee_0, zigbee_str_data, zigbee_dest_address, zigbee_src_address
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

UIFLOW2 TX Example:

UIFLOW2 RX Example:

<!-- .. only:: builder_html -->

    |cores3_zigbee_tx_example.m5f2|

    |stickc_plus2_zigbee_rx_example.m5f2|

## class ZigbeeUnit

## Constructors

<!-- .. class:: ZigbeeUnit(id: Literal[0, 1, 2], port: list | tuple, verbose: bool=True) -->

    Create a Zigbee unit.

    :param id: The ID of the unit.
    :param port: The port that the unit is connected to.
    :param verbose: Print the log information. Default is True.

    UIFLOW2:

## Methods

<!-- .. method:: ZigbeeUnit.set_module_param(device_type: int, pan_id: int, channel: int, transfer_mode: int, custom_address: int, ant_type: int, encryption_enable=ENCRYPTION_ENABLE, encryption_key=b'\x11\x12\x13\x14', node_type=DEVICE_TYPE_ROUTER, node_ant_type=ANT_TYPRE_ON_BOARD, node_transfer_mode=TRANSFER_MODE_PASS_THROUGH, node_custom_address=0x0066,) -->

    :param int device_type: The device type of the Zigbee module.
    :param int pan_id: The PAN ID of the Zigbee module. The PAN ID is a 16-bit value that is used to identify the network.
    :param int channel: The channel of the Zigbee module. The channel range is from 11 to 26
    :param int transfer_mode: The transfer mode of the Zigbee module.
    :param int custom_address: The custom address of the Zigbee module.
    :param int ant_type: The antenna type of the Zigbee module.
    :param int encryption_enable: The encryption status of the Zigbee module.
    :param bytes encryption_key: The encryption key of the Zigbee module.
    :param int node_type: The node type of the Zigbee module.
    :param int node_ant_type: The antenna type of the Zigbee node.
    :param int node_transfer_mode: The transfer mode of the Zigbee node.
    :param int node_custom_address: The custom address of the Zigbee node.

    Set the parameters of the Zigbee module.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.set_device_type(device_type: int) -->

    :param int device_type: The device type of the Zigbee module.

    Set the device type of the Zigbee module.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.set_pan_id(pan_id: int) -->

    :param int pan_id: The PAN ID of the Zigbee module.

    Set the PAN ID of the Zigbee module.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.set_channel(channel: int) -->

    :param int channel: The channel of the Zigbee module.

    Set the channel of the Zigbee module.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.set_transfer_mode(transfer_mode: int) -->

    :param int transfer_mode: The transfer mode of the Zigbee module.

    Set the transfer mode of the Zigbee module.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.get_custom_address() -> int -->

    Get the custom address of the Zigbee module.

    :return: The custom address of the Zigbee module.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.set_custom_address(custom_address: int) -->

    :param int custom_address: The custom address of the Zigbee module.

    Set the custom address of the Zigbee module.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.set_ant_type(ant_type: int) -->

    :param int ant_type: The antenna type of the Zigbee module.

    Set the antenna type of the Zigbee module.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.get_short_address() -> int -->

    Get the short address of the Zigbee module.

    :return: The short address of the Zigbee module.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.isconnected() -> bool -->

    Check whether the Zigbee module is connected to the Zigbee network.

    :return: True if the Zigbee module is connected to the Zigbee network, False otherwise.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.receive_none_block(receive_callback) -->

    :param receive_callback: The callback function that is called when the Zigbee module receives data.

    Receive data from the Zigbee module.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.stop_receive() -->

    Stop receiving data from the Zigbee module.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.p2p_transmission(address: int, data: bytes) -->

    :param int address: The custom address of the Zigbee module that the data is sent to.
    :param bytes data: The data that is sent to the Zigbee module.

    Send data to the Zigbee module.

    UIFLOW2:

<!-- .. method:: ZigbeeUnit.broadcast(data: bytes) -->

    :param bytes data: The data that is sent to the Zigbee module.

    Broadcast data to all Zigbee modules.

    UIFLOW2:
