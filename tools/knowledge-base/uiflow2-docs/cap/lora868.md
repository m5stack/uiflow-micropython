# LoRa868 Cap

<!-- .. sku: U201 -->

<!-- .. include:: ../refs/cap.lora868.ref -->

Cap LoRa868 is a high-performance LoRa communication and GNSS global navigation expansion module designed for the Cardputer-Adv.

Support the following products:

    |LoRa868Cap|

## UiFlow2 Example

#### Sender

Open the |cardputer_adv_lora868_cap_sender_example.m5f2| project in UiFlow2.

Use the keyboard to enter the text you want to send and press ENTER to send it.

UiFlow2 Code Block:

Example output:

    None

#### Receiver

Open the |cardputer_adv_lora868_cap_receiver_example.m5f2| project in UiFlow2.

This example receives and displays data.

UiFlow2 Code Block:

Example output:

    None

#### GPS Usage

Open the |cardputer_adv_lora868_cap_gps_example.m5f2| project in UiFlow2.

This example demonstrates how to use the GPS functionality of the LoRa868 Cap.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Sender

Use the keyboard to enter the text you want to send and press ENTER to send it.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import MatrixKeyboard
from cap import LoRa868Cap
from unit import KeyCode

kb = None
cap_lora868 = None

keycode = None
key = None
buf = None

def kb_pressed_event(kb_0):
    global kb, cap_lora868, keycode, key, buf
    keycode = kb.get_key()
    if keycode >= 0x20 and keycode <= 0x7E:
        key = chr(keycode)
        buf = str(buf) + str(key)
        M5.Lcd.printf(key)
    elif keycode == (KeyCode.KEYCODE_ENTER):
        cap_lora868.send(buf, None)
        buf = ""
        M5.Lcd.fillScreen(0x000000)
        M5.Lcd.setCursor(0, 0)
        M5.Lcd.printf("\n")
        M5.Lcd.printf(">>> ")

def setup():
    global kb, cap_lora868, keycode, key, buf

    M5.begin()
    Widgets.fillScreen(0x000000)

    cap_lora868 = LoRa868Cap(
        freq_khz=868000,
        bw="250",
        sf=8,
        coding_rate=8,
        preamble_len=12,
        syncword=0x12,
        output_power=10,
    )
    kb = MatrixKeyboard()
    kb.set_callback(kb_pressed_event)
    M5.Lcd.setFont(Widgets.FONTS.DejaVu12)
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
    M5.Lcd.setCursor(0, 0)
    M5.Lcd.printf(">>> ")
    buf = ""

def loop():
    global kb, cap_lora868, keycode, key, buf
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

#### Receiver

This example receives and displays data.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import time
from cap import LoRa868Cap

cap_lora868 = None

lora_data = None
cur_time = None
time_buf = None
rx_text = None

def cap_lora868_receive_event(received_data):
    global cap_lora868, lora_data, cur_time, time_buf, rx_text
    lora_data = received_data
    cur_time = time.gmtime()
    time_buf = ""
    time_buf = str(time_buf) + str("[")
    time_buf = str(time_buf) + str((cur_time[3]))
    time_buf = str(time_buf) + str(":")
    time_buf = str(time_buf) + str((cur_time[4]))
    time_buf = str(time_buf) + str(":")
    time_buf = str(time_buf) + str((cur_time[5]))
    time_buf = str(time_buf) + str("] -> ")
    M5.Lcd.print(time_buf, 0x33FF33)
    rx_text = lora_data.decode()
    M5.Lcd.print(rx_text, 0xFFFFFF)
    M5.Lcd.printf("\n")

def setup():
    global cap_lora868, lora_data, cur_time, time_buf, rx_text

    M5.begin()
    Widgets.fillScreen(0x000000)

    cap_lora868 = LoRa868Cap(
        freq_khz=868000,
        bw="250",
        sf=8,
        coding_rate=8,
        preamble_len=12,
        syncword=0x12,
        output_power=10,
    )
    cap_lora868.set_irq_callback(cap_lora868_receive_event)
    M5.Lcd.setFont(Widgets.FONTS.DejaVu12)
    M5.Lcd.setCursor(0, 0)
    M5.Lcd.setTextScroll(True)
    cap_lora868.start_recv()

def loop():
    global cap_lora868, lora_data, cur_time, time_buf, rx_text
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

#### GPS Usage

This example demonstrates how to use the GPS functionality of the LoRa868 Cap.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from cap import GPSCap

label0 = None
label1 = None
label2 = None
cap_lora868 = None

def setup():
    global label0, label1, label2, cap_lora868

    M5.begin()
    Widgets.fillScreen(0x000000)
    label0 = Widgets.Label("label0", 11, 16, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 11, 46, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 10, 77, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    cap_lora868 = GPSCap(id=2)

def loop():
    global label0, label1, label2, cap_lora868
    M5.update()
    label0.setText(str(cap_lora868.get_latitude()))
    label1.setText(str(cap_lora868.get_longitude()))
    label2.setText(str(cap_lora868.get_gps_time()))

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

#### class LoRa868Cap

## LoRa868Cap
Create a LoRa868Cap object.

:param int pin_rst: (RST) Reset pin number.
:param int pin_cs: (NSS) Chip select pin number.
:param int pin_irq: (IRQ) Interrupt pin number.
:param int pin_busy: (BUSY) Busy pin number.
:param int freq_khz: LoRa RF frequency in KHz, with a range of 850000 KHz to 930000 KHz.
:param str bw: Bandwidth, options include:

    - ``"7.8"``: 7.8 KHz
    - ``"10.4"``: 10.4 KHz
    - ``"15.6"``: 15.6 KHz
    - ``"20.8"``: 20.8 KHz
    - ``"31.25"``: 31.25 KHz
    - ``"41.7"``: 41.7 KHz
    - ``"62.5"``: 62.5 KHz
    - ``"125"``: 125 KHz
    - ``"250"``: 250 KHz
    - ``"500"``: 500 KHz
:param int sf: Spreading factor, range from 7 to 12. Higher spreading factors allow reception of weaker signals but with slower data rates.
:param int coding_rate: Forward Error Correction (FEC) coding rate expressed as 4/N, with a range from 5 to 8.
:param int preamble_len: Length of the preamble sequence in symbols, range from 0 to 255.
:param int syncword: Sync word to mark the start of the data frame, default is 0x12.
:param int output_power: Output power in dBm, range from -9 to 22.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from cap import LoRa868Cap

        cap_lora868_0 = LoRa868Cap(5, 1, 10, 2, 868000, '250', 8, 8, 12, 0x12, 10)

### `set_freq`
Set frequency in kHz.

:param int freq_khz: Frequency in kHz (850000 ~ 930000), default is 868000.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.set_freq(868000)

### `set_sf`
Set spreading factor (SF).

:param int sf: Spreading factor (7 ~ 12)

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.set_sf(7)

### `set_bw`
Set bandwidth.

:param str bw: Bandwidth in kHz as string. Must be one of:
               '7.8', '10.4', '15.6', '20.8', '31.25', '41.7',
               '62.5', '125', '250', '500'.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.set_bw(bw)

### `set_coding_rate`
Set coding rate.

:param int coding_rate: Coding rate (5 ~ 8)

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.set_coding_rate(coding_rate)

### `set_syncword`
Set syncword.

:param int syncword: Sync word (0 ~ 0xFF)

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.set_syncword(syncword)

### `set_preamble_len`
Set preamble length.

:param int preamble_len: Preamble length, range: 0~255.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.set_preamble_len(preamble_len)

### `set_output_power`
Set output power in dBm.

:param int output_power: Output power in dBm (-9 ~ 22)

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.set_output_power(output_power)

### `send`
Send data

:param str | list | tuple | int | bytearray packet: The data to be sent.
:param int tx_at_ms: The timestamp in milliseconds when to send the data (optional). Default is None.
:returns: timestamp
:rtype: int

Send a data packet and return the timestamp after the packet is sent.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.send()

### `recv`
Receive data

:param int timeout_ms: Timeout in milliseconds (optional). Default is None.
:param int rx_length: Length of the data to be read. Default is 0xFF.
:param RxPacket rx_packet: An instance of `RxPacket` (optional) to reuse.
:returns: Received packet instance
:rtype: RxPacket

Attempt to receive a LoRa packet. Returns `None` if timeout occurs, or returns the received packet instance.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        data = module_lora868v12_0.recv()

### `start_recv`
Start receive data

This method initiates the process to begin receiving data.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.start_recv()

### `set_irq_callback`
Set the interrupt callback function to be executed on IRQ.

:param callback: The callback function to be invoked when the interrupt is triggered.
                  The callback should not take any arguments and should return nothing.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.set_irq_callback()

### `standby`
Set module to standby mode.

Puts the LoRa module into standby mode, consuming less power.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.standby()

### `sleep`
Set module to sleep mode.

Reduces the power consumption by putting the module into deep sleep mode.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.sleep()

### `irq_triggered`
Check IRQ trigger.

:returns: Returns `True` if an interrupt service routine (ISR) has been triggered since the last send or receive started.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        module_lora868v12_0.irq_triggered()

### `deinit`

#### class GPSCap

## GPSCap
Initialize the GPSCap with a specific UART id and port for communication.

:param int id: The UART ID for communication with the GPS module. It can be 0, 1, or 2.
:param int rx: The RX pin for UART communication. If None, uses default pin from board definition.
:param int tx: The TX pin for UART communication. If None, uses default pin from board definition.
:param int pps: The PPS (Pulse Per Second) pin, used for high-precision time synchronization. Default is -1 (not used).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from cap import GPSCap
        gps_0 = GPSCap(id=2)
