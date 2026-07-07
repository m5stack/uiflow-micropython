# NFC Unit

<!-- .. sku: -->

<!-- .. include:: ../refs/unit.nfc.ref -->

This library drives **Unit NFC** (ST25R3916 on I2C). It discovers ISO14443 Type A tags, resolves chip type (Classic, Ultralight / NTAG family, DESFire, Plus, etc.),
and exposes high-level read/write helpers for supported tag kinds.

Support the following products:

    |NFCUnit|

## UiFlow2 Example

#### Detect card

Open the |cores3_unit_nfc_example.m5f2| project in UiFlow2.

This example polls the reader, shows UID, type name, and user memory size on the screen, and plays a short tone when a tag is present.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Detect card

This example polls the reader, shows UID, type name, and user memory size on the screen, and plays a short tone when a tag is present.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import Pin
from hardware import I2C
from unit import NFCUnit
import time

page0 = None
label_title = None
label_uid = None
label_type = None
label_size = None
i2c0 = None
nfc_0 = None
card_0 = None
card_uid = None
new = None
card_type = None
card_memory = None
write_buf = None
count = None
last_time = None

def setup():
    global \
        page0, \
        label_title, \
        label_uid, \
        label_type, \
        label_size, \
        i2c0, \
        nfc_0, \
        card_0, \
        card_uid, \
        new, \
        card_type, \
        card_memory, \
        write_buf, \
        count, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "NFC Card detect",
        x=58,
        y=5,
        text_c=0x14ACDB,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_uid = m5ui.M5Label(
        "UID:",
        x=18,
        y=70,
        text_c=0xFFFFFF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_type = m5ui.M5Label(
        "Type:",
        x=10,
        y=100,
        text_c=0xFFFFFF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_size = m5ui.M5Label(
        "Size:",
        x=16,
        y=130,
        text_c=0xFFFFFF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    nfc_0 = NFCUnit(i2c0)
    page0.screen_load()
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)
    new = True
    write_buf = bytearray(16)
    write_buf[0] = 0x12
    count = 0

def loop():
    global \
        page0, \
        label_title, \
        label_uid, \
        label_type, \
        label_size, \
        i2c0, \
        nfc_0, \
        card_0, \
        card_uid, \
        new, \
        card_type, \
        card_memory, \
        write_buf, \
        count, \
        last_time
    M5.update()
    card_0 = nfc_0.detect()
    if card_0:
        card_uid = card_0.uid_str
        card_type = card_0.type_name
        card_memory = card_0.user_memory
        label_uid.set_text(str((str("UID: ") + str(card_uid))))
        label_type.set_text(str((str("Type: ") + str(card_type))))
        label_size.set_text(str((str("Size: ") + str(card_memory))))
        if (time.ticks_diff((time.ticks_ms()), last_time)) >= 3000 or new:
            last_time = time.ticks_ms()
            Speaker.tone(900, 100)
            print((str("read data befor write ") + str((nfc_0.read(card_0, 1)))))
            count = (count if isinstance(count, (int, float)) else 0) + 1
            write_buf[-1] = 0x12 + count
            time.sleep_ms(100)
            if nfc_0.write(card_0, 1, write_buf):
                print("write success")
                time.sleep_ms(100)
                print((str("read data after write ") + str((nfc_0.read(card_0, 1)))))
        new = False
    else:
        new = True

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

#### NFCUnit

<!-- .. class:: unit.nfc.NFCUnit -->

    Driver for Unit NFC. Pass a configured ``I2C`` bus instance (for example from ``hardware.I2C``).

    :param i2c: I2C bus used to talk to the ST25R3916.

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from hardware import Pin, I2C
            from unit import NFCUnit

            i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
            nfc = NFCUnit(i2c0)

<!-- .. method:: detect() -->

        Poll for a Type A tag in the field.

        :returns: A :class:`unit.nfc.Card` instance if a tag was found and identified, otherwise ``None``.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                card = nfc.detect()
                if card:
                    print(card.uid_str, card.type_name)

<!-- .. method:: write(card, index, data) -->

        Write one **address unit**.

<!-- .. note:: -->
            Only MIFARE Classic is supported for now.

        ``data`` must be **16** bytes; ``index`` is the block number. Sector trailers and block ``0`` require valid keys/access rules from the card.

        :param unit.nfc.Card card: Tag from :meth:`detect`.
        :param int index: Block index.
        :param bytes data: Exactly 16 bytes for Classic.
        :returns: ``True`` on success, ``False`` otherwise.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                ok = nfc.write(card, index, data)

<!-- .. method:: read(card, index) -->

        Read one **address unit** for the current tag.

        - **MIFARE Classic**: ``index`` is the **global block number** (0-based). Returns **16** bytes on success, or ``None``.
        - **Type 2 family** (Ultralight / NTAG / ST25TA / ISO18092 where applicable): ``index`` is the **page number**. Returns **4** bytes on success, or ``None``.
        - Other chip types: ``None`` (use chip-specific flows outside this helper).

        :param unit.nfc.Card card: Tag returned by :meth:`detect`.
        :param int index: Block index (Classic) or page index (Type 2).
        :returns: ``bytes`` or ``None``.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                data = nfc.read(card, index)

<!-- .. method:: halt() -->

        Send HLTA to put the Type A PICC into HALT state.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                nfc.halt()

<!-- .. method:: rf_off() -->

        Turn the reader RF field off.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                nfc.rf_off()

<!-- .. method:: rf_on() -->

        Turn the reader RF field on.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                nfc.rf_on()

#### Card

<!-- .. class:: unit.nfc.Card -->

    Object returned by :meth:`NFCUnit.detect` when a tag is present. Holds the anti-collision result and the resolved type metadata from the stack (SAK/ATQA/version/ATS paths as implemented in firmware).

    **Attributes**

    UiFlow2 Code Block:

<!-- .. attribute:: uid -->

        ``bytes`` — UID bytes (length ``uid_len``).

<!-- .. attribute:: type_id -->

        ``int`` — Internal type id used by this driver (aligned with the ``TYPE_NAMES`` table in ``unit/nfc.py``).

<!-- .. attribute:: type_name -->

        ``str`` — Resolved chip label from the identification logic in firmware; same strings as ``TYPE_NAMES`` in ``unit/nfc.py``. ``type_id`` selects the row below (unknown or unclassified tags use ``Unknown``).

<!-- .. list-table:: ``type_id`` and ``type_name`` (index into ``TYPE_NAMES``) -->
            :header-rows: 1
            :widths: 8 42

            - - ``type_id``
              - ``type_name``
            - - 0
              - ``Unknown``
            - - 1
              - ``MIFARE_Classic_Mini``
            - - 2
              - ``MIFARE_Classic_1K``
            - - 3
              - ``MIFARE_Classic_2K``
            - - 4
              - ``MIFARE_Classic_4K``
            - - 5
              - ``MIFARE_Ultralight``
            - - 6
              - ``MIFARE_Ultralight_EV1_1``
            - - 7
              - ``MIFARE_Ultralight_EV1_2``
            - - 8
              - ``MIFARE_Ultralight_Nano``
            - - 9
              - ``MIFARE_UltralightC``
            - - 10
              - ``NTAG_203``
            - - 11
              - ``NTAG_210u``
            - - 12
              - ``NTAG_210``
            - - 13
              - ``NTAG_212``
            - - 14
              - ``NTAG_213``
            - - 15
              - ``NTAG_215``
            - - 16
              - ``NTAG_216``
            - - 17
              - ``ST25TA_512B``
            - - 18
              - ``ST25TA_2K``
            - - 19
              - ``ST25TA_16K``
            - - 20
              - ``ST25TA_64K``
            - - 21
              - ``ISO_14443_4``
            - - 22
              - ``MIFARE_Plus_2K``
            - - 23
              - ``MIFARE_Plus_4K``
            - - 24
              - ``MIFARE_Plus_SE``
            - - 25
              - ``MIFARE_DESFire_2K``
            - - 26
              - ``MIFARE_DESFire_4K``
            - - 27
              - ``MIFARE_DESFire_8K``
            - - 28
              - ``MIFARE_DESFire_Light``
            - - 29
              - ``NTAG_4XX``
            - - 30
              - ``ISO_18092``

<!-- .. attribute:: user_memory -->

        ``int`` — Advertised user memory size in **bytes** for known types (``0`` if unknown; used for Type 2 dump heuristics).

<!-- .. attribute:: uid_str -->

        UID as upper-case hex string.

<!-- .. method:: is_classic() -->

        Return ``True`` if ``type_id`` is a MIFARE Classic family id (Mini / 1K / 2K / 4K).

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                card.is_classic()
