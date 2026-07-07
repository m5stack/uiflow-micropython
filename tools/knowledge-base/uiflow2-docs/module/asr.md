
# ASR Module

<!-- .. sku:M147 -->
<!-- .. include:: ../refs/module.asr.ref -->

This is the driver library of ASR Module.

Support the following products:

|ASRModule|

## UiFlow2 Example

#### ASR Example

Open the |asr_core2_example.m5f2| project in UiFlow2.

This example shows how to use Module ASR to get the current command word, command number, and trigger an event when you say hello to do something you want to do.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### ASR Example

This example shows how to use Module ASR to get the current command word, command number, and trigger an event when you say hello to do something you want to do.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from module import ASRModule
import time

page0 = None
label0 = None
label1 = None
label2 = None
module_asr_0 = None

def module_asr_0_hello_event(args):
    global page0, label0, label1, label2, module_asr_0
    module_asr_0.send_message(0x5A)

def setup():
    global page0, label0, label1, label2, module_asr_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "label0",
        x=1,
        y=69,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "label1",
        x=1,
        y=103,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label2 = m5ui.M5Label(
        "label2",
        x=1,
        y=138,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    page0.screen_load()
    module_asr_0 = ASRModule(2, tx=27, rx=34)
    module_asr_0.add_command_word(
        module_asr_0.search_command_num("hello"), "hello", module_asr_0_hello_event
    )

def loop():
    global page0, label0, label1, label2, module_asr_0
    M5.update()
    label0.set_text(str((str("Is Receive:") + str((module_asr_0.get_received_status())))))
    label1.set_text(str((str("Command Num:") + str((module_asr_0.get_current_command_num())))))
    label2.set_text(str((str("Command Word:") + str((module_asr_0.get_current_command_word())))))
    time.sleep(1)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

## **API**

#### ASRModule

## ASRModule
Voice recognition hardware module.

:param int id: UART port ID for communication. Default is 2.
:param int tx: TX pin number.
:param int rx: RX pin number.
:param bool verbose: Enable verbose output. Default is False.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import ASRUnit

        # Initialize with UART1, TX on pin 2, RX on pin 1
        asr = ASRModule(id=2, tx=2, rx=1)
