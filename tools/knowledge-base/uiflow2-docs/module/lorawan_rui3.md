# LoRaWAN-EU868 Module

<!-- .. include:: ../refs/module.lorawan_rui3.ref -->

The Module LoRaWAN868 is a LoRaWAN programmable data transfer unit based on the STM32WLE5 chip. The module supports long-range communication, low-power operation, and high sensitivity characteristics, making it suitable for IoT communication needs in a variety of complex environments.

Support the following products:

|Modlue-LoraWAN 868|

Micropython LoRaWAN-EU868 P2P Mode TX Example:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import LoRaWANModule_RUI3
import time

title0 = None
label0 = None
module_lorawaneu868_0 = None

def setup():
    global title0, label0, module_lorawaneu868_0

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LoraWAN868 P2P Send", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )
    label0 = Widgets.Label(
        "Press BtnA to Send", 1, 105, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18
    )

    module_lorawaneu868_0 = LoRaWANModule_RUI3(2, tx=17, rx=16, rst=13)
    module_lorawaneu868_0.set_network_mode(0)
    module_lorawaneu868_0.set_p2p_frequency(868000000)
    module_lorawaneu868_0.set_p2p_spreading_factor(8)
    module_lorawaneu868_0.set_p2p_bandwidth(0)
    module_lorawaneu868_0.set_p2p_tx_power(22)
    module_lorawaneu868_0.set_p2p_code_rate(0)
    module_lorawaneu868_0.set_p2p_preamble_length(8)

def loop():
    global title0, label0, module_lorawaneu868_0
    M5.update()
    label0.setText(str("Press BtnA to Send"))
    if BtnA.wasPressed():
        module_lorawaneu868_0.send_p2p_data("abcdef", timeout=0, to_hex=False)
        label0.setText(str("Sent"))
        time.sleep(1)

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

Micropython LoRaWAN-EU868 P2P Mode RX Example:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import LoRaWANModule_RUI3

title0 = None
label0 = None
module_lorawaneu868_0 = None

def setup():
    global title0, label0, module_lorawaneu868_0

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LoraWAN868 P2P Receive", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )
    label0 = Widgets.Label(
        "Touch to Receive", 2, 37, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18
    )

    M5.Lcd.setTextScroll(True)
    M5.Lcd.setTextColor(0xFFFFFF, 0x330000)
    module_lorawaneu868_0 = LoRaWANModule_RUI3(2, tx=17, rx=18, rst=7)
    module_lorawaneu868_0.set_network_mode(0)
    module_lorawaneu868_0.set_p2p_frequency(868000000)
    module_lorawaneu868_0.set_p2p_spreading_factor(8)
    module_lorawaneu868_0.set_p2p_bandwidth(0)
    module_lorawaneu868_0.set_p2p_tx_power(22)
    module_lorawaneu868_0.set_p2p_code_rate(0)
    module_lorawaneu868_0.set_p2p_preamble_length(8)

def loop():
    global title0, label0, module_lorawaneu868_0
    M5.update()
    if M5.Touch.getCount():
        M5.Lcd.printf(
            (str((str((module_lorawaneu868_0.get_p2p_receive_data(5000, False))))) + str("\n"))
        )

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

UIFLOW2 LoRaWAN-EU868 P2P Mode TX Example:

    |module_lorawan868_p2p_tx_core_example.m5f2|

UIFLOW2 LoRaWAN-EU868 P2P Mode RX Example:

    |module_lorawan868_p2p_rx_cores3_example.m5f2|

## **API**

#### LoRaWANModule_RUI3

## LoRaWANModule_RUI3
Create an AtomDTULoRaWANRUI3Base object.

:param int id: The UART ID to use (0, 1, or 2). Default is 2.
:param port: A list or tuple containing the TX and RX pin numbers.
:type port: list | tuple
:param bool debug: Whether to enable debug mode. Default is False.

MicroPython Code Block:

    .. code-block:: python

        from base import AtomDTULoRaWANRUI3Base

        lorawan_rui3 = AtomDTULoRaWANRUI3Base(2, port=(19, 22))

### `set_abp_config`
Configure the device for ABP (Activation By Personalization) mode.

:param str dev_addr: The device address for ABP configuration.
:param str apps_key: The application session key for encryption.
:param str nwks_key: The network session key for communication.

MicroPython Code Block:

    .. code-block:: python

        lorawan_rui3.set_abp_config(
            dev_addr="26011D89",
            apps_key="2B7E151628AED2A6ABF7158809CF4F3C",
            nwks_key="2B7E151628AED2A6ABF7158809CF4F3C"
        )

### `get_abp_config`
Retrieve the current ABP configuration.

:returns: A tuple containing (device_address, apps_key, networks_key).
:rtype: tuple[str, str, str]

MicroPython Code Block:

    .. code-block:: python

        print(lorawan_rui3.get_abp_config())

### `set_otaa_config`
Configure the device for OTAA (Over-The-Air Activation) mode.

:param str device_eui: The device EUI for OTAA configuration.
:param str app_key: The application key for encryption.
:param str app_eui: The application EUI for OTAA configuration.

MicroPython Code Block:

    .. code-block:: python

        lorawan_rui3.set_otaa_config(
            device_eui="2CF7F1C0420000AA",
            app_key="2B7E151628AED2A6ABF7158809CF4F3C"
            app_eui="80000000000000AA",
        )

### `get_otaa_config`
Retrieve the current OTAA configuration.

:returns: A tuple containing (device_eui, app_key, app_eui).
:rtype: tuple[str, str, str]

MicroPython Code Block:

    .. code-block:: python

        print(lorawan_rui3.get_otaa_config())
