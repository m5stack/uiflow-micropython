
EXTIO2 Unit
==========
.. sku:U011-B
.. include:: ../refs/unit.extio2.ref

EXT.IO2 is an IO extended unit, based on STM32F030 main controller, using I2C communication interface and providing 8 IO expansion. Each IO supports independent configuration of digital I/O, ADC, SERVO control, RGB LED control modes. Supports configuration of device I2C address, which means that users can mount multiple EXT.IO2 UNITs on the same I2C BUS to extend more IO resources. Suitable for multiple digital/analog signal acquisition, with lighting/servo control applications.

Support the following products:

|EXTIO2Unit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/extio2/extio2_core2_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |extio2_core2_example.m5f2|

class EXTIO2Unit
----------------

Constructors
------------

.. class:: EXTIO2Unit(i2c, address)

    Initialize EXTIO2Unit with I2C or PAHUBUnit and address for communication.

    :param  i2c: The I2C or PAHUBUnit interface for communication with the EXTIO2Unit.
    :param int address: The I2C address for the unit, default is _DEFAULT_ADDRESS.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: EXTIO2Unit.set_config_mode(id, mode)

    Set the configuration mode for a specific channel.

    :param int id: The channel ID to set the mode for.
    :param  mode: The mode to set, defined by the EXTIO2Unit. Can be 0, 1, 2, 3, or 4.

    UIFLOW2:

        |set_config_mode.png|

.. method:: EXTIO2Unit.write_output_pin(id, value)

    Write a value to an output pin of the EXTIO2Unit.

    :param int id: The pin ID to write the value to.
    :param  value: The value to write, either 0 or 1.

    UIFLOW2:

        |write_output_pin.png|

.. method:: EXTIO2Unit.write_servo_angle(id, angle)

    Write an angle to a servo connected to the EXTIO2Unit.

    :param int id: The servo ID to set the angle for.
    :param int angle: The angle to set the servo to (0-255).

    UIFLOW2:

        |write_servo_angle.png|

.. method:: EXTIO2Unit.write_servo_pulse(id, pulse)

    Write a pulse width to a servo connected to the EXTIO2Unit.

    :param int id: The servo ID to set the pulse for.
    :param int pulse: The pulse width to set the servo to, in microseconds.

    UIFLOW2:

        |write_servo_pulse.png|

.. method:: EXTIO2Unit.write_rgb_led(id, value)

    Write an RGB color value to a NeoPixel LED.

    :param int id: The NeoPixel ID to set the color for.
    :param  value: The RGB value to set, represented as a 24-bit integer.

    UIFLOW2:

        |write_rgb_led.png|

.. method:: EXTIO2Unit.set_address(address)

    Set the I2C address for the EXTIO2Unit.

    :param int address: The new I2C address to set for the unit.

    UIFLOW2:

        |set_address.png|

.. method:: EXTIO2Unit.get_config_mode(id)

    Get the current configuration mode of a specific channel.

    :param int id: The channel ID to get the mode for.

    UIFLOW2:

        |get_config_mode.png|

.. method:: EXTIO2Unit.read_input_pin(id)

    Read the value of an input pin.

    :param int id: The pin ID to read the value from.

    UIFLOW2:

        |read_input_pin.png|

.. method:: EXTIO2Unit.read_adc8_pin(id)

    Read the 8-bit ADC value of a pin.

    :param int id: The pin ID to read the ADC value from.

    UIFLOW2:

        |read_adc8_pin.png|

.. method:: EXTIO2Unit.read_adc12_pin(id)

    Read the 12-bit ADC value of a pin.

    :param int id: The pin ID to read the ADC value from.

    UIFLOW2:

        |read_adc12_pin.png|

.. method:: EXTIO2Unit.read_servo_angle(id)

    Read the angle of a servo.

    :param int id: The servo ID to read the angle from.

    UIFLOW2:

        |read_servo_angle.png|

.. method:: EXTIO2Unit.read_servo_pulse(id)

    Read the pulse width of a servo.

    :param int id: The servo ID to read the pulse width from.

    UIFLOW2:

        |read_servo_pulse.png|

.. method:: EXTIO2Unit.read_rgb_led(id)

    Read the RGB color value of a NeoPixel LED.

    :param int id: The NeoPixel ID to read the color from.

    UIFLOW2:

        |read_rgb_led.png|

.. method:: EXTIO2Unit.pin(id, mode, value)

    Create and return a Pin object with the specified mode and value.

    :param  id: The pin ID to create the Pin object for.
    :param int mode: The mode to set for the pin (default is input).
    :param  value: The value to set for the pin, if applicable.

