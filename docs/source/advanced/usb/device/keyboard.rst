keyboard
=====================================

.. currentmodule:: usb.device.keyboard

.. module:: keyboard
    :synopsis: USB HID keyboard

usb device keyboard

.. include:: ../../../refs/advanced.usb.device.keyboard.ref

.. note::

    Requires native USB device support and the ``usb.device`` package.
    See `Board Capabilities <../../../quick-reference/board-capabilities.html>`_.

Key codes are imported from ``usb.device.hid``, not ``unit`` or
``usb.device.keyboard``. See `Keyboard key codes <../../../hardware/keycode.html>`_ for the
complete ``usb.device.hid.KeyCode`` list and the distinction from CardKB
character codes. In this namespace, Enter is ``KeyCode.ENTER`` (40) and
Escape is ``KeyCode.ESCAPE`` (41); ``KeyCode.KEYCODE_ENTER`` does not exist.

.. code-block:: python

    from usb.device.keyboard import Keyboard
    from usb.device.hid import KeyCode

    keyboard = Keyboard()

The examples below use this ``keyboard`` instance.


Micropython Example
--------------------------------

USB keyboard
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../../../examples/advanced/usb/device/m5cores3_usbd_keyboard_example.py
        :language: python
        :linenos:


UIFlow2.0 Example
------------------------------

USB keyboard
++++++++++++++++++++++++++++

    |example.png|

.. only:: builder_html

    |m5cores3_usbd_keyboard_example.m5f2|


class Keyboard
------------------------------

.. class:: usb.device.keyboard.Keyboard()

    Create Keyboard object

    UIFlow2.0

        |init.png|

.. method:: Keyboard.set_modifiers(right_gui: bool = False, right_alt: bool = False, right_shift: bool = False, right_ctrl: bool = False, \
                       left_gui: bool = False, left_alt: bool = False, left_shift: bool = False, left_ctrl: bool = False)

    Set modifier keys

    - ``right_gui`` The state of the right-side GUI key. True indicates that the key is pressed.
    - ``right_alt`` The state of the right-side Alt key. True indicates that the key is pressed.
    - ``right_shift`` The state of the right-side Shift key. True indicates that the key is pressed.
    - ``right_ctrl`` The state of the right-side Ctrl key. True indicates that the key is pressed.
    - ``left_gui`` The state of the left-side GUI key. True indicates that the key is pressed.
    - ``left_alt`` The state of the left-side Alt key. True indicates that the key is pressed.
    - ``left_shift`` The state of the left-side Shift key. True indicates that the key is pressed.
    - ``left_ctrl``  The state of the left-side Ctrl key. True indicates that the key is pressed.

    :note: Changes will take effect after calling Keyboard.send_report().

    UIFlow2.0

        |set_modifiers.png|


.. method:: Keyboard.set_keys(k0: int = 0, k1: int = 0, k2: int = 0, k3: int = 0, k4: int = 0, k5: int = 0)

    Press specified keys (up to 6 key values at a time)

    - ``k0~k5`` The input is a standard HID key value. For details, see `Keyboard key codes <../../../hardware/keycode.html>`_. Use nonnegative HID usage IDs here; set modifiers separately with ``set_modifiers()``.

    :note: Changes will take effect after calling Keyboard.send_report().

    example: Press the lowercase 'a'

    ::

        keyboard.set_keys(k0=KeyCode.A)
        keyboard.send_report()
        keyboard.set_keys(k0=0)
        keyboard.send_report()

    example: Press the uppercase 'A'

    ::

        keyboard.set_modifiers(right_shift=True)
        keyboard.set_keys(k0=KeyCode.A)
        keyboard.send_report()
        keyboard.set_modifiers(right_shift=False)
        keyboard.set_keys(k0=0)
        keyboard.send_report()

    UIFlow2.0

        |set_keys.png|

.. method:: Keyboard.send_report()

    Send keyboard status report

    UIFlow2.0

        |send_report.png|

.. method:: Keyboard.input(key)

    input key

    - ``key`` A supported ASCII string, or a nonnegative USB HID usage ID from ``usb.device.hid.KeyCode``. An integer is a HID ID, not an ASCII character code. For modifiers, use ``set_modifiers()`` or ``send_keys()`` instead.

    example::

        keyboard.input("Hello M5")
        keyboard.input(KeyCode.A)

    UIFlow2.0

        |input.png|



.. method:: Keyboard.send_keys(down_keys, timeout_ms=100)

    Send a report for an iterable of HID key values. Nonnegative values
    occupy the six key slots; negative ``KeyCode`` modifier constants
    contribute their mask to the modifier byte. This method sends its
    own report and does not use the state set by ``set_keys()`` or
    ``set_modifiers()``.

    :param down_keys: Iterable of USB HID usage IDs and/or negative modifiers.
    :param int timeout_ms: Maximum wait for a previous pending report.
    :return: ``True`` when queued, or ``False`` on timeout/failure.

    .. code-block:: python

        keyboard.send_keys([KeyCode.LEFT_SHIFT, KeyCode.A])
        keyboard.send_keys([])  # Release all keys.
