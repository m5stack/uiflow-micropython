
JoystickUnit
==============

.. include:: ../refs/unit.joystick2.ref

The joystick is an input unit for control, utilizing an I2C communication interface and supporting three-axis control signals (X/Y-axis analog input for displacement and Z-axis digital input for key presses). It is ideal for applications like gaming and robot control.

Support the following products:

|JoystickUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import JoystickUnit
    from hardware import *
    i2c = I2C(1, scl=22, sda=21)
    joystick = JoystickUnit(i2c)
    joystick.read_adc_value()
    joystick.read_button_status()
    joystick.set_rgb_led(255, 0, 0)
    joystick.get_rgb_led()
    joystick.set_deadzone_position(200, 200)
    while True:
        joystick.read_axis_position()

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

class JoystickUnit
--------------------

Constructors
------------

.. class:: JoystickUnit(i2c, address)

    Initialize the Joystick Unit.

    :param I2C i2c: I2C port to use.
    :param int address: I2C address of the Joystick Unit.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: JoystickUnit.set_axis_x_invert(invert)

    Invert the X-axis of the joystick.


    :param bool invert: Whether to invert the X-axis.

    UIFLOW2:

        |set_axis_x_invert.png|

.. method:: JoystickUnit.set_axis_y_invert(invert)

    Invert the Y-axis of the joystick.


    :param bool invert: Whether to invert the Y-axis.

    UIFLOW2:

        |set_axis_y_invert.png|

.. method:: JoystickUnit.set_axis_swap(swap)

    Swap the X-axis and Y-axis of the joystick.


    :param bool swap: Whether to swap the X-axis and Y-axis.

    UIFLOW2:

        |set_axis_swap.png|

.. method:: JoystickUnit.get_adc_value()

    Read the ADC value of the joystick.

    :return (tuple): Returns a tuple of the X-axis and Y-axis ADC values, from 0 to 65535


    UIFLOW2:

        |get_adc_value.png|

.. method:: JoystickUnit.get_button_status()

    Read the button status of the joystick.

    :return (bool): Returns the button status. True if pressed, False if not pressed.


    UIFLOW2:

        |get_button_status.png|

.. method:: JoystickUnit.set_led_brightness(brightness)

    Set the brightness of the RGB LED.


    :param float brightness: The brightness value (0-100).

    UIFLOW2:

        |set_led_brightness.png|

.. method:: JoystickUnit.fill_color(v)

    Set the RGB LED color of the joystick.


    :param  v: The RGB value (0x000000-0xFFFFFF).

    UIFLOW2:

        |fill_color.png|

.. method:: JoystickUnit.fill_color_rgb(r, g, b)

    Set the RGB LED color of the joystick.


    :param int r: The red value (0-255).
    :param int g: The green value (0-255).
    :param int b: The blue value (0-255).

    UIFLOW2:

        |fill_color_rgb.png|

.. method:: JoystickUnit.set_axis_x_mapping(adc_neg_min, adc_neg_max, adc_pos_min, adc_pos_max)

    ::

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

        |set_axis_x_mapping.png|

.. method:: JoystickUnit.set_axis_y_mapping(adc_neg_min, adc_neg_max, adc_pos_min, adc_pos_max)

    ::

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

        |set_axis_y_mapping.png|

.. method:: JoystickUnit.set_deadzone_adc(x_adc_raw, y_adc_raw)

    Set the dead zone of the joystick.


    :param int x_adc_raw: The dead zone of the X-axis. Range is 0 to 32768.
    :param int y_adc_raw: The dead zone of the Y-axis. Range is 0 to 32768.

    UIFLOW2:

        |set_deadzone_adc.png|

.. method:: JoystickUnit.set_deadzone_position(x_pos, y_pos)

    Set the dead zone of the joystick.


    :param int x_pos: The dead zone of the X-axis. Range is 0 to 4096.
    :param int y_pos: The dead zone of the Y-axis. Range is 0 to 4096.

    UIFLOW2:

        |set_deadzone_position.png|

.. method:: JoystickUnit.get_axis_position()

    Read the position of the joystick.

    :return (tuple): Returns a tuple of the X-axis and Y-axis positions. The range is -4096 to 4096.


    UIFLOW2:

        |get_axis_position.png|

.. method:: JoystickUnit.set_address(address)

    Set the I2C address of the Joystick Unit.


    :param int address: The I2C address to set.

    UIFLOW2:

        |set_address.png|

.. method:: JoystickUnit.get_firmware_version()

    Read the firmware version of the Joystick Unit.

    :return (int): Returns the firmware version.


    UIFLOW2:

        |get_firmware_version.png|

.. method:: JoystickUnit.get_x_raw()

    Read the raw X-axis value of the joystick.

    :return (int): Returns the raw X-axis value.


    UIFLOW2:

        |get_x_raw.png|

.. method:: JoystickUnit.get_y_raw()

    Read the raw Y-axis value of the joystick.

    :return (int): Returns the raw Y-axis value.


    UIFLOW2:

        |get_y_raw.png|

.. method:: JoystickUnit.get_x_position()

    Read the X-axis position of the joystick.

    :return (int): Returns the X-axis position.


    UIFLOW2:

        |get_x_position.png|

.. method:: JoystickUnit.get_y_position()

    Read the Y-axis position of the joystick.

    :return (int): Returns the Y-axis position.


    UIFLOW2:

        |get_y_position.png|



