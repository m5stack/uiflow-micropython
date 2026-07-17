# COMX LTE Module

LTEModule Class provides a set of methods to control the LTE module. Through the
chat script of AT commands, the module is set to PPP mode and then the data is
sent to the Internet through the serial port.

Support the following products:

    COMX LTE

## MicroPython Example

#### HTTP GET over LTE

This example demonstrates how to use PPP dial-up on the LTE module and then use
the `requests2` library to send an HTTP GET request.

```python
import os, sys, io
import M5
from M5 import *
from module import LTEModule
import requests2

label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
label9 = None
label10 = None
title0 = None
comlte_0 = None
http_req = None

def setup():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        label9, \
        label10, \
        title0, \
        comlte_0, \
        http_req

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Connecting", 16, 47, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("IPv4:", 16, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Netmask:", 16, 112, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Gateway:", 16, 144, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("DNS:", 16, 176, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("HTTP Code:", 16, 208, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 80, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 120, 112, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("label8", 120, 144, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label9 = Widgets.Label("label9", 80, 176, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label10 = Widgets.Label("label10", 140, 208, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title("COM.LTE Sample Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    comlte_0 = LTEModule(2, 14, 13, verbose=True)
    comlte_0.chat2("IP", "CMNET")
    comlte_0.active(True)
    comlte_0.connect(authmode=comlte_0.AUTH_NONE, username="", password="")
    while not (comlte_0.isconnected()):
        pass
    label0.setText(str("Connected"))
    label6.setText(str(comlte_0.ifconfig()[0]))
    label7.setText(str(comlte_0.ifconfig()[1]))
    label8.setText(str(comlte_0.ifconfig()[2]))
    label9.setText(str(comlte_0.ifconfig()[3]))
    http_req = requests2.get(
        "https://httpbin.org/get", headers={"Content-Type": "application/json"}
    )
    label10.setText(str(http_req.status_code))
    http_req.close()

def loop():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        label9, \
        label10, \
        title0, \
        comlte_0, \
        http_req
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            comlte_0.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### Chat script

Set the LTE module to PPP mode through a custom AT command chat script.

```python
import os, sys, io
import M5
from M5 import *
from module import LTEModule
import requests2

label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
label9 = None
label10 = None
title0 = None
comlte_0 = None
http_req = None

def setup():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        label9, \
        label10, \
        title0, \
        comlte_0, \
        http_req

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Connecting", 16, 47, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("IPv4:", 16, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Netmask:", 16, 112, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Gateway:", 16, 144, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("DNS:", 16, 176, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("HTTP Code:", 16, 208, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 80, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 120, 112, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("label8", 120, 144, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label9 = Widgets.Label("label9", 80, 176, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label10 = Widgets.Label("label10", 140, 208, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title("COM.LTE Sample Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    comlte_0 = LTEModule(2, 14, 13, verbose=True)
    comlte_0.chat(
        [
            ["ABORT", "BUSY"],
            ["ABORT", "NO ANSWER"],
            ["ABORT", "NO CARRIER"],
            ["ABORT", "NO DIALTONE"],
            ["ABORT", "\\nRINGING\\r\\n\\r\\nRINGING\\r"],
            ["SAY", "modem init: press <ctrl>-C to disconnect\\n"],
            ["", "+++ATH"],
            ["SAY", "Before Connecting\\n"],
            ["OK", 'AT+CGDCONT=1,"IP","CMNET"'],
            ["SAY", "\\n + defining PDP context\\n"],
            ["", "ATD*99#"],
            ["SAY", "Number Dialled\\n"],
            ["SAY", "\\n + attaching"],
            ["SAY", "\\n + requesting data connection"],
            ["CONNECT", "\\d\\c"],
            ["SAY", "\\n + connected"],
        ]
    )
    comlte_0.active(True)
    comlte_0.connect(authmode=comlte_0.AUTH_NONE, username="", password="")
    while not (comlte_0.isconnected()):
        pass
    label0.setText(str("Connected"))
    label6.setText(str(comlte_0.ifconfig()[0]))
    label7.setText(str(comlte_0.ifconfig()[1]))
    label8.setText(str(comlte_0.ifconfig()[2]))
    label9.setText(str(comlte_0.ifconfig()[3]))
    http_req = requests2.get(
        "https://httpbin.org/get", headers={"Content-Type": "application/json"}
    )
    label10.setText(str(http_req.status_code))
    http_req.close()

def loop():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        label9, \
        label10, \
        title0, \
        comlte_0, \
        http_req
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            comlte_0.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## **API**

#### LTEModule

## `LTEModule`
LTE module class.

- Parameter `id` (`int`): UART ID connected to the LTE module.
- Parameter `tx` (`int`): Connect to the UART TX pin of the LTE module.
- Parameter `rx` (`int`): Connect to the UART RX pin of the LTE module.
- Parameter `verbose` (`bool`): Whether to print verbose information.

```python
from module import LTEModule

comlte_0 = LTEModule(2, 14, 13, verbose=True)
```

### `execute_at_command2`

### `response_at_command2`

### `chat`
Chat with the LTE module.

- Parameter `script` (`tuple`): A tuple of commands to chat with the LTE module.
                     Each command is a tuple of two elements: the first
                     element is the expect value, and the second element
                     is the command. For example, (("OK", "AT").

```python
comlte_0.chat((("OK", "AT"), ("OK", "AT+CGDCONT=1,"IP","CMNET""), ("OK", "ATD*99#")))
```

### `chat2`
Chat with the LTE module to establish a PPP connection.

- Parameter `pdp_type` (`str`): PDP type. For example, "IP", "PPP", "IPV4V6", "IPV6".
- Parameter `apn` (`str`): Access Point Name. For example, "CMNET".

```python
comlte_0.chat2("IP", "CMNET")
```

### `deinit`
Deinitialize the LTE module.

```python
comlte_0.deinit()
```

### `active([is_active])`

        Activate (“up”) or deactivate (“down”) the network interface, if a
        boolean argument is passed. Otherwise, query current state if no
        argument is provided.

        - Parameter `is_active` (`bool`): If True, the LTE module is enabled, if False, the LTE module is disabled.

        - Returns: Returns the activation status of the LTE module.
        - Return type: bool

```python
comlte_0.active(True)
comlte_0.active(False)
comlte_0.active()
```
### `connect(authmode=AUTH_NONE, username="", password="")`

        Initiate a PPP connection with the given parameters.

        - Parameter `authmode` (`int`): Authentication Mode, either LTEModule.AUTH_NONE, LTEModule.AUTH_PAP, or LTEModule.AUTH_CHAP.
        - Parameter `username` (`str`): An optional user name to use with the authentication mode.
        - Parameter `password` (`str`): An optional password to use with the authentication mode.

        - Returns: None

```python
comlte_0.connect(authmode=AUTH_NONE, username="", password="")
comlte_0.connect()
```
### `isconnected()`

        Returns True if the PPP link is connected and up. Returns False otherwise.

        - Returns: True if the PPP link is connected and up, False otherwise.
        - Return type: bool

```python
comlte_0.isconnected()
```
### `ifconfig()`

        Get IP-level network interface parameters: IP address, subnet mask,
        gateway and DNS server. This method returns a 4-tuple with the above
        information.

        - Returns: A 4-tuple with IP address, subnet mask, gateway and DNS server.

```python
comlte_0.ifconfig()
comlte_0.ifconfig()[0] # IP address
comlte_0.ifconfig()[1] # network
comlte_0.ifconfig()[2] # gateway
comlte_0.ifconfig()[3] # DNS server
```
