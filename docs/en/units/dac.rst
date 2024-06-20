DAC Unit
========

.. include:: ../refs/unit.dac.ref

The `Dac2` class interfaces with a GP8413 15-bit Digital to Analog Converter (DAC), capable of converting digital signals into two channels of analog voltage output, ranging from 0-5V and 0-10V.

Support the following products:

    |DACUnit|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/dac/dac_core_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |dac_core_example.m5f2|


class DACUnit
-------------

Constructors
------------

.. class:: DACUnit(i2c: I2C, address: int = 0x60, vdd: float = 5.0, vout: float = 3.3)

    Create an DACUnit object.

    :param i2c: I2C object
    :param address: I2C address
    :param vdd: Supply voltage
    :param vout: Output voltage

    UIFLOW2:

        |init.svg|


.. _unit.DACUnit.Methods:

Methods
-------

.. method:: DACUnit.get_value() -> int

    Get the current value of the DAC.

    :return: The DAC value as a 16-bit unsigned value.

    UIFLOW2:

        |get_value.svg|


.. method:: DACUnit.get_voltage() -> float

    Get the current voltage of the DAC.

    :return: The DAC voltage as a float.

    UIFLOW2:

        |get_voltage.svg|


.. method:: DACUnit.set_value(value: int) -> None

    Set the value of the DAC.

    :param value: The DAC value as a 16-bit unsigned value.

    UIFLOW2:

        |set_value.svg|


.. method:: DACUnit.set_voltage(voltage: float) -> None

    Set the voltage of the DAC.

    :param voltage: The DAC voltage as a float. The voltage must be between 0 and 3.3V.

    UIFLOW2:

        |set_voltage.svg|


.. method:: DACUnit.get_raw_value() -> int

    Get the raw value of the DAC.

    :return: The raw DAC value as a 12-bit unsigned value.

    UIFLOW2:

        |get_raw_value.svg|


.. method:: DACUnit.set_raw_value(value: int) -> None

    Set the raw value of the DAC.

    :param value: The raw DAC value as a 12-bit unsigned value.

    UIFLOW2:

        |set_raw_value.svg|


.. method:: DACUnit.get_normalized_value() -> float

    Get the normalized value of the DAC.

    :return: The normalized DAC value as a float.

    UIFLOW2:

        |get_normalized_value.svg|


.. method:: DACUnit.set_normalized_value(value: float) -> None

    Set the normalized value of the DAC.

    :param value: The normalized DAC value as a float.

    UIFLOW2:

        |set_normalized_value.svg|

.. method:: DACUnit.save_to_eeprom() -> None

    Save the current DAC value to EEPROM.

    UIFLOW2:

        |save_to_eeprom.svg|
