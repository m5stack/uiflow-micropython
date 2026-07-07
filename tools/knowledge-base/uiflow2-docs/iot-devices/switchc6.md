# SwitchC6

<!-- .. module:: switchc6 -->
    :synopsis: A module for controlling the SwitchC6 device

<!-- .. include:: ../refs/iot-devices.switchc6.ref -->

The SwitchC6 is a device that can be controlled using the M5Stack platform. This module provides functions to interact with the SwitchC6 device.

|SwitchC6|

## UiFlow2 Example

#### SwitchC6 Control

Open the |cores3_switchc6_example.m5f2| project in UiFlow2.

This example demonstrates how to control the SwitchC6 device using UiFlow2.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### SwitchC6 Control

This example demonstrates how to control the SwitchC6 device using MicroPython.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import switchc6

page0 = None
switch0 = None
label0 = None
label1 = None
label2 = None
label3 = None
switchc6_controller = None

switchc6_target_mac = None
switchc6_onoff = None
switchc6_voltage = None

def switch0_checked_event(event_struct):
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage
    switchc6_controller.toggle_switch("E4B3-2386-18B8", timeout=2000)

def switchc6_controller_off_event(args):
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage
    _, switchc6_target_mac, switchc6_onoff, switchc6_voltage = args
    label0.set_text(str(switchc6_target_mac))
    label1.set_text(str(switchc6_onoff))
    label2.set_text(str(switchc6_voltage))

def switch0_unchecked_event(event_struct):
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage
    switchc6_controller.set_switch("E4B3-2386-18B8", False, timeout=2000)

def switchc6_controller_on_event(args):
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage
    _, switchc6_target_mac, switchc6_onoff, switchc6_voltage = args
    label0.set_text(str(switchc6_target_mac))
    label1.set_text(str(switchc6_onoff))
    label2.set_text(str(switchc6_voltage))

def switch0_event_handler(event_struct):
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            switch0_checked_event(event_struct)
        else:
            switch0_unchecked_event(event_struct)
    return

def setup():
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    switch0 = m5ui.M5Switch(
        x=76,
        y=49,
        w=154,
        h=77,
        bg_c=0xE7E3E7,
        bg_c_checked=0x2196F3,
        circle_c=0xFFFFFF,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=19,
        y=151,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "label1",
        x=17,
        y=173,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label2 = m5ui.M5Label(
        "label2",
        x=17,
        y=195,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label3 = m5ui.M5Label(
        "label3",
        x=18,
        y=217,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    switch0.add_event_cb(switch0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    switchc6_controller = switchc6.SwitchC6Controller(
        ["E4B3-2386-18B8"], wifi_channel=0, verbose=False
    )
    switchc6_controller.set_callback(switchc6_controller_off_event, switchc6_controller.OFF)
    switchc6_controller.set_callback(switchc6_controller_on_event, switchc6_controller.ON)
    label3.set_text(str(switchc6_controller.get_firmware_version("E4B3-2386-18B8", timeout=5000)))
    label1.set_text(str(switchc6_controller.get_capacitor_voltage("E4B3-2386-18B8", timeout=5000)))
    label2.set_text(str(switchc6_controller.get_switch_status("E4B3-2386-18B8", timeout=5000)))

def loop():
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage
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

    None

## **API**

#### SwitchC6Controller

## SwitchC6Controller
Create a SwitchC6Controller instance to control M5Stack SwitchC6 devices.

:param target_mac: List of target MAC addresses in "XXXX-XXXX-XXXX" format.
:param wifi_channel: WiFi channel to use for communication (default is 0, which uses the current channel).
:param verbose: If True, print debug information (default is False).
:raises ValueError: If any MAC address in target_mac is not in the "XXXX-XXXX-XXXX" format.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        import switchc6

        controller = switchc6.SwitchC6Controller(
            target_mac=["1122-AABB-CCDD", "2233-BBEE-DDEE"],
            wifi_channel=0,
            verbose=True
        )

### `espnow_recv_callback`

### `set_switch`
Set the switch state of the target device.

:param target_mac: Target MAC address in "XXXX-XXXX-XXXX" format.
:param onoff: True to turn on, False to turn off.
:param timeout: Timeout in milliseconds for waiting for a response (default is 5000).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        switchc6.set_switch("1122-AABB-CCDD", True, timeout=5000)

### `toggle_switch`
Toggle the switch status of the target device.

:param target_mac: Target MAC address in "XXXX-XXXX-XXXX" format.
:param timeout: Timeout in milliseconds for waiting for a response (default is 5000).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        switchc6.toggle_switch("1122-AABB-CCDD", timeout=5000)

### `get_capacitor_voltage`
Get the capacitor voltage of the target device.

:param target_mac: Target MAC address in "XXXX-XXXX-XXXX" format.
:param timeout: Timeout in milliseconds for waiting for a response (default is 5000).
:returns: The capacitor voltage as a float.
:rtype: float

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        switchc6.get_capacitor_voltage("1122-AABB-CCDD", timeout=5000)

### `get_switch_status`
Get the switch status of the target device.

:param target_mac: Target MAC address in "XXXX-XXXX-XXXX" format.
:param timeout: Timeout in milliseconds for waiting for a response (default is 5000).
:returns: True if the switch is ON, False if it is OFF.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        switchc6.get_switch_status("1122-AABB-CCDD", timeout=5000)

### `set_callback`
Set a callback function for the specified trigger.

:param handler: The callback function to be called when the trigger occurs.
:param trigger: The trigger type (0 for OFF, 1 for ON).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        switchc6.set_callback(handler, trigger)

### `get_firmware_version`
Get the firmware version of the target device.

:param target_mac: Target MAC address in "XXXX-XXXX-XXXX" format.
:param timeout: Timeout in milliseconds for waiting for a response (default is 5000).

:returns: The firmware version as a string.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        switchc6.get_firmware_version("1122-AABB-CCDD", timeout=5000)
