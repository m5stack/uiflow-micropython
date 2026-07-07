
# ASR Unit

<!-- .. sku:U194 -->
<!-- .. include:: ../refs/unit.asr.ref -->

**Unit ASR** is an **AI** offline speech recognition unit, featuring the built-in AI smart offline speech module **CI-03T**. This unit offers powerful functions such as speech recognition, voiceprint recognition, speech enhancement, and speech detection. It supports AEC (Acoustic Echo Cancellation) to effectively eliminate echoes and noise interference, improving the accuracy of speech recognition. Additionally, it supports mid-speech interruption, allowing for flexible interruption during the recognition process and quick response to new commands. The product is pre-configured with wake-up words and feedback commands at the factory. The device uses **UART** serial communication for data transmission and also supports waking up the device via UART or voice keywords. This unit supports user customization of the **wake-up** recognition word and can recognize up to 300 command words. It is equipped with a **microphone** for clear audio capture and includes a **speaker** for high-quality audio feedback. This product is widely used in AI assistants, smart homes, security monitoring, automotive systems, robotics, smart hardware, healthcare, and other fields, making it an ideal choice for realizing smart voice interactions.

Support the following products:

|ASRUnit|

## UiFlow2 Example

#### ASR Example

Open the |asr_cores3_example.m5f2| project in UiFlow2.

This example shows how to use Unit ASR to get the current command word, command number, and trigger an event when you say hello to do something you want to do.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### ASR Example

This example shows how to use Unit ASR to get the current command word, command number, and trigger an event when you say hello to do something you want to do.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import ASRUnit

title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
asr_0 = None

def asr_0_hello_event(args):
    global title0, label0, label1, label2, label3, asr_0
    print("Rec Hello")

def setup():
    global title0, label0, label1, label2, label3, asr_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "UnitASR M5CoreSe Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("msg:", 0, 51, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("rec cmd num:", 0, 93, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label(
        "rec cmd word:", 0, 134, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label3 = Widgets.Label(
        "rec cmd handler state:", 0, 178, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    asr_0 = ASRUnit(2, port=(1, 2))
    print(asr_0.search_command_num("hello"))
    print(asr_0.search_command_word(0x32))
    asr_0.add_command_word(0x32, "hello", asr_0_hello_event)

def loop():
    global title0, label0, label1, label2, label3, asr_0
    M5.update()
    if asr_0.get_received_status():
        label0.setText(str((str("msg:") + str((asr_0.get_current_raw_message())))))
        label1.setText(str((str("rec cmd num:") + str((asr_0.get_current_command_num())))))
        label2.setText(str((str("rec cmd word:") + str((asr_0.get_current_command_word())))))
        label3.setText(str((str("rec cmd handler state:") + str((asr_0.get_command_handler())))))

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

#### ASRUnit

## ASRUnit
Voice recognition hardware module.

:param int id: UART port ID for communication. Default is 2.
:param list|tuple port: Tuple containing TX and RX pin numbers.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import ASRUnit

        # Initialize with UART1, TX on pin 2, RX on pin 1
        asr = ASRUnit(id=2, port=(1, 2))

### `get_received_status`
Get message reception status.

:returns: True if a message is received, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        asr.get_received_status()

### `send_message`
Send command via UART.

:param int command_num: Command number to send (0-255)

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        asr.send_message(0x30)

### `get_current_raw_message`
Get the raw message received in hexadecimal format.

:returns: The raw message as a string in hexadecimal format.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        asr.get_current_raw_message()

### `get_current_command_word`
Get the command word corresponding to the current command number.

:returns: The command word as a string.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        asr.get_current_command_word()

### `get_current_command_num`
Get the current command number.

:returns: The current command number as a string.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        asr.get_current_command_num()

### `get_command_handler`
Check if the current command has an associated handler.

:returns: True if the command has an associated handler, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        asr.get_command_handler()

### `add_command_word`
Register custom command and handler.

:param int command_num: Command number (0-255)
:param str command_word: Voice command text
:param callable event_handler: Handler function

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        def custom_handler(unit):
            print("Custom command detected!")

        asr.add_command_word(0x50, "custom command", custom_handler)

### `remove_command_word`
Remove a command word from the command list by its word.

:param str command_word: Command word to remove

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        asr.remove_command_word("custom command")

### `search_command_num`
Search for the command number associated with a command word.

:param str command_word: Command word to search for
:returns: The command number if found, otherwise -1
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        asr.search_command_num("custom command")

### `search_command_word`
Search for the command word associated with a command number.

:param int command_num: Command number to search for
:returns: The command word if found, otherwise "Unknown command word"
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        asr.search_command_word(0x50)

### `get_command_list`
Get the list of all commands and their associated handlers.

:returns: A dictionary of command numbers and their corresponding command words and handlers.
:rtype: dict

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        asr.get_command_list()

### `check_tick_callback`
Check if a handler is defined for the current command and schedule its execution.

:returns: The handler if defined, otherwise None
:rtype: None

MicroPython Code Block:

    .. code-block:: python

        asr.check_tick_callback()
