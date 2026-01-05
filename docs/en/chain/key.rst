Chain Key
=========

.. include:: ../refs/chain.key.ref

Chain Key is a key module that can be connected to the M5Chain series devices. This module provides functions to read the key states.

Support the following products:

    |Chain Key|

UiFlow2 Example
---------------

USB Keyboard
^^^^^^^^^^^^

Open the |chain_key_usb_keyboard_example.m5f2| project in UiFlow2.

This example demonstrates how to use the Chain Key as a USB keyboard.

UiFlow2 Code Block:

    |chain_key_usb_keyboard_example.png|

Example output:

    None

MicroPython Example
-------------------

USB Keyboard
^^^^^^^^^^^^

This example demonstrates how to use the Chain Key as a USB keyboard.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/key/chain_key_usb_keyboard_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

KeyChain
^^^^^^^^

.. autoclass:: chain.key.KeyChain
    :members:
    :member-order: bysource
    :exclude-members:
