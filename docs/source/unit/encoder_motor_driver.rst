EncoderMotor Driver Unit
========================

.. sku: U232

.. include:: ../refs/unit.encoder_motor_driver.ref

The ``EncoderMotorDriverUnit`` class controls Unit EncoderMotor Driver over I2C.
It supports signed open-loop PWM, position and speed control, encoder feedback,
motor sleep, soft start and stop, RGB LED control, and input power monitoring.

Support the following products:

    |Unit EncoderMotor Driver|

UiFlow2 Example
---------------

Basic Motor Control
^^^^^^^^^^^^^^^^^^^

Open the |m5cores3_unit_encoder_motor_driver_basic_example.m5f2| project in UiFlow2.

Select **CoreS3** and connect the Unit to **Port A**
(``SDA=G2``, ``SCL=G1``, I2C 100 kHz). The default Unit address is ``0x2F``.

The m5ui page provides three touch buttons:

* **+** adds 20 percentage points to the signed PWM target. Pressing it while
  the target is 80 sets the target to 0.
* **-** subtracts 20 percentage points from the signed PWM target. Pressing it
  while the target is -80 sets the target to 0.
* **STOP** sets PWM to 0.

Positive and negative PWM select opposite directions. The center label displays
the commanded PWM percentage in the range ``-80~80``; it does not display RPM
or encoder counts. The target starts at 0.

.. note::

    This example uses the Unit's default open-loop mode and enabled motor
    driver. If a previous program selected a closed-loop mode or disabled the
    driver, restore open-loop mode with ``set_motor_mode(MODE_OPEN_LOOP)`` and
    enable it with ``enable_motor()`` before running this example. Restarting
    the Unit also restores these runtime defaults. Motor power must be present.
    Press **STOP** before ending the example.

UiFlow2 Code Block:

    |m5cores3_unit_encoder_motor_driver_basic_example.png|

Example output:

    The CoreS3 screen shows the signed PWM target. For example, two **+** taps
    from startup display ``40``; **STOP** displays ``0``.

MicroPython Example
-------------------

Basic Motor Control
^^^^^^^^^^^^^^^^^^^

Run the following example on CoreS3 with the same connection and Unit runtime
settings described above. The ``+``, ``-`` and ``STOP`` controls have the same
behavior as the UiFlow2 project.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/encoder_motor_driver/m5cores3_unit_encoder_motor_driver_basic_example.py
        :language: python
        :linenos:

Example output:

    The center label shows the PWM target. If the Unit is not detected,
    the screen shows a connection-check prompt.

**API**
-------

EncoderMotorDriverUnit
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: unit.encoder_motor_driver.EncoderMotorDriverUnit
    :members:
