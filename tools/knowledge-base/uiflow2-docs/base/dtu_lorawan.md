# Atom DTU LoRaWAN-Series Base

<!-- .. sku: K061/K062/K063 -->

<!-- .. include:: ../refs/base.dtu_lorawan.ref -->

This is the driver library for the Atom DTU LoRaWAN-Series Base to accept and send data from the LoRaWAN module.

Support the following products:

    ===================== ===================== =====================
    |Atom DTU LoRaWAN470| |Atom DTU LoRaWAN868| |Atom DTU LoRaWAN915|
    ===================== ===================== =====================

## UiFlow2 Example

#### LoRaWAN communication

Open the |atoms3r_dtu_lorawan_example.m5f2| project in UiFlow2.

This example shows how to receive and send data using the Atom DTU LoRaWAN Base.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### LoRaWAN communication

This example shows how to receive and send data using the Atom DTU LoRaWAN Base.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomDTULoRaWANBase

title0 = None
base_lorawan470 = None

def setup():
    global title0, base_lorawan470

    M5.begin()
    title0 = Widgets.Title("LoRaWAN", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    base_lorawan470 = AtomDTULoRaWANBase(2, port=(5, 6))
    base_lorawan470.set_join_mode(0)
    base_lorawan470.config_otaa("xxxx", "xxxx", "xxxx")
    base_lorawan470.set_frequency_band_mask("0400")
    base_lorawan470.set_rx_window_param(0, 0, 505300000)
    base_lorawan470.set_class_mode(2)
    base_lorawan470.set_uplink_downlink_mode(1)
    base_lorawan470.set_uplink_app_port(1)
    base_lorawan470.join(1, 1, 20, 20)
    print("LoRaWAN configuration complete")

def loop():
    global title0, base_lorawan470
    M5.update()
    if BtnA.isPressed():
        print("Send Message")
        base_lorawan470.send_data("11", 1, 15)

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

#### AtomDTULoRaWANBase

## AtomDTULoRaWANBase
Create an AtomDTULoRaWANBase object

:param int id: The UART ID to use (0, 1, or 2). Default is 2.
:param port: A list or tuple containing the TX and RX pin numbers.
:type port: list | tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from base import AtomDTULoRaWANBase

        dtu_lorawan = AtomDTULoRaWANBase(0, (6, 5))

### `deinit`

## LoRaWAN_470
Create an LoRaWAN object.

:param int tx: The UART TX pin number.
:param int rx: The UART RX pin number.
:param bool debug: Whether to enable debug mode.

MicroPython Code Block:

    .. code-block:: python

        from driver.asr650x import LoRaWAN_470

        lora = LoRaWAN_470(tx=17, rx=16)

### `config_abp`
Config the ABP join mode information.

:param str devaddr: The device address.
:param str appskey: The application session key.
:param str nwkskey: The network session key.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        lora.config_abp("0037CAE1FC3542B9", "70B3D57ED003B699", "67FA4ED1075A20573BCDD7594C458698")

### `config_ABP`
Config the ABP join mode information.
Parameter:
Return:
    None

### `get_abp_config`
Get the ABP join mode information.

:returns: The ABP join mode information(devaddr, appskey, newskey).
:rtype: tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        lora.get_abp_config()

### `get_ABP_config`
Get the ABP join mode information.
Parameter:
    self
Return:
    (devaddr, appskey, newskey)

### `config_otaa`
Config the OTAA join mode information.

:param str deveui: The device EUI.
:param str appeui: The application EUI.
:param str appkey: The application key.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        lora.config_otaa("0037CAE1FC3542B9", "70B3D57ED003B699", "67FA4ED1075A20573BCDD7594C458698")

### `config_OTAA`
Config the OTAA join mode information.
Parameter:

Return:
    True
    False

### `get_otaa_config`
Get the OTAA join mode information.

:returns: The OTAA join mode information(deveui, appeui, appkey).
:rtype: tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        lora.get_otaa_config()

### `get_OTAA_config`
Get the OTAA join mode information.
Parameter:
Return:
    (deveui, appeui, appkey)

### `check_join_status`
Check the LoRaWAN network join status.

:returns: The LoRaWAN network join status.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        lora.check_join_status()

### `check_uplink_status`
Check the data uplink status.

:returns: The data uplink status.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        lora.check_uplink_status()

### `check_downlink_data`
Check downlink data, if have downlink data, return the message.

:param int timeout: The timeout time.
:returns: False if no downlink data, otherwise return the downlink data.
:rtype: bool | str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        lora.check_downlink_data()

## LoRaWAN_Asr650x
Create an LoRaWAN object.

:param machine.UART uart: The UART object.
:param bool debug: Whether to enable debug mode.

MicroPython Code Block:

    .. code-block:: python

        from driver.asr650x import LoRaWAN_Asr650x

        lora = LoRaWAN_Asr650x(uart)

### `get_product_serial_number`
AT+CGSN?

### `reset_module_to_default`
Reset module to default config.
Parameter:
    None
Return:
    True
    False

### `get_device_address`

### `get_DevAddr`
Get Device address.
Parameter:
    None
Return:
    DevAddr: xxxxxxxx  4 bytes

### `set_device_address`

### `set_DevAddr`
Set Device address.
Parameter:
    devaddr: xx:xx:xx:xx  4 bytes
Return:
    True
    False

### `get_device_eui`

### `get_DevEui`
Get Device EUI.
Parameter:
    None
Return:
    DevEui: xxxxxxxxxxxxxxxx 8 byte

### `set_device_eui`

### `set_DevEui`
Set Device EUI.
Parameter:
    deveui: xxxxxxxxxxxxxxxx 8 bytes
Return:
    True
    False

### `get_app_eui`

### `get_AppEui`
Get Application EUI.
Parameter:
    None
Return:
    AppEui: xxxxxxxxxxxxxxxx 8 bytes

### `set_app_eui`

### `set_AppEui`
Set Application EUI.
Parameter:
    appeui: xxxxxxxxxxxxxxxx 8 bytes
Return:
    True
    False

### `get_appkey`

### `get_AppKey`
get App Key.
Parameter:
    None
Return:
    key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 16 bytes
    False

### `set_appkey`

### `set_AppKey`
Set App Key.
Parameter:
    None
Return:
    key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 16 bytes
    False

### `get_app_session_key`

### `get_APPSKEY`
Set App Session Key.
Parameter:
    AppSKEY: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 16 bytes
Return:
    True
    False

### `set_app_session_key`

### `set_APPSKEY`
Set App Session Key.
Parameter:
    AppSKEY: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 16 bytes
Return:
    True
    False

### `get_nwk_session_key`

### `get_NWKSKEY`
Get Network Session Key.
Parameter:
    None
Return:
    NWKSKEY: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 16 bytes
    False

### `set_nwk_session_key`

### `set_NWKSKEY`
Set Network Session Key.
Parameter:
    NWKSKEY: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 16 bytes
Return:
    True
    False

### `get_join_mode`
Set LoRaWAN Mode.
Parameter:
    None
Return:
    True
    False

### `set_join_mode`
Set the LoRaWAN join mode.

:param int mode: The LoRaWAN join mode.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        lora.set_join_mode(0)

### `get_frequency_band_mask`
Get frequency band mask.
Parameter:
    None
Return:
    mask

### `set_frequency_band_mask`
Set the frequency band mask.

:param str mask: The frequency band mask.

MicroPython Code Block:

    .. code-block:: python

        lora.set_frequency_band_mask("0001")

### `get_uplink_downlink_mode`
Get uplink and downlink mode.
Parameter:
    None
Return:
    mode:
        1 Same frequency mode
        2 Inter-frequency mode

### `set_uplink_downlink_mode`
Set the uplink and downlink frequency.

:param int mode: The uplink and downlink frequency.

MicroPython Code Block:

    .. code-block:: python

        lora.set_uplink_downlink_mode(1)

### `get_work_mode`
Get model work mode.
Parameter:
    None
Return:
    mode
    False

### `set_work_mode`
Get model work mode.
Parameter:
    mode
        only support 2
Return:
    True
    False

### `get_class_mode`
Get class mode.
Parameter:
    None
Return:
    class mode:
        0 classA
        1 classB
        2 classB
    False

### `set_class_mode`
Set the class mode, if the class mode is 0, the branch, para1, para2, para3, para4 will be ignored.

:param int class_mode: The class mode.
:param int branch: The branch selection.
:param int para1: Set the beacon frequency, unit is Hz.
:param int para2: Set the beacon data rate.
:param int para3: Set ping frequency, unit is Hz.
:param int para4: Set ping data rate.

MicroPython Code Block:

    .. code-block:: python

        lora.set_class_mode(0, 0, 0, 0, 0, 0)

### `get_status`
Get status.
Parameter:
    None
Return:
    status:
        0
        1
        2
        3
        4
        5
        6
        7
        8
    False

### `join`
Join the LoRaWAN network.

:param int para1: 0 stop join, 1 start join.
:param int para2: 0 close auto join, 1 open auto join.
:param int para3: join interval, unit is second(7~255).
:param int para4: join retry times(1~256).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        lora.join(1, 1, 8, 1)

        lora.join(0)

### `send_data`
Send data payload to LoRaWAN gateway.

:param str payload: The data to send.
:param int confirm: The confirm mode.
:param int nbtrials: The number of trials.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        lora.send_data("Hello, World!", 1, 1)

### `receive_data`
Receive downlink data if have.
Parameter:
    None
Return:
    data
    False

### `set_uplink_confirm_mode`
Set uplink confirmed mode, setting before send data.
Parameter:
    mode:
        0 unconfirmed mode
        1 confirmed
Return:
    True
    False

### `set_uplink_app_port`
Set the uplink app port.

:param int port: The uplink app port.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        lora.set_uplink_app_port(1)

### `set_datarate`
Set datarate.
Parameter:
    rate:
        0 SF12 BW125
        1 SF11 BW125
        2 SF10 BW125
        3 SF9  BW125
        4 SF8  BW125
        5 SF7  BW125
Return:
    True
    False

### `set_report_mode`
Set report mode and report interval.
Parameter:
    mode:
        0
        1
    interval:  s
Return:
    True
    False

### `set_tx_power`
Set tx power dBm.
Parameter:
    power:
        0 17dBm
        1 15dBm
        2 13dBm
        3 11dBm
        4 9dBm
        5 7dBm
        6 5dBm
        7 3dBm
Return:
    True
    False

### `enable_adaptive_datarate`
Set adaptive datarate status.
Parameter:
    status:
        0 disable
        1 enable
Return:
    True
    False

### `set_rx_window_param`
Set the receive window parameter.

:param int rx1_offset: The RX1 offset.
:param int rx2_dr: The RX2 data rate.
:param int rx2_freq: The RX2 frequency.

MicroPython Code Block:

    .. code-block:: python

        lora.set_rx_window_param(0, 0, 868100000)

### `set_rx1_delay_time`
Set receive window param.
Parameter:
    delay
Return:
    True
    False
