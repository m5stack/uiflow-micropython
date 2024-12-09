
Angle8 Unit
===========
.. sku:U154
.. include:: ../refs/unit.angle8.ref

UNIT 8Angle is an input unit integrating 8 adjustable potentiometers, internal STM32F030 microcomputer as acquisition and communication processor, and the host computer adopts I2C communication interface, each adjustable potentiometer corresponds to 1 RGB LED light, and there is also a physical toggle switch and its corresponding RGB LED light, containing 5V->3V3 DCDC circuit.

Support the following products:

|Angle8Unit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/angle8/angle8_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |angle8unit_cores3_example.m5f2|

class Angle8Unit
----------------

Constructors
------------

.. class:: Angle8Unit(i2c, address)

    Initialize the Angle8Unit with the specified I2C interface and address.

    :param  i2c: The I2C or PAHUBUnit instance for communication.
    :param int address: The I2C address of the device (default is ANGLE8_ADDR).

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: Angle8Unit.available()

    Check if the device is available on the I2C bus.

.. method:: Angle8Unit.get_adc12_raw(channel)

    Get the raw 12-bit ADC value from the specified channel.

    :param int channel: The channel number (1 to 8).

    UIFLOW2:

        |get_adc12_raw.png|

.. method:: Angle8Unit.get_adc8_raw(channel)

    Get the raw 8-bit ADC value from the specified channel.

    :param int channel: The channel number (1 to 8).

    UIFLOW2:

        |get_adc8_raw.png|

.. method:: Angle8Unit.get_switch_status()

    Get the status of the switch button.


    UIFLOW2:

        |get_switch_status.png|

.. method:: Angle8Unit.set_led_rgb(channel, rgb, bright)

    Set the RGB color and brightness of the specified LED channel.

    :param int channel: The LED channel number (0 to 8).
    :param int rgb: The RGB color value (0x00 to 0xFFFFFF).
    :param int bright: The brightness level (0 to 100, default is 50).

    UIFLOW2:

        |set_led_rgb.png|

.. method:: Angle8Unit.set_led_rgb_from(begin, end, rgb, bright, per_delay)

    Set the RGB color and brightness for a range of LED channels.

    :param int begin: The starting LED channel (0 to 8).
    :param int end: The ending LED channel (0 to 8).
    :param int rgb: The RGB color value (0x00 to 0xFFFFFF).
    :param int bright: The brightness level (0 to 100, default is 50).
    :param int per_delay: The delay in milliseconds between setting each channel (default is 0).

    UIFLOW2:

        |set_led_rgb_from.png|

.. method:: Angle8Unit.set_angle_sync_bright(channel, rgb)

    Set the LED brightness synchronized with the angle value.

    :param int channel: The LED channel number (0 to 8).
    :param int rgb: The RGB color value (0x00 to 0xFFFFFF).

    UIFLOW2:

        |set_angle_sync_bright.png|

.. method:: Angle8Unit.get_device_spec(mode)

    Get device specifications such as firmware version or I2C address.

    :param int mode: The register to read (FW_VER_REG or I2C_ADDR_REG).

    UIFLOW2:

        |get_device_spec.png|

.. method:: Angle8Unit.set_i2c_address(address)

    Set a new I2C address for the device.

    :param int address: The new I2C address (1 to 127).

    UIFLOW2:

        |set_i2c_address.png|

.. method:: Angle8Unit.readfrommem(reg, num)

    Read a specified number of bytes from a device register.

    :param  reg: The register address to read from.
    :param  num: The number of bytes to read.