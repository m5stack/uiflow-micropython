# IR

<!-- .. include:: ../refs/hardware.ir.ref -->

IR is used to control the infrared receiving/transmitting tube built into the host device.

The specific support of the host for IR is as follows:

<!-- .. table:: -->
    :widths: auto
    :align: center
######

###### | Controller        | IR Transmitter  | IR Receiver |

###### | Atom Lite         | |S|             |             |

###### | Atom Matrix       | |S|             |             |

###### | Atom U            | |S|             |             |

###### | AtomS3 Lite       | |S|             |             |

###### | AtomS3U           | |S|             |             |

###### | StickC            | |S|             |             |

###### | StickC-Plus       | |S|             |             |

###### | StickC-Plus2      | |S|             |             |

###### | Cardputer         | |S|             |             |

###### | Capsule           | |S|             |             |

###### | StickS3           | |S|             | |S|         |

<!-- .. |S| unicode:: U+2714 -->

## UiFlow2 Example

#### IR Transmission

Open the |sticks3_ir_tx_example.m5f2| project in UiFlow2.

This example demonstrates infrared (IR) transmission functionality. When button A is pressed, it sends IR data with a specified address and data value.
The example displays the address and data being transmitted.

UiFlow2 Code Block:

Example output:

    None

#### IR Reception

Open the |sticks3_ir_rx_example.m5f2| project in UiFlow2.

This example demonstrates infrared (IR) reception functionality using NEC decode protocol.
When IR data is received, it displays the address and data values on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### IR Transmission

This example demonstrates infrared (IR) transmission functionality. When button A is pressed, it sends IR data with a specified address and data value.
The example displays the address and data being transmitted.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import IR

label_title = None
label_addr = None
label_data = None
label_tip = None
ir = None
data = None
addr = None

def btna_click_event_cb(state):
    global label_title, label_addr, label_data, label_tip, ir, data, addr
    data = (data if isinstance(data, (int, float)) else 0) + 1
    ir.tx(addr, data)
    print((str("IR: Send addr: ") + str((str(addr) + str((str(" data: ") + str(data)))))))
    label_data.setText(str((str("data: ") + str(data))))

def setup():
    global label_title, label_addr, label_data, label_tip, ir, data, addr
    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("IR", 58, 5, 1.0, 0x1AEAEB, 0x000000, Widgets.FONTS.DejaVu18)
    label_addr = Widgets.Label("addr:", 5, 45, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data:", 5, 70, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_tip = Widgets.Label(
        "BtnA Send", 18, 200, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_click_event_cb)
    ir = IR()
    ir.rx_cb(ir_rx_event)
    addr = 56
    data = 0
    Power.setExtOutput(True)
    label_addr.setText(str((str("addr: ") + str(addr))))

def loop():
    global label_title, label_addr, label_data, label_tip, ir, data, addr
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

Example output:

    None

#### IR Reception

This example demonstrates infrared (IR) reception functionality using NEC decode protocol.
When IR data is received, it displays the address and data values on the screen.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import IR

label_title = None
label0 = None
label_addr = None
label_data = None
ir = None
data = None
addr = None

def ir_rx_event(_data, _addr, _ctrl):
    global label_title, label0, label_addr, label_data, ir, data, addr
    data = _data
    addr = _addr
    label_addr.setText(str((str("addr: ") + str(addr))))
    label_data.setText(str((str("data: ") + str(data))))

def setup():
    global label_title, label0, label_addr, label_data, ir, data, addr

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("IR RX", 41, 5, 1.0, 0x0FBAE1, 0x000000, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("NEC Decode", 8, 50, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_addr = Widgets.Label("addr:", 5, 115, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data:", 5, 145, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)

    Speaker.setPA(False)
    ir = IR()
    ir.rx_cb(ir_rx_event)

def loop():
    global label_title, label0, label_addr, label_data, ir, data, addr
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

Example output:

    None

## class IR

## Constructors

<!-- .. class:: IR() -->

    Initializes the IR unit with the appropriate pins based on the M5Stack board type.

    UiFlow2:

## Methods

<!-- .. method:: IR.tx(cmd, data) -->

    Transmits an IR signal with the specified command and data using the NEC protocol.

    :param  cmd: The command code to be transmitted.
    :param  data: The data associated with the command.

    UiFlow2:

<!-- .. method:: IR.rx_cb(cb) -->

    Registers a callback for infrared reception. When an NEC-format IR signal is received, the callback is invoked with two arguments: ``(data, addr)``.

    Only supported on boards with an IR receiver (e.g. StickS3).

    :param cb: Callback function with signature ``cb(data, addr)``. ``data`` and ``addr`` are 8-bit values (0–255).

    UiFlow2:
