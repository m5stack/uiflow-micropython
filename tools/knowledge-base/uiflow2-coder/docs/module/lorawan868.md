
# LoRaWAN868 Module

COM.LoRaWAN is a LoRaWAN communication module in the M5Stack stackable module series, supporting node-to-node or LoRaWAN communication.

Support the following products:

LoRaWAN868Module

Micropython TX Example:

```python
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

## class LoRaWAN868Module

## Constructors

### `class LoRaWAN868Module(id, port, band)`

    Initialize the LoRaWANModule.

    - Parameter `id` (`int`): The UART ID to use for communication.
    - Parameter `port`: The UART port to use for communication, specified as a tuple of (rx, tx) pins.
    - Parameter `band`: The frequency to use for LoRa communication

## Methods

### `LoRaWAN868Module.set_mode(mode)`

    Set the mode of the LoRaWAN module.

    - Parameter `mode`: The mode to set.

### `LoRaWAN868Module.set_parameters(freq, power, sf, bw, cr, preamble, crc, iq_inv, save)`

    Set the parameters of the LoRaWAN module.

    - Parameter `freq`: Set LoRa listening/sending frequency in Hz.
    - Parameter `power`: LoRa signal output power in dBm;
    - Parameter `sf`: Spreading factor, from 5~12
    - Parameter `bw`: Bandwidth 0 – 125K, 1 – 250K, 2 – 500K;
    - Parameter `cr`: 1 – 4/5, 2 – 4/6, 3 – 4/7, 4 – 4/8;
    - Parameter `preamble`: Preamble Length from 8~65535 bit;
    - Parameter `crc`: 0 – disable CRC check, 1 – enable CRC check;
    - Parameter `iq_inv`: 0 -- not inverted, 1 – inverted;
    - Parameter `save`: Save parameters to FLASH, 0 – not save, 1 – save.

### `LoRaWAN868Module.wake_up()`

    Wake up the device through a serial port interrupt. After resetting, the device is in sleep state. In theory, sending any data through the serial port can trigger the interrupt and wake up the device.

### `LoRaWAN868Module.sleep()`

    Put the device into low-power mode.

### `LoRaWAN868Module.reset()`

    Reset the device.

### `LoRaWAN868Module.restore_factory_settings()`

    Restore the device to factory settings. The parameters will reset and the device will enter sleep mode after response ends.

### `LoRaWAN868Module.set_copyright(enable)`

    Enable or disable copyright information print when boot loader mode begins. Default is enable.

    - Parameter `enable` (`bool`): Set True to enable, False to disable.

### `LoRaWAN868Module.set_auto_low_power(enable)`

    Enable or disable automatic low-power mode. Default is enable.

    - Parameter `enable` (`bool`): Set True to enable, False to disable.

### `LoRaWAN868Module.query_chip_id()`

    Query the unique ID of the chip, which can be used to query the corresponding serial number.

### `LoRaWAN868Module.enable_rx(timeout)`

    Enable the LoRaWAN module to receive data.

    - Parameter `timeout` (`int`): The timeout for the receive operation.

### `LoRaWAN868Module.set_deveui(deveui)`

    Set or query the DevEui. DevEui must be 16 hex characters (0-9, A-F).

    - Parameter `deveui`: The DevEui to set. If None, query the current DevEui.

### `LoRaWAN868Module.set_appeui(appeui)`

    Set or query the AppEui. AppEui must be 16 hex characters (0-9, A-F).

    - Parameter `appeui`: The AppEui to set. If None, query the current AppEui.

### `LoRaWAN868Module.set_appkey(appkey)`

    Set or query the AppKey. AppKey must be 32 hex characters (0-9, A-F).

    - Parameter `appkey`: The AppKey to set. If None, query the current AppKey.

### `LoRaWAN868Module.set_nwkskey(nwkskey)`

    Set or query the NwkSKey. NwkSKey must be 32 hex characters (0-9, A-F).

    - Parameter `nwkskey`: The NwkSKey to set. If None, query the current NwkSKey.

### `LoRaWAN868Module.set_appskey(appskey)`

    Set or query the AppSKey. AppSKey must be 32 hex characters (0-9, A-F).

    - Parameter `appskey`: The AppSKey to set. If None, query the current AppSKey.

### `LoRaWAN868Module.set_devaddr(devaddr)`

    Set or query the DevAddr. DevAddr must be 8 hex characters (0-9, A-F).

    - Parameter `devaddr`: The DevAddr to set. If None, query the current DevAddr.

### `LoRaWAN868Module.set_otaa_mode(enable)`

    Set or query the OTAA mode. 1 for OTAA mode, 0 for ABP mode.

    - Parameter `enable` (`bool`): Set True for OTAA mode, False for ABP mode.

### `LoRaWAN868Module.set_adr(enable)`

    Enable or disable the ADR (Adaptive Data Rate) function. Default is enabled.

    - Parameter `enable` (`bool`): Set True to enable ADR, False to disable.

### `LoRaWAN868Module.set_channel_mask(mask)`

    Set or query the LoRaWAN working channel mask.

    - Parameter `mask`: The channel mask in hexadecimal format, e.g., 0000000000000000000000FF for channels 0~7.

### `LoRaWAN868Module.join_network()`

    Join the network using OTAA (Over-The-Air Activation). This command triggers the join process.

### `LoRaWAN868Module.set_duty_cycle(cycle)`

    Set or query the communication cycle in milliseconds. For example, 60000 means communication every 60 seconds.

    - Parameter `cycle`: The communication cycle in milliseconds.

### `LoRaWAN868Module.set_class_mode(mode)`

    Set or query the device&#x27;s communication mode. Only Class A or Class C are valid.

    - Parameter `mode`: Set &quot;A&quot; for Class A or &quot;C&quot; for Class C.

### `LoRaWAN868Module.set_ack(enable)`

    Enable or disable the ACK receipt function. If enabled, the device waits for acknowledgment from the gateway.

    - Parameter `enable` (`bool`): Set True to enable ACK, False to disable.

### `LoRaWAN868Module.set_app_port(port)`

    Set or query the application port (fport) for upstream data. Valid range is 0~255.

    - Parameter `port`: The application port to set.

### `LoRaWAN868Module.set_retransmission_count(count)`

    Set or query the number of retransmissions if communication fails. The valid range is 3~8.

    - Parameter `count`: The number of retransmissions to set. If None, query the current setting.

### `LoRaWAN868Module.send_hex(hex_data)`

    Send hex data in LoRaWAN or LoRa mode. Hex characters must be in pairs (e.g., &quot;AABB&quot;).

    - Parameter `hex_data`: The hex data to send, up to 64 bytes.

### `LoRaWAN868Module.send_string(string_data)`

    Send string data in LoRaWAN or LoRa mode. The string must consist of ASCII characters.

    - Parameter `string_data`: The string data to send, up to 64 bytes.

### `LoRaWAN868Module.query_lorawan_mode()`

    Query if the device is in LoRaWAN or normal LoRa mode.

### `LoRaWAN868Module.save_parameters_to_flash()`

    Save the current LoRa parameters to FLASH memory.

### `LoRaWAN868Module.at_cmd(cmd, data)`

    Send an AT command to the LoRaWAN module.

    - Parameter `cmd`: The AT command to send.
    - Parameter `data`: The data to send with the AT command.

### `LoRaWAN868Module.at_query(cmd)`

    Query the current settings of the LoRaWAN module.

    - Parameter `cmd`: The AT command to query.

### `LoRaWAN868Module.at_receive()`

    Receive a response from the LoRaWAN module.

### `LoRaWAN868Module.flush()`

    Clear the UART buffer.

### `LoRaWAN868Module.any()`

    Check if there is any data in the UART buffer.

### `LoRaWAN868Module.receive_data()`

    Receive data from the LoRaWAN module.

## Constants

### `LoRaWAN868Module.BAND_470`
### `LoRaWAN868Module.BAND_868`
### `LoRaWAN868Module.BAND_915`

    LoRa band frequency

### `LoRaWAN868Module.MODE_LORA`
### `LoRaWAN868Module.MODE_LORAWAN`

    LoRa Mode
