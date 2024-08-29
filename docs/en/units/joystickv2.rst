
JoystickV2Unit
==============

.. include:: ../refs/unit.joystickv2unit.ref

The joystick is an input unit for control, utilizing an I2C communication interface and supporting three-axis control signals (X/Y-axis analog input for displacement and Z-axis digital input for key presses). It is ideal for applications like gaming and robot control.

Support the following products:

|JoystickV2Unit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import JoystickV2Unit
    from hardware import *
    i2c = I2C(1, scl=22, sda=21)
    joystick = JoystickV2Unit(i2c)
    joystick.read_adc_value()
    joystick.read_button_status()
    joystick.set_rgb_led(255, 0, 0)
    joystick.get_rgb_led()
    joystick.set_deadzone_position(200, 200)
    while True:
        joystick.read_axis_position()

UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

class JoystickV2Unit
--------------------

Constructors
------------

.. class:: JoystickV2Unit(i2c, address)

	Initialize the JoystickV2 Unit.

    :param I2C i2c: I2C port to use.
    :param int address: I2C address of the JoystickV2 Unit.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: JoystickV2Unit.set_axis_x_invert(invert)

    Invert the X-axis of the joystick.

    :param bool invert: Whether to invert the X-axis.

    UIFLOW2:

        |set_axis_x_invert.svg|

.. method:: JoystickV2Unit.set_axis_y_invert(invert)

    Invert the Y-axis of the joystick.

    :param bool invert: Whether to invert the Y-axis.

    UIFLOW2:

        |set_axis_y_invert.svg|

.. method:: JoystickV2Unit.set_axis_swap(swap)

    Swap the X-axis and Y-axis of the joystick.

    :param bool swap: Whether to swap the X-axis and Y-axis.

    UIFLOW2:

        |set_axis_swap.svg|

.. method:: JoystickV2Unit.read_adc_value()

    Read the ADC value of the joystick.


    UIFLOW2:

        |read_adc_value.svg|

.. method:: JoystickV2Unit.read_button_status()

    Read the button status of the joystick.


    UIFLOW2:

        |read_button_status.svg|

.. method:: JoystickV2Unit.set_rgb_led(r, g, b)

    Set the RGB LED color of the joystick.

    :param int r: The red value (0-255).
    :param int g: The green value (0-255).
    :param int b: The blue value (0-255).

    UIFLOW2:

        |set_rgb_led.svg|

.. method:: JoystickV2Unit.get_rgb_led()

    Get the RGB LED color of the joystick.


    UIFLOW2:

        |get_rgb_led.svg|

.. method:: JoystickV2Unit.set_axis_x_mapping(adc_neg_min, adc_neg_max, adc_pos_min, adc_pos_max)

    Set the mapping parameters of the X-axis.

ADC Raw     0                                                    65536
            |------------------------------------------------------|
Mapped    -4096                   0           0                   4096
            |---------------------|-dead zone-|--------------------|
      adc_neg_min        adc_neg_max        adc_pos_min         adc_pos_max


    :param int adc_neg_min: The minimum ADC value of the negative range.
    :param int adc_neg_max: The maximum ADC value of the negative range.
    :param int adc_pos_min: The minimum ADC value of the positive range.
    :param int adc_pos_max: The maximum ADC value of the positive range.

    UIFLOW2:

        |set_axis_x_mapping.svg|

.. method:: JoystickV2Unit.set_axis_y_mapping(adc_neg_min, adc_neg_max, adc_pos_min, adc_pos_max)

    Set the mapping parameters of the Y-axis.

ADC Raw     0                                                    65536
            |------------------------------------------------------|
Mapped    -4096                   0           0                   4096
            |---------------------|-dead zone-|--------------------|
      adc_neg_min        adc_neg_max        adc_pos_min         adc_pos_max


    :param int adc_neg_min: The minimum ADC value of the negative range.
    :param int adc_neg_max: The maximum ADC value of the negative range.
    :param int adc_pos_min: The minimum ADC value of the positive range.
    :param int adc_pos_max: The maximum ADC value of the positive range.

    UIFLOW2:

        |set_axis_y_mapping.svg|

.. method:: JoystickV2Unit.set_deadzone_adc(x_adc_raw, y_adc_raw)

    Set the dead zone of the joystick.

    :param int x_adc_raw: The dead zone of the X-axis. Range is 0 to 32768.
    :param int y_adc_raw: The dead zone of the Y-axis. Range is 0 to 32768.

    UIFLOW2:

        |set_deadzone_adc.svg|

.. method:: JoystickV2Unit.set_deadzone_position(x_pos, y_pos)

    Set the dead zone of the joystick.

    :param int x_pos: The dead zone of the X-axis. Range is 0 to 4096.
    :param int y_pos: The dead zone of the Y-axis. Range is 0 to 4096.

    UIFLOW2:

        |set_deadzone_position.svg|

.. method:: JoystickV2Unit.read_axis_position()

    Read the position of the joystick.


    UIFLOW2:

        |read_axis_position.svg|

.. method:: JoystickV2Unit.set_address(address)

    Set the I2C address of the JoystickV2 Unit.

    :param int address: The I2C address to set.

    UIFLOW2:

        |set_address.svg|

.. method:: JoystickV2Unit.read_fw_version()

    Read the firmware version of the JoystickV2 Unit.


    UIFLOW2:

        |read_fw_version.svg|



