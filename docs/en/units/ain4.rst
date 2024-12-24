
AIN4-20mA Unit
==============

.. include:: ../refs/unit.ain4.ref

The following products are supported:

|AIN4_20MAUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/ain4/ain4_core2_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |ain4_core2_example.m5f2|


class AIN4_20MAUnit
-------------------

Constructors
------------

.. class:: AIN4_20MAUnit(i2c, address)

    Init I2C port & UNIT AIN 4-20mA I2C Address.

    :param I2C i2c: I2C port to use.
    :param int|list|tuple address: I2C address of the Unit AIN4-20mA.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: AIN4_20MAUnit.get_adc_raw_value() -> int

    Retrieves the raw ADC value from the channel.

    :return: Raw ADC value as a 12-bit integer.

.. method:: AIN4_20MAUnit.get_adc_raw16_value() -> int

    Retrieves the raw ADC value from the channel.

    Note: This method will be removed in the next few versions, please use get_adc_raw_value()

    :return: Raw ADC value as a 12-bit integer.

    UIFLOW2:

        |get_adc_raw16_value.png|

.. method:: AIN4_20MAUnit.get_current_value() -> float

    Retrieves the current value (in mA) from the channel.

    :return: Current value in milliamperes (mA).

.. method:: AIN4_20MAUnit.get_4_20ma_current_value() -> float

    Retrieves the current value (in mA) from the channel.

    Note: This method will be removed in the next few versions, please use get_current_value()

    :return: Current value in milliamperes (mA).

    UIFLOW2:

        |get_4_20ma_current_value.png|

.. method:: AIN4_20MAUnit.set_cal_current(val)

    Sets the calibration current for the specified channel.

    :param int val: The calibration current value, ranging from 4 to 20 mA.

    UIFLOW2:

        |set_cal_current.png|

.. method:: AIN4_20MAUnit.get_device_spec() -> int

    Retrieves the firmware version or i2c address of the AIN 4-20mA unit.

    :return: Firmware version or I2C address.

    :Note: This method will be removed in the next few versions, please use get_firmware_version() and get_i2c_address()

    UIFLOW2:

        |get_device_spec.png|

.. method:: AIN4_20MAUnit.get_firmware_version() -> int

    Retrieves the firmware version of the AIN 4-20mA unit.

    :return: Firmware version.

    UIFLOW2:

        |get_firmware_version.png|

.. method:: AIN4_20MAUnit.get_i2c_address() -> str

    Retrieves the current I2C address of the AIN 4-20mA unit.

    :return: I2C address as a string in hexadecimal format.

    UIFLOW2:

        |get_i2c_address.png|

.. method:: AIN4_20MAUnit.set_i2c_address(addr)

    Sets a new I2C address for the AIN 4-20mA unit.

    :param int addr: The new I2C address, must be between 0x08 and 0x77.

    UIFLOW2:

        |set_i2c_address.png|





