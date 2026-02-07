ACSSR Unit
==========

.. include:: ../refs/unit.acssr.ref

Support the following products:

    |ACSSR Unit|


Micropython I2C Example:

    .. literalinclude:: ../../../examples/unit/acssr/cores3_acssr_i2c_example.py
        :language: python
        :linenos:


Micropython Modbus Example:

    .. literalinclude:: ../../../examples/unit/acssr/cores3_acssr_modbus_example.py
        :language: python
        :linenos:


UIFLOW2 I2C Example:

    |i2c_example.png|


UIFLOW2 Modbus Example:

    |modbus_example.png|


.. only:: builder_html

    |cores3_acssr_i2c_example.m5f2|

    |cores3_acssr_modbus_example.m5f2|


class ACSSRUnit
---------------

Constructors
------------

.. class:: ACSSRUnit(bus, address=None)

    Create an ACSSRUnit object.

    :param bus: I2C bus or Modbus.
    :param address: Slave address. Default is 0x50 in I2C mode. Default is 0x04 in Modbus mode.

    UIFLOW2:

        |init.png|


.. _unit.ACSSRUnit.Methods:

Methods
-------

.. method:: ACSSRUnit.on() -> None

    Turn on the relay.

    UIFLOW2:

        |on.png|


.. method:: ACSSRUnit.off() -> None

    Turn off the relay.

    UIFLOW2:

        |off.png|


.. method:: ACSSRUnit.__call__([x])

    Turn on the relay if x is True, otherwise turn off the relay.

    :param x: True or False.

    UIFLOW2:

        |call.png|


.. method:: ACSSRUnit.value([x])

    Turn on the relay if x is True, otherwise turn off the relay.

    :param x: True or False.

    UIFLOW2:

        |value.png|


.. method:: ACSSRUnit.fill_color(rgb: int = 0) -> None

    Set the color of the LED.

    :param rgb: RGB color value. Default is 0.

    UIFLOW2:

        |fill_color.png|


.. method:: ACSSRUnit.get_firmware_version() -> int

    Get the firmware version of the unit.

    :return: Firmware version.

    UIFLOW2:

        |get_firmware_version.png|


.. method:: ACSSRUnit.set_address(new_address: int) -> None

    Set the I2C address of the unit.

    :param new_address: New I2C address. The range is 0x01-0x7f.

    UIFLOW2:

        |set_address.png|

        |set_address1.png|
