# COMX LTE Module

<!-- .. sku: M031-A -->

<!-- .. include:: ../refs/module.lte.ref -->

LTEModule Class provides a set of methods to control the LTE module. Through the
chat script of AT commands, the module is set to PPP mode and then the data is
sent to the Internet through the serial port.

Support the following products:

    |COMX LTE|

## UiFlow2 Example

#### HTTP GET over LTE

Open the |core2_lte_http_example.m5f2| project in UiFlow2.

This example demonstrates how to use PPP dial-up on the LTE module and then use
the `requests2` library to send an HTTP GET request.

UiFlow2 Code Block:

Example output:

    None

#### Chat script

Open the |core2_lte_chat_example.m5f2| project in UiFlow2.

Set the LTE module to PPP mode through a custom AT command chat script.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### HTTP GET over LTE

This example demonstrates how to use PPP dial-up on the LTE module and then use
the `requests2` library to send an HTTP GET request.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

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

Example output:

    None

#### Chat script

Set the LTE module to PPP mode through a custom AT command chat script.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

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

Example output:

    None

## **API**

#### LTEModule

## LTEModule
LTE module class.

:param int id: UART ID connected to the LTE module.
:param int tx: Connect to the UART TX pin of the LTE module.
:param int rx: Connect to the UART RX pin of the LTE module.
:param bool verbose: Whether to print verbose information.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from module import LTEModule

        comlte_0 = LTEModule(2, 14, 13, verbose=True)

### `execute_at_command2`

### `response_at_command2`

### `chat`
Chat with the LTE module.

:param tuple script: A tuple of commands to chat with the LTE module.
                     Each command is a tuple of two elements: the first
                     element is the expect value, and the second element
                     is the command. For example, (("OK", "AT").

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        comlte_0.chat((("OK", "AT"), ("OK", "AT+CGDCONT=1,"IP","CMNET""), ("OK", "ATD*99#")))

### `chat2`
Chat with the LTE module to establish a PPP connection.

:param str pdp_type: PDP type. For example, "IP", "PPP", "IPV4V6", "IPV6".
:param str apn: Access Point Name. For example, "CMNET".

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        comlte_0.chat2("IP", "CMNET")

### `deinit`
Deinitialize the LTE module.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        comlte_0.deinit()

<!-- .. py:method:: active([is_active]) -->

        Activate (“up”) or deactivate (“down”) the network interface, if a
        boolean argument is passed. Otherwise, query current state if no
        argument is provided.

        :param bool is_active: If True, the LTE module is enabled, if False, the LTE module is disabled.

        :return: Returns the activation status of the LTE module.
        :rtype: bool

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                comlte_0.active(True)
                comlte_0.active(False)
                comlte_0.active()

<!-- .. py:method:: connect(authmode=AUTH_NONE, username="", password="") -->

        Initiate a PPP connection with the given parameters.

        :param int authmode: Authentication Mode, either LTEModule.AUTH_NONE, LTEModule.AUTH_PAP, or LTEModule.AUTH_CHAP.
        :param str username: An optional user name to use with the authentication mode.
        :param str password: An optional password to use with the authentication mode.

        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                comlte_0.connect(authmode=AUTH_NONE, username="", password="")
                comlte_0.connect()

<!-- .. py:method:: isconnected() -->

        Returns True if the PPP link is connected and up. Returns False otherwise.

        :return: True if the PPP link is connected and up, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                comlte_0.isconnected()

<!-- .. py:method:: ifconfig() -->

        Get IP-level network interface parameters: IP address, subnet mask,
        gateway and DNS server. This method returns a 4-tuple with the above
        information.

        :return: A 4-tuple with IP address, subnet mask, gateway and DNS server.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                comlte_0.ifconfig()
                comlte_0.ifconfig()[0] # IP address
                comlte_0.ifconfig()[1] # network
                comlte_0.ifconfig()[2] # gateway
                comlte_0.ifconfig()[3] # DNS server
