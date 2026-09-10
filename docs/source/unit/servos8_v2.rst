.. py:currentmodule:: unit.servos8_v2

8Servos2 Unit
=============

.. sku: U222

.. include:: ../refs/unit.servos8_v2.ref

The ``Servos8V2Unit`` class controls the Unit 8Servos2-I2C over I2C. The
device provides eight configurable channels for GPIO input, GPIO output, ADC,
servo, RGB, and PWM operation. It also provides power monitoring and device
information APIs.

Support the following products:

    |Unit 8Servos2-I2C|

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

Open the |basic_8servos_v2_servo_control_example.m5f2| project in UiFlow2.

This example initializes Unit 8Servos2-I2C for servo control. Button A selects
a channel or the all-channel option. Buttons B and C increase or decrease the
servo angle in 10-degree steps. The screen displays the selected channel and
current angle.

UiFlow2 Code Block:

    |example.png|

Example output:

    The selected servo output moves to the angle shown on the screen.

MicroPython Example
-------------------

Servo control
^^^^^^^^^^^^^

This example initializes Unit 8Servos2-I2C for servo control. Button A selects
a channel or the all-channel option. Buttons B and C increase or decrease the
servo angle in 10-degree steps.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/8servos2/basic_8servos_v2_servo_control_example.py
        :language: python
        :linenos:

Example output:

    The screen displays the selected channel and angle, and the selected servo
    output moves when the angle is changed.

**API**
-------

Servos8V2Unit
^^^^^^^^^^^^^

.. autoclass:: unit.servos8_v2.Servos8V2Unit
    :members:
    :member-order: bysource
