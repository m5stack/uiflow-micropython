Tab5 Keyboard
=============

.. py:currentmodule:: tab5.keyboard

.. include:: ../refs/tab5.keyboard.ref

The `Keyboard` class controls the Tab5 keyboard controller over I2C. It supports
character input callbacks, raw key matrix events, keyboard mode configuration,
backlight brightness, RGB LED settings, and I2C address management.

UiFlow2 Example
---------------

keyboard input
^^^^^^^^^^^^^^

Open the |tab5_keyboard_example.m5f2| project in UiFlow2.

This example reads character input from the Tab5 keyboard and appends it to a text area.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

keyboard input
^^^^^^^^^^^^^^

This example reads character input from the Tab5 keyboard and appends it to a text area.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/tab5/keyboard/tab5_keyboard_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

Keyboard
^^^^^^^^

.. autoclass:: tab5.keyboard.Keyboard
    :members:
    :member-order: bysource
