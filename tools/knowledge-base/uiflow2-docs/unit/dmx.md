# DMX512 Unit

<!-- .. include:: ../refs/unit.dmx.ref -->

DMX Unit is a communication unit specifically designed for DMX-512 data transmission scenarios. It integrates the CA-IS3092W isolated half-duplex RS-485 transceiver, providing up to 5kVrms electrical isolation protection. The onboard 120Ω termination resistor switch matches the characteristic impedance of the signal transmission line, preventing signal reflection and distortion, and can be connected according to the usage scenario.

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
from unit import DMX512Unit
import time

Title = None
label1 = None
label0 = None
dmx_0 = None

ch_data = None

def setup():
    global Title, label1, label0, dmx_0, ch_data

    M5.begin()
    Widgets.fillScreen(0x222222)
    Title = Widgets.Title("DMX512Unit Send example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Not Sent", 2, 129, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "Not initialized", 2, 76, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    dmx_0 = DMX512Unit(1, port=(13, 14), mode=1)
    label0.setText(str("Initialized"))
    ch_data = 0

def loop():
    global Title, label1, label0, dmx_0, ch_data
    M5.update()
    label1.setText(str("Not Sent"))
    dmx_0.write_data(1, ch_data)
    dmx_0.write_data(2, ch_data)
    dmx_0.write_data(3, ch_data)
    ch_data = (ch_data if isinstance(ch_data, (int, float)) else 0) + 1
    if ch_data >= 255:
        ch_data = 0
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
from unit import DMX512Unit

Title = None
label0 = None
label1 = None
dmx_0 = None

dmx_data = None
dmx_data2 = None

def dmx_0_channel1_receive_event(received_data):
    global Title, label0, label1, dmx_0, dmx_data, dmx_data2
    dmx_data = received_data
    label0.setText(str((str("Channel 1:") + str(dmx_data))))

def dmx_0_channel2_receive_event(received_data):
    global Title, label0, label1, dmx_0, dmx_data, dmx_data2
    dmx_data2 = received_data
    label1.setText(str((str("Channel 2:") + str(dmx_data2))))

def setup():
    global Title, label0, label1, dmx_0, dmx_data, dmx_data2

    M5.begin()
    Widgets.fillScreen(0x222222)
    Title = Widgets.Title("DMX512Unit Rec example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Channel 1:", 0, 57, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Channel 2:", 2, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    dmx_0 = DMX512Unit(1, port=(13, 14), mode=2)
    dmx_0.attach_channel(1, dmx_0_channel1_receive_event)
    dmx_0.attach_channel(2, dmx_0_channel2_receive_event)
    dmx_0.receive_none_block()

def loop():
    global Title, label0, label1, dmx_0, dmx_data, dmx_data2
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

## class DMX512Unit

## Constructors

<!-- .. class:: DMX512Unit(id, port, mode = DMX_MASTER) -->

    Initializes the DMX512 unit with a specified UART ID and port pins.

    :param Literal[0,1,2] id: UART device ID(DMX port id).
    :param list|tuple port: UART TX and RX pins.
    :param int mode: Operating mode (1 for Master, 2 for Slave).

    UIFLOW2:

## Methods

<!-- .. method:: DMX512Unit.dmx_init(mode) -> None -->

    Initializes the DMX512 communication with UART pins and mode.

    :param  mode: Operating mode (1 for Master, 2 for Slave).

    UIFLOW2:

<!-- .. method:: DMX512Unit.deinit() -> None -->

    Deinitializes the DMX512 unit and stops any ongoing operations.

    UIFLOW2:

<!-- .. method:: DMX512Unit.write_data(channel, data) -> None -->

    Updates the data for a specified DMX channel. Data is sent on the next update cycle.

    :param  channel: DMX channel number (1-512).
    :param  data: Data value to be sent (0-255).
        @raises ValueError if the channel number is out of range.

    UIFLOW2:

<!-- .. method:: DMX512Unit.clear_buffer() -> None -->

    Clears the DMX buffer and resets the data.

    UIFLOW2:

<!-- .. method:: DMX512Unit.read_data(channel) -> int -->

    Reads data from a specified DMX channel in Slave mode.

    :param  channel: DMX channel number (1-512).

    UIFLOW2:

<!-- .. method:: DMX512Unit.receive_none_block() -> None -->

    Starts non-blocking data reception for the specified channels with associated callbacks.

    UIFLOW2:

<!-- .. method:: DMX512Unit.attach_channel(channel, callback) -> None -->

    Attaches a callback function to a specified DMX channel.

    :param channel: DMX channel number (1-512) to attach the callback to.
    :param callback: The function to be called when data changes on the specified channel.

    UIFLOW2:

<!-- .. method:: DMX512Unit.stop_receive() -> None -->

    Stops the non-blocking data reception task.

    UIFLOW2:

<!-- .. method:: DMX512Unit.detach_channel(channel) -> None -->

    Detaches the callback function from a specified DMX channel.

    :param channel: DMX channel number (1-512) to detach the callback from.
