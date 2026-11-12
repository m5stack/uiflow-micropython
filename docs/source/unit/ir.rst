IR Unit
=======

.. include:: ../refs/unit.ir.ref

Support the following products:

    |IR|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/ir/ir_core_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |ir_core_example.m5f2|


class IRUnit
------------

Constructors
------------

.. class:: IRUnit(port)

    Create an IRUnit object.

    :param tuple port: The port to which the IR unit is connected. the tuple is a pair of values, the first value is the receive pin, and the second value is the transmit pin.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: IRUnit.tx(cmd, data)

    Sends an ir signal value to an address.

    :param int cmd: NEC address byte (0-255).
    :param int data: NEC command byte (0-255).

    UIFLOW2:

        |tx.png|


.. method:: IRUnit.rx_cb(cb)

    Register a callback for received NEC infrared data.

    :param callable cb: Called as ``cb(data, addr, ctrl)`` with the command byte,
        address byte, and control value (0 for a normal frame or -1 for a repeat).

    UIFLOW2:

        |rx_event.png|
