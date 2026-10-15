4EncoderMotor Driver Unit
=========================

.. sku: U233

.. include:: ../refs/unit.encoder4_motor_driver.ref

This library controls Unit 4EncoderMotor Driver over I2C, including four motor
channels, open-loop PWM, position and speed control, and encoder feedback.

Support the following products:

    |Unit 4EncoderMotor Driver|

UiFlow2 Example
---------------

Four-Motor PWM Control
^^^^^^^^^^^^^^^^^^^^^^

Open the |m5cores3_unit_4encoder_motor_driver_basic_example.m5f2| project in UiFlow2.

Use **CoreS3** and connect the Unit to **Port A** (``SDA=G2``, ``SCL=G1``,
I2C 100 kHz). The default Unit address is ``0x24``.

The m5ui page provides four sliders and a **STOP** touch button:

* Each **M1~M4** slider sets the corresponding motor's PWM target from
  ``0~100`` percent and updates the adjacent label. Moving a slider sets the
  Unit RGB LED to green (``0x009900``).
* **STOP** stops all four motors, changes the RGB LED to red (``0xCC0000``),
  and resets all four displayed values to 0. The slider positions stay unchanged.
  Moving a slider again sends a new PWM target to that motor.

The displayed values are PWM targets. This example uses positive PWM only;
it does not read encoder counts or measured speed.

.. note::

    The sliders start at 0 and the labels show ``00``. Startup selects
    open-loop mode for all four motors and sets the RGB LED to green; it does
    not write initial PWM values. If an earlier program left motor output
    active, press **STOP** before adjusting a slider. Motor power must be present.
    Press **STOP** before ending the example.

UiFlow2 Code Block:

    |m5cores3_unit_4encoder_motor_driver_basic_example.png|

Example output:

    Moving M1 to 40 displays ``40`` beside M1 and sets its PWM to 40 percent.
    **STOP** displays ``0`` beside all four motors and turns the Unit RGB LED red.

MicroPython Example
-------------------

Four-Motor PWM Control
^^^^^^^^^^^^^^^^^^^^^^

Run the same example on CoreS3 with the connection described above.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/encoder4_motor_driver/m5cores3_unit_4encoder_motor_driver_basic_example.py
        :language: python
        :linenos:

Example output:

    Four sliders control the motor PWM targets independently; **STOP** stops
    all four motors. If the Unit is not detected, a connection-check prompt is shown.

**API**
-------

Encoder4MotorDriverUnit
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: unit.encoder4_motor_driver.Encoder4MotorDriverUnit
    :members:
