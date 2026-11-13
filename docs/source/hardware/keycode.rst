Keyboard key codes
==================

UiFlow2 contains two different classes named ``KeyCode``. Select the import
for the keyboard API being used; their names and integer values are not
interchangeable. No keyboard object is needed to read these constants.

* ``usb.device.hid.KeyCode``: USB HID usage IDs and modifier masks for sending
  reports to a USB host.
* ``unit.cardkb.KeyCode`` (also exported as ``unit.KeyCode``): CardKB legacy
  character and special-key values, including ``KEYCODE_ENTER``.

For example, HID ``ENTER`` is 40 (0x28), CardKB ``KEYCODE_ENTER`` is
10 (0x0A), and the character ``"("`` is also 40 in ASCII. Comparing a
character code with a HID usage ID can therefore match an unrelated key.

USB HID KeyCode
----------------

.. class:: usb.device.hid.KeyCode

    A constant namespace; use the class attributes without instantiating it.
    It is used by `USB device keyboard <../advanced/usb/device/keyboard.html>`_. Sending USB reports
    requires a controller and firmware with runtime USB device support;
    this list alone does not establish that a board supports USB HID.

.. code-block:: python

    from usb.device.hid import KeyCode as HIDKeyCode

    assert HIDKeyCode.ENTER == 0x28
    assert HIDKeyCode.A == 0x04

Use nonnegative usage IDs with ``keyboard.set_keys()`` and then call
``keyboard.send_report()``. Negative modifier values below are for
``keyboard.send_keys()``; with ``set_keys()``, set modifiers separately
using ``keyboard.set_modifiers()``. A modifier mask is not an ordinary
key-array entry.

The complete exported constant list is:

* ``A = 4`` (0x04)
* ``B = 5`` (0x05)
* ``C = 6`` (0x06)
* ``D = 7`` (0x07)
* ``E = 8`` (0x08)
* ``F = 9`` (0x09)
* ``G = 10`` (0x0A)
* ``H = 11`` (0x0B)
* ``I = 12`` (0x0C)
* ``J = 13`` (0x0D)
* ``K = 14`` (0x0E)
* ``L = 15`` (0x0F)
* ``M = 16`` (0x10)
* ``N = 17`` (0x11)
* ``O = 18`` (0x12)
* ``P = 19`` (0x13)
* ``Q = 20`` (0x14)
* ``R = 21`` (0x15)
* ``S = 22`` (0x16)
* ``T = 23`` (0x17)
* ``U = 24`` (0x18)
* ``V = 25`` (0x19)
* ``W = 26`` (0x1A)
* ``X = 27`` (0x1B)
* ``Y = 28`` (0x1C)
* ``Z = 29`` (0x1D)
* ``N1 = 30`` (0x1E)
* ``N2 = 31`` (0x1F)
* ``N3 = 32`` (0x20)
* ``N4 = 33`` (0x21)
* ``N5 = 34`` (0x22)
* ``N6 = 35`` (0x23)
* ``N7 = 36`` (0x24)
* ``N8 = 37`` (0x25)
* ``N9 = 38`` (0x26)
* ``N0 = 39`` (0x27)
* ``ENTER = 40`` (0x28)
* ``ESCAPE = 41`` (0x29)
* ``BACKSPACE = 42`` (0x2A)
* ``TAB = 43`` (0x2B)
* ``SPACE = 44`` (0x2C)
* ``MINUS = 45`` (0x2D)
* ``EQUAL = 46`` (0x2E)
* ``OPEN_BRACKET = 47`` (0x2F)
* ``CLOSE_BRACKET = 48`` (0x30)
* ``BACKSLASH = 49`` (0x31)
* ``HASH = 50`` (0x32)
* ``SEMICOLON = 51`` (0x33)
* ``QUOTE = 52`` (0x34)
* ``GRAVE = 53`` (0x35)
* ``COMMA = 54`` (0x36)
* ``DOT = 55`` (0x37)
* ``SLASH = 56`` (0x38)
* ``CAPS_LOCK = 57`` (0x39)
* ``F1 = 58`` (0x3A)
* ``F2 = 59`` (0x3B)
* ``F3 = 60`` (0x3C)
* ``F4 = 61`` (0x3D)
* ``F5 = 62`` (0x3E)
* ``F6 = 63`` (0x3F)
* ``F7 = 64`` (0x40)
* ``F8 = 65`` (0x41)
* ``F9 = 66`` (0x42)
* ``F10 = 67`` (0x43)
* ``F11 = 68`` (0x44)
* ``F12 = 69`` (0x45)
* ``PRINTSCREEN = 70`` (0x46)
* ``SCROLL_LOCK = 71`` (0x47)
* ``PAUSE = 72`` (0x48)
* ``INSERT = 73`` (0x49)
* ``HOME = 74`` (0x4A)
* ``PAGEUP = 75`` (0x4B)
* ``DELETE = 76`` (0x4C)
* ``END = 77`` (0x4D)
* ``PAGEDOWN = 78`` (0x4E)
* ``RIGHT = 79`` (0x4F)
* ``LEFT = 80`` (0x50)
* ``DOWN = 81`` (0x51)
* ``UP = 82`` (0x52)
* ``KP_NUM_LOCK = 83`` (0x53)
* ``KP_DIVIDE = 84`` (0x54)
* ``KP_AT = 85`` (0x55)
* ``KP_MULTIPLY = 85`` (0x55)
* ``KP_MINUS = 86`` (0x56)
* ``KP_PLUS = 87`` (0x57)
* ``KP_ENTER = 88`` (0x58)
* ``KP_1 = 89`` (0x59)
* ``KP_2 = 90`` (0x5A)
* ``KP_3 = 91`` (0x5B)
* ``KP_4 = 92`` (0x5C)
* ``KP_5 = 93`` (0x5D)
* ``KP_6 = 94`` (0x5E)
* ``KP_7 = 95`` (0x5F)
* ``KP_8 = 96`` (0x60)
* ``KP_9 = 97`` (0x61)
* ``KP_0 = 98`` (0x62)
* ``LEFT_CTRL = -1`` (-0x01)
* ``LEFT_SHIFT = -2`` (-0x02)
* ``LEFT_ALT = -4`` (-0x04)
* ``LEFT_UI = -8`` (-0x08)
* ``RIGHT_CTRL = -16`` (-0x10)
* ``RIGHT_SHIFT = -32`` (-0x20)
* ``RIGHT_ALT = -64`` (-0x40)
* ``RIGHT_UI = -128`` (-0x80)


``ESCAPE``, ``PAGEUP``, ``PAGEDOWN``, ``LEFT_UI`` and ``RIGHT_UI`` are the
actual exported spellings. ``KP_AT`` and ``KP_MULTIPLY`` are aliases with
the same value. Do not invent alternative names such as ``ESC`` or
``KEYCODE_ENTER`` in this namespace.

CardKB KeyCode
----------------

.. class:: unit.cardkb.KeyCode

    A constant namespace also available through ``from unit import KeyCode``.
    These ``KEYCODE_*`` names exist in UiFlow2; they are not USB HID usage IDs.
    Use them for the character values returned by CardKB in I2C mode.

.. code-block:: python

    from unit import KeyCode as CardKBKeyCode

    assert CardKBKeyCode.KEYCODE_ENTER == 0x0A
    assert CardKBKeyCode.KEYCODE_LEFT == 180

The complete exported constant list is:

* ``KEYCODE_UNKNOWN = 0`` (0x00)
* ``KEYCODE_BACKSPACE = 8`` (0x08)
* ``KEYCODE_TAB = 9`` (0x09)
* ``KEYCODE_ENTER = 10`` (0x0A)
* ``KEYCODE_ESC = 27`` (0x1B)
* ``KEYCODE_SPACE = 32`` (0x20)
* ``KEYCODE_DEL = 127`` (0x7F)
* ``KEYCODE_LEFT = 180`` (0xB4)
* ``KEYCODE_UP = 181`` (0xB5)
* ``KEYCODE_DOWN = 182`` (0xB6)
* ``KEYCODE_RIGHT = 183`` (0xB7)


The `CardKB Unit <../unit/cardkb.html>`_ I2C driver returns an integer or ``None`` when
the queue is empty. Printable keys use character values, for example
``ord("a") == 97``. UART and ESP-NOW ``get_key()`` return
``(key_id, key_state)`` tuples or ``None`` instead. The V2 report protocol
uses HID usage IDs in those tuples and in ``get_report()``; the I2C driver
converts V2 key presses to character values. Do not compare a tuple or an
unconverted HID ID directly with a CardKB character constant.

Built-in Cardputer keyboards
----------------------------

``hardware.Keyboard.get_key(point)`` is a low-level key-map lookup requiring
a ``Point2D`` argument. It returns a mapped integer character/special-key
value; it is not a USB HID key reader or the no-argument queue API below.

``hardware.MatrixKeyboard.get_key()`` reads the built-in keyboard on
Cardputer or Cardputer Adv and returns an integer, or ``None`` when no key
is queued. Printable values can be converted with ``chr(value)``. These
values are not USB HID usage IDs. In the current implementation:

* Cardputer: Enter is 13 (0x0D); Escape is 27, Backspace is 8, and the
  Fn-arrow values are Left 180, Up 181, Down 182 and Right 183.
* Cardputer Adv: Enter is 10 (0x0A), matching
  ``CardKBKeyCode.KEYCODE_ENTER``; the Fn-arrow values are also 180--183.

Check for ``None`` before numeric comparisons. For an Enter test intended
to accept both built-in keyboards, compare with both character codes:

.. code-block:: python

    key = kb.get_key()  # kb is an initialized hardware.MatrixKeyboard
    if key is None:
        pass
    elif key in (0x0A, 0x0D):
        print("Enter")
    elif 0x20 <= key <= 0x7E:
        print(chr(key))

The `LoRa1262 Cap <../cap/lora1262.html>`_ sender uses the Cardputer Adv character path,
so ``from unit import KeyCode`` resolves to the CardKB constants. To
send that character through USB, translate it to the corresponding HID
usage ID or pass a supported character string to ``keyboard.input()``.
Neither operation is a direct identity mapping of integer codes.
