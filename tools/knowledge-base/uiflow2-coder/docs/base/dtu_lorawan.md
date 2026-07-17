# Atom DTU LoRaWAN-Series Base

This is the driver library for the Atom DTU LoRaWAN-Series Base to accept and send data from the LoRaWAN module.

Support the following products:

    Atom DTU LoRaWAN470 Atom DTU LoRaWAN868 Atom DTU LoRaWAN915

## MicroPython Example

#### LoRaWAN communication

This example shows how to receive and send data using the Atom DTU LoRaWAN Base.

```python
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

## **API**

#### AtomDTULoRaWANBase

## `AtomDTULoRaWANBase`
Create an AtomDTULoRaWANBase object

- Parameter `id` (`int`): The UART ID to use (0, 1, or 2). Default is 2.
- Parameter `port`: A list or tuple containing the TX and RX pin numbers.
- Type of `port`: list | tuple

```python
from base import AtomDTULoRaWANBase

dtu_lorawan = AtomDTULoRaWANBase(0, (6, 5))
```

### `deinit`

## `LoRaWAN_470`
Create an LoRaWAN object.

- Parameter `tx` (`int`): The UART TX pin number.
- Parameter `rx` (`int`): The UART RX pin number.
- Parameter `debug` (`bool`): Whether to enable debug mode.

```python
from driver.asr650x import LoRaWAN_470

lora = LoRaWAN_470(tx=17, rx=16)
```

### `config_abp`
Config the ABP join mode information.

- Parameter `devaddr` (`str`): The device address.
- Parameter `appskey` (`str`): The application session key.
- Parameter `nwkskey` (`str`): The network session key.

```python
lora.config_abp("0037CAE1FC3542B9", "70B3D57ED003B699", "67FA4ED1075A20573BCDD7594C458698")
```

### `config_ABP`
Config the ABP join mode information.
Parameter:
Return:
    None

### `get_abp_config`
Get the ABP join mode information.

- Returns: The ABP join mode information(devaddr, appskey, newskey).
- Return type: tuple

```python
lora.get_abp_config()
```

### `get_ABP_config`
Get the ABP join mode information.
Parameter:
    self
Return:
    (devaddr, appskey, newskey)

### `config_otaa`
Config the OTAA join mode information.

- Parameter `deveui` (`str`): The device EUI.
- Parameter `appeui` (`str`): The application EUI.
- Parameter `appkey` (`str`): The application key.

```python
lora.config_otaa("0037CAE1FC3542B9", "70B3D57ED003B699", "67FA4ED1075A20573BCDD7594C458698")
```

### `config_OTAA`
Config the OTAA join mode information.
Parameter:

Return:
    True
    False

### `get_otaa_config`
Get the OTAA join mode information.

- Returns: The OTAA join mode information(deveui, appeui, appkey).
- Return type: tuple

```python
lora.get_otaa_config()
```

### `get_OTAA_config`
Get the OTAA join mode information.
Parameter:
Return:
    (deveui, appeui, appkey)

### `check_join_status`
Check the LoRaWAN network join status.

- Returns: The LoRaWAN network join status.
- Return type: bool

```python
lora.check_join_status()
```

### `check_uplink_status`
Check the data uplink status.

- Returns: The data uplink status.
- Return type: bool

```python
lora.check_uplink_status()
```

### `check_downlink_data`
Check downlink data, if have downlink data, return the message.

- Parameter `timeout` (`int`): The timeout time.
- Returns: False if no downlink data, otherwise return the downlink data.
- Return type: bool | str

```python
lora.check_downlink_data()
```

## `LoRaWAN_Asr650x`
Create an LoRaWAN object.

- Parameter `uart` (`machine.UART`): The UART object.
- Parameter `debug` (`bool`): Whether to enable debug mode.

```python
from driver.asr650x import LoRaWAN_Asr650x

lora = LoRaWAN_Asr650x(uart)
```

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

- Parameter `mode` (`int`): The LoRaWAN join mode.

```python
lora.set_join_mode(0)
```

### `get_frequency_band_mask`
Get frequency band mask.
Parameter:
    None
Return:
    mask

### `set_frequency_band_mask`
Set the frequency band mask.

- Parameter `mask` (`str`): The frequency band mask.

```python
lora.set_frequency_band_mask("0001")
```

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

- Parameter `mode` (`int`): The uplink and downlink frequency.

```python
lora.set_uplink_downlink_mode(1)
```

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

- Parameter `class_mode` (`int`): The class mode.
- Parameter `branch` (`int`): The branch selection.
- Parameter `para1` (`int`): Set the beacon frequency, unit is Hz.
- Parameter `para2` (`int`): Set the beacon data rate.
- Parameter `para3` (`int`): Set ping frequency, unit is Hz.
- Parameter `para4` (`int`): Set ping data rate.

```python
lora.set_class_mode(0, 0, 0, 0, 0, 0)
```

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

- Parameter `para1` (`int`): 0 stop join, 1 start join.
- Parameter `para2` (`int`): 0 close auto join, 1 open auto join.
- Parameter `para3` (`int`): join interval, unit is second(7~255).
- Parameter `para4` (`int`): join retry times(1~256).

```python
lora.join(1, 1, 8, 1)

lora.join(0)
```

### `send_data`
Send data payload to LoRaWAN gateway.

- Parameter `payload` (`str`): The data to send.
- Parameter `confirm` (`int`): The confirm mode.
- Parameter `nbtrials` (`int`): The number of trials.

```python
lora.send_data("Hello, World!", 1, 1)
```

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

- Parameter `port` (`int`): The uplink app port.

```python
lora.set_uplink_app_port(1)
```

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

- Parameter `rx1_offset` (`int`): The RX1 offset.
- Parameter `rx2_dr` (`int`): The RX2 data rate.
- Parameter `rx2_freq` (`int`): The RX2 frequency.

```python
lora.set_rx_window_param(0, 0, 868100000)
```

### `set_rx1_delay_time`
Set receive window param.
Parameter:
    delay
Return:
    True
    False
