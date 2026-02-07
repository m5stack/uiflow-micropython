
Encoder8 Unit
=============
.. sku:U153
.. include:: ../refs/unit.encoder8.ref

UNIT 8Encoder is a set of 8 rotary encoders as one of the input unit, the internal use of STM32 single-chip microcomputer as the acquisition and communication processor, and the host computer using I2C communication interface, each rotary encoder corresponds to 1 RGB LED light, encoder in addition to left and right rotation, but also radially pressed, in addition to a physical toggle switch and its corresponding RGB LED light, including 5V->3V3 DCDC circuit.

Support the following products:

|Encoder8Unit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/encoder8/encoder8_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |encoder8_cores3_example.m5f2|

class Encoder8Unit
------------------

Constructors
------------

.. class:: Encoder8Unit(i2c, slave_addr, address)

    Initialize the Encoder8 Unit with the specified I2C interface and address.

    :param  i2c: The I2C interface or PAHUBUnit instance for communication.
    :param int slave_addr: Deprecated parameter, kept for backward compatibility.
    :param int address: The I2C address of the Encoder8 Unit. Default is 0x41.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: Encoder8Unit.init_i2c_address(slave_addr)

    Set or change the I2C address of the Encoder8 Unit.

    :param int slave_addr: The new I2C address to set.

.. method:: Encoder8Unit.available()

    Check if the Encoder8 Unit is connected on the I2C bus.

.. method:: Encoder8Unit.get_counter_value(channel)

    Get the current counter value of the specified channel.

    :param int channel: The encoder channel (1-8). Default is 1.

    :return: The current counter value as an integer.

    UIFLOW2:

        |get_counter_value.png|

.. method:: Encoder8Unit.set_counter_value(channel, value)

    Set the counter value for the specified channel.

    :param int channel: The encoder channel (1-8). Default is 1.
    :param int value: The counter value to set.

    UIFLOW2:

        |set_counter_value.png|

.. method:: Encoder8Unit.get_increment_value(channel)

    Get the incremental value of the specified channel.

    :param int channel: The encoder channel (1-8). Default is 1.
    
    :return: The incremental value as an integer.

    UIFLOW2:

        |get_increment_value.png|

.. method:: Encoder8Unit.reset_counter_value(channel)

    Reset the counter value for the specified channel.

    :param int channel: The encoder channel (1-8). Default is 1.

    UIFLOW2:

        |reset_counter_value.png|

.. method:: Encoder8Unit.get_button_status(channel)

    Get the button status for the specified channel.

    :param int channel: The encoder channel (1-8). Default is 1.

    :return: True if the button is pressed, False otherwise.

    UIFLOW2:

        |get_button_status.png|

.. method:: Encoder8Unit.get_switch_status()

    Get the status of the global switch.

    :return: True if the switch is on, False otherwise.

    UIFLOW2:

        |get_switch_status.png|

.. method:: Encoder8Unit.set_led_rgb(channel, rgb)

    Set the RGB color of the specified channel&#x27;s LED.

    :param int channel: The encoder channel (1-8). Default is 1.
    :param int rgb: The RGB color value (0-0xFFFFFF). Default is 0.

    UIFLOW2:

        |set_led_rgb.png|

.. method:: Encoder8Unit.set_led_rgb_from(begin, end, rgb)

    Set the RGB color for a range of channels&#x27; LEDs.

    :param int begin: The starting channel index. Default is 0.
    :param int end: The ending channel index. Default is 0.
    :param int rgb: The RGB color value (0-0xFFFFFF). Default is 0.

    UIFLOW2:

        |set_led_rgb_from.png|

.. method:: Encoder8Unit.get_device_status(mode)

    Get the device firmware version or I2C address.

    :param int mode: The mode to read. 0xFE for firmware version, 0xFF for I2C address. Default is 0xFE.

    :return: The value read from the specified mode register.

    UIFLOW2:

        |get_device_status.png|

.. method:: Encoder8Unit.set_i2c_address(addr)

    Set a new I2C address for the device.

    :param int addr: The new I2C address. Default is 0x41.

    UIFLOW2:

        |set_i2c_address.png|

.. method:: Encoder8Unit.read_reg_data(reg, num)

    Read data from a specified register.

    :param int reg: The register address to read from.
    :param int num: The number of bytes to read.

.. method:: Encoder8Unit.write_reg_data(reg, byte_lst)

    Write data to a specified register.

    :param  reg: The register address to write to.
    :param  byte_lst: A list of bytes to write to the register.

.. method:: Encoder8Unit.deinit()

    Deinitialize the Encoder8 Unit instance.

