Chain Joystick
==============

.. include:: ../refs/chain.joystick.ref

Chain Joystick is a joystick module that can be connected to the M5Chain series devices. This module provides functions to read the joystick position and button states.

UiFlow2 Example
---------------

USB Mouse
^^^^^^^^^

Open the |chain_joystick_usb_mouse_example.m5f2| project in UiFlow2.

This example demonstrates how to use the Chain Joystick as a USB mouse.

UiFlow2 Code Block:

    |chain_joystick_usb_mouse_example.png|

Example output:

    None

MicroPython Example
-------------------

USB Mouse
^^^^^^^^^

This example demonstrates how to use the Chain Joystick as a USB mouse.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/joystick/chain_joystick_usb_mouse_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

JoystickChain
^^^^^^^^^^^^^

.. autoclass:: chain.joystick.JoystickChain
    :members:
    :member-order: bysource
    :exclude-members:

    For other button and some general methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.
