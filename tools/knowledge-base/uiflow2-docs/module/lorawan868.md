
# LoRaWAN868 Module

<!-- .. include:: ../refs/module.lorawan868.ref -->

COM.LoRaWAN is a LoRaWAN communication module in the M5Stack stackable module series, supporting node-to-node or LoRaWAN communication.

Support the following products:

|LoRaWAN868Module|

Micropython TX Example:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import LoRaWAN868Module
import time

lorawan868_0 = None

def setup():
    global lorawan868_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    lorawan868_0 = LoRaWAN868Module(1, (17, 16))
    lorawan868_0.wake_up()
    lorawan868_0.set_parameters(0, 0, 5, 0, 1, 8, 0, 0, 0)
    lorawan868_0.set_auto_low_power(False)
    print(lorawan868_0.query_chip_id())
    print(lorawan868_0.query_lorawan_mode())
    print(lorawan868_0.any())
    lorawan868_0.set_mode(LoRaWAN868Module.MODE_LORA)

def loop():
    global lorawan868_0
    M5.update()
    lorawan868_0.send_hex("Hello Lora!")
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

Micropython RX Example:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import LoRaWAN868Module

lorawan868_0 = None

def setup():
    global lorawan868_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    lorawan868_0 = LoRaWAN868Module(1, (17, 16))
    lorawan868_0.wake_up()
    lorawan868_0.set_parameters(0, 0, 5, 0, 1, 8, 0, 0, 0)
    lorawan868_0.set_auto_low_power(False)
    print(lorawan868_0.query_chip_id())
    print(lorawan868_0.query_lorawan_mode())
    print(lorawan868_0.any())
    lorawan868_0.set_mode(LoRaWAN868Module.MODE_LORA)
    lorawan868_0.enable_rx(0)

def loop():
    global lorawan868_0
    M5.update()
    if lorawan868_0.any():
        print(lorawan868_0.receive_data())
        lorawan868_0.enable_rx(0)

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

    |lorawan868_example_tx.m5f2|

    |lorawan868_example_rx.m5f2|

## class LoRaWAN868Module

## Constructors

<!-- .. class:: LoRaWAN868Module(id, port, band) -->

    Initialize the LoRaWANModule.

    :param int id: The UART ID to use for communication.
    :param  port: The UART port to use for communication, specified as a tuple of (rx, tx) pins.
    :param  band: The frequency to use for LoRa communication

    UIFLOW2:

## Methods

<!-- .. method:: LoRaWAN868Module.set_mode(mode) -->

    Set the mode of the LoRaWAN module.

    :param  mode: The mode to set.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_parameters(freq, power, sf, bw, cr, preamble, crc, iq_inv, save) -->

    Set the parameters of the LoRaWAN module.

    :param  freq: Set LoRa listening/sending frequency in Hz.
    :param  power: LoRa signal output power in dBm;
    :param  sf: Spreading factor, from 5~12
    :param  bw: Bandwidth 0 – 125K, 1 – 250K, 2 – 500K;
    :param  cr: 1 – 4/5, 2 – 4/6, 3 – 4/7, 4 – 4/8;
    :param  preamble: Preamble Length from 8~65535 bit;
    :param  crc: 0 – disable CRC check, 1 – enable CRC check;
    :param  iq_inv: 0 -- not inverted, 1 – inverted;
    :param  save: Save parameters to FLASH, 0 – not save, 1 – save.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.wake_up() -->

    Wake up the device through a serial port interrupt. After resetting, the device is in sleep state. In theory, sending any data through the serial port can trigger the interrupt and wake up the device.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.sleep() -->

    Put the device into low-power mode.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.reset() -->

    Reset the device.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.restore_factory_settings() -->

    Restore the device to factory settings. The parameters will reset and the device will enter sleep mode after response ends.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_copyright(enable) -->

    Enable or disable copyright information print when boot loader mode begins. Default is enable.

    :param bool enable: Set True to enable, False to disable.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_auto_low_power(enable) -->

    Enable or disable automatic low-power mode. Default is enable.

    :param bool enable: Set True to enable, False to disable.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.query_chip_id() -->

    Query the unique ID of the chip, which can be used to query the corresponding serial number.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.enable_rx(timeout) -->

    Enable the LoRaWAN module to receive data.

    :param int timeout: The timeout for the receive operation.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_deveui(deveui) -->

    Set or query the DevEui. DevEui must be 16 hex characters (0-9, A-F).

    :param  deveui: The DevEui to set. If None, query the current DevEui.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_appeui(appeui) -->

    Set or query the AppEui. AppEui must be 16 hex characters (0-9, A-F).

    :param  appeui: The AppEui to set. If None, query the current AppEui.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_appkey(appkey) -->

    Set or query the AppKey. AppKey must be 32 hex characters (0-9, A-F).

    :param  appkey: The AppKey to set. If None, query the current AppKey.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_nwkskey(nwkskey) -->

    Set or query the NwkSKey. NwkSKey must be 32 hex characters (0-9, A-F).

    :param  nwkskey: The NwkSKey to set. If None, query the current NwkSKey.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_appskey(appskey) -->

    Set or query the AppSKey. AppSKey must be 32 hex characters (0-9, A-F).

    :param  appskey: The AppSKey to set. If None, query the current AppSKey.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_devaddr(devaddr) -->

    Set or query the DevAddr. DevAddr must be 8 hex characters (0-9, A-F).

    :param  devaddr: The DevAddr to set. If None, query the current DevAddr.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_otaa_mode(enable) -->

    Set or query the OTAA mode. 1 for OTAA mode, 0 for ABP mode.

    :param bool enable: Set True for OTAA mode, False for ABP mode.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_adr(enable) -->

    Enable or disable the ADR (Adaptive Data Rate) function. Default is enabled.

    :param bool enable: Set True to enable ADR, False to disable.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_channel_mask(mask) -->

    Set or query the LoRaWAN working channel mask.

    :param  mask: The channel mask in hexadecimal format, e.g., 0000000000000000000000FF for channels 0~7.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.join_network() -->

    Join the network using OTAA (Over-The-Air Activation). This command triggers the join process.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_duty_cycle(cycle) -->

    Set or query the communication cycle in milliseconds. For example, 60000 means communication every 60 seconds.

    :param  cycle: The communication cycle in milliseconds.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_class_mode(mode) -->

    Set or query the device&#x27;s communication mode. Only Class A or Class C are valid.

    :param  mode: Set &quot;A&quot; for Class A or &quot;C&quot; for Class C.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_ack(enable) -->

    Enable or disable the ACK receipt function. If enabled, the device waits for acknowledgment from the gateway.

    :param bool enable: Set True to enable ACK, False to disable.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_app_port(port) -->

    Set or query the application port (fport) for upstream data. Valid range is 0~255.

    :param  port: The application port to set.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.set_retransmission_count(count) -->

    Set or query the number of retransmissions if communication fails. The valid range is 3~8.

    :param  count: The number of retransmissions to set. If None, query the current setting.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.send_hex(hex_data) -->

    Send hex data in LoRaWAN or LoRa mode. Hex characters must be in pairs (e.g., &quot;AABB&quot;).

    :param  hex_data: The hex data to send, up to 64 bytes.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.send_string(string_data) -->

    Send string data in LoRaWAN or LoRa mode. The string must consist of ASCII characters.

    :param  string_data: The string data to send, up to 64 bytes.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.query_lorawan_mode() -->

    Query if the device is in LoRaWAN or normal LoRa mode.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.save_parameters_to_flash() -->

    Save the current LoRa parameters to FLASH memory.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.at_cmd(cmd, data) -->

    Send an AT command to the LoRaWAN module.

    :param  cmd: The AT command to send.
    :param  data: The data to send with the AT command.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.at_query(cmd) -->

    Query the current settings of the LoRaWAN module.

    :param  cmd: The AT command to query.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.at_receive() -->

    Receive a response from the LoRaWAN module.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.flush() -->

    Clear the UART buffer.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.any() -->

    Check if there is any data in the UART buffer.

    UIFLOW2:

<!-- .. method:: LoRaWAN868Module.receive_data() -->

    Receive data from the LoRaWAN module.

    UIFLOW2:

## Constants

<!-- .. data:: LoRaWAN868Module.BAND_470 -->
<!-- .. data:: LoRaWAN868Module.BAND_868 -->
<!-- .. data:: LoRaWAN868Module.BAND_915 -->

    LoRa band frequency

<!-- .. data:: LoRaWAN868Module.MODE_LORA -->
<!-- .. data:: LoRaWAN868Module.MODE_LORAWAN -->

    LoRa Mode
