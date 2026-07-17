# GatewayH2 Module

This library is the driver for Module Gateway H2, and the module communicates via UART.

Support the following products:

    Module Gateway H2

> Note: When using this module, you need to flash the NCP firmware to the module. For details, refer to the `ESP Zigbee NCP <https://docs.m5stack.com/en/esp_idf/zigbee/module_gateway_h2/zigbee_ncp>`_ documentation.
## MicroPython Example

#### Switch Control

The example demonstrates group control and targeted device operation for light nodes through SwitchEndpoint of Gateway H2 module.

```python
import os, sys, io
import M5
from M5 import *
from module import GatewayH2Module

title0 = None
label0 = None
label1 = None
label2 = None
label_addr = None
module_h2_0 = None
module_h2_0_ep = None
device_addr = None
device_count = None
device_list = None

def first_index(my_list, elem):
    try:
        index = my_list.index(elem) + 1
    except:
        index = 0
    return index

def module_h2_0_ep_bind_event(addr):
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        module_h2_0, \
        module_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list
    device_addr = addr
    print(device_addr)
    if first_index(device_list, device_addr) == 0:
        device_list.append(device_addr)
        device_count = device_count + 1
        label_addr.setText(str((str("new device addr: ") + str(device_addr))))

def btn_pwr_was_clicked_event(state):
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        module_h2_0, \
        module_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list
    if not not len(device_list):
        module_h2_0_ep.toggle()

def setup():
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        module_h2_0, \
        module_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Switch Endpoint Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "press the power button toggle", 2, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "if has device connect", 2, 26, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label(
        "connect device: ", 2, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_addr = Widgets.Label("None", 5, 115, 1.0, 0x00FF00, 0x222222, Widgets.FONTS.DejaVu18)
    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btn_pwr_was_clicked_event)
    module_h2_0 = GatewayH2Module(2, 17, 10)
    module_h2_0_ep = module_h2_0.create_switch_ep()
    module_h2_0_ep.set_bind_callback(module_h2_0_ep_bind_event)
    device_count = 0
    device_list = []

def loop():
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        module_h2_0, \
        module_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list
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

## **API**

#### GatewayH2Module

### `class module.gateway_h2.GatewayH2Module`

    Create an GatewayH2Module object.

    - Parameter `id` (`int`): UART id.
    - Parameter `tx` (`int`): the UART TX pin.
    - Parameter `rx` (`int`): the UART RX pin.

```python
from module import GatewayH2Module

module_gateway_h2 = GatewayH2Module(id = 1, tx = 10, rx = 17)
```
### `create_switch_endpoint()`

        Create Switch Endpoint.

```python
h2_switch_endpoint = module_gateway_h2.create_switch_endpoint()
```

#### SwitchEndpoint

### `class SwitchEndpoint`

    Return by GatewayH2Module.create_switch_endpoint() or GatewayH2Unit.create_switch_endpoint()

### `on([addr])`

        Turn on the light.

        - Parameter `addr`: The device address (optional).

        - If called as `on()`, turn on all devices.
        - If called as `on(addr)`, turn on special address devices.

```python
h2_switch_endpoint.on(addr)
h2_switch_endpoint.on()
```
### `off([addr])`

        Turn off the light.

        - Parameter `addr`: The device address (optional).

        - If called as `off()`, turn off all devices.
        - If called as `off(addr)`, turn off special address devices.

```python
h2_switch_endpoint.off(addr)
h2_switch_endpoint.off()
```
### `toggle([addr])`

        Toggle the light state.

        - Parameter `addr`: The device address (optional).

        - If called as `toggle()`, toggle all devices.
        - If called as `toggle(addr)`, toggle special address devices.

```python
h2_switch_endpoint.toggle(addr)
h2_switch_endpoint.toggle()
```
