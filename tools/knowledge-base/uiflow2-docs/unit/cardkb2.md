# CardKB2 Unit

<!-- .. include:: ../refs/unit.cardkb2.ref -->

This is the driver library of CardKB2 Unit, which is used to obtain key input data.

Support the following products:

    |CardKB2 Unit|

## UiFlow2 Example

#### CardKB2 I2C Mode

Open the |cardkb2_i2c_core2_example.m5f2| project in UiFlow2.

This example display the keyboard input on the screen and serial.

UiFlow2 Code Block:

Example output:

    input key char

#### CardKB2 UART Mode

Open the |cardkb2_uart_core2_example.m5f2| project in UiFlow2.

This example display the keyboard input on the screen and serial.

UiFlow2 Code Block:

Example output:

    input key char and state

#### CardKB2 ESP-NOW Mode

Open the |cardkb2_espnow_core2_example.m5f2| project in UiFlow2.

This example display the keyboard input on the screen and serial.

UiFlow2 Code Block:

Example output:

    input key char and state

## MicroPython Example

#### CardKB2 I2C Mode

This example display the keyboard input on the screen and serial.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import CardKBUnit
from hardware import Pin
from hardware import I2C

title0 = None
label0 = None
i2c0 = None
cardkb2_0 = None

char = None

def cardkb2_0_i2c_pressed_event(kb):
    global title0, label0, i2c0, cardkb2_0, char
    char = cardkb2_0.get_char()
    label0.setText(str((str(char) + str(" was pressed"))))
    print((str(char) + str(" was pressed")))

def setup():
    global title0, label0, i2c0, cardkb2_0, char

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "CardKB2 I2C Mode Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 3, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    cardkb2_0 = CardKBUnit(i2c0, mode=CardKBUnit.CardKB_I2C_MODE)
    cardkb2_0.set_callback(cardkb2_0_i2c_pressed_event)
    char = ""

def loop():
    global title0, label0, i2c0, cardkb2_0, char
    M5.update()
    cardkb2_0.tick()

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

    input key char

#### CardKB2 UART Mode

This example display the keyboard input on the screen and serial.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import CardKBUnit

title0 = None
label0 = None
cardkb2_0 = None

key_id = None
key_status = None

def cardkb2_0_pressed_event(kb):
    global title0, label0, cardkb2_0, key_id, key_status
    key_id, key_status = kb
    if key_status == (CardKBUnit.KEY_STATE_PRESS):
        label0.setText(str((str("Key ID ") + str((str(key_id) + str(" Press"))))))
        print((str("Key ID ") + str((str(key_id) + str(" Press")))))
    elif key_status == (CardKBUnit.KEY_STATE_RELEASE):
        label0.setText(str((str("Key ID ") + str((str(key_id) + str(" Release"))))))
        print((str("Key ID ") + str((str(key_id) + str(" Release")))))

def setup():
    global title0, label0, cardkb2_0, key_id, key_status

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "CardKB2 UART Mode Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 3, 107, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    cardkb2_0 = CardKBUnit(2, port=(33, 32), mode=CardKBUnit.CardKB_UART_MODE)
    cardkb2_0.set_callback(cardkb2_0_pressed_event)

def loop():
    global title0, label0, cardkb2_0, key_id, key_status
    M5.update()
    cardkb2_0.tick()

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

    input key char and state

#### CardKB2 ESP-NOW Mode

This example display the keyboard input on the screen and serial.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import CardKBUnit

title0 = None
label0 = None
cardkb2_0 = None

key_id = None
key_status = None

def cardkb2_0_pressed_event(kb):
    global title0, label0, cardkb2_0, key_id, key_status
    key_id, key_status = kb
    if key_status == (CardKBUnit.KEY_STATE_PRESS):
        label0.setText(str((str("Key ID ") + str((str(key_id) + str(" Press"))))))
        print((str("Key ID ") + str((str(key_id) + str(" Press")))))
    elif key_status == (CardKBUnit.KEY_STATE_RELEASE):
        label0.setText(str((str("Key ID ") + str((str(key_id) + str(" Release"))))))
        print((str("Key ID ") + str((str(key_id) + str(" Release")))))

def setup():
    global title0, label0, cardkb2_0, key_id, key_status

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "CardKB2 ESPNOW Mode Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 3, 107, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    cardkb2_0 = CardKBUnit(mode=CardKBUnit.CardKB_ESP_NOW_MODE)
    cardkb2_0.set_callback(cardkb2_0_pressed_event)

def loop():
    global title0, label0, cardkb2_0, key_id, key_status
    M5.update()
    cardkb2_0.tick()

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

    input key char and state

## **API**

#### Class CardKB2Unit

## CardKBUnit
Create a CardKBUnit object.

:param args: Positional arguments passed to the underlying communication class.
:param int mode: The communication mode. Default modes are:

    - ``CardKBUnit.CardKB_I2C_MODE`` : I2C mode
    - ``CardKBUnit.CardKB_UART_MODE`` : UART mode
    - ``CardKBUnit.CardKB_ESP_NOW_MODE`` : ESP-NOW mode

.. note::

    This is a factory class. It returns an instance of the appropriate subclass
    based on the specified mode.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from cardkb import CardKBUnit
        from hardware import I2C, Pin

        # I2C mode
        i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
        cardkb_0 = CardKBUnit(i2c0, mode=CardKBUnit.CardKB_I2C_MODE)

        # UART mode
        cardkb_0 = CardKBUnit(2, port=(33, 32), mode=CardKBUnit.CardKB_UART_MODE)

        # ESP-NOW mode
        cardkb_0 = CardKBUnit(mode=CardKBUnit.CardKB_ESP_NOW_MODE)

## CardKBBase
Base class for CardKB unit communication.

This class provides the common interface and logic for all CardKB communication modes.

### `get_key`
Get the next key from the key buffer.

:return: The key value (int or tuple depending on mode)

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        key = cardkb_0.get_key()
        print(key)

### `get_string`
Get the next key as a string.

:return: The string representation of the next key.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        s = cardkb_0.get_string()
        print(s)

### `get_char`
Get the next key as a character.

:return: The character corresponding to the next key code.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        c = cardkb_0.get_char()
        print(c)

### `is_pressed`
Check whether any key is currently pressed.

:return: ``True`` if a key is pressed, ``False`` otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        if cardkb_0.is_pressed():
            print("Key pressed!")

### `set_callback`
Set the callback function for key press events.

:param handler: The callback function to invoke when a key is pressed.
    The callback receives the CardKB instance as its argument.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        # I2C mode example
        def on_key_pressed(kb):
            print("Key pressed:", kb.get_char())

        cardkb_0.set_callback(on_key_pressed)

        # UART/ESP-NOW mode example
        def on_key_event(kb):
            key_id, key_state = kb.get_key()
            print("Key event - ID:", key_id, "State:", key_state)

### `tick`
Poll for key events and trigger the callback if a key is pressed.

This method should be called periodically in the main loop to process key events.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        while True:
            cardkb_0.tick()

## CardKBI2C
CardKB unit driver over I2C communication.

:param I2C i2c: The I2C bus instance.
:param int address: The I2C address of the CardKB unit. Defaults to ``0x5F``.
:param mode: Ignored. Reserved for factory compatibility.

:raises Exception: If the CardKB unit is not found on the I2C bus.

.. note::

    Do not instantiate this class directly. Use :class:`CardKBUnit` with
    ``mode=CardKBUnit.CardKB_I2C_MODE`` instead.

MicroPython Code Block:

    .. code-block:: python

        from hardware import I2C, Pin
        from cardkb import CardKBUnit

        i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
        cardkb_0 = CardKBUnit(i2c0, mode=CardKBUnit.CardKB_I2C_MODE)

### `get_firmware_version`
Read the firmware version from the CardKB unit.

:return: The firmware version byte.
:rtype: int

MicroPython Code Block:

    .. code-block:: python

        version = cardkb_0.get_firmware_version()
        print("Firmware version:", version)

## CardKBUART
CardKB unit driver over UART communication.

:param int id: The UART bus ID (0, 1, or 2). Defaults to ``1``.
:param port: A list or tuple of ``(rx_pin, tx_pin)``.
:param mode: Ignored. Reserved for factory compatibility.

.. note::

    Do not instantiate this class directly. Use :class:`CardKBUnit` with
    ``mode=CardKBUnit.CardKB_UART_MODE`` instead.

MicroPython Code Block:

    .. code-block:: python

        from cardkb import CardKBUnit

        cardkb_0 = CardKBUnit(2, port=(33, 32), mode=CardKBUnit.CardKB_UART_MODE)

### `tick`
Poll the key buffer and trigger the callback if a key is available.

This method should be called periodically in the main loop to process
key events received via UART.

MicroPython Code Block:

    .. code-block:: python

        while True:
            cardkb_0.tick()

## CardKBESPNOW
CardKB unit driver over ESP-NOW wireless communication.

:param mode: Ignored. Reserved for factory compatibility.

.. note::

    Do not instantiate this class directly. Use :class:`CardKBUnit` with
    ``mode=CardKBUnit.CardKB_ESP_NOW_MODE`` instead.

.. note::

    This class uses a broadcast MAC address (``ffffffffffff``) and fixes the
    Wi-Fi channel to 0. Key data is received asynchronously via IRQ callback.

MicroPython Code Block:

    .. code-block:: python

        from cardkb import CardKBUnit

        cardkb_0 = CardKBUnit(mode=CardKBUnit.CardKB_ESP_NOW_MODE)

### `espnow_recv_callback`
Callback function invoked when an ESP-NOW packet is received.

:param espnow_obj: The ESP-NOW object containing the received data.
:return: ``True`` if the frame is valid and a key was appended, ``False`` otherwise.
:rtype: bool

### `get_key`
Get the next key from the buffer received via ESP-NOW.

:return: The key tuple ``(key_id, key_state)``, or ``None`` if the buffer is empty.
:rtype: tuple or None

MicroPython Code Block:

    .. code-block:: python

        key = cardkb_0.get_key()
        if key:
            print("key_id:", key[0], "key_state:", key[1])

### `is_pressed`
Check whether any key data is buffered from ESP-NOW.

:return: ``True`` if there is buffered key data, ``False`` otherwise.
:rtype: bool

MicroPython Code Block:

    .. code-block:: python

        if cardkb_0.is_pressed():
            print("Key received via ESP-NOW!")

### `tick`
Poll the key buffer and trigger the callback if a key is available.

This method should be called periodically in the main loop to process
key events received via ESP-NOW.

MicroPython Code Block:

    .. code-block:: python

        while True:
            cardkb_0.tick()
