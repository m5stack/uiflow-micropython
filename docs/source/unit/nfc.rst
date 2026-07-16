NFC Unit
========

.. sku:

.. include:: ../refs/unit.nfc.ref

This library drives **Unit NFC** (ST25R3916 on I2C). It discovers ISO14443 Type A tags, resolves chip type (Classic, Ultralight / NTAG family, DESFire, Plus, etc.), 
and exposes high-level read/write helpers for supported tag kinds.
The lower-level ``driver.st25r3916.ST25R3916`` transport supports both I2C and SPI. Unit NFC uses I2C; NFCCap and other combo products can pass a pre-built SPI chip object into ``NFCUnit``.


Support the following products:

    |NFCUnit|

UiFlow2 Example
---------------

Detect card
^^^^^^^^^^^

Open the |cores3_unit_nfc_example.m5f2| project in UiFlow2.

This example polls the reader, shows UID, type name, and user memory size on the screen, and plays a short tone when a tag is present.

UiFlow2 Code Block:

    |cores3_unit_nfc_example.png|

Example output:

    None

MicroPython Example
-------------------

Detect card
^^^^^^^^^^^

This example polls the reader, shows UID, type name, and user memory size on the screen, and plays a short tone when a tag is present.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/nfc/cores3_unit_nfc_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

NFCUnit
^^^^^^^

.. class:: unit.nfc.NFCUnit

    Driver for Unit NFC. Pass a configured ``I2C`` bus instance (for example from ``hardware.I2C``).

    :param i2c: I2C bus used to talk to the ST25R3916.

    ``NFCUnit`` can also wrap a pre-built ``driver.st25r3916.ST25R3916`` object for SPI mode.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import Pin, I2C
            from unit import NFCUnit

            i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
            nfc = NFCUnit(i2c0)

    SPI products create the ST25R3916 chip first, then wrap it with ``NFCUnit``:

    MicroPython Code Block:

        .. code-block:: python

            import machine
            from driver.st25r3916 import ST25R3916
            from unit import NFCUnit

            spi = machine.SPI(1, baudrate=2000000, polarity=0, phase=1)
            nfc = NFCUnit(chip=ST25R3916(spi=spi, cs=6, irq=4))

    .. method:: detect()

        Poll for a Type A tag in the field.

        :returns: A :class:`unit.nfc.Card` instance if a tag was found and identified, otherwise ``None``.

        UiFlow2 Code Block:

            |detect.png|

        MicroPython Code Block:

            .. code-block:: python

                card = nfc.detect()
                if card:
                    print(card.uid_str, card.type_name)

    .. method:: write(card, index, data)

        Write one **address unit**.

        .. note::
            Use writable test cards only. Do not write UID pages, lock bytes, sector trailers, access-control blocks, or cards used for access/payment/identity.

        For **MIFARE Classic**, ``data`` must be **16** bytes and ``index`` is the global block number.
        For **Type 2** tags, ``data`` must be **4** bytes and ``index`` is the page number.
        Sector trailers, block ``0``, lock bytes, and configuration pages require valid card-specific access rules.
        :param unit.nfc.Card card: Tag from :meth:`detect`.
        :param int index: Block index for Classic, or page index for Type 2.
        :param bytes data: Exactly 16 bytes for Classic, or exactly 4 bytes for Type 2.
        :returns: ``True`` on success, ``False`` otherwise.

        UiFlow2 Code Block:

            |write.png|

        MicroPython Code Block:

            .. code-block:: python

                ok = nfc.write(card, index, data)

    .. method:: read(card, index)

        Read one **address unit** for the current tag.

        - **MIFARE Classic**: ``index`` is the **global block number** (0-based). Returns **16** bytes on success, or ``None``.
        - **Type 2 family** (Ultralight / NTAG / ST25TA / ISO18092 where applicable): ``index`` is the **page number**. Returns **4** bytes on success, or ``None``.
        - Other chip types: ``None`` (use chip-specific flows outside this helper).

        :param unit.nfc.Card card: Tag returned by :meth:`detect`.
        :param int index: Block index (Classic) or page index (Type 2).
        :returns: ``bytes`` or ``None``.

        UiFlow2 Code Block:

            |read.png|

        MicroPython Code Block:

            .. code-block:: python

                data = nfc.read(card, index)

    .. method:: halt()

        Send HLTA to put the Type A PICC into HALT state.

        UiFlow2 Code Block:

            |halt.png|

        MicroPython Code Block:

            .. code-block:: python

                nfc.halt()

    .. method:: rf_off()

        Turn the reader RF field off.

        UiFlow2 Code Block:

            |rf_off.png|

        MicroPython Code Block:

            .. code-block:: python

                nfc.rf_off()

    .. method:: rf_on()

        Turn the reader RF field on.

        UiFlow2 Code Block:

            |rf_on.png|

        MicroPython Code Block:

            .. code-block:: python

                nfc.rf_on()

Card
^^^^

.. class:: unit.nfc.Card

    Object returned by :meth:`NFCUnit.detect` when a tag is present. Holds the anti-collision result and the resolved type metadata from the stack (SAK/ATQA/version/ATS paths as implemented in firmware).

    **Attributes**

    UiFlow2 Code Block:

        |attribute.png|

    .. attribute:: uid

        ``bytes`` — UID bytes (length ``uid_len``).

    .. attribute:: type_id

        ``int`` — Internal type id used by this driver (aligned with the ``TYPE_NAMES`` table in ``unit/nfc.py``).

    .. attribute:: type_name

        ``str`` — Resolved chip label from the identification logic in firmware; same strings as ``TYPE_NAMES`` in ``unit/nfc.py``. ``type_id`` selects the row below (unknown or unclassified tags use ``Unknown``).

        .. list-table:: ``type_id`` and ``type_name`` (index into ``TYPE_NAMES``)
            :header-rows: 1
            :widths: 8 42

            * - ``type_id``
              - ``type_name``
            * - 0
              - ``Unknown``
            * - 1
              - ``MIFARE_Classic_Mini``
            * - 2
              - ``MIFARE_Classic_1K``
            * - 3
              - ``MIFARE_Classic_2K``
            * - 4
              - ``MIFARE_Classic_4K``
            * - 5
              - ``MIFARE_Ultralight``
            * - 6
              - ``MIFARE_Ultralight_EV1_1``
            * - 7
              - ``MIFARE_Ultralight_EV1_2``
            * - 8
              - ``MIFARE_Ultralight_Nano``
            * - 9
              - ``MIFARE_UltralightC``
            * - 10
              - ``NTAG_203``
            * - 11
              - ``NTAG_210u``
            * - 12
              - ``NTAG_210``
            * - 13
              - ``NTAG_212``
            * - 14
              - ``NTAG_213``
            * - 15
              - ``NTAG_215``
            * - 16
              - ``NTAG_216``
            * - 17
              - ``ST25TA_512B``
            * - 18
              - ``ST25TA_2K``
            * - 19
              - ``ST25TA_16K``
            * - 20
              - ``ST25TA_64K``
            * - 21
              - ``ISO_14443_4``
            * - 22
              - ``MIFARE_Plus_2K``
            * - 23
              - ``MIFARE_Plus_4K``
            * - 24
              - ``MIFARE_Plus_SE``
            * - 25
              - ``MIFARE_DESFire_2K``
            * - 26
              - ``MIFARE_DESFire_4K``
            * - 27
              - ``MIFARE_DESFire_8K``
            * - 28
              - ``MIFARE_DESFire_Light``
            * - 29
              - ``NTAG_4XX``
            * - 30
              - ``ISO_18092``

    .. attribute:: user_memory

        ``int`` — Advertised user memory size in **bytes** for known types (``0`` if unknown; used for Type 2 dump heuristics).

    .. attribute:: uid_str

        UID as upper-case hex string.

    .. method:: is_classic()

        Return ``True`` if ``type_id`` is a MIFARE Classic family id (Mini / 1K / 2K / 4K).

        UiFlow2 Code Block:

            |is_classic.png|

        MicroPython Code Block:

            .. code-block:: python

                card.is_classic()
