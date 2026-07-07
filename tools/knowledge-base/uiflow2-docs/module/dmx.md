# DMX512 Module

<!-- .. include:: ../refs/module.dmx.ref -->

DMX-Base is a functional base specially designed for DMX-512 data transmission scenarios, communicating and enabling control with M5 host through serial port, equipped with XLR-5 and XLR-3 male and female interfaces, convenient for users to connect DMX devices with different interfaces, in addition, the module has HT3.96 pitch 485 interface to facilitate connection to Expansion 485 devices.

Support the following products:

|dmx|

Micropython Example Send Data:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import DMX512Module
import time

Title = None
label1 = None
label0 = None
module_dmx_0 = None

ch_data = None

def setup():
    global Title, label1, label0, module_dmx_0, ch_data

    M5.begin()
    Widgets.fillScreen(0x222222)
    Title = Widgets.Title(
        "DMX512Module Send example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label("Not Sent", 2, 129, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "Not initialized", 2, 76, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    module_dmx_0 = DMX512Module(2, mode=1)
    ch_data = 0
    label0.setText(str("Initialized"))

def loop():
    global Title, label1, label0, module_dmx_0, ch_data
    M5.update()
    label1.setText(str("Not Sent"))
    ch_data = ch_data + 1
    if ch_data >= 255:
        ch_data = 0
    module_dmx_0.write_data(1, ch_data)
    module_dmx_0.write_data(2, ch_data)
    module_dmx_0.write_data(3, ch_data)
    label1.setText(str("Sent"))
    time.sleep(0.7)

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

Micropython Example Receive Data:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import DMX512Module

Title = None
label0 = None
label1 = None
module_dmx_0 = None

dmx_data = None
dmx_data2 = None

def module_dmx_0_channel1_receive_event(received_data):
    global Title, label0, label1, module_dmx_0, dmx_data, dmx_data2
    dmx_data = received_data
    label0.setText(str((str("Channel 1:") + str(dmx_data))))

def module_dmx_0_channel2_receive_event(received_data):
    global Title, label0, label1, module_dmx_0, dmx_data, dmx_data2
    dmx_data2 = received_data
    label1.setText(str((str("Channel 2:") + str(dmx_data2))))

def setup():
    global Title, label0, label1, module_dmx_0, dmx_data, dmx_data2

    M5.begin()
    Widgets.fillScreen(0x222222)
    Title = Widgets.Title(
        "DMX512Module Rec example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("Channel 1:", 0, 82, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Channel 2:", 0, 134, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    module_dmx_0 = DMX512Module(1, mode=2)
    module_dmx_0.attach_channel(1, module_dmx_0_channel1_receive_event)
    module_dmx_0.attach_channel(2, module_dmx_0_channel2_receive_event)
    module_dmx_0.receive_none_block()

def loop():
    global Title, label0, label1, module_dmx_0, dmx_data, dmx_data2
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

UIFLOW2 Master Example:

UIFLOW2 Slave Example:

<!-- .. only:: builder_html -->

    |dmx512_core2_send_example.m5f2|

    |dmx512_core2_receive_example.m5f2|

## class DMX512Module

## Constructors

<!-- .. class:: DMX512Module(id, mode = DMX_MASTER) -->

    Initializes the DMX512 module with a specified UART ID and port pins.

    :param Literal[0,1,2] id: UART device ID(DMX port id).
    :param int mode: Operating mode (1 for Master, 2 for Slave).

    UIFLOW2:

## Methods

<!-- .. method:: DMX512Module.dmx_init(mode) -> None -->

    Initializes the DMX512 communication with UART pins and mode.

    :param  mode: Operating mode (1 for Master, 2 for Slave).

    UIFLOW2:

<!-- .. method:: DMX512Module.deinit() -> None -->

    Deinitializes the DMX512 module and stops any ongoing operations.

    UIFLOW2:

<!-- .. method:: DMX512Module.write_data(channel, data) -> None -->

    Updates the data for a specified DMX channel. Data is sent on the next update cycle.

    :param  channel: DMX channel number (1-512).
    :param  data: Data value to be sent (0-255).
        @raises ValueError if the channel number is out of range.

    UIFLOW2:

<!-- .. method:: DMX512Module.clear_buffer() -> None -->

    Clears the DMX buffer and resets the data.

    UIFLOW2:

<!-- .. method:: DMX512Module.read_data(channel) -> int -->

    Reads data from a specified DMX channel in Slave mode.

    :param  channel: DMX channel number (1-512).

    UIFLOW2:

<!-- .. method:: DMX512.receive_none_block() -> None -->
    :no-index:

    Starts non-blocking data reception for the specified channels with associated callbacks.

    UIFLOW2:

<!-- .. method:: DMX512Module.attach_channel(channel, callback) -> None -->

    Attaches a callback function to a specified DMX channel.

    :param channel: DMX channel number (1-512) to attach the callback to.
    :param callback: The function to be called when data changes on the specified channel.

    UIFLOW2:

<!-- .. method:: DMX512.stop_receive() -> None -->
    :no-index:

    Stops the non-blocking data reception task.

    UIFLOW2:

<!-- .. method:: DMX512Module.detach_channel(channel) -> None -->

    Detaches the callback function from a specified DMX channel.

    :param channel: DMX channel number (1-512) to detach the callback from.
