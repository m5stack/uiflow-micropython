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

    Connect an ISO485 Unit to CoreS3 Port C (RX=18, TX=17) and configure the
    ACSSR for Modbus mode, 115200 baud, 8N1, device address ``0x04``.

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

.. class:: ACSSRUnit(bus, address=0x50)

    Factory returning the driver selected by the bus object. It does not
    change the ACSSR hardware's communication mode.

    :param bus: A ``machine.I2C`` instance, or a configured Modbus master
        providing ``read_coils`` and the register/coil operations used below.
    :param int address: Device address. The factory default is ``0x50`` in
        both modes. For a Modbus device at its default address, explicitly
        pass ``address=0x04``.
    :return: ``unit.acssr.ACSSRI2CUnit`` for ``machine.I2C``;
        ``unit.acssr.ACSSRModbusUnit`` for a Modbus master.

    The implementation class ``ACSSRModbusUnit`` has a default address of
    ``0x04``, but the factory always forwards its own ``address`` argument.
    Selecting a bus does not select that implementation default.

    .. code-block:: python

        from unit import ACSSRUnit, ISO485Unit
        from modbus import ModbusRTUMaster

        # I2C: use the configured I2C bus.
        acssr_i2c = ACSSRUnit(i2c0, address=0x50)

        # Modbus: CoreS3 Port C, ISO485 Unit, ACSSR in Modbus mode.
        rs485 = ISO485Unit(2, port=(18, 17))
        rs485.init(baudrate=115200, data_bits=8, stop_bits=1, parity=None)
        master = ModbusRTUMaster(uart=rs485)
        acssr_modbus = ACSSRUnit(master, address=0x04)

    Use methods on the returned instance, such as ``acssr_modbus.value()``.
    The factory class itself does not define the instance methods below.

    UIFLOW2:

        |init.png|


.. _unit.ACSSRUnit.Methods:

Methods
-------

``ACSSRUnit`` is a factory: it returns an ``ACSSRI2CUnit`` for an I2C bus or an
``ACSSRModbusUnit`` for a Modbus bus. The methods below belong to the returned
object and are available in both modes.

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
