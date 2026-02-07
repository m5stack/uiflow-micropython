
Color Unit
===========
.. sku:U009
.. include:: ../refs/unit.color.ref

Support the following products:

|ColorUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/color/color_core2_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |color_core2_example.m5f2|

class ColorUnit
---------------

Constructors
------------

.. class:: ColorUnit(i2c, address= _TCS3472_DEFAULT_ADDR)

    Initialize ColorUnit sensor with the given I2C interface and address.

    :param I2C i2c: The I2C bus instance for communication.
    :param int address: The I2C address of the sensor, default is _TCS3472_DEFAULT_ADDR(0x29).

    UIFLOW2:

        |init.png|

Methods
-------

.. method:: ColorUnit.get_lux() -> float

    Get the lux value computed from the color channels.

    :return: The computed lux value as a float.

    UIFLOW2:

        |get_lux.png|

.. method:: ColorUnit.get_color_temperature() -> float

    Get the color temperature in degrees Kelvin.

    :return: The color temperature as a float in Kelvin.

    UIFLOW2:

        |get_color_temperature.png|

.. method:: ColorUnit.get_color_rgb_bytes() -> tuple

    Get the RGB color detected by the sensor.

    :return: A tuple of red, green, and blue component values as bytes (0-255).

    UIFLOW2:

        |get_color_rgb_bytes.png|

.. method:: ColorUnit.get_color_r() -> int

    Get the red component of the RGB color.

    :return: The red component value (0-255).

    UIFLOW2:

        |get_color_r.png|

.. method:: ColorUnit.get_color_g() -> int

    Get the green component of the RGB color.

    :return: The green component value (0-255).

    UIFLOW2:

        |get_color_g.png|

.. method:: ColorUnit.get_color_b() -> int

    Get the blue component of the RGB color.

    :return: The blue component value (0-255).

    UIFLOW2:

        |get_color_b.png|

.. method:: ColorUnit.get_color_h() -> int

    Get the hue (H) value of the color in degrees.

    :return: The hue value as an integer in the range [0, 360].

    UIFLOW2:

        |get_color_h.png|

.. method:: ColorUnit.get_color_s() -> float

    Get the saturation (S) value of the color.

    :return: The saturation value as a float in the range [0, 1].

    UIFLOW2:

        |get_color_s.png|

.. method:: ColorUnit.get_color_v() -> float

    Get the value (V) of the color (brightness).

    :return: The value as a float in the range [0, 1].

    UIFLOW2:

        |get_color_v.png|

.. method:: ColorUnit.get_color() -> int

    Get the RGB color as an integer value.

    :return: An integer representing the RGB color, with 8 bits per channel.

    UIFLOW2:

        |get_color.png|

.. method:: ColorUnit.get_color565() -> int

    Get the RGB color in 5-6-5 format as an integer.
    :return: An integer representing the RGB color in 5-6-5 format.

    UIFLOW2:

        |get_color565.png|

.. method:: ColorUnit.get_active() -> bool

    Get the active state of the sensor.

    :return: True if the sensor is active, False if it is inactive.

    UIFLOW2:

        |get_active.png|

.. method:: ColorUnit.set_active(val)

    Set the active state of the sensor.

    :param bool val: : True to activate the sensor, False to deactivate it.

    UIFLOW2:

        |set_active.png|

.. method:: ColorUnit.get_integration_time() -> float

    Get the integration time of the sensor in milliseconds.

    :return: The integration time as a float.

    UIFLOW2:

        |get_integration_time.png|

.. method:: ColorUnit.set_integration_time(val)

    Set the integration time of the sensor.

    :param float val: : The desired integration time in milliseconds.
    :raise ValueError: If the integration time is out of the allowed range.

    UIFLOW2:

        |set_integration_time.png|

.. method:: ColorUnit.get_gain() -> int

    Get the gain of the sensor.

    :return: The gain value, which should be one of 1, 4, 16, or 60.

    UIFLOW2:

        |get_gain.png|

.. method:: ColorUnit.set_gain(val)

    Set the gain of the sensor.

    :param int val: : The desired gain value (1, 4, 16, or 60).
    :raise ValueError: If the gain is not one of the allowed values.

    UIFLOW2:

        |set_gain.png|

.. method:: ColorUnit.read_interrupt() -> bool

    Read the interrupt status.

    :return: True if the interrupt is set, False otherwise.

    UIFLOW2:

        |read_interrupt.png|

.. method:: ColorUnit.clear_interrupt()

    Clear the interrupt status of the sensor by writing to the interrupt register.

    UIFLOW2:

        |clear_interrupt.png|

.. method:: ColorUnit.get_color_raw()

    Read the raw RGBC color detected by the sensor.

    :return: A tuple containing raw red, green, blue, and clear color data.

    UIFLOW2:

        |get_color_raw.png|

.. method:: ColorUnit.get_cycles()

    Get the persistence cycles of the sensor.

    :return: The persistence cycles or -1 if interrupts are disabled.

    UIFLOW2:

        |get_cycles.png|

.. method:: ColorUnit.set_cycles(val)

    Set the persistence cycles for the sensor.

    :param int val: : The number of persistence cycles, or -1 to disable interrupts.
    :raise ValueError: If the value is not one of the permitted cycle values.

    UIFLOW2:

        |set_cycles.png|

.. method:: ColorUnit.get_min_value()

    Get the minimum threshold value (AILT register) of the sensor.

    :return: The minimum threshold value.

    UIFLOW2:

        |get_min_value.png|

.. method:: ColorUnit.set_min_value(val)

    Set the minimum threshold value (AILT register) of the sensor.

    :param int val: : The minimum threshold value to set.

    UIFLOW2:

        |set_min_value.png|

.. method:: ColorUnit.get_max_value()

    Get the maximum threshold value (AIHT register) of the sensor.

    :return: The maximum threshold value.

    UIFLOW2:

        |get_max_value.png|

.. method:: ColorUnit.set_max_value(val)

    Set the maximum threshold value (AIHT register) of the sensor.

    :param int val: : The maximum threshold value to set.

    UIFLOW2:

        |set_max_value.png|

.. method:: ColorUnit.get_glass_attenuation()

    Get the Glass Attenuation factor used to compensate for lower light levels due to glass presence.

    :return: The glass attenuation factor (ga).

    UIFLOW2:

        |get_glass_attenuation.png|

.. method:: ColorUnit.set_glass_attenuation(value)

    Set the Glass Attenuation factor used to compensate for lower light levels due to glass presence.

    :param float value: : The glass attenuation factor to set. Must be greater than or equal to 1.
    :raise ValueError: If the value is less than 1.

    UIFLOW2:

        |set_glass_attenuation.png|
