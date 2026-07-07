
# UWB Unit

<!-- .. include:: ../refs/unit.uwb.ref -->

UWB is a Unit which integrates the UWB(Ultra Wide Band) communication protocol which uses nanosecond pulses to locate objects and define position and orientation. The design uses the Ai-ThinkerBU01 Transceiver module which is based on Decawave's DW1000 design. The internal STM32 chip with its integrated ranging algorithm,is capable of 10cm positioning accuracy and also supports AT command control. Applications include: Indoor wireless tracking/range finding of assets,which works by triangulating the position of the base station/s and tag (the base station resolves the position information and outputs it to the tag).
The firmware currently carried by this Unit only supports the transmission of ranging information, and does not currently support the transmission of custom information. When in use, it supports the configuration of 4 base station devices (using different IDs), and only a single tag device is allowed to operate at the same time.

Support the following products:

|UWBUnit|

Micropython Anchor Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import UWBUnit

label0 = None
label4 = None
label1 = None
label5 = None
label2 = None
label6 = None
label3 = None
label7 = None
circle0 = None
circle1 = None
circle2 = None
circle3 = None
uwb_0 = None

def uwb_0_0_online_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle0.setColor(color=0x33FF33, fill_c=0x33FF33)

def uwb_0_1_online_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle1.setColor(color=0x33FF33, fill_c=0x33FF33)

def uwb_0_2_online_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle2.setColor(color=0x33FF33, fill_c=0x33FF33)

def uwb_0_3_online_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle3.setColor(color=0x33FF33, fill_c=0x33FF33)

def uwb_0_0_offline_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle0.setColor(color=0xFF0000, fill_c=0xFF0000)

def uwb_0_1_offline_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle1.setColor(color=0xFF0000, fill_c=0xFF0000)

def uwb_0_2_offline_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle2.setColor(color=0xFF0000, fill_c=0xFF0000)

def uwb_0_3_offline_event(args):
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    circle3.setColor(color=0xFF0000, fill_c=0xFF0000)

def setup():
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Anchor0", 0, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("label4", 0, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu12)
    label1 = Widgets.Label("Anchor1", 80, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 80, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu12)
    label2 = Widgets.Label("Anchor2", 160, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 160, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu12)
    label3 = Widgets.Label("Anchor3", 240, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 240, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu12)
    circle0 = Widgets.Circle(38, 50, 15, 0xFF0000, 0xFF0000)
    circle1 = Widgets.Circle(118, 52, 15, 0xFF0000, 0xFF0000)
    circle2 = Widgets.Circle(193, 51, 15, 0xFF0000, 0xFF0000)
    circle3 = Widgets.Circle(273, 51, 15, 0xFF0000, 0xFF0000)

    uwb_0 = UWBUnit(2, port=(33, 32), device_mode=UWBUnit.TAG, verbose=False)
    uwb_0.set_callback(0, uwb_0.ONLINE, uwb_0_0_online_event)
    uwb_0.set_callback(1, uwb_0.ONLINE, uwb_0_1_online_event)
    uwb_0.set_callback(2, uwb_0.ONLINE, uwb_0_2_online_event)
    uwb_0.set_callback(3, uwb_0.ONLINE, uwb_0_3_online_event)
    uwb_0.set_callback(0, uwb_0.OFFLINE, uwb_0_0_offline_event)
    uwb_0.set_callback(1, uwb_0.OFFLINE, uwb_0_1_offline_event)
    uwb_0.set_callback(2, uwb_0.OFFLINE, uwb_0_2_offline_event)
    uwb_0.set_callback(3, uwb_0.OFFLINE, uwb_0_3_offline_event)
    uwb_0.set_measurement_interval(5)
    uwb_0.set_measurement(True)

def loop():
    global \
        label0, \
        label4, \
        label1, \
        label5, \
        label2, \
        label6, \
        label3, \
        label7, \
        circle0, \
        circle1, \
        circle2, \
        circle3, \
        uwb_0
    M5.update()
    uwb_0.update()
    label4.setText(str(uwb_0.get_distance(0)))
    label5.setText(str(uwb_0.get_distance(1)))
    label6.setText(str(uwb_0.get_distance(2)))
    label7.setText(str(uwb_0.get_distance(3)))

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

Micropython Tag Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import UWBUnit

label0 = None
label1 = None
uwb_0 = None

anchor_id = None

def btnA_wasClicked_event(state):  # noqa: N802
    global label0, label1, uwb_0, anchor_id
    anchor_id = (anchor_id + 1) % 4
    uwb_0.set_device_mode(UWBUnit.ANCHOR, anchor_id)
    label1.setText(str(uwb_0.get_device_id()))

def setup():
    global label0, label1, uwb_0, anchor_id

    M5.begin()
    label0 = Widgets.Label("label0", 29, 36, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label1 = Widgets.Label("0", 44, 98, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu72)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)

    anchor_id = 0
    uwb_0 = UWBUnit(2, port=(33, 32), device_mode=UWBUnit.ANCHOR, device_id=0, verbose=False)
    print(uwb_0.isconnected())
    print(uwb_0.get_version())
    if (uwb_0.get_device_mode()) == 1:
        label0.setText(str("Anchor"))
    else:
        label0.setText(str("Tag"))
    label1.setText(str(uwb_0.get_device_id()))

def loop():
    global label0, label1, uwb_0, anchor_id
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

UIFLOW2 Anchor Example:

UIFLOW2 Tag Example:

<!-- .. only:: builder_html -->

    |core2_uwb_anchor_example.m5f2|

    |stickc_plus2_uwb_tag_example.m5f2|

## class UWBUnit

## Constructors

<!-- .. class:: UWBUnit(id, port, device_mode, device_id, verbose) -->

    Create a UWB unit object.

    :param  id: UART ID.
    :param  port: The port that the unit is connected to.
    :param  device_mode: device mode.
    :param  device_id: device ID.
    :param bool verbose: verbose output.

    UIFLOW2:

## Methods

<!-- .. method:: UWBUnit.get_distance(index) -->

    Get the distance to the anchor ID (0 ~ 3).

    :return (float): distance in meters.
    :param int index: anchor ID (0 ~ 3).

    UIFLOW2:

<!-- .. method:: UWBUnit.get_device_id() -->

    Get the device ID.

    :return (int): device ID.

    UIFLOW2:

<!-- .. method:: UWBUnit.get_device_mode() -->

    Get the device mode.

    :return (int): device mode.

    UIFLOW2:

<!-- .. method:: UWBUnit.set_device_mode(mode, id) -->

    Set the device mode and ID.

    :param int mode: device mode.
        Options:
        - ``Anchor``: UWBUnit.ANCHOR
        - ``Tag``: UWBUnit.TAG
    :param int id: device ID.

    UIFLOW2:

<!-- .. method:: UWBUnit.isconnected() -->

    Check if the UWB unit is connected.

    :return: True if connected, False otherwise.

    UIFLOW2:

<!-- .. method:: UWBUnit.get_version() -->

    Get the UWB unit firmware version.

    :return: firmware version.

    UIFLOW2:

<!-- .. method:: UWBUnit.reset() -->

    Reset the UWB unit.

<!-- .. method:: UWBUnit.set_measurement_interval(interval) -->

    Set the measurement interval.

    :param int interval: measurement interval.

    UIFLOW2:

<!-- .. method:: UWBUnit.set_measurement(enable) -->

    Set the measurement output.

    :param bool enable: enable or disable measurement output.

    UIFLOW2:

<!-- .. method:: UWBUnit.set_callback(anchor, event, callback) -->

    Set the callback function for the anchor status.

    :param int anchor: anchor ID (0 ~ 3).
    :param int event: anchor status.
        Options:
        - ``ONLINE``: UWBUnit.ONLINE
        - ``OFFLINE``: UWBUnit.OFFLINE
    :param  callback: callback function.

    UIFLOW2:

<!-- .. method:: UWBUnit.update() -->

    Update the distances and anchor status.

    UIFLOW2:

## Constants

<!-- .. data:: UWBUnit.UNKNOWN -->
<!-- .. data:: UWBUnit.ANCHOR -->
<!-- .. data:: UWBUnit.TAG -->

    device role

<!-- .. data:: UWBUnit.OFFLINE -->
<!-- .. data:: UWBUnit.ONLINE -->
<!-- .. data:: UWBUnit._mode_map -->

    device status
