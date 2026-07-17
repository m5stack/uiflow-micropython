# LoRaWAN-EU868 Module

The Module LoRaWAN868 is a LoRaWAN programmable data transfer unit based on the STM32WLE5 chip. The module supports long-range communication, low-power operation, and high sensitivity characteristics, making it suitable for IoT communication needs in a variety of complex environments.

Support the following products:

Modlue-LoraWAN 868

Micropython LoRaWAN-EU868 P2P Mode TX Example:

```python
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

## **API**

#### LoRaWANModule_RUI3

## `LoRaWANModule_RUI3`
Create an AtomDTULoRaWANRUI3Base object.

- Parameter `id` (`int`): The UART ID to use (0, 1, or 2). Default is 2.
- Parameter `port`: A list or tuple containing the TX and RX pin numbers.
- Type of `port`: list | tuple
- Parameter `debug` (`bool`): Whether to enable debug mode. Default is False.

```python
from base import AtomDTULoRaWANRUI3Base

lorawan_rui3 = AtomDTULoRaWANRUI3Base(2, port=(19, 22))
```

### `set_abp_config`
Configure the device for ABP (Activation By Personalization) mode.

- Parameter `dev_addr` (`str`): The device address for ABP configuration.
- Parameter `apps_key` (`str`): The application session key for encryption.
- Parameter `nwks_key` (`str`): The network session key for communication.

```python
lorawan_rui3.set_abp_config(
    dev_addr="26011D89",
    apps_key="2B7E151628AED2A6ABF7158809CF4F3C",
    nwks_key="2B7E151628AED2A6ABF7158809CF4F3C"
)
```

### `get_abp_config`
Retrieve the current ABP configuration.

- Returns: A tuple containing (device_address, apps_key, networks_key).
- Return type: tuple[str, str, str]

```python
print(lorawan_rui3.get_abp_config())
```

### `set_otaa_config`
Configure the device for OTAA (Over-The-Air Activation) mode.

- Parameter `device_eui` (`str`): The device EUI for OTAA configuration.
- Parameter `app_key` (`str`): The application key for encryption.
- Parameter `app_eui` (`str`): The application EUI for OTAA configuration.

```python
lorawan_rui3.set_otaa_config(
    device_eui="2CF7F1C0420000AA",
    app_key="2B7E151628AED2A6ABF7158809CF4F3C"
    app_eui="80000000000000AA",
)
```

### `get_otaa_config`
Retrieve the current OTAA configuration.

- Returns: A tuple containing (device_eui, app_key, app_eui).
- Return type: tuple[str, str, str]

```python
print(lorawan_rui3.get_otaa_config())
```
