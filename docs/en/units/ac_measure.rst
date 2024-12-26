
ACMeasure Unit
==============
.. sku:U164
.. include:: ../refs/unit.ac_measure.ref

C Measure Unit is a single-phase AC measurement module with isolation capabilities. It utilizes the STM32+HLW8032 scheme to monitor high-precision current, voltage, power, and other data in real time. The module features a built-in AC isolation chip, B0505ST16-W5, and communicates with the STM32 through the EL357 optocoupler isolation chip.

Support the following products:

|ACMeasureUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/ac_meausre/acmeasure_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |acmeasure_cores3_example.m5f2|

class ACMeasureUnit
-------------------

Constructors
------------

.. class:: ACMeasureUnit(i2c, address)

    Initialize the AC Measure unit by setting the I2C port and the AC Measure slave address.

    :param  i2c: The I2C interface object or PAHUBUnit used for communication.
    :param  address: The I2C address of the AC Measure unit, default is 0x42.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ACMeasureUnit.init_i2c_address(slave_addr)

    Initialize the I2C address for the AC Measure unit.

    :param int slave_addr: The I2C address of the AC Measure unit, should be between 1 and 127.

.. method:: ACMeasureUnit.get_voltage_str()

    Get the voltage string value from the AC Measure unit.

    :return: The voltage value as a string.

    UIFLOW2:

        |get_voltage_str.png|

.. method:: ACMeasureUnit.get_current_str()

    Get the current string value from the AC Measure unit.

            
    :return: The current value as a string.

    UIFLOW2:

        |get_current_str.png|

.. method:: ACMeasureUnit.get_active_power_str()

    Get the active power string value from the AC Measure unit.

            
    :return: The active power value as a string.

    UIFLOW2:

        |get_active_power_str.png|

.. method:: ACMeasureUnit.get_apparent_power_str()

    Get the apparent power string value from the AC Measure unit.

            
    :return: The apparent power value as a string.

    UIFLOW2:

        |get_apparent_power_str.png|

.. method:: ACMeasureUnit.get_power_factor_str()

    Get the power factor string value from the AC Measure unit.

            
    :return: The power factor value as a string.

    UIFLOW2:

        |get_power_factor_str.png|

.. method:: ACMeasureUnit.get_kwh_str()

    Get the kWh string value from the AC Measure unit.

            
    :return: The kWh value as a string.

    UIFLOW2:

        |get_kwh_str.png|

.. method:: ACMeasureUnit.get_voltage_byte()

    Get the raw voltage value from the AC Measure unit.

            
    :return: The raw voltage value as an integer.

    UIFLOW2:

        |get_voltage_byte.png|

.. method:: ACMeasureUnit.get_current_byte()

    Get the raw current value from the AC Measure unit.

            
    :return: The raw current value as an integer.

    UIFLOW2:

        |get_current_byte.png|

.. method:: ACMeasureUnit.get_active_power_byte()

    Get the raw active power value from the AC Measure unit.

            
    :return: The raw active power value as an integer.

    UIFLOW2:

        |get_active_power_byte.png|

.. method:: ACMeasureUnit.get_apparent_power_byte()

    Get the raw apparent power value from the AC Measure unit.

            
    :return: The raw apparent power value as an integer.

    UIFLOW2:

        |get_apparent_power_byte.png|

.. method:: ACMeasureUnit.get_power_factor_byte()

    Get the raw power factor value from the AC Measure unit.

    :return: The raw power factor value as an integer.

    UIFLOW2:

        |get_power_factor_byte.png|

.. method:: ACMeasureUnit.get_kwh_byte()

    Get the raw kWh value from the AC Measure unit.

    :return: The raw kWh value as an integer.

    UIFLOW2:

        |get_kwh_byte.png|

.. method:: ACMeasureUnit.get_voltage_coeff()

    Get the voltage coefficient value from the AC Measure unit.

    :return: The voltage coefficient value as an integer.

    UIFLOW2:

        |get_voltage_coeff.png|

.. method:: ACMeasureUnit.set_voltage_coeff(value)

    Set the voltage coefficient value for the AC Measure unit.

    :param int value: The voltage coefficient value to set, between 0 and 255.

    UIFLOW2:

        |set_voltage_coeff.png|

.. method:: ACMeasureUnit.get_current_coeff()

    Get the current coefficient value from the AC Measure unit.


    :return: The current coefficient value as an integer.

    UIFLOW2:

        |get_current_coeff.png|

.. method:: ACMeasureUnit.set_current_coeff(value)

    Set the current coefficient value for the AC Measure unit.

    :param int value: The current coefficient value to set, between 0 and 255.

    UIFLOW2:

        |set_current_coeff.png|

.. method:: ACMeasureUnit.set_save_coeff()

    Save the voltage and current coefficient values to flash memory.


    UIFLOW2:

        |set_save_coeff.png|

.. method:: ACMeasureUnit.get_data_ready()

    Check if the AC Measure unit data is ready.


    :return: True if data is ready, False otherwise.

    UIFLOW2:

        |get_data_ready.png|

.. method:: ACMeasureUnit.set_jump_bootloader()

    Set the AC Measure unit to jump to the bootloader.

.. method:: ACMeasureUnit.get_device_status(mode)

    Get the firmware version or I2C address based on the specified mode.

    :param int mode: The mode to select the desired status (0xFE for firmware version, 0xFF for I2C address).

    :return: The requested device status as an integer.

    UIFLOW2:

        |get_device_status.png|

.. method:: ACMeasureUnit.set_i2c_address(addr)

    Set a new I2C address for the AC Measure unit.

    :param int addr: The new I2C address to set, between 0x01 and 0x7F.

    UIFLOW2:

        |set_i2c_address.png|
    

