.. py:currentmodule:: chain.servos8_v2

Chain 8Servos2
==============

.. sku: U223

.. include:: ../refs/chain.servos8_v2.ref

The ``Servos8V2Chain`` class controls the Unit 8Servos2-Chain through a
``ChainBus``. The device provides eight configurable channels for GPIO input,
GPIO output, ADC, servo, RGB, and PWM operation. It also provides power
monitoring, UID, firmware, bootloader, and device type APIs.

Support the following products:

    |Unit 8Servos2-Chain|

Constants
---------

Use the following constants with ``set_channel_mode()``:

- ``MODE_INPUT``: GPIO input mode.
- ``MODE_OUTPUT``: GPIO output mode.
- ``MODE_ADC``: ADC input mode.
- ``MODE_SERVO``: Servo control mode.
- ``MODE_RGB``: RGB output mode for WS2812 LEDs.
- ``MODE_PWM``: PWM duty output mode.

Use ``PULL_NONE``, ``PULL_UP``, or ``PULL_DOWN`` with
``set_input_pull()``.

.. note::

    Channels 0-3 share one PWM frequency, and channels 4-7 share another.
    Setting the frequency of one channel changes every channel in the same
    group. Selecting servo mode sets the channel's shared group to 50 Hz.

UiFlow2 Example
---------------

Servo control
^^^^^^^^^^^^^

Initialize Unit 8Servos2-Chain, set a channel to servo mode, and set its
angle.

UiFlow2 Code Block:

    |example.png|

Example output:

    The selected servo moves to the configured angle.

MicroPython Example
-------------------

Basic control
^^^^^^^^^^^^^

This example reads device information and power values from Unit
8Servos2-Chain, then moves each servo channel between 0 and 180 degrees.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/8servos2/m5basic_chain_8servos2_basic_example.py
        :language: python
        :linenos:

Example output:

    Device information and power values are printed to the serial console,
    and each connected servo moves through the test sequence.

**API**
-------

Servos8V2Chain
^^^^^^^^^^^^^^

.. autoclass:: chain.servos8_v2.Servos8V2Chain
    :members:
    :member-order: bysource

    For general Chain device methods, refer to
    :class:`KeyChain <chain.key.KeyChain>`.
