# Atom DTU LoRaWAN-Series(RAK3172) Base

<!-- .. sku:U184-CN470,U184-AS923,U184-EU868,U184-US915 -->

<!-- .. include:: ../refs/base.lorawan_rui3.ref -->

SKU: A152-CN470, A152-US915, A152-EU868

The Atom DTU LoRaWAN-Series is a LoRaWAN programmable data transfer unit (DTU) based on the STM32WLE5 chip. The module supports long-range communication, low-power operation, and high sensitivity characteristics, making it suitable for IoT communication needs in a variety of complex environments.

- **Frequency band support**: CN470 (470MHz), EU868 (868MHz), US915 (915MHz)
- **Communication protocol**:

  - Supports LoRaWAN Class A, Class B, Class C modes
  - Supports LoRa Point-to-Point (P2P) communication mode.

- **Communication Interface**:

  - UART interface: Used to send AT commands to control LoRaWAN network access, data sending/receiving, P2P mode communication, etc.
  - RS485 interface: supports wired communication of industrial equipment with high reliability.

- **Internet access method**:

  - OTAA (Over-The-Air Activation)
  - ABP (Activation By Personalization)

Support the following products:

================== ================== ==================
|LoRaWAN-CN470|       |LoRaWAN-EU868| |LoRaWAN-US915|
================== ================== ==================

Micropython LoRaWAN-EU868 LoRaWAN OTAA Mode Example:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import RGB
from base import AtomDTULoRaWANRUI3Base

rgb = None
base_lorawaneu868 = None

def setup():
    global rgb, base_lorawaneu868

    M5.begin()
    rgb = RGB()
    base_lorawaneu868 = AtomDTULoRaWANRUI3Base(2, port=(19, 22))
    base_lorawaneu868.set_network_mode(1)
    base_lorawaneu868.set_otaa_config(
        "70B3D57ED007006A", "A843ECB026197C981D67AEFACC72D01E", "70B3D57ED0063472"
    )
    base_lorawaneu868.set_rx_delay_on_window1(1)
    base_lorawaneu868.set_rx_delay_on_window2(2)
    base_lorawaneu868.set_rx_data_rate_on_windows2(0)
    base_lorawaneu868.set_lorawan_node_class("C")
    if base_lorawaneu868.join_network(10000):
        print("Success join the network")
        rgb.fill_color(0x33FF33)
        base_lorawaneu868.send_data(1, "AABBCC", 0)
    else:
        print("Failed Join to the network")
        rgb.fill_color(0xFF0000)

def loop():
    global rgb, base_lorawaneu868
    M5.update()
    if BtnA.wasPressed():
        if (base_lorawaneu868.get_received_data_count()) != 0:
            print(base_lorawaneu868.get_received_data_string())
        else:
            print("Message queue is empty")

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

Micropython LoRaWAN-EU868 P2P Mode TX Example:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import RGB
from base import AtomDTULoRaWANRUI3Base

rgb = None
base_lorawaneu868 = None

def setup():
    global rgb, base_lorawaneu868

    M5.begin()
    rgb = RGB()
    base_lorawaneu868 = AtomDTULoRaWANRUI3Base(2, port=(19, 22))
    base_lorawaneu868.set_network_mode(0)
    base_lorawaneu868.set_p2p_frequency(600000000)
    base_lorawaneu868.set_p2p_spreading_factor(7)
    base_lorawaneu868.set_p2p_bandwidth(0)
    base_lorawaneu868.set_p2p_tx_power(14)
    base_lorawaneu868.set_p2p_code_rate(0)
    base_lorawaneu868.set_p2p_preamble_length(8)
    print("Press the button to send P2P message")

def loop():
    global rgb, base_lorawaneu868
    M5.update()
    if BtnA.wasPressed():
        base_lorawaneu868.send_p2p_data("AABBCC", timeout=0, to_hex=False)

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
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import RGB
from base import AtomDTULoRaWANRUI3Base

rgb = None
base_lorawaneu868 = None

def setup():
    global rgb, base_lorawaneu868

    M5.begin()
    rgb = RGB()
    base_lorawaneu868 = AtomDTULoRaWANRUI3Base(2, port=(19, 22))
    base_lorawaneu868.set_network_mode(0)
    base_lorawaneu868.set_p2p_frequency(600000000)
    base_lorawaneu868.set_p2p_spreading_factor(7)
    base_lorawaneu868.set_p2p_bandwidth(0)
    base_lorawaneu868.set_p2p_tx_power(14)
    base_lorawaneu868.set_p2p_code_rate(0)
    base_lorawaneu868.set_p2p_preamble_length(8)
    print("Press the button to send P2P message")

def loop():
    global rgb, base_lorawaneu868
    M5.update()
    if BtnA.wasPressed():
        base_lorawaneu868.send_p2p_data("AABBCC", timeout=0, to_hex=False)

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

UIFLOW2 LoRaWAN-EU868 LoRaWAN OTAA Mode Example:

    |base_lorawan868_otaa_atom_lite_example.m5f2|

UIFLOW2 LoRaWAN-EU868 P2P Mode TX Example:

    |base_lorawan868_p2p_tx_atom_lite_example.m5f2|

UIFLOW2 LoRaWAN-EU868 P2P Mode RX Example:

    |base_lorawan868_p2p_rx_atom_lite_example.m5f2|

## **API**

#### AtomDTULoRaWANRUI3Base

## AtomDTULoRaWANRUI3Base
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
