DCSSR Unit
==========

.. include:: ../refs/unit.dcssr.ref

Support the following products:

    |DCSSR Unit|


class DCSSRUnit
---------------

Constructors
------------

.. class:: DCSSRUnit(bus, address=0x50)

    Create an DCSSRUnit object.

    :param i2c: I2C bus or Modbus.
    :param address: Slave address. Default is 0x50 in I2C mode. Default is 0x04 in Modbus mode.

    UIFLOW2:

        |init.png|


DCSSRUnit class inherits ACSSRUnit class, See :ref:`unit.ACSSRUnit.Methods <unit.ACSSRUnit.Methods>` for more details.
